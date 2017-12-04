from nltk.tokenize import word_tokenize


class Document(object):

    tokenized_fields = ('title_tokenized', 'summary_tokenized', 'key_words_tokenized')
    signs_to_remove = [',', '\'', ';', ':', '.', '?', '!']

    def __init__(self, id):
        self.id = id
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
        self.title_tokenized = word_tokenize(self.title)
        self.summary_tokenized = word_tokenize(self.summary)
        self.key_words_tokenized = word_tokenize(self.key_words)

    def clean_tokens(self, common_words):

        for token in self.title_tokenized:
            if token in common_words or token in Document.signs_to_remove:
                self.title_tokenized.remove(token)

        for token in self.summary_tokenized:
            if token in common_words or token in Document.signs_to_remove:
                self.summary_tokenized.remove(token)

        for token in self.key_words_tokenized:
            if token in common_words or token in Document.signs_to_remove:
                self.key_words_tokenized.remove(token)

    def __repr__(self):
        return "DOCID : {}\nTITLE : {}\nSUMMARY : {}\nKEYWORDS : {}".format(self.id, self.title_tokenized, self.summary_tokenized, self.key_words_tokenized)
