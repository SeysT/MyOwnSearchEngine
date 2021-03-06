import pickle
import os

from nltk.tokenize import word_tokenize


class DocumentCollection(object):

    def __init__(self, source_data_filepath='', name='', load_on_creation=False):
        self.source_data_filepath = source_data_filepath
        self.collection = {}
        self.name = name
        if load_on_creation:
            self.load_collection()
            self.generate_vocabulary()

    def save(self, filepath):
        with open(filepath, 'wb') as collection_file:
            pickler = pickle.Pickler(collection_file)
            pickler.dump(self.collection)

    def load_from_file(self, filepath):
        with open(filepath, 'rb') as collection_file:
            depickler = pickle.Unpickler(collection_file)
            self.collection = depickler.load()
        self.generate_vocabulary()

    def load_collection(self):
        raise NotImplementedError

    def generate_vocabulary(self):
        self._generate_vocabulary()
        self._generate_vocabulary_size()
        self._generate_token_number()

    def _generate_vocabulary(self):
        self.vocabulary = {}
        for document in self.collection.values():
            for attr in document.tokenized_fields:
                for token in getattr(document, attr):
                    try:
                        self.vocabulary[token] += 1
                    except KeyError:
                        self.vocabulary[token] = 1

    def _generate_vocabulary_size(self):
        self.vocabulary_size = len(self.vocabulary.keys())

    def _generate_token_number(self):
        self.token_number = 0
        for frequence in self.vocabulary.values():
            self.token_number += frequence

    def __getitem__(self, key):
        """This methods wraps the __getitem__ methods of self.collection"""
        return self.collection[key]

    def __setitem__(self, key, value):
        """This methods wraps the __setitem__ methods of self.collection"""
        self.collection[key] = value

    def __delitem__(self, key):
        """This methods wraps the __delitem__ methods of self.collection"""
        del self.collection[key]

    def items(self):
        """This methods wraps the items methods of self.collection"""
        return self.collection.items()

    def values(self):
        """This methods wraps the values methods of self.collection"""
        return self.collection.values()

    def keys(self):
        """This methods wraps the keys methods of self.collection"""
        return self.collection.keys()

    def __len__(self):
        """This methods wraps the len methods of self.collection"""
        return len(self.collection)


class MetaDocumentCollection(object):
    """This class allows us to group collections in a single interface.
    This makes it easier to use our collection properties for a significant
    amount of data when files are splitted in multiple directories.
    """

    def __init__(self, data_dirpath='', name='', load_on_creation=False):
        self.data_dirpath = data_dirpath
        self.name = name
        self.meta_collection = {}  # must contains DocumentCollection objects
        if load_on_creation:
            self.load_collection()
            self.generate_vocabulary()

    def save(self, dirpath):
        for collection in self.meta_collection.values():
            with open(os.path.join(dirpath, collection.name) + '.collection', 'wb') as collection_file:
                pickler = pickle.Pickler(collection_file)
                pickler.dump(collection)

    def load_from_dir(self, dirpath):
        for file in os.listdir(dirpath):
            with open(os.path.join(dirpath, file), 'rb') as collection_file:
                depickler = pickle.Unpickler(collection_file)
                self.meta_collection[file] = depickler.load()
        self.generate_vocabulary()

    def load_collection(self):
        raise NotImplementedError

    def generate_vocabulary(self):
        self._generate_vocabulary()
        self._generate_vocabulary_size()
        self._generate_token_number()

    def generate_half_document_collection(self):
        for coll in self.get_collections():
            coll.collection = {
                key: value
                for key, value
                in list(coll.collection.items())[:len(coll.collection) // 2]
            }

    def _generate_vocabulary(self):
        self.vocabulary = {}
        for collection in self.meta_collection.values():
            for document in collection.values():
                for attr in document.tokenized_fields:
                    for token in getattr(document, attr):
                        try:
                            self.vocabulary[token] += 1
                        except KeyError:
                            self.vocabulary[token] = 1

    def _generate_vocabulary_size(self):
        self.vocabulary_size = len(self.vocabulary.keys())

    def _generate_token_number(self):
        self.token_number = 0
        for frequence in self.vocabulary.values():
            self.token_number += frequence

    def __getitem__(self, key):
        """This methods wraps the __getitem__ methods of self.collection"""
        for collection in self.meta_collection.values():
            try:
                item = collection[key]
                return item
            except KeyError:
                continue
        raise KeyError

    def __setitem__(self, key, value):
        """This methods wraps the __setitem__ methods of self.collection"""
        is_set = False
        for collection in self.meta_collection.values():
            try:
                collection[key] = value
                is_set = True
            except KeyError:
                continue
        if not is_set:
            raise KeyError

    def __delitem__(self, key):
        """This methods wraps the __delitem__ methods of self.collection"""
        is_del = False
        for collection in self.meta_collection.values():
            try:
                del self.collection[key]
                is_del = True
            except KeyError:
                continue
        if not is_del:
            raise KeyError

    def get_collections(self):
        col = {}
        for collection in self.meta_collection.values():
            col[collection.name] = collection
        return col.values()

    def items(self):
        """This methods wraps the items methods of self.collection"""
        items = []
        for collection in self.meta_collection.values():
            items.append(collection.items())
        return items

    def values(self):
        """This methods wraps the values methods of self.collection"""
        values = []
        for collection in self.meta_collection.values():
            values.append(collection.values())
        return values

    def keys(self):
        """This methods wraps the keys methods of self.collection"""
        keys = []
        for collection in self.meta_collection.values():
            keys.append(collection.keys())
        return keys

    def __len__(self):
        """This methods wraps the len methods of self.collection"""
        length = 0
        for collection in self.meta_collection.values():
            length += len(collection)
        return length


class CACMDocumentCollection(DocumentCollection):

    def __init__(self, source_data_filepath='', stop_list_filepath='', load_on_creation=False):
        self.common_words = []
        self.stop_list_filepath = stop_list_filepath
        self.name = 'cacm'
        if load_on_creation:
            # needs to be done before calling the load_collection method that
            # needs the common words to clean the tokens
            self.load_common_words()
        super().__init__(source_data_filepath, self.name, load_on_creation)

    def load_common_words(self):
        with open(self.stop_list_filepath, 'r') as sl:
            data = sl.read()

        self.common_words = [line.strip() for line in data.split('\n')]

    def load_collection(self):
        with open(self.source_data_filepath, 'r') as df:
            data = df.read()

        current_id = None
        for line in data.split('\n'):
            if line.startswith('.I'):
                if current_id:
                    self.collection[current_id].tokenize_doc()
                    self.collection[current_id].clean_tokens(self.common_words)
                current_id = line.replace('.I ', '')
                self.collection[current_id] = CACMDocument(current_id)
            elif line in CACMDocument.fields_mapping.keys():
                attr = CACMDocument.fields_mapping[line]
            else:
                attr_value = getattr(self.collection[current_id], attr, None)
                to_add = line.strip()
                setattr(
                    self.collection[current_id],
                    attr,
                    '{}\n{}'.format(attr_value, to_add) if attr_value else to_add,
                )
        self.collection[current_id].tokenize_doc()
        self.collection[current_id].clean_tokens(self.common_words)


class StanfordDocumentCollection(MetaDocumentCollection):

    def __init__(self, data_dirpath='', load_on_creation=False):
        self.name = 'cs276'
        self.current_doc_id = 0
        super().__init__(data_dirpath, self.name, load_on_creation)

    def load_collection(self):
        for directory in os.listdir(self.data_dirpath):
            print("DIRECTORY", directory)
            collection = DocumentCollection(name=directory)
            for filename in os.listdir(os.path.join(self.data_dirpath, directory)):

                with open(os.path.join(self.data_dirpath, directory, filename), 'r')as df:
                    data = df.read()

                tokens = [token for token in data.split()]

                # modify document collection to add the Stanford Document
                collection[self.current_doc_id] = StanfordDocument(
                    self.current_doc_id,
                    filename,
                    tokens
                )
                self.current_doc_id += 1
            self.meta_collection[directory] = collection


class Document(object):
    tokenized_fields = []

    def __init__(self, id):
        self.id = id

    @property
    def term_bag(self):
        term_bag = {}
        for attr in self.tokenized_fields:
            for token in getattr(self, attr):
                try:
                    term_bag[token] += 1
                except KeyError:
                    term_bag[token] = 1
        return term_bag


class CACMDocument(Document):
    tokenized_fields = [
        'title_tokenized',
        'summary_tokenized',
        'key_words_tokenized',
    ]
    signs_to_remove = [',', '\'', ';', ':', '.', '?', '!', '(', ')']
    fields_mapping = {
        '.T': 'title',
        '.W': 'summary',
        '.B': 'publication_date',
        '.A': 'authors',
        '.N': 'add_date',
        '.X': 'references',
        '.K': 'key_words',
        '.C': 'citations',
    }

    def __init__(self, id):
        super(CACMDocument, self).__init__(id)
        for field in self.fields_mapping.values():
            setattr(self, field, '')
        for tokenized_field in self.tokenized_fields:
            setattr(self, tokenized_field, [])

    def tokenize_doc(self):
        for attr in CACMDocument.tokenized_fields:
            setattr(
                self,
                attr,
                word_tokenize(getattr(self, attr.replace('_tokenized', '')))
            )

    def clean_tokens(self, common_words):
        for attr in CACMDocument.tokenized_fields:
            new_attr_value = [
                token.lower()
                for token in getattr(self, attr)
                if not (
                    token.lower() in common_words or
                    token.lower() in CACMDocument.signs_to_remove
                )
            ]
            setattr(self, attr, new_attr_value)

    def __repr__(self):
        return "DOCID : {}\nTITLE : {}\nSUMMARY : {}\nKEYWORDS : {}".format(
            self.id,
            self.title.replace('\n', ' '),
            self.summary.replace('\n', ' '),
            self.key_words.replace('\n', ' ')
        )


class StanfordDocument(Document):
    tokenized_fields = [
        'content'
    ]

    def __init__(self, id, title, content):
        super().__init__(id)
        self.content = content
        self.title = title

    def __repr__(self):
        return "DOCID : {}\nTITLE : {}\nCONTENT: {}\n".format(
            self.id,
            self.title,
            ' '.join(self.content)
        )
