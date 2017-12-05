from document import Document, fields_mapping

data_filename = 'Data/CACM/cacm.all'
stop_list_filename = 'Data/CACM/common_words'


def create_document_collection():
    document_collection = {}

    with open(data_filename, 'r') as df:
        data = df.read()

    current_id = None
    for line in data.split('\n'):
        if line.startswith('.I'):
            if current_id:
                document_collection[current_id].tokenize_doc()
                document_collection[current_id].clean_tokens(common_words)
            current_id = line.replace('.I ', '')
            document_collection[current_id] = Document(current_id)
        elif line in fields_mapping.keys():
            attr = fields_mapping[line]
        else:
            attr_value = getattr(document_collection[current_id], attr, None)
            to_add = line.strip()
            setattr(
                document_collection[current_id],
                attr,
                '{}\n{}'.format(attr_value, to_add) if attr_value else to_add
            )

    return document_collection


def create_common_words_set():

    with open(stop_list_filename, 'r') as sl:
        data = sl.read()

    return [line.strip() for line in data.split('\n')]


if __name__ == '__main__':
    common_words = create_common_words_set()
    document_collection = create_document_collection()
    test = document_collection['1765']

    print(test)
