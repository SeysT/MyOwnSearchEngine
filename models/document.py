import pickle
import os

from nltk.tokenize import word_tokenize


class DocumentCollection(object):

    def __init__(self, data_filename='', load_on_creation=False):
        self.data_filename = data_filename
        self.collection = {}
        if load_on_creation:
            self.load_collection()
            self.generate_vocabulary()

    def save(self, filename):
        with open(filename, 'wb') as collection_file:
            pickler = pickle.Pickler(collection_file)
            pickler.dump(self.collection)

    def load_from_file(self, filename):
        with open(filename, 'rb') as collection_file:
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


class CACMDocumentCollection(DocumentCollection):

    def __init__(self, data_filename='', stop_list_filename='', load_on_creation=False):
        self.stop_list_filename = stop_list_filename
        self.common_words = []
        if load_on_creation:
            # needs to be done before calling the load_collection method that
            # needs the common words to clean the tokens
            self.load_common_words()
        super().__init__(data_filename, load_on_creation)

    def load_common_words(self):
        with open(self.stop_list_filename, 'r') as sl:
            data = sl.read()

        self.common_words = [line.strip() for line in data.split('\n')]

    def load_collection(self):
        with open(self.data_filename, 'r') as df:
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


class StanfordDocumentCollection(DocumentCollection):
    def load_collection(self):
        for directory in os.listdir(self.data_filename):
            print("DIRECTORY", directory)
            for filename in os.listdir(self.data_filename + '/' + directory):

                with open(self.data_filename + '/' + directory + '/' + filename, 'r')as df:
                    data = df.read()

                tokens = [token for token in data.split()]

                # modify document collection to add the Stanford Document
                self.collection[filename] = StanfordDocument(filename, tokens)


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
        'key_words_tokenized'
    ]
    signs_to_remove = [',', '\'', ';', ':', '.', '?', '!']
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
        self.title = ''
        self.title_tokenized = []
        self.summary = ''
        self.summary_tokenized = []
        self.publication_date = ''
        self.authors = ''
        self.add_date = ''
        self.references = ''
        self.key_words = ''
        self.key_words_tokenized = []
        self.citations = ''

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

    def __init__(self, id, content):
        super().__init__(id)
        self.content = content

    def __repr__(self):
        return "DOCID : {}\n CONTENT: {}\n".format(
            self.id,
            self.content
        )
