import logging
from dateutil.parser import parse
from geodaisy.converters import geojson_to_wkt, wkt_to_geojson

def detectGeoJSON(field):
    '''
    Return True if a Value is GeoJSON and False Otherwise.
    '''
    if type(field) is dict and "type" in field and "coordinates" in field:
        return True
    return False

def detectWKT(field):
    '''
    Return True if a Value is Well-Known Text (WKT) and
    False Otherwise.
    '''
    if type(field) is str:
        wktStarters = (
            'POINT',
            'LINESTRING',
            'POLYGON',
            'MULTIPOINT',
            'MULTILINESTRING',
            'MULTIPOLYGON',
            'GEOMETRYCOLLECTION',
            'BBOX',
            'N/A'
        )
        starter = field.split(' ')[0]
        if starter.upper() in wktStarters:
            return True
    return False

def formatRecord(record):
    '''
    Format a Dictionary Record of Data (with Attribute Name Keys Mapping to
    Attribute Values) so that:
      1.  Times are Represented as JSON Objects.
      2.  Geometries are Represented as GeoJSON Geometries.
    '''
    for attribute in record:
        if detectWKT(attribute):
            record[attribute] = wkt_to_geojson(attribute)
            continue
        try: record[attribute] = parse(record[attribute])
        except: continue
    return record

def toWKT(geoJSON):
    '''
    Convert a GeoJSON Dictionary to a WKT Geometry.
    '''
    geo = {
        'type': geoJSON.get('type', 'Polyogn'),
        'coordinates': geoJSON.get('coordinates', [])
    }
    geoStr = str(geo).replace("'", '"').replace('(', '[').replace(')', ']')
    return geojson_to_wkt(geoStr)

def queryFromFilter(filters):
    '''
    Format a Filter Dictionary as an Elasticsearch Query.
    '''
    # Return All Data if there are no Filters
    if len(filters) == 0:
        return {
            'query': {
                'match_all': filters
            }
        }
    # Otherwise, Match a Particular Field
    # TODO: Do Other Queries than "Match"
    else:
        return {
            'query': {
                'match': filters
            }
        }
