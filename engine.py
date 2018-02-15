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
from os import path, listdir

from models.document import CACMDocumentCollection, StanfordDocumentCollection
from models.request import BooleanRequest, VectorialRequest
from models.reverse_index import StanfordReverseIndex, CACMReverseIndex


if __name__ == '__main__':
    args = docopt(__doc__, version='My Own Search Engine 0.2')

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
            if 'cacm.collection' in listdir(path.join('Data', 'Collection')):
                print('Using default file {} for collection...'.format(
                    path.join('Data', 'Collection', 'cacm.collection')
                ))
                collection = CACMDocumentCollection()
                collection.load_from_file(path.join('Data', 'Collection', 'cacm.collection'))
                duration = (time() - start_time) * 1000
                print('Collection has been loaded in {:.2f} milliseconds.'.format(duration))
            else:
                print('No default collection found, building it...')
                collection = CACMDocumentCollection(
                    source_data_filepath=path.join('Data', 'CACM', 'cacm.all'),
                    stop_list_filepath=path.join('Data', 'CACM', 'common_words'),
                    load_on_creation=True,
                )
                duration = time() - start_time
                print('Collection has been created in {:.2f} seconds.'.format(duration))
                collection.save(path.join('Data', 'Collection', 'cacm.collection'))

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
            if 'cacm.hash' in listdir(path.join('Data', 'Index')):
                print('Using default Hash Table {} for index...'.format(
                    path.join('Data', 'Index', 'cacm.hash')
                ))
                reverse_index = CACMReverseIndex()
                reverse_index.load_hash_table()
                duration = (time() - start_time) * 1000
                print('Hash Table has been loaded in {:.2f} milliseconds.'.format(duration))
            else:
                print('No default index found, building it...')
                reverse_index = CACMReverseIndex(document_collection=collection)
                duration = time() - start_time
                print('Index has been created in {:.2f} seconds.'.format(duration))
                reverse_index.save(path.join('Data', 'Index', 'cacm.index'))

    elif args['cs276']:
        if args['--collection']:
            collection = StanfordDocumentCollection()
            collection.load_from_dir(args['--collection'])
            duration = time() - start_time
            print('Collection has been loaded from directory {} in {:.2f} seconds.'.format(
                args['--collection'],
                duration
            ))
        else:
            if listdir(path.join('Data', 'Collection', 'CS276')):
                print('Using default directory {} for collection...'.format(
                    path.join('Data', 'Collection', 'CS276')
                ))
                collection = StanfordDocumentCollection()
                collection.load_from_dir(path.join('Data', 'Collection', 'CS276'))
                duration = time() - start_time
                print('Collection has been loaded in {:.2f} seconds.'.format(duration))
            else:
                print('No default directory found, building it...')
                collection = StanfordDocumentCollection(
                    data_dirpath=path.join('Data', 'CS276'),
                    load_on_creation=True,
                )
                duration = time() - start_time
                print('Collection has been created in {:.2f} seconds.'.format(duration))
                collection.save(path.join('Data', 'Collection', 'CS276'))

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
            if 'cs276.hash' in listdir(path.join('Data', 'Index')):
                print('Using default Hash Table {} for index...'.format(
                    path.join('Data', 'Index', 'cs276.hash')
                ))
                reverse_index = StanfordReverseIndex()
                reverse_index.load_hash_table()
                duration = (time() - start_time) * 1000
                print('Hash Table has been loaded from file in {:.2f} milliseconds.'.format(
                    duration
                ))
            else:
                print('No default Hash Table found, building index...')
                reverse_index = StanfordReverseIndex(collection)
                duration = time() - start_time
                print('Index has been creadted in {:.2f} seconds.'.format(duration))
                reverse_index.save(path.join('Data', 'Index', 'cs276.index'))

    start_time = time()
    request = (
        VectorialRequest(reverse_index, collection)
        if args['vectorial']
        else BooleanRequest(reverse_index, collection)
    )
    results = request.return_results(args['<request>'])
    duration = time() - start_time

    if args['cacm']:
        print('We have found {} results in {:.2f} milliseconds.'.format(
            len(results),
            duration * 1000
        ))
    elif args['cs276']:
        print('We have found {} results in {:.2f} seconds.'.format(len(results), duration))

    for result in results[:int(args['--results'])]:
        print(collection[result])
