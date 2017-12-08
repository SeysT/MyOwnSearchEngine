from nltk.tokenize import word_tokenize

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


class Document(object):

    tokenized_fields = [
        'title_tokenized',
        'summary_tokenized',
        'key_words_tokenized'
    ]
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
        for attr in Document.tokenized_fields:
            setattr(
                self,
                attr,
                word_tokenize(getattr(self, attr.replace('_tokenized', '')))
            )

    def clean_tokens(self, common_words):
        for attr in Document.tokenized_fields:
            new_attr_value = [
                token.lower()
                for token in getattr(self, attr)
                if not (
                    token.lower() in common_words or
                    token.lower() in Document.signs_to_remove
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
