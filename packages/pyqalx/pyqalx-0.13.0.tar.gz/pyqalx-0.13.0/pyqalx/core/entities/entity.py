import os
from itertools import zip_longest

import requests

from pyqalx.core.encryption import QalxEncrypt
from pyqalx.core.entities.object_dict import ObjectDict

from pyqalx.core.errors import (
    QalxAPIResponseError,
    QalxEntityTypeNotFound,
    QalxError,
    QalxQueueError,
)


class QalxListEntity(ObjectDict):
    """
    Simple wrapper around a pyqalxapi_dict so we can keep extra keys
    on the API list response.  Instantiates each entity in `data` to the
    correct QalxEntity subclass.
    """

    _data_key = "data"

    def __new__(cls, pyqalxapi_list_response_dict, *args, **kwargs):
        """
        A QalxListEntity is just an ObjectDict that has a list of
        QalxEntity instances stored on the `_data_key`.
        :param pyqalxapi_list_response_dict: A dict that gets returned from
        a pyqalxapi list endpoint.  This should at minimum have a `data`
        key but may have other keys which we preserve
        :param kwargs: Must contain `child` key which is a subclass of `QalxEntity`

        """
        cls.child = kwargs["child"]

        if not issubclass(cls.child, (QalxEntity,)):
            raise QalxEntityTypeNotFound(
                f"Expected `child` to be a subclass of "
                f"`QalxEntity`.  Got `{cls.child}`"
            )

        return super(QalxListEntity, cls).__new__(
            cls, pyqalxapi_list_response_dict
        )

    def __init__(self, pyqalxapi_list_response_dict, *args, **kwargs):
        super().__init__(pyqalxapi_list_response_dict)

        if (
            self._data_key not in pyqalxapi_list_response_dict
            or not isinstance(
                pyqalxapi_list_response_dict[self._data_key], list
            )
        ):
            raise QalxAPIResponseError(
                "Expected `{0}` key in "
                "`pyqalxapi_list_response_dict` and for"
                " it to be a list".format(self._data_key)
            )
        # Cast all the entities in data to be an instance of `self.child`
        keyfile = kwargs.pop("keyfile", None)
        self[self._data_key] = [
            self.child(e, keyfile=keyfile)
            for e in pyqalxapi_list_response_dict[self._data_key]
        ]


class AggregationResult(QalxListEntity):
    """
    Class for aggregation result responses from the API
    """


class QalxEntity(ObjectDict):
    """Base class for qalx entities_response.

    QalxEntity children need to be populated with either a
    `requests.models.Response` which is the type returned by the methods
    on `pyqalxapi.api.PyQalxAPI` or with a `dict`.

    Entities can behave either like a dict or attribute lookups can be used
    as getters/setters

    >>> class AnEntity(QalxEntity):
    ...     pass
    >>> c = AnEntity({"guid":"123456789", "info":{"some":"info"}})
    >>> # dict style lookups
    >>> c['guid']
    '123456789'
    >>> # attribute style lookups
    >>> c.guid
    '123456789'


    :param pyqalxapi_dict: a 'dict' representing a qalx entity object to
        populate the entity
    :type pyqalxapi_dict: dict
    """

    entity_type: str

    def __init__(self, pyqalxapi_dict, *args, **kwargs):
        super().__init__(pyqalxapi_dict)

    @classmethod
    def _chunks(cls, _iterable, chunk_size, fillvalue=None):
        """
        Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        Taken from the itertools documentation
        """
        args = [iter(_iterable)] * chunk_size
        return zip_longest(fillvalue=fillvalue, *args)

    @classmethod
    def pluralise(cls):
        """
        Pluralises the entity type
        """
        vowels = {"a", "e", "i", "o", "u", "y"}
        singular = cls.entity_type
        plural = singular + "s"
        if len(singular) > 1 and singular.endswith("y"):
            if singular[-2] not in vowels:
                plural = singular[:-1] + "ies"
        return plural

    def __super_setattr__(self, name, value):
        """
        Convenience method for setting proper attributes on the entity class.
        Because we are using `ObjectDict` if we did
        `self.<name> = value` this would set the
        dict key of `<name>` which we don't want.  So we call
        the supermethod to properly set the attribute
        :param name: The name of the attribute to set
        :param value: The value of the attribute to set
        """
        super(ObjectDict, self).__setattr__(name, value)

    def __dir__(self):
        """
        By default `ObjectDict` __dir__ only returns the keys on the dict.
        We want it to return everything as normal as entities might have
        methods that the user needs to know about
        """
        return super(ObjectDict, self).__dir__()


class QalxFileEntity(QalxEntity):
    _file_bytes = None
    _file_key = "file"

    def __init__(self, *args, **kwargs):
        """
        QalxFileEntity subclasses can be provided with a `keyfile` kwarg.
        This gets set on the instance of the entity and will allow for seamless
        decryption of files
        """
        self.__super_setattr__("_key_file", kwargs.pop("keyfile", None))
        super(QalxFileEntity, self).__init__(*args, **kwargs)

    def read_file(self):
        """
        If this Item contains a file, will read the file data and cache it
        against the Item.

        :param key_file:    The path to the encryption key to be used for
                            decrypting the file data. If it is not provided
                            and the data was encrypted, the data will be read
                            in the encrypted format
        :return:    The content of the URL as a bytes object.  Accessible from
                    the `_file_bytes` attribute
        :raises: pyqalx.errors.QalxError
        """
        if not self.get(self._file_key):
            raise QalxError("Item doesn't have file data.")
        else:
            response = requests.get(url=self[self._file_key]["url"])
            if response.ok:
                file_bytes = response.content
                if (
                    self[self._file_key].get("keyfile") is not None
                    and self._key_file is not None
                ):
                    qalx_encrypt = QalxEncrypt(self._key_file)
                    file_bytes = qalx_encrypt.decrypt(file_bytes)
                self.__super_setattr__("_file_bytes", file_bytes)
                return self._file_bytes
            else:
                raise QalxError(
                    "Error with file retrieval: \n\n" + response.text
                )

    def save_file_to_disk(self, filepath, filename=None):
        """
        If this Item contains a file, will read the file from the URL (or from
        the cached bytes on the instance) and save the file to disk.  Provide
        an optional `filename` argument if you don't want to use the same
        filename as the one stored on the Item

        :param filepath: The path where this file should be saved
        :type filepath: str
        :param filename: The optional name of this file. Defaults to the name
            of the file on the instance
        :type filename: str
        :param key_file:    The path to the encryption key to be used for
                            decrypting the file data. If it is not provided
                            and the data was encrypted, the data will be read
                            in the encrypted format
        :type key_file:     str
        :raises: pyqalx.errors.QalxError
        """
        if filename is None:
            filename = self[self._file_key]["name"]
        if self._file_bytes is None:
            self.read_file()
        _filepath = os.path.join(filepath, filename)
        with open(_filepath, "wb") as f:
            f.write(self._file_bytes)
        return _filepath


class QalxQueueableEntity(QalxEntity):
    """
    A mixin which allows an entity to be sumitted to queue
    """

    @classmethod
    def add_to_queue(cls, payload, queue, children=False, **message_kwargs):
        """
        Submits an entity, entity guid or list of entities/entity guids
        to the given queue
        :param payload:subclassed instance of ~entities.entity.QalxEntity,
        a guid, or a list containing a combination of both
        :param queue: An instance of ~entities.queue.Queue
        Usage:
        :type queue:~entities.queue.Queue
        :param children:Whether we are submitting the child entities to the
        queue rather than the given entity
        :type children: bool
        Example usage for an Item
        Item.add_to_queue(item, queue)
        Item.add_to_queue(item.guid, queue)
        Item.add_to_queue([item, item.guid], queue)
        """
        entity_type = cls.entity_type
        if children:
            #  Get the children off this entity and submit them to the queue
            if not hasattr(cls, "child_entity_class"):
                raise QalxQueueError(
                    f"`{cls}` is not an entity that " f"has children."
                )
            if not isinstance(payload, cls):
                raise QalxQueueError(
                    f"Expected payload of type `{cls}"
                    f"` when calling `{cls.__name__}.add_to_queue` "
                    f"with `children=True`. "
                    f"Got `{type(payload)}`."
                )
            # SQS needs the guid as a string - not UUID
            message_kwargs[f"parent_{entity_type}_guid"] = str(payload["guid"])
            entity_type = cls.child_entity_class.entity_type
            payload = list(payload[cls.child_entity_class.pluralise()].values())
        return queue._send_message(
            payload=payload, entity_type=entity_type, **message_kwargs
        )
