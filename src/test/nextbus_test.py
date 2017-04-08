import pytest
import xml.etree.ElementTree as ET
from .. import nextbus

def test_get_agency_list():

    response_xml = nextbus.get_agency_list()
    response_element = ET.fromstring(response_xml)

    assert_xml_contains_valid_tags(response_element, ['body'])
    for child in response_element:
        assert_xml_contains_valid_tags(child, ['agency'])

def test_get_route_list():

    response_xml = nextbus.get_route_list('cyride')
    response_element = ET.fromstring(response_xml)

    assert_xml_contains_valid_tags(response_element, ['body'])
    for child in response_element:
        assert_xml_contains_valid_tags(child, ['route'])

def test_get_route_config():

    response_xml = nextbus.get_route_config('cyride', '811')
    response_element = ET.fromstring(response_xml)
    acceptable_tags = ['route']

    #Assert top level body tag exists
    assert_xml_contains_valid_tags(response_element, ['body'])
    #Assert only route tags are allowed below the body tag
    for child in response_element:
        assert_xml_contains_valid_tags(child, ['route'])

    #Assert only one route tag exists and only stop, direction, and path
    #tags are allowed below route
    #route_element = response_element.findall('route')
    #assert 1 == len(route_element)
    #for child in route_element:
        #assert_xml_contains_valid_tags(child, ['stop', 'direction', 'path'])

def assert_xml_contains_valid_tags(child, acceptable_tags):

    assert 1 == len(filter(lambda acceptable_tag : child.tag == acceptable_tag, acceptable_tags)), 'The tag \'' +  child.tag + '\' is not an acceptable tag.'
