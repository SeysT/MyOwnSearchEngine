"""
This file defines all functions needed to calculate measures on our request.
These measures are used to estimate efficiency of our search engine.
"""


def measure(func):
    """
    This function is a decorator for rappel and precision measures.
    It makes sure to have set inputs for the decorated function.
    """
    def new_func(relevant_documents, found_documents):
        return func(set(relevant_documents), set(found_documents))

    return new_func


@measure
def precision(relevant_documents, found_documents):
    """
    This function calculate the precision for the result of a request.
    + params:
        - relevant_documents: set containing ids of relevant documents.
        - found_documents: set containing ids of found documents.
    + returns:
        number of found and relevant documents divided by the number of found documents.
    """
    relevant_found_documents = relevant_documents.intersection(found_documents)
    return len(relevant_found_documents) / len(found_documents)


@measure
def recall(relevant_documents, found_documents):
    """
    This function calculate the rappel for the result of a request.
    + params:
        - relevant_documents: set containing ids of relevant documents.
        - found_documents: set containing ids of found documents.
    + returns:
        number of found and relevant documents divided by the number of relevant documents.
    """
    relevant_found_documents = relevant_documents.intersection(found_documents)
    return len(relevant_found_documents) / len(relevant_documents)


def e_measure(relevant_documents, found_documents, alpha=0.5):
    """
    This function calculate the E-measure for the result of a request.
    + params:
        - relevant_documents: set containing ids of relevant documents.
        - found_documents: set containing ids of found documents.
    + returns:
        a measure depending of precision and rappel.
    """
    p = precision(relevant_documents, found_documents)
    r = recall(relevant_documents, found_documents)
    return 1 - (1 / (alpha * (1 / p) + (1 - alpha) * (1 / r)))


def f_measure(relevant_documents, found_documents, alpha=0.5):
    """
    This function calculate the F-measure for the result of a request.
    + params:
        - relevant_documents: set containing ids of relevant documents.
        - found_documents: set containing ids of found documents.
    + returns:
        a measure depending of E-measure.
    """
    return 1 - e_measure(relevant_documents, found_documents, alpha)


def r_measure(relevant_documents, found_documents):
    """
    This function calculate the R-measure for the result of a request.
    + params:
        - relevant_documents: set containing ids of relevant documents.
        - found_documents: set containing ids of found documents.
    + returns:
        calculate precision for the number of relevant documents
    """
    return precision(relevant_documents, found_documents[:len(relevant_documents)])


def average_precision(relevant_documents, found_documents):
    """
    This function calculate the average precision for the result of a request.
    + params:
        - relevant_documents: set containing ids of relevant documents.
        - found_documents: set containing ids of found documents.
    + returns:
        the mean of precision at every rank before rappel equals 1.
    """
    average_precision = []
    for index, document in enumerate(found_documents, start=1):
        average_precision.append(precision(relevant_documents, found_documents[:index]))
        if recall(relevant_documents, found_documents[:index]) == 1:
            break
    return sum(average_precision) / len(average_precision)
