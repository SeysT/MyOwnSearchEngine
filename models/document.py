from nltk.tokenize import word_tokenize


class DocumentCollection(object):

    def __init__(self, data_filename='', stop_list_filename='', load_on_creation=True):
        self.data_filename = data_filename
        self.stop_list_filename = stop_list_filename
        self.common_words = []
        self.collection = {}
        if load_on_creation:
            self.load_common_words()
            self.load_collection()

    def load_common_words(self):
        with open(self.stop_list_filename, 'r') as sl:
            data = sl.read()

        self.common_words = [line.strip() for line in data.split('\n')]

    def load_collection(self):
        raise NotImplementedError

    @property
    def vocabulary(self):
        vocabulary = {}
        for document in self.collection.values():
            for attr in document.tokenized_fields:
                for token in getattr(document, attr):
                    try:
                        vocabulary[token] += 1
                    except KeyError:
                        vocabulary[token] = 1

        return vocabulary

    @property
    def vocabulary_size(self):
        return len(self.vocabulary.keys())

    @property
    def token_number(self):
        token_number = 0
        for frequence in self.vocabulary.values():
            token_number += frequence

        return token_number


class CACMDocumentCollection(DocumentCollection):
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
            self.title_tokenized,
            self.summary_tokenized,
            self.key_words_tokenized
        )