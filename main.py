from math import log

import numpy as np
import matplotlib.pyplot as plt

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


def get_vocabulary(document_collection):
    vocabulary = {}
    for document in document_collection.values():
        for field in Document.tokenized_fields:
            for token in getattr(document, field):
                try:
                    vocabulary[token] += 1
                except KeyError:
                    vocabulary[token] = 1

    return vocabulary


def get_token_number(vocabulary):
    token_number = 0
    for frequence in vocabulary.values():
        token_number += frequence

    return token_number


def get_vocabulary_size(vocabulary):
    return len(vocabulary.keys())


if __name__ == '__main__':
    common_words = create_common_words_set()

    document_collection = create_document_collection()

    vocabulary = get_vocabulary(document_collection)
    token_number = get_token_number(vocabulary)
    vocabulary_size = get_vocabulary_size(vocabulary)

    frequence = np.array(list(vocabulary.values()))
    frequence.sort()
    frequence = frequence[::-1]
    rank = np.array(list(range(1, len(frequence) + 1)))

    half_document_collection = {
        key: value
        for key, value
        in list(document_collection.items())[:len(document_collection) // 2]
    }

    half_vocabulary = get_vocabulary(half_document_collection)
    half_token_number = get_token_number(half_vocabulary)
    half_vocabulary_size = get_vocabulary_size(half_vocabulary)

    b_Heap = (
        log(vocabulary_size / half_vocabulary_size) /
        log(token_number / half_token_number)
    )
    k_Heap = (
        (vocabulary_size - half_vocabulary_size) /
        (token_number ** b_Heap - half_token_number ** b_Heap)
    )

    vocabulary_size_1_million = k_Heap * (1000000) ** b_Heap

    print('Question 1:')
    print('CACM contains {} tokens.'.format(token_number))
    print('Question 2:')
    print('CACM has a vocabulary size of {}.'.format(vocabulary_size))
    print('Question 3:')
    print('Half of CACM contains {} tokens.'.format(half_token_number))
    print('Half of CACM has a vocabulary size of {}.'.format(
        half_vocabulary_size
    ))
    print('We can deduce Heap law parameter k = {}, b = {}.'.format(
        k_Heap,
        b_Heap,
    ))
    print('Question 4:')
    print(
        'If CACM has 1 million tokens, its vocabulary size '
        'would be around {}.'.format(vocabulary_size_1_million)
    )

    plt.subplot(2, 1, 2)
    plt.plot(np.log(frequence), np.log(rank))
    plt.ylabel('Log(f)')
    plt.xlabel('Log(r)')

    plt.subplot(2, 1, 1)
    plt.title('Question 5')
    plt.plot(frequence, rank)
    plt.ylabel('Frequence (f)')
    plt.xlabel('Rank (r)')

    plt.show()
