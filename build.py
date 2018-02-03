from models.document import CACMDocumentCollection, StanfordDocumentCollection
from models.bsbi_construction import StanfordReverseIndex, CACMReverseIndex
import os
from datetime import datetime


if __name__ == '__main__':
    begin = datetime.now()
    if 'cacm.collection' in os.listdir('Data/Collection'):
        cacm_document_collection = CACMDocumentCollection()
        cacm_document_collection.load_from_file('Data/Collection/cacm.collection')
    else:
        cacm_document_collection = CACMDocumentCollection(
            source_data_filepath='Data/CACM/cacm.all',
            stop_list_filepath='Data/CACM/common_words',
            load_on_creation=True
        )
        cacm_document_collection.save('Data/Collection/cacm.collection')

    print("======= Loading collection time : ", datetime.now() - begin, " =======")
    cacm_reverse_index = CACMReverseIndex(cacm_document_collection)
    print("======= Total building time : ", datetime.now() - begin, " =======")

    begin = datetime.now()
    if 'CS276' in os.listdir('Data/Collection'):
        stanford_document_collection = StanfordDocumentCollection()
        stanford_document_collection.load_from_dir('Data/Collection/CS276')
    else:
        stanford_document_collection = StanfordDocumentCollection(
            data_dirpath='Data/CS276',
            load_on_creation=True,
        )
        stanford_document_collection.save('Data/Collection/CS276')

    print("======= Loading collection time : ", datetime.now() - begin, " =======")
    stanford_reverse_index = StanfordReverseIndex(stanford_document_collection)
    print("======= Total building time : ", datetime.now() - begin, " =======")
