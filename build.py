from models.document import CACMDocumentCollection, StanfordDocumentCollection
from models.reverse_index import ReverseIndex


if __name__ == '__main__':
    cacm_document_collection = CACMDocumentCollection(
        data_filename='Data/CACM/cacm.all',
        stop_list_filename='Data/CACM/common_words',
        load_on_creation=True
    )

    cacm_reverse_index = ReverseIndex(document_collection=cacm_document_collection)

    cacm_document_collection.save('Data/Collection/cacm.collection')
    cacm_reverse_index.save('Data/Index/cacm.index')

    stanford_document_collection = StanfordDocumentCollection(
        data_dirname='Data/CS276',
        load_on_creation=True
    )

    stanford_document_collection.save('Data/Collection/CS276')
