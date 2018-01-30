# const taille_bloc
# fonction a écrire :
# parse block : stocke tous les termID, docID en mémoire jusqu'à remplir le block
#
# tri du block
# write block to disk : sauvegarde du bloc de l'index sur le disque

import operator
import os
import ast


class ReverseIndex(object):
    """
    + attributes:
        - term_dict : dict that contains all the terms of all the documents and
        their affected id under the form {token: id}
    """
    term_id = 0

    def __init__(self, document_collection=None):
        """
        We init the reverse_index attribute to an empty dict.
        If a document collection, we initialize reverse_index calling create_index method.
        """
        self.reverse_index = {}
        # { (term, termID), ...}
        self.term_dict = {}

    def create_index(self):
        raise NotImplementedError


class StanfordReverseIndex(ReverseIndex):

    def __init__(self, document_collection=None):
        super().__init__(document_collection)
        if document_collection:
            self.parse_all_terms(document_collection)
            self.create_index(document_collection)

    def parse_all_terms(self, document_collection):
        for collection in document_collection.values():
            for document in collection:
                for token in document.term_bag:
                    try:
                        self.term_dict[token]  # check if the term already exists
                    except KeyError:
                        self.term_dict[token] = ReverseIndex.term_id
                        ReverseIndex.term_id += 1

    def create_index(self, document_collection):
        # document_collection = StanfordDocumentCollection(
        #     data_dirname='Data/CS276',
        #     load_on_creation=True,
        # )

        for collection in document_collection.values():
            Mapper.map(self.term_dict, collection)
            # send collections as blocs to the mapper

# differentiate the stanford index from the CACM Index
# in Stanford, we have to open documents once in a while


class Mapper(object):

    """A bloc is defined as following :
        A folder or a file, containing multiple documents (the size and the
        number of documents is given by the document collection)
    """
    output_file = 0

    @staticmethod
    def map(term_dict, collection):
        print("Start collection")
        term_id_dict = {}
        for index, doc in enumerate(collection):
            if index % 1000 == 0:
                print(index)
            for term, frequence in doc.term_bag.items():
                term_id = term_dict[term]
                try:
                    # term_id_dict[term_id] += 1
                    # {term: [frequence_col, [(document_id, frequence_doc, doc_len)...]]}
                    term_id_dict[term_id][0] += 1
                    term_id_dict[term_id][1].append(
                        (doc.id, frequence, len(doc.term_bag))
                    )
                except KeyError:
                    # term_id_dict[term_id] = 1
                    term_id_dict[term_id] = [1, [(doc.id, frequence, len(doc.term_bag))]]
        sorted_keys = sorted(term_id_dict.items(), key=operator.itemgetter(0))
        # store sorted keys line by line in the file so that lines can be
        # extracted one by one when merging the list
        with open('temp/' + str(Mapper.output_file), 'a') as collection_file:
            for k in sorted_keys:
                # for token, id in term_dict.items():
                #     if k[0] == id:
                #         print("term_id", k[0], "word", token)
                collection_file.write(str(k))
                collection_file.write('\n')
        print("FILE FINISHED", Mapper.output_file)
        Mapper.output_file += 1

    @staticmethod
    def save_to_disk():
        pass
        # write the bloc to the disk
        # for term_id in term_dict:
            # emit(term_id, postings (doc_id, term_dict[term_id]))


class Reducer(object):

    @staticmethod
    def reduce():
        # open a small amount of each file (the beginning part)
        # take the first element, output the lowest one to a file
        # then pick another element from another file
        # loop
        # posting_list = []
        # for posting in postings:
        #     posting_list.append(posting)
        # sorted(posting_list)
        # emit(term_id, posting_list)
        file_paths = os.listdir('temp/')
        files = Reducer.open_files(file_paths)

        with open('Data/Index/cs276.index', 'w', 1) as output_file:
            buffers = Buffers(files)
            while not buffers.isEmpty:
                # check that we have got all the postings corresponding to the
                # same id before writing the posting list to the index
                L = []  # list of entries sharing the same term_id
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
                # {term: [fr equence_col, [(document_id, frequence_doc, doc_len)...]]}
                # term_id_dict[term_id][0] += 1
                # term_id_dict[term_id][1].append(
                #     (doc.id, frequence, len(doc.term_bag))
                # )
                new_entry = (term_id, [0, []])
                for entry in L:
                    new_entry[1][0] += entry[1][0]
                    for posting in entry[1][1]:
                        new_entry[1][1].append(
                            (posting[0], posting[1], posting[2])
                        )

                # then write it
                output_file.write(str(new_entry))
                output_file.write('\n')
                if term_id % 100 == 0:
                    print("INDEXED_TERM", term_id)
            print("loop ended")
        print("closed file & leaving function")
    # @staticmethod
    # def select_min_value(choices):
    #     """Implements the k-way merging : selects the choices with the lowest
    #     value.
    #         + choices : array of index
    #     """
    #     min_index = 0
    #     while min_index not in choices:
    #         min_index += 1
    #     for i in range(min_index + 1, len(choices)):
    #         if i in choices and choices[i] < choices[min_index]:
    #             min_index = i
    #     return min_index

    @staticmethod
    def open_files(filenames):
        """Opens the files containing the sorted parts of the index.
            + filenames: array of strings, that are the paths to the files
            return: Dictionnary of files
        """
        files = {}
        for i in range(len(filenames)):
            files[i] = open('temp/' + filenames[i], 'r', 1)  # select line buffering
        return files


class Buffers(object):
    # inspired from https://github.com/spiralout/external-sort

    def __init__(self, files):
        self.files = files
        self.buffers = {i: None for i in range(len(files))}
        self.empty_buffers = set()

    def _select_min_value(self, choices):
        """Implements the k-way merging : selects the choices with the lowest
        value.
            + choices : array of index
        """
        min_index = -1
        # print("CHOICES", choices)
        # while min_index not in choices:
        #     if self.isEmpty:
        #         print("Stuck in loop of_select_min_value")
        #     min_index += 1
        for an_index in choices: #ensure min_index is in choices
            min_index = an_index
            break
        # for i in range(min_index + 1, len(choices)):
        #     if i in choices and choices[i] < choices[min_index]:
        #         min_index = i
        for i in choices:
            if choices[i] < choices[min_index]:
                min_index = i
        return min_index

    def _fill_buffers(self):
        """Fill in the buffers with data from the partial index files
        """
        for i in range(len(self.buffers)):
            # TODO : convert the string value to a tuple to sort it
            if self.buffers[i] is None and i not in self.empty_buffers:
                # self.buffers[i] = self.files[i].readline()
                line = self.files[i].readline()
                if line == '':  # EOF
                    self.empty_buffers.add(i)
                    print("EMPTY BUFFERS", self.empty_buffers, len(self.empty_buffers), len(self.files))
                    continue
                value = ast.literal_eval(line)
                # print("BLOC", i, "TERM_ID", line[1:2], end='     ')
                self.buffers[i] = value
        if self.isEmpty:
            return False
        else:
            return True

    def _get_buffers_values(self):
        # returning the tem_id for sorting
        return {i: self.buffers[i][0] for i in range(len(self.buffers)) if i not in self.empty_buffers}

    def update(self):
        if self._fill_buffers():
            # print("ALL_INDEX", self._get_buffers_values(), end='   ')
            min_index = self._select_min_value(self._get_buffers_values())
            # print("MIN_INDEX", min_index, end='   ')
            # print("TERM_ID_VALUE", self.buffers[min_index][0])
            return min_index, self.buffers[min_index]
        else:
            return -1, None

    def remove_value(self, index):
        self.buffers[index] = None

    @property
    def isEmpty(self):
        return len(self.empty_buffers) == len(self.files)  # All files ended


# if __name__ == '__main__':
#
#
#     def map(self):
#         # segmenting the collection into blocks, loading one block in memory
#         # for directory in os.listdir(self.collection.data_filename):
#         with open(self.data_filename, 'r') as df:
#             data = df.read()
#
#         # tuple format : (term_id, position)
#         tuple_list = []
#
#
#
#
#         # for i in range(int(len(self.hash_table) / BLOCK_SIZE)):
#         #     self.threads[i] = WorkerThread(
#         #         self.hash_table[
#         #             self.mapped_term_id:self.mapped_term_id + BLOCK_SIZE
#         #         ]
#         #     )
#         #     self.mapped_term_id += BLOCK_SIZE
#
#     def reduce(self):
#         pass
#
#
# class WorkerThread(Thread):
#
#     def __init__(self, block):
#         super().__init__()
#         self.block = block
#
#     def run(self):
#         print(block)


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
