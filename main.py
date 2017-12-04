from document import Document
from nltk.tokenize import word_tokenize

data_filename = 'Data/CACM/cacm.all'
stop_list_filename = 'Data/CACM/common_words'

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

document_collection = {}
common_words = []


def populate_document_collection():
    with open(data_filename, 'r') as df:
        data = df.read()

    for line in data.split('\n'):
        if line.startswith('.I'):
            current_id = line.replace('.I ', '')
            document_collection[current_id] = Document(current_id)
        elif line in fields_mapping.keys():
            attr = fields_mapping[line]
        else:
            attr_value = getattr(document_collection[current_id], attr)
            to_add = line.strip()
            setattr(
                document_collection[current_id],
                attr,
                '{}\n{}'.format(attr_value, to_add) if attr_value else to_add
            )
    return document_collection


def populate_common_words_set():
    with open(stop_list_filename, 'r') as sl:
        data = sl.read()

    for line in data.split('\n'):
        common_words.append(line.strip())

    return common_words


def tokenize_collection(document_collection):
    for el in document_collection.values():
        el.tokenize_doc()


def clean_document_collection(document_collection, common_words):
    for el in document_collection.values():
        el.clean_tokens(common_words)


if __name__ == '__main__':
    populate_document_collection()
    populate_common_words_set()
    test = document_collection['1765']

    tokenize_collection(document_collection)
    print(test)
    clean_document_collection(document_collection, common_words)

    print(test)
