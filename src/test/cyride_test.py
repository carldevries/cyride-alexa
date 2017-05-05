import pytest
from json import load
from mock import Mock

# The test resources path with respect to the base application directory
resources_path = 'src\\test\\resources\\amazon\\'

# Import and mock the get_device_address call. amazon.get_device_address must
# be imported and mocked before importing the lambda_function module so the
# mock is properly bound.  If it's not the mock will fail silently.
from .. import amazon
mock_echo_device_location = open(resources_path + 'alexa_device_address_api_response.json').read()
amazon.get_device_address = Mock(return_value=mock_echo_device_location)

from .. import cyride

# FIXTURES

# set_environment_varibles sets the AGENCY_NAME and MAPQUEST_API_KEY which are
# expected to be set in the AWS enviornment.  The environment variables need to
# be available for each test.  The monkeypatch module can only be used in a
# fixture with a function level scope so unfortunately this runs for each test.
# The properties parameter comes from the conftest.py properties fixture.


@pytest.fixture(autouse=True)
def set_environment_variables(monkeypatch, properties):

    monkeypatch.setenv('AGENCY_NAME', 'cyride')
    monkeypatch.setenv('MAPQUEST_API_KEY', properties['MAPQUEST_API_KEY'])

# next_arrival_event_one loads the specified request to be passed to the
# cyride-alexa application entry point.  It also sets the ALEXA_DEVICE_ID and
# ALEXA_CONSENT_TOKEN which are needed for requesting device location data from
# Amazon, but due to certificate issues that functions mocked above.


@pytest.fixture(scope='module')
def next_arrival_event_one(properties):

    file = open(resources_path + 'cyride_alexa_next_arrival_request_one.json')
    event = load(file)

    system = event['context']['System']
    system['device']['deviceId'] = properties['ALEXA_DEVICE_ID']
    system['user']['permissions']['consentToken'] = properties['ALEXA_CONSENT_TOKEN']
    return event

# Tests


@pytest.mark.usefixture('set_environment_variables')
def test_cyride_one(next_arrival_event_one):

    response = cyride.ride(next_arrival_event_one, '')
    assert 'Hello!' == response['response']['outputSpeech']['text']
