# mapquest is a module for making GET requests to MapQuest webservices and
# returning the data.  All requests require and API key which can be obtained
# for free from MapQuest's developer portal.

import httpgetclient

host = 'www.mapquestapi.com'
headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Host': host,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
           }

# geocode is a function for creating the a request to MapQuest's geocoding
# service.  The goal of executing this function should be to obtain the
# latitude and longitude coordinates for a given address.  The request is
# executed using the httpgetclient module and the content is returned as a
# string in JSON format.
# Inputs:
#   address - The address for which geocoding data is requested.  The address
#       can be given in several forms with more or less details; however, more
#       tends to be better. (Ex. 123 4th Street Des Moines, IA 50309)
#   api_key - The MapQuest API key tied to the application requesting geocoding
#       data from the webservice.
# Outputs:
#    @return - A string containing the response content in a JSON format.


def geocode(address, api_key):

    params = {
                'key': api_key,
                'location': address
             }

    return _process_request('/geocoding/v1/address', params)

# reverse_geocode is a function for creating the a request to MapQuest's
# reverse geocoding service.  The goal of executing this function should be to
# obtain a street address for a given latitude and longitude coordinates.  The
# request is executed using the httpgetclient module and the content is
# returned as a string in JSON.
# Inputs:
#   address - The address for which geocoding data is requested.  The address
#       can be given in several forms with more or less details; however, more
#       tends to be better. (Ex. 123 4th Street Des Moines, IA 50309)
#   api_key - The MapQuest API key tied to the application requesting geocoding
#       data from the webservice.
# Outputs:
#    @return - A string containing the response content in a JSON format.


def reverse_geocode(lat, lon, api_key):

    params = {
                'key': api_key,
                'location': str(lat) + ',' + str(lon),
                'includeNearestIntersection': 'true'
             }

    return _process_request('/geocoding/v1/reverse', params)

# _process_request comment


def _process_request(path, params):

    url = 'http://' + host
    response = httpgetclient.send_request(url, path, params, headers)
    return response.read()
