"""
This file defines different ponderation functions to use in vectorial request.
A ponderation function needs to have at least these arguments:
    - tf: the number of appearence of given token in document
    - df: the number of document of the collection which contains given token
    - collection: collection given for the request
    - document_id: the id of the document to calculate the ponderation
The function should return wd = ptf * pdf * nd

Some variables defines in function:
    - N: number of document given in the collection
    - doc_len: number of token in the given document
    - tf_max: max tf for given document
"""
from math import log10


__all__ = [
    'tf_df',
    'only_tf',
    'only_logtf',
    'tf_idf',
    'tf_idf_normalized',
    'logtf_idf',
    'logtf_idf_normalized',
    'normalizedtf_df',
    'normalizedtf_df_normalized',
]


def tf_df(tf, df, collection, document_id):
    """
    - ptf = tf
    - pdf = 1 / df
    - nd = 1
    """
    return tf * (1 / df) * 1


def only_tf(tf, df, collection, document_id):
    """
    - ptf = tf
    - pdf = 1
    - nd = 1
    """
    return tf * 1 * 1


def only_logtf(tf, df, collection, document_id):
    """
    - ptf = (1 + log10(tf))
    - pdf = 1
    - n = 1
    """
    return (1 + log10(tf)) * 1 * 1


def tf_idf(tf, df, collection, document_id):
    """
    - ptf = tf
    - pdf = log10(N / df)
    - n = 1
    """
    N = len(collection)
    return tf * log10(N / df)


def tf_idf_normalized(tf, df, collection, document_id):
    """
    - ptf = tf
    - pdf = log10(N / df)
    - n = (1 / doc_len)
    """
    N = len(collection)
    try:
        doc_len = sum(collection[document_id].term_bag.values())
    except KeyError:
        doc_len = 1
    return tf * log10(N / df) * (1 / doc_len)


def logtf_idf(tf, df, collection, document_id):
    """
    - ptf = (1 + log10(tf))
    - pdf = log10(N / df)
    - n = 1
    """
    N = len(collection)
    return (1 + log10(tf)) * log10(N / df)


def logtf_idf_normalized(tf, df, collection, document_id):
    """
    - ptf = (1 + log10(tf))
    - pdf = log10(N / df)
    - n = (1 / doc_len)
    """
    N = len(collection)
    try:
        doc_len = sum(collection[document_id].term_bag.values())
    except KeyError:
        doc_len = 1
    return (1 + log10(tf)) * log10(N / df) * (1 / doc_len)


def normalizedtf_df(tf, df, collection, document_id):
    """
    - ptf = tf / tf_max
    - pdf = 1 / df
    - n = 1
    """
    try:
        tf_max = max(collection[document_id].term_bag.values())
    except KeyError:
        tf_max = 1
    return (tf / tf_max) * (1 / df) * 1


def normalizedtf_df_normalized(tf, df, collection, document_id):
    """
    - ptf = tf / tf_max
    - pdf = 1 / df
    - n = 1 / doc_len
    """
    try:
        tf_max = max(collection[document_id].term_bag.values())
        doc_len = sum(collection[document_id].term_bag.values())
    except KeyError:
        tf_max = 1
        doc_len = 1
    return (tf / tf_max) * (1 / df) * doc_len
