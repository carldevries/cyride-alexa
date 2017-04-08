import httpgetclient

geocode_path = '/geocoding/v1/address'
reverse_geocode_path = '/geocoding/v1/reverse'
host = 'www.mapquestapi.com'
headers =   {
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding' : 'gzip, deflate, sdch',
                'Accept-Language' : 'en-US,en;q=0.8',
                'Host' : host,
                'Connection' : 'keep-alive',
                'Upgrade-Insecure-Requests' : '1',
                'Cache-Control' : 'max-age=0'
            }

def geocode(address, api_key):

    return  _proces_request(geocode_path,   {
                                                'key' : api_key,
                                                'location' : address
                                            })

def reverse_geocode(lat, lon, api_key):

    return _process_request(reverse_geocode_path,   {
                                                        'key' : api_key,
                                                        'location' : str(lat) + ',' + str(lon),
                                                        'includeNearestIntersection' : 'true'
                                                    })

def _process_request(path, params):

    request = httpgetclient.build_request(host, path, params, headers)
    response = httpgetclient.send_request(request)
    assert 200 == response.getcode(), 'The MapQuest response status code to ' + path + ' is ' + str(response.getcode())
    return response.read()
