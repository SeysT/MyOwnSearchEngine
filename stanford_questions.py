import numpy as np
import matplotlib.pyplot as plt
import os

from math import log

from models.document import StanfordDocumentCollection

if __name__ == '__main__':

    if os.listdir(os.path.join('Data', 'Collection', 'CS276')):
        document_collection = StanfordDocumentCollection()
        document_collection.load_from_dir(os.path.join('Data', 'Collection', 'CS276'))
    else:
        document_collection = StanfordDocumentCollection(
            data_dirpath=os.path.join('Data', 'CS276'),
            load_on_creation=True,
        )

    vocabulary = document_collection.vocabulary
    token_number = document_collection.token_number
    vocabulary_size = document_collection.vocabulary_size

    frequence = np.array(list(vocabulary.values()))
    frequence.sort()
    frequence = frequence[::-1]
    rank = np.array(list(range(1, len(frequence) + 1)))

    half_document_collection = document_collection
    half_document_collection.generate_half_document_collection()
    half_document_collection.generate_vocabulary()

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
    print('CS276 contains {} tokens.'.format(token_number))
    print('Question 2:')
    print('CS276 has a vocabulary size of {}.'.format(vocabulary_size))
    print('Question 3:')
    print('Half of CS276 contains {} tokens.'.format(half_token_number))
    print('Half of CS276 has a vocabulary size of {}.'.format(
        half_vocabulary_size
    ))
    print('We can deduce Heap law parameter k = {}, b = {}.'.format(
        k_Heap,
        b_Heap,
    ))
    print('Question 4:')
    print(
        'If CS276 has 1 million tokens, its vocabulary size '
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
