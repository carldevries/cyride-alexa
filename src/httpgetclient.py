import urllib
import urllib2
import logging

def build_request(host, path, params, header_attributes):

    encodedParams = urllib.urlencode(params)
    request = urllib2.Request('http://' + host + path + '?' + encodedParams, headers = header_attributes)

    return request

def send_request(request):

    response = urllib2.urlopen(request)
    logging.debug('Received response code: %s', str(response.getcode()))

    return response
