from models.document import CACMDocumentCollection, StanfordDocumentCollection
from models.reverse_index import ReverseIndex
from models.bsbi_construction import StanfordReverseIndex
import os
from datetime import datetime


if __name__ == '__main__':
    cacm_document_collection = CACMDocumentCollection(
        data_filename='Data/CACM/cacm.all',
        stop_list_filename='Data/CACM/common_words',
        load_on_creation=True
    )

    cacm_reverse_index = ReverseIndex(document_collection=cacm_document_collection)

    cacm_document_collection.save('Data/Collection/cacm.collection')
    cacm_reverse_index.save('Data/Index/cacm.index')

    begin = datetime.now()
    if 'CS276' in os.listdir('Data/Collection'):
        stanford_document_collection = StanfordDocumentCollection(
            data_dirname='Data/CS276',
            load_on_creation=False
        )
        stanford_document_collection.load_from_dir('Data/Collection/CS276')
    else:
        stanford_document_collection = StanfordDocumentCollection(
            data_dirname='Data/CS276',
            load_on_creation=True,
        )
        stanford_document_collection.save('Data/Collection/CS276')

    print("======= Loading collection time : ", datetime.now() - begin, " =======")
    stanford_reverse_index = StanfordReverseIndex(document_collection=stanford_document_collection)
    print("======= Total building time : ", datetime.now() - begin, " =======")
