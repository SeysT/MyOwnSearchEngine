"""
My Own Search Engine project.
This is the CLI engine for searching in CACM and CS276 collections.

Usage:
    engine.py cacm (vectorial | boolean) <request> [--collection=<filepath>]
                                                   [--index=<filepath>]
                                                   [--results=<len>]
    engine.py cs276 (vectorial | boolean) <request> [--collection=<filepath>]
                                                    [--index=<filepath>]
                                                    [--results=<len>]
    engine.py (-h | --help)
    engine.py --version

General options:
    -h --help                   Show this screen.
    --version                   Show version.
    -r --results=<len>          Number of results to display [default: 10].

Options for CACM collection:
    -c --collection=<filepath>  Use the given collection file instead of creating it.
    -i --index=<filepath>       Use the given index file instead of creating it.

"""
from docopt import docopt

from time import time
from os import path

from models.document import CACMDocumentCollection, StanfordDocumentCollection
from models.request import BooleanRequest, VectorialRequest
from models.reverse_index import StanfordReverseIndex, CACMReverseIndex


if __name__ == '__main__':
    args = docopt(__doc__, version='My Own Search Engine 0.1')

    start_time = time()
    if args['cacm']:
        if args['--collection']:
            collection = CACMDocumentCollection()
            collection.load_from_file(args['--collection'])
            duration = (time() - start_time) * 1000
            print('Collection has been loaded from file {} in {:.2f} milliseconds.'.format(
                args['--collection'],
                duration
            ))
        else:
            collection = CACMDocumentCollection()
            collection.load_from_file(path.join('Data', 'Collection', 'cacm.collection'))
            duration = (time() - start_time) * 1000
            print('Collection has been loaded from file {} in {:.2f} milliseconds.'.format(
                path.join('Data', 'Collection', 'cacm.collection'),
                duration
            ))
        start_time = time()
        if args['--index']:
            reverse_index = CACMReverseIndex()
            reverse_index.load_from_file(args['--index'])
            duration = (time() - start_time) * 1000
            print('Index has been loaded from file {} in {:.2f} milliseconds.'.format(
                args['--index'],
                duration
            ))
        else:
            reverse_index = CACMReverseIndex()
            reverse_index.load_hash_table()
            duration = (time() - start_time) * 1000
            print('Hash Table has been loaded from file in {:.2f} milliseconds.'.format(
                duration
            ))
    elif args['cs276']:
        if args['--collection']:
            collection = StanfordDocumentCollection()
            collection.load_from_dir(args['--collection'])
            duration = (time() - start_time) * 1000
            print('Collection has been loaded from file {} in {:.2f} milliseconds.'.format(
                args['--collection'],
                duration
            ))
        else:
            collection = StanfordDocumentCollection()
            collection.load_from_dir(path.join('Data', 'Collection', 'CS276'))
            duration = (time() - start_time) * 1000
            print('Collection has been loaded from file {} in {:.2f} milliseconds.'.format(
                path.join('Data', 'Collection', 'CS276'),
                duration
            ))

        start_time = time()
        if args['--index']:
            reverse_index = StanfordReverseIndex()
            reverse_index.load_from_file(args['--index'])
            duration = (time() - start_time) * 1000
            print('Index has been loaded from file {} in {:.2f} milliseconds.'.format(
                args['--index'],
                duration
            ))
        else:
            reverse_index = StanfordReverseIndex()
            reverse_index.load_hash_table()
            duration = (time() - start_time) * 1000
            print('Hash Table has been loaded from file in {:.2f} milliseconds.'.format(
                duration
            ))

    start_time = time()
    request = (
        VectorialRequest(reverse_index, collection)
        if args['vectorial']
        else BooleanRequest(reverse_index, collection)
    )
    results = request.return_results(args['<request>'])
    duration = (time() - start_time) * 1000

    print('We have found {} results in {:.2f} milliseconds.'.format(len(results), duration))

    for result in results[:int(args['--results'])]:
        print(collection[result])
