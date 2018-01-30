# const taille_bloc
# fonction a écrire :
# parse block : stocke tous les termID, docID en mémoire jusqu'à remplir le block
#
# tri du block
# write block to disk : sauvegarde du bloc de l'index sur le disque

from threading import Thread
from math import ceil
import operator
import os
from models.document import StanfordDocumentCollection

from models.document import CACMDocumentCollection


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
        if document_collection:
            self.create_index(document_collection)

    def parse_all_terms(self, collection):
        for document in collection.values():
            for token in document.term_bag:
                try:
                    self.term_dict[token]  # check if the term already exists
                except KeyError:
                    self.term_dict[token] = ReverseIndex.term_id
                    ReverseIndex.term_id += 1

    def create_index(self):
        raise NotImplementedError


class StanfordReverseIndex(ReverseIndex):

    def create_index(self, document_collection):
        # document_collection = StanfordDocumentCollection(
        #     data_dirname='Data/CS276',
        #     load_on_creation=True,
        # )

        for collection in document_collection.values():
            Mapper.map(collection)
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
    def map(collection):
        term_dict = {}
        for doc in collection:
            for term_id, frequence in doc.term_bag.items():
                try:
                    # term_dict[term_id] += 1
                    # {term: [frequence_col, [(document_id, frequence_doc, doc_len)...]]}
                    term_dict[term_id][0] += 1
                    term_dict[term_id][1].append(
                        (doc.id, frequence, len(doc.term_bag))
                    )
                except KeyError:
                    # term_dict[term_id] = 1
                    term_dict[term_id] = [1, [(doc.id, frequence, len(doc.term_bag))]]
        sorted_keys = sorted(term_dict.items(), key=operator.itemgetter(0))
        # store sorted keys line by line in the file so that lines can be
        # extracted one by one when merging the list
        with open('temp/' + str(Mapper.output_file), 'a') as collection_file:
            for k in sorted_keys:
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
    def reduce(term_id, postings):
        # open a small amount of each file (the beginning part)
        # take the first element, output the lowest one to a file
        # then pick another element from another file
        # loop
        posting_list = []
        for posting in postings:
            posting_list.append(posting)
        sorted(posting_list)
        # emit(term_id, posting_list)

    @staticmethod
    def select(choices):
        min_index = 0
        while min_index not in choices:
            min_index += 1
        for i in range(min_index + 1, len(choices)):
            if i in choices and choices[i] < choices[min_index]:
                min_index = i
        return min_index

    @staticmethod
    def open_files(filenames):
        for i in range(len(filenames)):
            files = open(filenames[i], 'r', 1)  # select line buffering
        return files


if __name__ == '__main__':
    if 'CS276' in os.listdir('Data/Collection'):
        document_collection = StanfordDocumentCollection(
            data_dirname='Data/CS276',
            load_on_creation=False
        )
        document_collection.load_from_dir('Data/Collection/CS276')
    else:
        document_collection = StanfordDocumentCollection(
            data_dirname='Data/CS276',
            load_on_creation=True,
        )
    rv_index = StanfordReverseIndex(document_collection)
    rv_index.create_index()
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
