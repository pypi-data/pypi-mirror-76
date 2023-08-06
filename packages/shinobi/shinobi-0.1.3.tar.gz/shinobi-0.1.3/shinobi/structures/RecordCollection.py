import pandas as pd
from shinobi.models.DataStructure import DataStructure
from shinobi.structures.Record import Record

class RecordCollection(DataStructure):
    def __init__(self, *args, records=None, **kwargs):
        super(RecordCollection, self).__init__(*args, **kwargs)
        if len(args) > 0:
            self.records = [Record(x) for x in args[0]]
        else:
            self.records = records

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]

    def __setitem__(self, index, value):
        self.records[index] = Record(value)

    def asDF(self):
        '''
        Return the Retrieved Data from the Index as a Pandas DataFrame.
        '''
        return pd.DataFrame([x.rec for x in self.records])

    def asList(self):
        '''
        Return the Retrieved Data from the Index as a List of Records.
        '''
        return self.records

    def toCSV(self, csvName):
        '''
        Return the Retrieved Data from the Index as a CSV at
        the Provided Path.
        '''
        df = self.asDF()
        df.to_csv(
            csvName,
            index=False
        )
