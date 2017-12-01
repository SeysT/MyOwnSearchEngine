from document import Document


data_filename = 'Data/CACM/cacm.all'

fields_mapping = {
    '.T': 'title',
    '.W': 'summary',
    '.B': 'publication_date',
    '.A': 'authors',
    '.N': 'add_date',
    '.X': 'references',
    '.K': 'key_words',
}

document_collection = {}

with open(data_filename, 'r') as data_filename:
    data = data_filename.read()

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
