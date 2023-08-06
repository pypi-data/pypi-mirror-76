from shinobi.analytics.WeatherForecast import WeatherForecast
from shinobi.backends.ElasticsearchBackend import ElasticsearchBackend
from shinobi.structures.Index import Index
from shinobi.structures.Record import Record
from shinobi.structures.RecordCollection import RecordCollection

def new(use, *args, **kwargs):
    '''
    Instantiate a New Object with the Necessary
    Arguments and Keyword Arguments.
    '''
    return eval(use)(*args, **kwargs)
