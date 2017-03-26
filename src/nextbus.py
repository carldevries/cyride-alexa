import zlib
import httpgetclient

host = 'webservices.nextbus.com'
path = '/service/publicXMLFeed'
headers = 	{
				'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding' : 'gzip, deflate, sdch',
				'Accept-Language' : 'en-US,en;q=0.8',
				'Host' : host,
				'Connection' : 'keep-alive',
				'Upgrade-Insecure-Requests' : '1',
				'Cache-Control' : 'max-age=0'
			}

def get_agency_list():

	return _process_request({
								'command' : 'agencyList'
							})

def get_route_list(agency):

	return _process_request({
								'command' : 'routeList',
								'a' : agency
							})

def get_route_config(agency, route):

	return _process_request({
								'command' : 'routeConfig',
								'a' : agency,
								'r' : route
							})

def get_predictions(agency, route, stop):
	
	return _process_request({
								'command' : 'predictions',
								'a' : agency,
								'r' : route,
								's' : stop
							})

def get_vehicle_locations(agency, route):

	return _process_request({
								'command' : 'vehicleLocations',
								'a' : agency,
								'r' : route,
								't' : '0'
							})

def _process_request(params):

	request = httpgetclient.build_request(host, path, params, headers)
	response = httpgetclient.send_request(request)
	assert 200 == response.getcode(), 'The NextBus ' + params['command'] + ' response status code is ' + str(response.getcode())
	return _decompress(response.read())

def _decompress(data):
	return zlib.decompress(data, 16 + zlib.MAX_WBITS)