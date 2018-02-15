from os import path, listdir

import matplotlib.pyplot as plt

import models.ponderation as ponderation_module

from models.document import CACMDocumentCollection
from models.request import VectorialRequest
from models.reverse_index import CACMReverseIndex
from models.measure import average_precision, r_measure, f_measure, e_measure, precision, recall


def get_measures(request_collection, ponderation):
    print('Calculating measures for ponderation {}...'.format(ponderation))
    mean_average_precision = []
    mean_r_measure = []
    mean_f_measure = []
    mean_e_measure = []
    all_precisions = []
    all_recalls = [i / 100 for i in range((1 * 100) + 1)]

    for document in request_collection.values():
        request = ' '.join(document.summary_tokenized)

        found_documents = VectorialRequest(index, collection).return_results(
            request,
            getattr(ponderation_module, ponderation)
        )
        try:
            relevant_documents = relevant_document_dict[document.id]
        except KeyError:
            continue

        mean_average_precision.append(average_precision(relevant_documents, found_documents))
        mean_r_measure.append(r_measure(relevant_documents, found_documents))
        mean_f_measure.append(f_measure(relevant_documents, found_documents))
        mean_e_measure.append(e_measure(relevant_documents, found_documents))

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

    all_precisions = [sum(elt) / len(elt) for elt in zip(*all_precisions)]
    mean_average_precision = sum(mean_average_precision) / len(mean_average_precision)
    mean_r_measure = sum(mean_r_measure) / len(mean_r_measure)
    mean_f_measure = sum(mean_f_measure) / len(mean_f_measure)
    mean_e_measure = sum(mean_e_measure) / len(mean_e_measure)

    return all_recalls, all_precisions, {
        'mean_average_precision': mean_average_precision,
        'mean_r_measure': mean_r_measure,
        'mean_f_measure': mean_f_measure,
        'mean_e_measure': mean_e_measure
    }


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

    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('Precision Recall')
    plt.axis([0, 1, 0, 1])

    measures_by_ponderation = {}

    for ponderation in ponderation_module.__all__:
        all_recalls, all_precisions, measures = get_measures(request_collection, ponderation)
        plt.plot(all_recalls, all_precisions, label=ponderation)
        measures_by_ponderation[ponderation] = measures

    plt.legend()
    plt.show()

    print('| Ponderation | Mean Average Precision | R-Measure | F-Measure | E-Measure |')
    for ponderation, measures in measures_by_ponderation.items():
        print('| {} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |'.format(
            ponderation,
            measures['mean_average_precision'],
            measures['mean_r_measure'],
            measures['mean_f_measure'],
            measures['mean_e_measure'],
        ))
