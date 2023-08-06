import json
from shinobi.models.DataStructure import DataStructure
from shinobi.utils import formatRecord, detectGeoJSON, toWKT

class Record(DataStructure):
    '''
    A Dictionary Record Mapping Attribute Names to Attribute Values.
    '''
    def __init__(self, *args, **kwargs):
        if len(args) > 0: dictionary = args[0]
        else: dictionary = {}
        kwargs.update(dictionary)
        super(Record, self).__init__(self, *args, **kwargs)
        self.raw = dictionary.copy()
        self.rec = formatRecord(dictionary)

    def __call__(self):
        return self.rec

    def __getitem__(self, key):
        return self.rec[key]

    def __setitem__(self, key, value):
        setattr(self, key, value)
        self.raw[key] = value
        self.rec[key] = value

    def __str__(self):
        return json.dumps(self.raw,
                          indent=3,
                          sort_keys=True)

    def ingestable(self):
        '''
        Make a Record Ready for Ingest by Formatting the Record
        with Appropriate Timestamps (Datetime Objects) and
        Geometries (WKT Strings).
        '''
        ingestRec = self.rec.copy()
        for attribute in ingestRec:
            if detectGeoJSON(ingestRec[attribute]):
                ingestRec[attribute] = toWKT(ingestRec[attribute])
        return ingestRec
