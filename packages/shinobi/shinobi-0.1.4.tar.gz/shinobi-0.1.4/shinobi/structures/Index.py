from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from shinobi.models.DataStructure import DataStructure
from shinobi.structures.Record import Record
from shinobi.structures.RecordCollection import RecordCollection
from shinobi.utils import queryFromFilter

class Index(DataStructure):
    '''
    Data Structure for Elasticsearch Index Data.
    '''
    def __init__(self, *args, source=None, project=None, **kwargs):
        super(Index, self).__init__(*args, **kwargs)
        self.filters = {}
        self.query = None
        self.es = Elasticsearch()
        if source is None or project is None:
            self.index = None
        else:
            self.index = str(project).lower() + '_' + str(source).lower()
        self.generator = None

    def __len__(self):
        if self.query is None: return 0
        return self.es.count(
            index=self.index,
            body=self.query
        )['count']

    def _makeGenerator(self):
        '''
        Create a Generator Object Over the Records Matching
        the Query for the Index.
        '''
        return scan(
            self.es,
            query=self.query,
            index=self.index,
            size=10000
        )

    def select(self, **filters):
        '''
        Assign the Class Generator to a Generator with Every
        Record Matching a Set of Filters.
        '''
        # Return any Record Referenced by ID by Itself
        self.filters = filters
        if 'ID' in [x.upper for x in filters]:
            ID = self.filters.pop('ID')
            value = self.es.get(
                index=self.index,
                id=ID
            )
            generator = lambda: (yield value)

        # Otherwise, Grab any Records from the Filter
        else:
            self.query = queryFromFilter(self.filters)
            generator = self._makeGenerator()
        self.generator = generator
        return self

    def collect(self):
        '''
        Return Selected Results as a Record Collection Object.
        '''
        records = [Record(x['_source']) for x in self.generator]
        return RecordCollection(records=records)
