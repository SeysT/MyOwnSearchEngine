import operator
import os
import ast
from datetime import datetime


class ReverseIndex(object):
    """
    This class contains our model for our reverse index
    + attributes:
        - reverse_index: contains the reverse index with the following structure:
            {term: [frequence_col, [(document_id, frequence_doc, doc_len)...]]}
        - term_dict: dict that contains all the terms of all the documents and
        their affected id under the form {term: id}
        - term_id: static attribute used to keep track of the last attributed id
    + core methods:
        - save: save the current self.reverse_index in the given filename in a
        text file
        - load_from_file: load the reverse index contained in the given text
        file
        - create_index: create reverse_index from given document_collection
    + wrapping methods:
        - __getitem__: return self.reverse_index[key]
        - __setitem__: self.reverse_index[key] = value
        - __delitem__: del self.reverse_index[key]
        - __len__: return len(self.reverse_index)
        - items: return self.reverse_index.items()
        - values: return self.reverse_index.values()
        - keys: return self.reverse_index.keys()
    """
    term_id = 0

    def __init__(self, document_collection=None):
        """
        We init the reverse_index attribute to an empty dict.
        """
        self.reverse_index = {}
        self.term_dict = {}

    def create_index(self, document_collection):
        raise NotImplementedError

    def __getitem__(self, key):
        """This methods wraps the __getitem__ methods of self.reverse_index"""
        return self.reverse_index[key]

    def __setitem__(self, key, value):
        """This methods wraps the __setitem__ methods of self.reverse_index"""
        self.reverse_index[key] = value

    def __delitem__(self, key):
        """This methods wraps the __delitem__ methods of self.reverse_index"""
        del self.reverse_index[key]

    def items(self):
        """This methods wraps the items methods of self.reverse_index"""
        return self.reverse_index.items()

    def values(self):
        """This methods wraps the values methods of self.reverse_index"""
        return self.reverse_index.values()

    def keys(self):
        """This methods wraps the keys methods of self.reverse_index"""
        return self.reverse_index.keys()

    def __len__(self):
        """This methods wraps the keys methods of self.reverse_index"""
        return len(self.reverse_index)


class StanfordReverseIndex(ReverseIndex):

    def __init__(self, document_collection=None):
        super().__init__(document_collection)
        if document_collection:
            self.parse_all_terms(document_collection)
            self.create_index(document_collection)

    def parse_all_terms(self, document_collection):
        """
        This method collects all the terms that exists in all the documents,
        and give them a unique id
        """
        begin = datetime.now()
        for collection in document_collection.values():
            for document in collection:
                for token in document.term_bag:
                    try:
                        self.term_dict[token]  # check if the term already exists
                    except KeyError:
                        self.term_dict[token] = ReverseIndex.term_id
                        ReverseIndex.term_id += 1
        print("======= Generating term id dictionnary time : ", datetime.now() - begin, " =======")

    def create_index(self, meta_document_collection):
        """
        Creates the index using a MapReduce approach. Each bloc is a
        sub-collection of Stanford collection (ie a bloc = collection formed by
        all the files in a folder)
        """
        begin = datetime.now()
        for collection in meta_document_collection.get_collections():
            # print(collection)
            # send collections as blocs to the mapper
            Mapper.map(
                self.term_dict,
                collection,
                'temp/' + collection.data_filename + '.index'
            )
        print("======= Time for mapping : ", datetime.now() - begin, " =======")

        # it takes some time before the mapping is finished and the reducing
        # phase can starts
        begin = datetime.now()
        # Here we use only one reducer, that is enought to merge the indexes
        # in one time because we read the partial text indexes line by line
        file_paths = ['temp/' + f for f in os.listdir('temp/')]
        print(file_paths)
        Reducer.reduce(
            file_paths,
            'Data/Index/cs276.index'
        )
        print("======= Time for reducing : ", datetime.now() - begin, " =======")


class Mapper(object):
    """
    Class defining a mapper that takes a bloc, parse it, sort the terms
    following their term_id and write the result to a text file
    """

    @staticmethod
    def map(term_dict, collection, filepath):
        """
        + attributes:
            - term_dict : dict containing all the possible terms and their id
            - collection : object of type Collection containing all the
            documents that need to be indexed
            - filepath: path where the partial index must be stored
        """
        # dictionnary that contains all the (term_id, term) tuple_list
        # will be sorted later
        # form : {term_id: [frequence_col, [(document_id, frequence_doc, doc_len)...]]}
        term_id_dict = {}
        for index, doc in enumerate(collection.values()):
            if index % 1000 == 0:
                print("GETTING TERM OF INDEX :", index)

            for term, frequence in doc.term_bag.items():
                term_id = term_dict[term]
                try:
                    term_id_dict[term_id][0] += 1
                    term_id_dict[term_id][1].append(
                        (doc.id, frequence, len(doc.term_bag))
                    )
                except KeyError:
                    term_id_dict[term_id] = [
                        1,
                        [(doc.id, frequence, len(doc.term_bag))]
                    ]

        # all the elements from the collection are in the dictionnary, we now
        # sort them by term_id
        sorted_terms = sorted(term_id_dict.items(), key=operator.itemgetter(0))
        # store sorted keys line by line in the file so that lines can be
        # extracted one by one when merging the list
        with open(filepath, 'a') as partial_index_file:
            for k in sorted_terms:
                partial_index_file.write(str(k))
                partial_index_file.write('\n')
        print("FILE FINISHED", filepath)


class Reducer(object):
    """
    Class defining a reducer that takes many blocs as input, defined as text
    files, and merge them into one bloc with external sorting method
    """
    @staticmethod
    def reduce(input_filepaths, output_filepath):
        """
        + attributes:
            - input_filepaths: array containing the filepaths of the different
            text files containing the partial indexes
            - output_filepath: path where the final index will be outputted
        """
        files = Reducer.open_files(input_filepaths)

        with open(output_filepath, 'w', 1) as output_file:
            buffers = Buffers(files)

            # a few hints here : we get the index entry with the lowest term_id,
            # then get all the following index entries with the same term_id,
            # whether they are from the same file or another one.
            # When we got all those values, we merge all those posting lists
            # into one, and write the final index entry to a file.
            # We iterate over all the possible term_id, and stop when the partial
            # index files are empty.
            while not buffers.isEmpty:
                L = []  # list of entries sharing the same term_id
                # index entry is like (term_id, [frequence_col, [(document_id, frequence_doc, doc_len)...]])
                _, index_entry = buffers.update()
                if index_entry is None:
                    break
                term_id = index_entry[0]
                while True:
                    min_value, index_entry = buffers.update()
                    if index_entry is None:
                        break
                    if term_id != index_entry[0]:  # new term, we will merge it later
                        break
                    L.append(index_entry)
                    buffers.remove_value(min_value)

                # merge the different terms into one
                new_entry = (term_id, [0, []])
                for entry in L:
                    new_entry[1][0] += entry[1][0]
                    for posting in entry[1][1]:
                        new_entry[1][1].append(
                            (posting[0], posting[1], posting[2])
                        )

                output_file.write(str(new_entry))
                output_file.write('\n')
                if term_id % 1000 == 0:
                    print("INDEXED_TERM", term_id)

    @staticmethod
    def open_files(input_filepaths):
        """Opens the files containing the sorted parts of the index.
            + filenames: array of strings, that are the paths to the files
            return: Dictionnary of files
        """
        files = {}
        for i in range(len(input_filepaths)):
            files[i] = open(input_filepaths[i], 'r', 1)  # select line buffering
        return files


class Buffers(object):
    # inspired from https://github.com/spiralout/external-sort
    """
    Class that will handle multiple buffers at the time, corresponding to
    multiple text files. At the beginning the buffers are filled with the first
    line of each file (one line = one index entry), then we refill them with
    the next line of the the file that the reducer has used.
    + attributes:
        - files: list of File objects that we need to pump the index entries from
        - buffers: dictionnary of buffers, of the form {file_ref: index_entry}
        - empty_buffers: set of buffers that are considered as empty, meaning
        the last line of the corresponding file has been reached
    """

    def __init__(self, files):
        self.files = files
        self.buffers = {i: None for i in range(len(files))}
        self.empty_buffers = set()

    def _select_min_value(self, choices):
        """Implements the k-way merging : selects the index of the choices with
        the lowest value (temr_id value for us).
            + choices : dictionnary of {buffer_index: value}
        """
        min_index = -1
        for an_index in choices:  # ensure min_index is in choices
            min_index = an_index
            break
        for i in choices:
            if choices[i] < choices[min_index]:
                min_index = i
        return min_index

    def _fill_buffers(self):
        """
        Fill in the buffers that are empty with data from the partial index
        files
        """
        for i in range(len(self.buffers)):
            if self.buffers[i] is None and i not in self.empty_buffers:
                line = self.files[i].readline()
                if line == '':  # EOF
                    self.empty_buffers.add(i)
                    print("EMPTY BUFFERS", self.empty_buffers, len(self.empty_buffers), len(self.files))
                    continue
                # converts the string to object : (term_id, [frequence_col, [(document_id, frequence_doc, doc_len)...]])
                self.buffers[i] = ast.literal_eval(line)  # converts the string
        if self.isEmpty:
            return False
        else:
            return True

    def _get_buffers_values(self):
        """
        Returns the term_id from each buffer to later pick the lowest
        """
        return {i: self.buffers[i][0] for i in range(len(self.buffers)) if i not in self.empty_buffers}

    def update(self):
        """
        Public method that fill the buffers if they are empty, then selects the
        buffer index with the lowest value.
        + return: buffer_index_min_value, corresponding_value
        """
        if self._fill_buffers():
            min_index = self._select_min_value(self._get_buffers_values())
            return min_index, self.buffers[min_index]
        else:
            return -1, None

    def remove_value(self, index):
        """
        Removes a value from the buffer designed by the index.
        """
        self.buffers[index] = None

    @property
    def isEmpty(self):
        return len(self.empty_buffers) == len(self.files)  # All files ended


# if __name__ == '__main__':
#
#     collection = CACMDocumentCollection(
#         data_filename='Data/CACM/cacm.all',
#         stop_list_filename='Data/CACM/common_words',
#         load_on_creation=True,
#     )
#
#     rv_index = ReverseIndex(collection)
#     rv_index.create_index()
#     print("END")
