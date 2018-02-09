"""
This file defines different ponderation functions to use in vectorial request.
A ponderation function needs to have at least these arguments:
    - doc_len: the number of token in the document
    - tf: the number of appearence of given token in document
    - df: the number of document of the collection which contains given token
The function should return wd = ptf * pdf * nd
"""
from math import log10


def tf_df(doc_len, tf, df):
    """
    - ptf = tf
    - pdf = 1 / df
    - nd = 1
    """
    return tf * (1 / df) * 1


def only_tf(doc_len, tf, df):
    """
    - ptf = tf
    - pdf = 1
    - nd = 1
    """
    return tf * 1 * 1


def only_logtf(doc_len, tf, df):
    """
    - ptf = (1 + log10(tf))
    - pdf = 1
    - n = 1
    """
    return (1 + log10(tf)) * 1 * 1


def tf_idf(doc_len, tf, df):
    """
    - ptf = tf
    - pdf = log10(doc_len / df)
    - n = 1
    """
    return tf * log10(doc_len / df)


def tf_idf_normalized(doc_len, tf, df):
    """
    - ptf = tf
    - pdf = log10(doc_len / df)
    - n = (1 / doc_len)
    """
    return tf * log10(doc_len / df) * (1 / doc_len)


def logtf_idf(doc_len, tf, df):
    """
    - ptf = (1 + log10(tf))
    - pdf = log10(doc_len / df)
    - n = 1
    """
    return (1 + log10(tf)) * log10(doc_len / df)


def logtf_idf_normalized(doc_len, tf, df):
    """
    - ptf = (1 + log10(tf))
    - pdf = log10(doc_len / df)
    - n = (1 / doc_len)
    """
    return (1 + log10(tf)) * log10(doc_len / df) * (1 / doc_len)
