import json
import os
import sys
import time

import elasticsearch
import elasticsearch.helpers

from .exceptions import ReactorException
from .util import reactor_logger, ElasticSearchClient


def create_indices(es_client: ElasticSearchClient,
                   conf: dict, recreate: bool = False, force: bool = False,
                   old_index: str = None, mappings_dir: str = None):
    reactor_logger.info('ElasticSearch version: %s', es_client.es_version)

    es_index_mappings = read_es_index_mappings(es_client.es_version[0], mappings_dir)
    es_index_settings = read_es_index_settings(es_client.es_version[0], mappings_dir)

    if not recreate:
        index = conf['writeback_index'] + '_alert' if es_client.es_version_at_least(6) else conf['writeback_index']
        if es_client.indices.exists(index):
            reactor_logger.warning('Index "%s" already exists. Skipping index creation.', index)
            create_templates(es_client, conf, es_index_mappings, es_index_settings)
            return None
    elif not force:
        if not query_yes_no("Recreating indices will delete ALL existing data. Are you sure you want to recreate?"):
            reactor_logger.warning('Initialisation abandoned.')
            return None

    if es_client.indices.exists_template(conf['writeback_index']):
        reactor_logger.info('Template "%s" already exists.'
                            ' Deleting in preparation for creating indices.', conf['writeback_index'])
        es_client.indices.delete_template(conf['writeback_index'])

    # (Re-)Create indices.
    if es_client.es_version_at_least(6):
        index_names = (
            conf['writeback_index'] + '_alert',
            conf['writeback_index'] + '_status',
            conf['writeback_index'] + '_silence',
            conf['writeback_index'] + '_error',
        )
    else:
        index_names = (
            conf['writeback_index'],
        )
    for index_name in index_names:
        if es_client.indices.exists(index_name):
            reactor_logger.info('Deleting index ' + index_name + '.')
            try:
                es_client.indices.delete(index_name)
            except elasticsearch.NotFoundError:
                # Why does this ever occur?? It shouldn't. But it does.
                pass
        es_client.indices.create(index_name, body={'settings': es_index_settings})
        # Confirm index has been created
        index_created = es_client.indices.exists(index_name)
        timeout = time.time() + 2.0
        while not index_created and time.time() < timeout:
            index_created = es_client.indices.exists(index_name)
        if not index_created:
            raise ReactorException('Failed to create index: %s' % index_name)
    try:
        for item in es_client.cat.aliases(format='json'):
            if item['alias'] != conf['alert_alias']:
                continue
            reactor_logger.info('Deleting index ' + item['index'] + '.')
            try:
                es_client.indices.delete(item['index'])
            except elasticsearch.NotFoundError:
                # Why does this ever occur?? It shouldn't. But it does.
                pass
    except elasticsearch.NotFoundError:
        # ElasticSearch v5.x.x returns a 404 if there are no indices
        pass

    if es_client.es_version_at_least(7):
        # TODO: remove doc_type completely when elasticsearch client allows doc_type=None
        #  doc_type is a deprecated feature and will be completely removed in ElasticSearch 8
        reactor_logger.info('Applying mappings for ElasticSearch v7.x')
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_alert', doc_type='_doc',
                                      body=es_index_mappings['alert'], include_type_name=True)
        es_client.indices.put_alias(index=conf['writeback_index'] + '_alert', name=conf['alert_alias'])
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_status', doc_type='_doc',
                                      body=es_index_mappings['status'], include_type_name=True)
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_silence', doc_type='_doc',
                                      body=es_index_mappings['silence'], include_type_name=True)
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_error', doc_type='_doc',
                                      body=es_index_mappings['error'], include_type_name=True)
    elif es_client.es_version_at_least(6, 2):
        reactor_logger.info('Applying mappings for ElasticSearch v6.x')
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_alert', doc_type='_doc',
                                      body=es_index_mappings['alert'])
        es_client.indices.put_alias(index=conf['writeback_index'] + '_alert', name=conf['alert_alias'])
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_status', doc_type='_doc',
                                      body=es_index_mappings['status'])
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_silence', doc_type='_doc',
                                      body=es_index_mappings['silence'])
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_error', doc_type='_doc',
                                      body=es_index_mappings['error'])
    elif es_client.es_version_at_least(6):
        reactor_logger.info('Applying mappings for ElasticSearch v6.x')
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_alert', doc_type='reactor_alert',
                                      body=es_index_mappings['alert'])
        es_client.indices.put_alias(index=conf['writeback_index'] + '_alert', name=conf['alert_alias'])
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_status', doc_type='reactor_status',
                                      body=es_index_mappings['status'])
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_silence', doc_type='reactor_silence',
                                      body=es_index_mappings['silence'])
        es_client.indices.put_mapping(index=conf['writeback_index'] + '_error', doc_type='reactor_error',
                                      body=es_index_mappings['error'])
    else:
        reactor_logger.info('Applying mappings for ElasticSearch v5.x')
        es_client.indices.put_mapping(index=conf['writeback_index'], doc_type='reactor_alert',
                                      body=es_index_mappings['alert'])
        es_client.indices.put_alias(index=conf['writeback_index'], name=conf['alert_alias'])
        es_client.indices.put_mapping(index=conf['writeback_index'], doc_type='reactor_status',
                                      body=es_index_mappings['status'])
        es_client.indices.put_mapping(index=conf['writeback_index'], doc_type='reactor_silence',
                                      body=es_index_mappings['silence'])
        es_client.indices.put_mapping(index=conf['writeback_index'], doc_type='reactor_error',
                                      body=es_index_mappings['error'])

    reactor_logger.info('New index "%s" created', conf['writeback_index'])
    create_templates(es_client, conf, es_index_mappings, es_index_settings)

    if old_index:
        reactor_logger.info('Copying data from old index %s to new index %s', old_index, conf['writeback_index'])
        elasticsearch.helpers.reindex(es_client, old_index, conf['writeback_index'])


def create_templates(es_client: ElasticSearchClient, conf: dict, es_index_mappings: dict, es_index_settings: dict):

    template_exists = es_client.indices.exists_template(conf['writeback_index'])

    if es_client.es_version_at_least(7):
        es_client.indices.put_template(name=conf['writeback_index'],
                                       body={'index_patterns': [conf['writeback_index'] + '_alert_*'],
                                             'aliases': {conf['alert_alias']: {}},
                                             'settings': es_index_settings,
                                             'mappings': es_index_mappings['alert']})
    elif es_client.es_version_at_least(6, 2):
        es_client.indices.put_template(name=conf['writeback_index'],
                                       body={'index_patterns': [conf['writeback_index'] + '_alert_*'],
                                             'aliases': {conf['alert_alias']: {}},
                                             'settings': es_index_settings,
                                             'mappings': {'_doc': es_index_mappings['alert']}})
    elif es_client.es_version_at_least(6):
        es_client.indices.put_template(name=conf['writeback_index'],
                                       body={'index_patterns': [conf['writeback_index'] + '_alert_*'],
                                             'aliases': {conf['alert_alias']: {}},
                                             'settings': es_index_settings,
                                             'mappings': {'reactor_alert': es_index_mappings['alert']}})
    else:
        es_client.indices.put_template(name=conf['writeback_index'],
                                       body={'template': conf['writeback_index'] + '_*',
                                             'aliases': {conf['alert_alias']: {}},
                                             'settings': es_index_settings,
                                             'mappings': {'reactor_alert': es_index_mappings['alert']}})

    if not template_exists:
        reactor_logger.info('New template "%s" created', conf['writeback_index'])
    else:
        reactor_logger.info('Existing template "%s" updated', conf['writeback_index'])


def read_es_index_mappings(es_version, mappings_dir: str = None):
    reactor_logger.info('Reading ElasticSearch v%s index mappings:', es_version)
    return {
        'silence': read_es_index_mapping('silence', es_version, mappings_dir),
        'status': read_es_index_mapping('status', es_version, mappings_dir),
        'alert': read_es_index_mapping('alert', es_version, mappings_dir),
        'error': read_es_index_mapping('error', es_version, mappings_dir)
    }


def read_es_index_settings(es_version, mappings_dir: str = None):
    reactor_logger.info('Reading ElasticSearch v%s index settings:', es_version)
    return read_es_index_mapping('settings', es_version, mappings_dir)


def read_es_index_mapping(mapping, es_version, mappings_dir: str = None):
    if not mappings_dir:
        base_path = os.path.abspath(os.path.dirname(__file__))
        mapping_path = f'mappings/{es_version}'
        mappings_dir = os.path.join(base_path, mapping_path)
    path = os.path.join(mappings_dir, f'{mapping}.json')
    with open(path, 'r') as f:
        reactor_logger.info("Reading index mapping '%s'", path)
        return json.load(f)


def query_yes_no(question: str, default="yes") -> bool:
    """
    Ask a yes/no question via `input()` and return their answer.
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'no').\n")
