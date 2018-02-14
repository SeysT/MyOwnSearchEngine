from os import path, listdir

import matplotlib.pyplot as plt

from models.reverse_index import CACMReverseIndex
from models.document import CACMDocumentCollection
from models.request import VectorialRequest
from models.measure import average_precision, precision, recall


if __name__ == '__main__':
    print('Loading index...')
    if 'cacm.collection' in listdir(path.join('Data', 'Collection')):
        collection = CACMDocumentCollection()
        collection.load_from_file(path.join('Data', 'Collection', 'cacm.collection'))
    else:
        collection = CACMDocumentCollection(
            source_data_filepath=path.join('Data', 'CACM', 'cacm.all'),
            stop_list_filepath=path.join('Data', 'CACM', 'common_words'),
            load_on_creation=True
        )
    if 'cacm.index' in listdir(path.join('Data', 'Index')):
        index = CACMReverseIndex()
        index.load_from_file(path.join('Data', 'Index', 'cacm.index'))
    else:
        index = CACMReverseIndex(document_collection=collection)

    print('Loading content of real queries...')
    qrels_filename = path.join('Data', 'CACM', 'qrels.text')
    with open(qrels_filename, 'r') as qrels_file:
        qrels_content = qrels_file.read()

    print('Loading relevants documents id for real queries...')
    relevant_document_dict = {}
    for line in qrels_content.split('\n')[:-1]:
        id_request, id_document, _, _ = line.split()
        try:
            relevant_document_dict[str(int(id_request))].append(id_document)
        except KeyError:
            relevant_document_dict[str(int(id_request))] = [id_document]

    print('Creating a request collection...')
    request_collection = CACMDocumentCollection(
        source_data_filepath=path.join('Data', 'CACM', 'query.text'),
        stop_list_filepath=path.join('Data', 'CACM', 'common_words'),
        load_on_creation=True,
    )

    mean_average_precision = []
    all_precisions = []
    all_recalls = [i / 100 for i in range((1 * 100) + 1)]

    for document in request_collection.values():
        print('Calculating recall and precisions for request {}...'.format(document.id))
        request = ' '.join(document.summary_tokenized)

        found_documents = VectorialRequest(request).return_results(index)
        try:
            relevant_documents = relevant_document_dict[document.id]
        except KeyError:
            continue

        mean_average_precision.append(average_precision(relevant_documents, found_documents))

        document_precision = [0 for _ in range((1 * 100) + 1)]
        for i, _ in enumerate(found_documents, 1):
            current_precision = precision(relevant_documents, found_documents[:i])
            current_recall = round(recall(relevant_documents, found_documents[:i]), 2)

            document_precision[all_recalls.index(current_recall)] = max(
                document_precision[all_recalls.index(current_recall)],
                current_precision
            )

        for i in range(0, len(document_precision) - 1):
            document_precision[i] = max(document_precision[i], max(document_precision[i + 1:]))

        all_precisions.append(document_precision)

    print('Aggregating results for all requests...')
    all_precisions = [sum(elt) / len(elt) for elt in zip(*all_precisions)]

    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('Precision Recall')
    plt.axis([0, 1, 0, 1])
    plt.plot(all_recalls, all_precisions)
    plt.show()

    mean_average_precision = sum(mean_average_precision) / len(mean_average_precision)
    print('mean_average_precision : {}'.format(mean_average_precision))
