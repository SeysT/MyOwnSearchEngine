class Document(object):

    index_fields = ('title', 'summary', 'key_words')

    def __init__(self, id):
        self.id = id
        self.title = ''
        self.summary = ''
        self.publication_date = ''
        self.authors = ''
        self.add_date = ''
        self.references = ''
        self.key_words = ''
