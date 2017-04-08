import pytest
import json
import os
from .. import cyride

request_one =   {
                    'request': {
                        'type': 'IntentRequest',
                        'requestId': 'EdwRequestId.5a69e678-7c52-4179-b410-21420e71a717',
                        'locale': 'en-US',
                        'timestamp': '2017-03-24T23:50:05Z',
                        'intent': {
                            'name': 'WhenIntent',
                            'slots': {
                                'RouteDirection': {
                                    'name': 'RouteDirection',
                                    'value': 'West'
                                },
                                'StreetAddress': {
                                    'name': 'StreetAddress',
                                        'value': '2823 Lincoln way'
                                },
                                'RouteColor': {
                                    'name': 'RouteColor',
                                    'value': 'red'
                                },
                                'RouteNumber': {
                                    'name': 'RouteNumber',
                                    'value': '1A'
                                }
                            }
                        }
                    }
                }

request_two =   {
                    'request':{
                        'locale':'en-US',
                        'timestamp':'2017-03-25T02:24:14Z',
                        'type':'IntentRequest',
                        'requestId':'EdwRequestId.ca19883d-7b0f-4a54-88f8-349721b2cb37',
                        'intent':{
                            'slots':{
                                'RouteDirection':{
                                    'name':'RouteDirection'
                                },
                                'StreetAddress':{
                                        'name':'StreetAddress',
                                'value':'2823 Lincoln way'
                                },
                                'RouteNumber':{
                                    'name':'RouteNumber',
                                    'value':'5'
                                },
                                'RouteColor':{
                                    'name':'RouteColor',
                                    'value':'yellow'
                               }
                            },
                            'name':'WhenIntent'
                        }
                    }
                }

request_three = {
                    'request':{
                        'locale':'en-US',
                        'timestamp':'2017-03-25T02:24:14Z',
                        'type':'IntentRequest',
                        'requestId':'EdwRequestId.ca19883d-7b0f-4a54-88f8-349721b2cb37',
                        'intent':{
                            'slots':{
                                'RouteDirection':{
                                    'name':'RouteDirection'
                                },
                                'RouteNumber':{
                                   'name':'RouteNumber',
                                     'value':'5'
                                },
                                'RouteColor':{
                                    'name':'RouteColor',
                                    'value':'yellow'
                                }
                            },
                            'name':'WhenIntent'
                        }
                    }
                }

def test_cyride_one():
    os.environ['AGENCY_NAME'] = 'CyRide'
    response = cyride.lambda_handler(request_one, '')
    assert 'Hello!' == response['response']['outputSpeech']['text']

def test_cyride_two():
    os.environ['AGENCY_NAME'] = 'CyRide'
    response = cyride.lambda_handler(request_two, '')
    assert 'Hello!' == response['response']['outputSpeech']['text']

def test_cyride_assert_basic_response():
    pass

def test_cyride_assert_no_streetaddress_returns_error():
    os.environ['AGENCY_NAME'] = 'CyRide'
    response = cyride.lambda_handler(request_three, '')
    assert 'You must provide a street address. Please try again.' == response['response']['outputSpeech']['text']
