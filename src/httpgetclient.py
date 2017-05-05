# This is a module for common http GET request code required by other modules.
# The functions in httpgetclient use urllib and urllib2 to build and execute
# GET requests.
import urllib
import urllib2
import logging

# send_request builds a GET request using the given arguments.  The request
# parameters are encoded if they are given.  The request is then sent and the
# response object is returned to the calling function.
# Inputs:
#   host - The host portion of the web address where the webservice is located.
#       The host must also include the protocol appended to the from since.
#   path - The location of the webservice on the host.
#   params - A dict containing the key value pairs to be encoded in the URL.
#   header_attributes - A dict containing the key value pairs to be sent in
#       in the request header.
# Outputs:
#   response - The response object returned by the webservice.
# Exceptions:
#   URLError - If an URLError is raised while executing the request then the
#       error is logged and reraised up the call stack.
#   AssertionError - If the HTTP status code for the request is not 200 then
#       an AssertionError is raised.


def send_request(host, path, params, header_attributes):

    encodedParams = ''
    if params is not None:
        encodedParams = '?' + urllib.urlencode(params)

    url = host.lower() + path + encodedParams
    request = urllib2.Request(url, headers=header_attributes)

    logging.debug('Sending request to %s', url)

    try:

        response = urllib2.urlopen(request)
        code = str(response.getcode())
        logging.debug('Received response code: %s', code)
        assert 200 != code, 'The url ' + url + ' returned status code ' + code

    except urllib2.URLError as e:
        logging.error('URLError raised: %s', str(e))
        raise e

    return response
