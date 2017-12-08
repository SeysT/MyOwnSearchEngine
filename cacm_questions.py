from math import log

import numpy as np
import matplotlib.pyplot as plt

from document import CACMDocumentCollection


if __name__ == '__main__':
    document_collection = CACMDocumentCollection(
        data_filename='Data/CACM/cacm.all',
        stop_list_filename='Data/CACM/common_words',
    )
    document_collection.load_common_words()
    document_collection.load_collection()

    vocabulary = document_collection.vocabulary
    token_number = document_collection.token_number
    vocabulary_size = document_collection.vocabulary_size

    frequence = np.array(list(vocabulary.values()))
    frequence.sort()
    frequence = frequence[::-1]
    rank = np.array(list(range(1, len(frequence) + 1)))

    half_document_collection = document_collection
    half_document_collection.collection = {
        key: value
        for key, value
        in list(document_collection.collection.items())[:len(document_collection.collection) // 2]
    }

    half_vocabulary = half_document_collection.vocabulary
    half_token_number = half_document_collection.token_number
    half_vocabulary_size = half_document_collection.vocabulary_size

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