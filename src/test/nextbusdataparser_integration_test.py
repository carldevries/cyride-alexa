# nextbusdataparser_integration_test contains integration tests to ensure the
# nextbusdataparser functions are able to parse messages directly from NextBus.
# The tests require the ability to send and receive a GET request to the
# NextBus public XML feed.
import pytest
import xml.etree.ElementTree as ET

from .. import nextbusdataparser
from .. import nextbus

resources_path = 'src\\test\\resources\\nextbus\\'

@pytest.mark.parametrize('agency_title, expected_agency_tag',
    [('CyRide', 'cyride'),
     ('AC Transit', 'actransit')])
def test_get_agency__agency_is_valid(agency_list_response, agency_title, expected_agency_tag):

    agency_list_elements = ET.fromstring(agency_list_response)
    agency = nextbusdataparser.get_agency(agency_title, agency_list_elements)
    assert expected_agency_tag == agency.attrib['tag']

@pytest.mark.usefixture('agency_list_response')
def test_get_agency__agency_is_invalid(agency_list_response):

    agency_list_elements = ET.fromstring(agency_list_response)
    agency = nextbusdataparser.get_agency('Dart', agency_list_elements)
    assert None == agency

@pytest.mark.parametrize('route_name, expected_route_tags',
    [('1 Red West', '811'),
     ('1 Red East', '810'),
     ('1A Red West', '813'),
     ('1A Red East', '812'),
     ('1B Red  East', '814'),
     ('2 Green West', '821'),
     ('2 Green East', '820'),
     ('3 Blue South', '831'),
     ('3 Blue North', '830'),
     ('3A Blue South', '832'),
     ('3B Blue North', '833'),
     ('4 Gray', '840'),
     ('4A Gray', '841'),
     ('5 Yellow', '850'),
     ('6 Brown South', '861'),
     ('6 Brown North', '860'),
     ('6A Towers', '862'),
     ('6B Brown', '863'),
     ('7 Purple', '870'),
     ('9 Plum', '890'),
     ('10 Pink', '910'),
     ('21 Cardinal', '921'),
     ('22 Gold', '922'),
     ('23 Orange', '923'),
     ('A West', '991'),
     ('A East', '992'),
     ('B', '993'),
     ('C', '994'),
     ('D', '995')
     ])
def test_get_routes(route_list_response, route_name, expected_route_tags):

    route_list_elements = ET.fromstring(route_list_response)
    routes = nextbusdataparser.get_routes(route_name, route_list_elements)
    assert expected_route_tags == routes[0].attrib['tag']

# Test cases (in order):
# 4329 Lincoln Swing Street Ames, IA 50014
# Howe Hall, 537 Bissell Rd, Ames, IA 50011
# Mary Greeley Medical Center Ames, IA 50010


@pytest.mark.parametrize('lat, lon, expected_stop',
    [(42.022247, -93.677157, '1185'),
     (42.026913, -93.651913, '1177'),
     (42.032726, -93.611741, '1159')])
def test_get_closest_stop(route_config_response, lat, lon, expected_stop):

    route_config_elements = ET.fromstring(route_config_response)
    stop = nextbusdataparser.get_closest_stop(lat, lon, route_config_elements)
    assert expected_stop == stop.attrib['tag']


@pytest.mark.parametrize('expected_vehicle, expected_time',
    [('1116', '78')])
def test_get_next_vehicle_prediction__valid_data(predictions_response, expected_vehicle, expected_time):

    predictions_elements = ET.fromstring(predictions_response)
    prediction = nextbusdataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle == prediction.attrib['vehicle']
    assert expected_time == prediction.attrib['minutes']


@pytest.mark.parametrize('expected_vehicle_data', [(None)])
def test_get_next_vehicle_prediction__no_data(predictions_response_no_data, expected_vehicle_data):

    predictions_elements = ET.fromstring(predictions_response_no_data)
    prediction = nextbusdataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == prediction


@pytest.mark.parametrize('expected_vehicle_data', [(None)])
def test_get_next_vehicle_prediction__invalid_data(predictions_response_invalid_data, expected_vehicle_data):

    predictions_elements = ET.fromstring(predictions_response_invalid_data)
    prediction = nextbusdataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == prediction


@pytest.mark.parametrize('vehicle_tag, expected_location',
    [('503', {'lat': 42.0254, 'lon': -93.65395}),
     ('111', None)])
def test_get_vehicle_location(vehicle_locations_response, vehicle_tag, expected_location):

    vehicle_location_elements = ET.fromstring(vehicle_locations_response)
    vehicle_location = nextbusdataparser.get_vehicle_location(vehicle_tag, vehicle_location_elements)
    assert expected_location == vehicle_location

# ############################# TEST FIXTURES #################################


@pytest.fixture(scope='module')
def agency_list_response():

    return nextbus.agency_list()


@pytest.fixture(scope='module')
def route_list_response():

    return nextbus.route_list('cyride')


@pytest.fixture(scope='module')
def route_config_response():

    return open(resources_path + 'cyride_route_config_response.xml').read()


@pytest.fixture(scope='module')
def predictions_response():

    return open(resources_path + 'cyride_predictions_response.xml').read()


@pytest.fixture(scope='module')
def predictions_response_no_data():

    return open(resources_path + 'cyride_predictions_no_data_response.xml').read()


@pytest.fixture(scope='module')
def predictions_response_invalid_data():

    f = open(resources_path + 'cyride_predictions_invalid_data_response.xml').read()
    return f


@pytest.fixture(scope='module')
def vehicle_locations_response():

    return open(resources_path + 'cyride_vehicle_locations_response.xml').read()

# This XML scenario need to be reviewed


@pytest.fixture(scope='module')
def vehicle_location_response_no_vehicles():

    f = open(resources_path + 'cyride_vehicle_locations_no_vehicles_response.xml')
    return f.read()
