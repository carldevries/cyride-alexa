# nextbusdataparser_test contains tests for making sure the data parsing
# functions correctly parse static
import pytest
import xml.etree.ElementTree as ET
from .. import nextbusdataparser

resources_path = 'src\\test\\resources\\nextbus\\'


@pytest.mark.parametrize('agency_title, expected_agency_tag',
    [('CyRide', 'cyride'),
     ('Collegetown Shuttle', 'collegetown'),
     ('Dart', None)])
def test_getAgencyTag(agency_list_response, agency_title, expected_agency_tag):

    agency_list_elements = ET.fromstring(agency_list_response)
    agency_tag = nextbusdataparser.get_agency_tag(agency_title, agency_list_elements)
    assert expected_agency_tag == agency_tag


@pytest.mark.parametrize('route_name, expected_route_tags',
    [('1 Red West', ['1W']),
     ('1 Red East', ['1E']),
     ('1A Red West', ['1AW']),
     ('1A Red East', ['1A']),
     ('2 Green West', ['2W']),
     ('2 Green East', ['2E']),
     ('3 Blue South', ['3S']),
     ('3 Blue North', ['3N']),
     ('3A Blue South', ['3A']),
     ('4 Gray', ['4']),
     ('4A Gray', ['4A']),
     ('5 Yellow', ['5']),
     ('6 Brown South', ['6S']),
     ('6 Brown North', ['6N']),
     ('6B Brown', ['6B']),
     ('7 Purple', ['7']),
     ('8 Aqua', ['8']),
     ('10 Pink', ['10']),
     ('23 Orange', ['23'])])
def test_get_route_tag(route_list_response, route_name, expected_route_tags):

    route_list_elements = ET.fromstring(route_list_response)
    route_tags = nextbusdataparser.get_route_tags(route_name, route_list_elements)
    assert expected_route_tags == route_tags

# Test cases (in order):
# 4329 Lincoln Swing Street Ames, IA 50014
# Howe Hall, 537 Bissell Rd, Ames, IA 50011
# Mary Greeley Medical Center Ames, IA 50010


@pytest.mark.parametrize('lat, lon, expected_stop',
    [(42.022247, -93.677157, '1185'),
     (42.026913, -93.651913, '1177'),
     (42.032726, -93.611741, '1159')])
def test_get_closest_stop_tag(route_config_response, lat, lon, expected_stop):

    route_config_elements = ET.fromstring(route_config_response)
    stop_tag = nextbusdataparser.get_closest_stop_tag(lat, lon, route_config_elements)
    assert expected_stop == stop_tag


@pytest.mark.parametrize('expected_vehicle_data',
    [({'vehicle': '1116', 'minutes': 78.0})])
def test_get_next_vehicle_prediction__valid_data(predictions_response, expected_vehicle_data):

    predictions_elements = ET.fromstring(predictions_response)
    vehicle_data = nextbusdataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == vehicle_data


@pytest.mark.parametrize('expected_vehicle_data', [(None)])
def test_get_next_vehicle_prediction__no_data(predictions_response_no_data, expected_vehicle_data):

    predictions_elements = ET.fromstring(predictions_response_no_data)
    vehicle_data = nextbusdataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == vehicle_data


@pytest.mark.parametrize('expected_vehicle_data', [(None)])
def test_get_next_vehicle_prediction__invalid_data(predictions_response_invalid_data, expected_vehicle_data):

    predictions_elements = ET.fromstring(predictions_response_invalid_data)
    vehicle_data = nextbusdataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == vehicle_data


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
    return open(resources_path + 'agency_list_response.xml').read()


@pytest.fixture(scope='module')
def route_list_response():
    return open(resources_path + 'cyride_route_list_response.xml').read()


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
