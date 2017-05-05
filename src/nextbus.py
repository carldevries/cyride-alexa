# nextbus is a module for making GET requests to NextBus public XML feed.
# NextBus is a company which contracts with transportation organizations to
# gather static and real time vehicle data and provide useful informatin such
# as speed, direction, and ETAs for a bus and a given stop.  The API is free
# to use and more information on contraints, proceedures, and formats can be
# found under the docs folder
import zlib
from httpgetclient import send_request

host = 'webservices.nextbus.com'
path = '/service/publicXMLFeed'
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Host': host,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
          }

# get_agency_list calls the NextBus API to request a list of agencies who allow
# their bus data to be shared publicly.
# Inputs: NA
#
# Outputs:
#   @return - A string containing the NextBus agency list in XML format.


def get_agency_list():

    params = {
                'command': 'agencyList'
             }
    return _process_request(params)

# get_route_list comment


def get_route_list(agency):

    params = {
                'command': 'routeList',
                'a': agency
             }
    return _process_request(params)

# get_route_config comment


def get_route_config(agency, route):

    params = {
                'command': 'routeConfig',
                'a': agency,
                'r': route
             }
    return _process_request(params)

# get_predictions comment


def get_predictions(agency, route, stop):

    params = {
                'command': 'predictions',
                'a': agency,
                'r': route,
                's': stop
             }
    return _process_request(params)

# get_vehicle_locations comment


def get_vehicle_locations(agency, route):

    params = {
                'command': 'vehicleLocations',
                'a': agency,
                'r': route,
                't': '0'
             }
    return _process_request(params)

# _process_request comment


def _process_request(params):

    response = send_request('http://' + host, path, params, headers)
    content = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
    return content
