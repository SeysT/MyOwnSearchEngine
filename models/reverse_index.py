import pickle


class ReverseIndex(object):
    """
    This class contains our model for our reverse index
    + attributes:
        - reverse_index: contains the reverse index with the following structure:
            {term: [frequence_doc, [document_ids...]]}
    + methods:
        - add_document: update self.reverse_index with a given document
        - save: save the current self.reverse_index in the given filename
        - load_from_file: load the reverse index contains in the given file
        - create_index: create reverse_index from given document_collection
    """

    def __init__(self, document_collection=None):
        """
        We init the reverse_index attribute to an empty dict.
        If a document collection, we initialize reverse_index calling create_index method.
        """
        self.reverse_index = {}
        if document_collection:
            self.create_index(document_collection)

    def add_document(self, document):
        """
        Update self.reverse_index given a document
        + params:
            - document: should contain a term_bag property built like this:
                {term, frequence}
        + return:
            None
        + summary:
            foreach term contains in keys of term_bag document:
                we update the frequence_doc of current term
                we add the document_id
        """
        for term in document.term_bag.keys():
            try:
                self.reverse_index[term][0] += 1
                self.reverse_index[term][1].append(document.id)
            except KeyError:
                self.reverse_index[term] = [1, [document.id]]

    def create_index(self, document_collection):
        """
        Create reverse_index from given document_collection
        + params:
            - document_collection: should be a DocumentCollection object
        + return:
            None
        """
        for document in document_collection.collection.values():
            self.add_document(document)

    def save(self, filename):
        """
        Save current self.reverse_index in the file with filename name
        + params:
            - filename: name of the file to store reverse index in
        + return:
            None
        """
        with open(filename, 'wb') as index_file:
            pickler = pickle.Pickler(index_file)
            pickler.dump(self.reverse_index)

    def load_from_file(self, filename):
        """
        Load reverse index contains in file with given filename.
        + params:
            - filename: name of the file to retrieve reverse index
        + return:
            None
        """
        with open(filename, 'rb') as index_file:
            depickler = pickle.Unpickler(index_file)
            self.reverse_index = depickler.load()
