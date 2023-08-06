import json
import requests
import datetime
from shinobi.models.Analytic import Analytic
from shinobi.structures.Record import Record
from shinobi.structures.RecordCollection import RecordCollection

def joinURLs(base, param):
    return base + '?' + param

class WeatherForecast(Analytic):
    '''
    The WeatherForecast Analytic Requests Forecast Data from an Open-Source,
    RESTful API, Extracts Key Data/Insights of Interest from Retrieved Forecasts,
    and Formats the Data for Ingest into Elasticsearch.

    Weather Data Comes from the Worldwide Open Weather Map Service.
    '''
    def __init__(self, *args, apiKey=None, **kwargs):
        super(WeatherForecast, self).__init__(*args, **kwargs)
        self.baseURL = '''https://api.openweathermap.org/data/2.5/forecast'''
        self.appID = apiKey
        self.forecast = None

    def _recordForecast(self, res, intervalHours, units='metric'):
        '''
        Format a Response from the Weather API as a RecordCollection.
        '''
        # Find the Units for the Measurements in the Forecast
        unitsSwitch = {
            'imperial': {
                'temperature': 'F',
                'windSpeed': 'mph'
            },
            'metric': {
                'temperature': 'C',
                'windSpeed': 'mps'
            },
            'standard': {
                'temperature': 'K',
                'windSpeed': 'mps'
            }
        }
        tempUnit = unitsSwitch[units]['temperature']
        windSpeedUnit = unitsSwitch[units]['windSpeed']

        # Create a Record Collection of the Forecasts 
        records = [
            Record(
                {
                    'city': res['city']['name'],
                    'latitude': res['city']['coord']['lat'],
                    'longitude': res['city']['coord']['lon'],
                    'country': res['city']['country'],
                    'population': res['city']['population'],
                    'sunriseTimestamp': datetime.datetime.utcfromtimestamp(res['city']['sunrise']).isoformat(),
                    'sunsetTimestamp': datetime.datetime.utcfromtimestamp(res['city']['sunset']).isoformat(),
                    'startTimestamp': x['dt_txt'].replace(' ', 'T'),
                    'endTimestamp': (datetime.datetime.strptime(x['dt_txt'], '%Y-%m-%d %H:%M:%S')\
                        + datetime.timedelta(hours=intervalHours)).isoformat(),
                    'temperature_{0}'.format(tempUnit): x['main']['temp'],
                    'feelsLike_{0}'.format(tempUnit): x['main']['feels_like'],
                    'tempMin_{0}'.format(tempUnit): x['main']['temp_min'],
                    'tempMax_{0}'.format(tempUnit): x['main']['temp_max'],
                    'atmposphericPressure_hPa': x['main']['pressure'],
                    'seaLevelPressure_hPa': x['main']['sea_level'],
                    'groundLevelPressure_hPa': x['main']['grnd_level'],
                    'percentHumidity': x['main']['humidity'],
                    'weather': x['weather'][0]['main'],
                    'weatherDescription': x['weather'][0]['description'],
                    'percentCloudiness': x['clouds']['all'],
                    'windSpeed_{0}'.format(windSpeedUnit): x['wind']['speed'],
                    'windDirection_def': x['wind']['deg'],
                    'visibility_m': x['visibility'],
                    'probabilityOfPrecipitation': x['pop']
                }
            ) for x in res['list']
        ]
        forecast = RecordCollection(records=records)
        return forecast

    def forecastFiveDays(self, lat, lon, units='metric'):
        '''
        Returns a Five-Day Weather Forecast around a Specific Lat-Lon Pair
        in 3-Hour Intervals.
        '''
        params = {
            'lat': lat,
            'lon': lon,
            'units': units,
            'appID': self.appID
        }
        paramURL = '''lat={lat}&lon={lon}&units={units}&appid={appID}'''.format(**params)
        res = requests.get(joinURLs(self.baseURL, paramURL)).json()
        self.forecast = self._recordForecast(res, 3, units=units)
        return self.forecast

    def forecastFiveDaysCity(self, city, state=None, countryCode=None, units='metric'):
        '''
        Returns a Five-Day Weather Forecast around a Specific City in
        3-Hour Intervals.
        '''
        params = {
            'city': city,
            'units': units,
            'appID': self.appID
        }
        if state is not None and countryCode is not None:
            params['state'] = state
            params['country'] = countryCode
            paramURL = '''q={city},{state},{country}&units={units}&appid={appID}'''.format(**params)
        elif state is not None:
            params['state'] = state
            paramURL = '''q={city},{state}&units={units}&appid={appID}'''.format(**params)
        else:
            paramURL = '''q={city}&units={units}&appid={appID}'''.format(**params)
        res = requests.get(joinURLs(self.baseURL, paramURL)).json()
        self.forecast = self._recordForecast(res, 3, units=units)
        return self.forecast
