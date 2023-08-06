import elasticsearch
from elasticsearch.helpers import bulk
from shinobi.models.Backend import Backend

class ElasticsearchBackend(Backend):
    '''
    A Class to Ingest and Manage the Elasticsearch Backend
    for a Particular Index.
    '''
    def __init__(self, *args, project=None, source=None, mappings=None, **kwargs):
        super(ElasticsearchBackend, self).__init__(*args, **kwargs)
        self.es = elasticsearch.Elasticsearch()
        self.project = project
        self.source = source
        self.mappings = mappings
        if self.project is None or self.source is None:
            self.index = None
        else:
            self.index = str(self.project).lower() + '_' + str(self.source).lower()

    def createIndex(self):
        '''
        Create an Empty Elasticsearch Index.
        '''
        if self.index is None:
            raise AttributeError('Cannot Write to NoneType Index.')
        if self.mappings is None: self.mappings = {}
        self.mappings = {
            'settings': {
                'number_of_shards': 2,
                'number_of_replicas': 1
            },
            'mappings': {
                'properties': {
                    attribute: {
                        'type': self.mappings[attribute]
                    } for attribute in self.mappings
                }
            }
        }
        self.es.indices.create(
            index=self.index,
            body=self.mappings
        )

    def deleteIndex(self):
        '''
        Delte an Existing Elasticsearch Index.
        '''
        if self.index is None:
            raise AttributeError('Cannot Delete NoneType Index.')
        self.es.indices.delete(index=self.index)

    def ingest(self, records):
        '''
        Ingest a List of Records to Elasticsearch.
        '''
        _ = bulk(
            self.es,
            [x.ingestable() for x in records],
            index=self.index
        )
        self.es.indices.refresh(index=self.index)

    def ingestRecord(self, record):
        '''
        Ingest a Single Record to Elasticsearch.
        '''
        self.ingest(self.index, [record])
