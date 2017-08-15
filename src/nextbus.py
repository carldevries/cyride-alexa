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
# Inputs: 
#   NA
# Outputs:
#   A string containing the NextBus agency list in XML format.


def get_agency_list():

    params = {
                'command': 'agencyList'
             }
    return _process_request(params)

# get_route_list calls the NextBus API to request a list of available routes
# and their associated tags.
# Inputs:
#   agency - The requested agency's tag attribute obtained from agencyList.
# Outputs:
#   A string containing the available CyRide routes in XML format.

def get_route_list(agency):

    params = {
                'command': 'routeList',
                'a': agency
             }
             
    return _process_request(params)

# get_route_config calls the NextBus API to request a list of stops for a given
# route.  The request returns stop, direction, and path data.  The route and
# terse parameters are optional.
# Inputs:
#   agency - The requested agency's tag attribute obtained from agencyList.
#   route -  The requested route's tag attribute obtained from routeList.
#   terse - A value of True requests NextBus not return path data to reduce the
#      response size.
# Outputs:
#   A string containing a given route's stop and direction data in XML format.


def get_route_config(agency, route=None, terse=False):

    params = {
                'command': 'routeConfig',
                'a': agency
             }
    
    if route is not None:
        params['r'] = route
        
    if terse:
        params['terse']   = ''
        
    return _process_request(params)

# get_predictions calls the NextBust API to request prediction data for a given
# route and stop tag combination. Requesting predictions using a stop id is not
# supported. See the NextBus XML Feed API documentation for the difference
# between stop tag and stop id. The use_short_titles argument is optional.
# Inputs:
#   agency - The requested agency's tag attribute obtained from agencyList.
#   route -  The requested route's tag attribute obtained from routeList.
#   stop_tag - The requested stop's tag attribute obtained from routeConfig.
#   use_short_titles - Returns the short title for a stop if it's available.
# Outputs:
#   A string containing a list of predictions for a given route and stop in XML
#      format. Predictions for multiple directions may exist. Each direction
#      may have multiple prediction objects when multiple vehicles are present.

def get_predictions(agency, route, stop_tag, use_short_titles=False):

    params = {
                'command': 'predictions',
                'a': agency,
                'r': route,
                's': stop_tag,
                'useShortTitles': use_short_titles
             }
             
    return _process_request(params)

# get_vehicle_locations calls the NextBus API to request vehicle location data
# updates for a given route within a window specified by last_time. When
# last_time is 0 (the default value) then updates within the last 15 minutes
# are returned.
# Inputs:
#   agency - The requested agency's tag attribute obtained from agencyList.
#   route -  The requested route's tag attribute obtained from routeList.
#   last_time - A time in the past(specified by epoch time (1970) in
#      milliseconds which determines how far back to search for GPS updates.
# Outputs:
#   A string containing a list of vehicles with position, heading, and timing
#      data in XML format.


def get_vehicle_locations(agency, route, last_time=0):

    params = {
                'command': 'vehicleLocations',
                'a': agency,
                'r': route,
                't': '0'
             }
             
    return _process_request(params)

# get_schedule calls the NextBus API to request a schedule for selected stops
# along a given route.  Expected stop time data for all stops is not
# necessarily available for all stops as it would be for predictions.
# Inputs:
#   agency - The requested agency's tag attribute obtained from agencyList.
#   route -  The requested route's tag attribute obtained from routeList.
# Outputs:
#   A string containing stop and expected arrival data in XML format.

def get_schedule(agency, route):

    params = {
                'command': 'schedule',
                'a': agency,
                'r': route
             }

    return _process_request(params)

# get_messages calls the NextBus API to request messages sent by CyRide. The 
# route tag is optional, but can be used to only request messages for certain
# routes. This function doesn't currently support requesting messages for
# multiple routes without requesting all messages.
# Inputs:
#   agency - The requested agency's tag attribute obtained from agencyList.
#   route -  The requested route's tag attribute obtained from routeList.
# Outputs:
#   A string containing a list of system wide messages and route specific
#      messages in an XML format.

def get_messages(agency, route=None):

    params = {
                'command': 'messages',
                'a': agency
             }
             
    if route is not None:
        params['r'] = route

    return _process_request(params)

# _process_request comment


def _process_request(params):

    response = send_request('http://' + host, path, params, headers)
    content = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
    return content
