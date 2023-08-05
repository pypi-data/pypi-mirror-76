from .convoKitMeta import ConvoKitMeta
from convokit.util import warn, deprecation

class CorpusObject:

    def __init__(self, obj_type: str, owner=None, id=None, meta=None):
        self.obj_type = obj_type  # utterance, speaker, conversation
        self._owner = owner
        if meta is None:
            meta = dict()
        self.meta = self.init_meta(meta)
        self.id = id

    def get_owner(self):
        return self._owner

    def set_owner(self, owner):
        self._owner = owner
        if owner is not None:
            self.meta = self.init_meta(self.meta)

    owner = property(get_owner, set_owner)

    def init_meta(self, meta):
        if self._owner is None:
            return meta
        else:
            ck_meta = ConvoKitMeta(self.owner.meta_index, self.obj_type)
            for key, value in meta.items():
                ck_meta[key] = value
            return ck_meta

    def get_id(self):
        return self._id

    def set_id(self, value):
        if not isinstance(value, str) and value is not None:
            self._id = str(value)
            warn("{} id must be a string. Input has been casted to string.".format(self.obj_type))
        self._id = value

    id = property(get_id, set_id)

    # def __eq__(self, other):
    #     if type(self) != type(other): return False
    #     # do not compare 'utterances' and 'conversations' in Speaker.__dict__. recursion loop will occur.
    #     self_keys = set(self.__dict__).difference(['_owner', 'meta', 'utterances', 'conversations'])
    #     other_keys = set(other.__dict__).difference(['_owner', 'meta', 'utterances', 'conversations'])
    #     return self_keys == other_keys and all([self.__dict__[k] == other.__dict__[k] for k in self_keys])

    def retrieve_meta(self, key: str):
        """
        Retrieves a value stored under the key of the metadata of corpus object

        :param key: name of metadata
        :return: value (if key not found, raises an error)
        """
        return self.meta[key]

    def add_meta(self, key: str, value) -> None:
        """
        Adds a key-value pair to the metadata of the corpus object

        :param key: name of metadata
        :return: None
        """
        self.meta[key] = value

    def get_info(self, key):
        """
        Gets attribute <key> of the corpus object. Returns None if the corpus object does not have this attribute.

        :param key: name of attribute
        :return: attribute <key>
        """
        deprecation("get_info()", "retrieve_meta()")
        return self.meta.get(key, None)

    def set_info(self, key, value):
        """
        Sets attribute <key> of the corpus object to <value>.

        :param key: name of attribute
        :param value: value to set
        :return: None
        """
        deprecation("set_info()", "add_meta()")
        self.meta[key] = value

    def del_info(self, key):
        if key in self.meta:
            del self.meta[key]

    def __str__(self):
        return "{}('id': {}, 'meta': {})".format(self.obj_type.capitalize(),
                                                 self.id,
                                                 self.meta)

    def __hash__(self):
        return hash(self.obj_type + str(self.id))

    def __repr__(self):
        copy = self.__dict__.copy()
        deleted_keys = ['utterances', 'conversations', 'user']
        for k in deleted_keys:
            if k in copy:
                del copy[k]
        try:
            return self.obj_type.capitalize() + "(" + str(copy) + ")"
        except AttributeError: # for backwards compatibility when corpus objects are saved as binary data, e.g. wikiconv
            return "(" + str(copy) + ")"
