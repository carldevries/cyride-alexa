import pytest
import xml.etree.ElementTree as ET
from .. import nextbusdataparser

agency_list_xml_response = '''<body copyright="All data copyright agencies listed below and NextBus Inc 2017.">
                                        <agency tag="west-hollywood" title="City of West Hollywood" regionTitle="California-Southern"/>
                                        <agency tag="collegetown" title="Collegetown Shuttle" regionTitle="Maryland"/>
                                        <agency tag="configdev" title="Config Stuff" regionTitle="Other"/>
                                        <agency tag="cyride" title="CyRide" regionTitle="Iowa"/>
                                        <agency tag="dc-streetcar" title="DC Streetcar" regionTitle="District of Columbia"/>
                                        <agency tag="umn-twin" title="University of Minnesota" regionTitle="Minnesota"/>
                                </body>'''

route_list_xml_response = '''<body copyright="All data copyright CyRide 2017.">
                                                <route tag="811" title="1 Red West"/>
                                                <route tag="810" title="1 Red East"/>
                                                <route tag="813" title="1A Red West"/>
                                                <route tag="812" title="1A Red East"/>
                                                <route tag="814" title="1B Red East"/>
                                                <route tag="821" title="2 Green West"/>
                                                <route tag="820" title="2 Green East"/>
                                                <route tag="831" title="3 Blue South"/>
                                                <route tag="830" title="3 Blue North"/>
                                                <route tag="832" title="3A Blue South"/>
                                                <route tag="833" title="3B Blue North"/>
                                                <route tag="840" title="4 Gray"/>
                                                <route tag="841" title="4A Gray"/>
                                                <route tag="850" title="5 Yellow"/>
                                                <route tag="861" title="6 Brown South"/>
                                                <route tag="860" title="6 Brown North"/>
                                                <route tag="862" title="6A Towers"/>
                                                <route tag="863" title="6B Brown"/>
                                                <route tag="870" title="7 Purple"/>
                                                <route tag="890" title="9 Plum"/>
                                                <route tag="910" title="10 Pink"/>
                                                <route tag="921" title="21 Cardinal"/>
                                                <route tag="922" title="22 Gold"/>
                                                <route tag="923" title="23 Orange"/>
                                                <route tag="991" title="A West"/>
                                                <route tag="992" title="A East"/>
                                                <route tag="993" title="B"/>
                                                <route tag="994" title="C"/>
                                                <route tag="995" title="D"/>
                                        </body>'''

route_config_xml_response = '''<body copyright="All data copyright CyRide 2017.">
                                                        <route tag="811" title="1 Red West" color="cc3333" oppositeColor="ffffff" latMin="42.01197" latMax="42.05117" lonMin="-93.68158" lonMax="-93.61051">
                                                                <stop tag="1150" title="North Grand Mall" lat="42.0495599" lon="-93.62179" stopId="1150"/>
                                                                <stop tag="1151" title="Duff Ave. at Kellogg Ave." lat="42.05117" lon="-93.6185699" stopId="1151"/>
                                                                <stop tag="1152" title="Duff Ave. at Northwood Dr." lat="42.0484" lon="-93.6141599" stopId="1152"/>
                                                                <stop tag="1153" title="Duff Ave. at 24th St." lat="42.04532" lon="-93.6141199" stopId="1153"/>
                                                                <stop tag="1154" title="Duff Ave. at 22nd St." lat="42.04402" lon="-93.61279" stopId="1154"/>
                                                                <stop tag="1155" title="Duff Ave. at 20th St." lat="42.0417499" lon="-93.61071" stopId="1155"/>
                                                                <stop tag="1156" title="Duff Ave. at O&apos;Neil Dr." lat="42.0400299" lon="-93.61071" stopId="1156"/>
                                                                <stop tag="1157" title="Duff Ave. at 16th St." lat="42.0380699" lon="-93.61069" stopId="1157"/>
                                                                <stop tag="1158" title="Duff Ave. at 14th St." lat="42.03541" lon="-93.61067" stopId="1158"/>
                                                                <stop tag="1159" title="Duff Ave. at 12th St." lat="42.03328" lon="-93.61063" stopId="1159"/>
                                                                <stop tag="1160" title="Mary Greely Hospital" lat="42.0316199" lon="-93.61058" stopId="1160"/>
                                                                <stop tag="1161" title="Duff Ave. at 9th St." lat="42.0298199" lon="-93.6105399" stopId="1161"/>
                                                                <stop tag="1162" title="Duff Ave. at 8th St." lat="42.02873" lon="-93.61051" stopId="1162"/>
                                                                <stop tag="1163" title="6th St. at Duff Ave." lat="42.02694" lon="-93.61108" stopId="1163"/>
                                                                <stop tag="1164" title="Ames Public Library" lat="42.0265599" lon="-93.6121199" stopId="1164"/>
                                                                <stop tag="1165" title="5th St. at Kellogg Ave." lat="42.0259599" lon="-93.6140699" stopId="1165"/>
                                                                <stop tag="1166" title="City Hall" lat="42.0258099" lon="-93.61785" stopId="1166"/>
                                                                <stop tag="1167" title="Allan Dr. at Grand Ave." lat="42.0256399" lon="-93.62045" stopId="1167"/>
                                                                <stop tag="1168" title="Lincoln Way at Elm Ave." lat="42.02291" lon="-93.6227999" stopId="1168"/>
                                                                <stop tag="1169" title="Lincoln Way at Maple Ave." lat="42.02284" lon="-93.6255099" stopId="1169"/>
                                                                <stop tag="1419" title="Lincoln Way at Hazel Ave." lat="42.02284" lon="-93.62721" stopId="1419"/>
                                                                <stop tag="1170" title="Lincoln Way at Russell Ave." lat="42.02283" lon="-93.62857" stopId="1170"/>
                                                                <stop tag="1238" title="Lincoln Way at Hilton Coliseum" lat="42.02281" lon="-93.6351799" stopId="1238"/>
                                                                <stop tag="1171" title="Lincoln Way at Beach Ave." lat="42.0227599" lon="-93.64006" stopId="1171"/>
                                                                <stop tag="1172" title="Lincoln Way at Union Dr." lat="42.02278" lon="-93.64224" stopId="1172"/>
                                                                <stop tag="1173" title="Lincoln Way at Lynn Ave." lat="42.02282" lon="-93.6469699" stopId="1173"/>
                                                                <stop tag="1174" title="Lake Laverne" lat="42.0236267" lon="-93.649643" stopId="1174"/>
                                                                <stop tag="1175" title="Enrollment Services Building" lat="42.02445" lon="-93.64954" stopId="1175"/>
                                                                <stop tag="1176" title="Student Services" lat="42.0251838" lon="-93.6507781" stopId="1176"/>
                                                                <stop tag="1177" title="Beyer Hall" lat="42.0253699" lon="-93.65296" stopId="1177"/>
                                                                <stop tag="1178" title="West St. at Hyland Ave." lat="42.02534" lon="-93.65542" stopId="1178"/>
                                                                <stop tag="1179" title="Hyland Ave. at Lincoln Way" lat="42.02303" lon="-93.6555999" stopId="1179"/>
                                                                <stop tag="1180" title="Lincoln Way at State Ave." lat="42.02273" lon="-93.6594199" stopId="1180"/>
                                                                <stop tag="1181" title="Lincoln Way at Wilmoth Ave." lat="42.02277" lon="-93.66208" stopId="1181"/>
                                                                <stop tag="1182" title="Lincoln Way at Franklin Ave." lat="42.0228" lon="-93.6655899" stopId="1182"/>
                                                                <stop tag="1183" title="Lincoln Way at Marshall Ave." lat="42.0228999" lon="-93.66994" stopId="1183"/>
                                                                <stop tag="1184" title="Lincoln Way at Hickory Dr." lat="42.02296" lon="-93.67358" stopId="1184"/>
                                                                <stop tag="1185" title="S. Dakota Ave. at Lincoln Swing" lat="42.0222299" lon="-93.6787099" stopId="1185"/>
                                                                <stop tag="1186" title="S. Dakota Ave. at Todd Dr." lat="42.0211199" lon="-93.6787" stopId="1186"/>
                                                                <stop tag="1187" title="S. Dakota Ave. at Clemens Blvd." lat="42.0176399" lon="-93.67868" stopId="1187"/>
                                                                <stop tag="1188" title="Steinbeck St. at S. Dakota Ave." lat="42.01458" lon="-93.6792599" stopId="1188"/>
                                                                <stop tag="1189" title="Dickenson Ave. at Steinbeck St." lat="42.0142299" lon="-93.68107" stopId="1189"/>
                                                                <stop tag="1190" title="Dickenson Ave. at Mortensen Rd." lat="42.0128999" lon="-93.68158" stopId="1190"/>
                                                                <stop tag="1191" title="Mortensen Rd. at Coconino Rd." lat="42.01206" lon="-93.6760599" stopId="1191"/>
                                                                <stop tag="1192" title="Mortensen Rd. at Dotson Dr." lat="42.01197" lon="-93.67355" stopId="1192"/>
                                                                <stop tag="1193" title="Ames Middle School" lat="42.0121999" lon="-93.67143" stopId="1193"/>
                                                        </route>
                                                </body>'''

predictions_xml_response = '''<body copyright="All data copyright CyRide 2017.">
                                                        <predictions agencyTitle="CyRide" routeTitle="1A Red East" routeTag="812" stopTitle="Lincoln Way at Beedle Dr." stopTag="1202" dirTitleBecauseNoPredictions="Kildee / Bessey">
                                                        </predictions>
                                                        <predictions agencyTitle="CyRide" routeTitle="1 Red East" routeTag="810" stopTitle="Lincoln Way at Beedle Dr." stopTag="1202">
                                                                <direction title="Mall via Hospital">
                                                                        <prediction epochTime="1489378631095" seconds="5544" minutes="92" isDeparture="false" affectedByLayover="true" dirTag="810_1_var3" vehicle="2115" block="7704" tripTag="71742" />
                                                                        <prediction epochTime="1489378631095" seconds="4688" minutes="78" isDeparture="false" affectedByLayover="true" dirTag="810_1_var3" vehicle="1116" block="7704" tripTag="71742" />
                                                                        <prediction epochTime="1489378631095" seconds="6192" minutes="103" isDeparture="false" affectedByLayover="true" dirTag="810_1_var3" vehicle="2117" block="7704" tripTag="71742" />
                                                                </direction>
                                                        </predictions>
                                                </body>'''

predictions_xml_response_no_data = '''<body copyright="All data copyright CyRide 2017.">
                                                        <predictions agencyTitle="CyRide" routeTitle="1A Red East" routeTag="812" stopTitle="Lincoln Way at Beedle Dr." stopTag="1202" dirTitleBecauseNoPredictions="Kildee / Bessey">
                                                        </predictions>
                                                        <predictions agencyTitle="CyRide" routeTitle="1 Red East" routeTag="810" stopTitle="Lincoln Way at Beedle Dr." stopTag="1202" dirTitleBecauseNoPredictions="Mall via Hospital">
                                                        </predictions>
                                                </body>'''

predictions_xml_response_invalid_data = '''<body copyright="All data copyright CyRide 2017.">
                                                                                        <predictions agencyTitle="CyRide" routeTitle="1A Red East" routeTag="812" stopTitle="Lincoln Way at Beedle Dr." stopTag="1202" dirTitleBecauseNoPredictions="Kildee / Bessey">
                                                                                        </predictions>
                                                                                        <predictions agencyTitle="CyRide" routeTitle="1 Red East" routeTag="810" stopTitle="Lincoln Way at Beedle Dr." stopTag="1202">
                                                                                        </predictions>
                                                                                </body>'''

vehicle_locations_xml_response = '''<body copyright="All data copyright CyRide 2017.">
                                                                <vehicle id="503" routeTag="811" dirTag="811_0_var0" lat="42.0254" lon="-93.65395" secsSinceReport="3" predictable="true" heading="270" speedKmHr="20"/>
                                                                <vehicle id="1007" routeTag="811" dirTag="811_0_var0" lat="42.0333" lon="-93.6564" secsSinceReport="3" predictable="true" heading="270" speedKmHr="30"/>
                                                                <vehicle id="2564" routeTag="811" dirTag="811_0_var0" lat="42.0444" lon="-93.65210" secsSinceReport="3" predictable="true" heading="270" speedKmHr="40"/>
                                                                <lastTime time="1489886297533"/>
                                                        </body>'''

#This XML scenario need to be reviewed
vehicle_location_xml_response_no_vehicles = '''<body copyright="All data copyright CyRide 2017.">
                                                                                <lastTime time="1489886297533"/>
                                                                        </body>'''

@pytest.mark.parametrize('agency_title, expected_agency_tag', [('CyRide', 'cyride'),
                                                                                                                        ('Collegetown Shuttle', 'collegetown'),
                                                                                                                        ('Dart', None)])
def test_getAgencyTag(agency_title, expected_agency_tag):
    agency_list_elements = ET.fromstring(agency_list_xml_response)
    agency_tag = cyridedataparser.get_agency_tag(agency_title, agency_list_elements)
    assert expected_agency_tag == agency_tag

@pytest.mark.parametrize('route_name, expected_route_tags', [('1 Red West', ['811']),
                                                                                                                ('1 Red East', ['810']),
                                                                                                                ('1A Red West', ['813']),
                                                                                                                ('1A Red East', ['812']),
                                                                                                                ('1B Red East', ['814']),
                                                                                                                ('2 Green West', ['821']),
                                                                                                                ('2 Green East', ['820']),
                                                                                                                ('3 Blue South', ['831']),
                                                                                                                ('3 Blue North', ['830']),
                                                                                                                ('3A Blue South', ['832']),
                                                                                                                ('3B Blue North', ['833']),
                                                                                                                ('4 Gray', ['840']),
                                                                                                                ('4A Gray', ['841']),
                                                                                                                ('5 Yellow', ['850']),
                                                                                                                ('6 Brown South', ['861']),
                                                                                                                ('6 Brown North', ['860']),
                                                                                                                ('6A Towers', ['862']),
                                                                                                                ('6B Brown', ['863']),
                                                                                                                ('7 Purple', ['870']),
                                                                                                                ('9 Plum', ['890']),
                                                                                                                ('10 Pink', ['910']),
                                                                                                                ('21 Cardinal', ['921']),
                                                                                                                ('22 Gold', ['922']),
                                                                                                                ('23 Orange', ['923']),
                                                                                                                ('A West', ['991']),
                                                                                                                ('A East', ['992']),
                                                                                                                ('B', ['993']),
                                                                                                                ('C', ['994']),
                                                                                                                ('D', ['995'])])
def test_get_route_tag(route_name, expected_route_tags):

    route_list_elements = ET.fromstring(route_list_xml_response)
    route_tags = cyridedataparser.get_route_tag(route_name, route_list_elements)
    assert expected_route_tags == route_tags

@pytest.mark.parametrize('latitude, longitude, expected_closest_stop', [        (42.022247, -93.677157, '1185'),#4329 Lincoln Swing Street Ames, IA 50014
                                                                                                                                                        (42.026913, -93.651913, '1177'),#Howe Hall, 537 Bissell Rd, Ames, IA 50011
                                                                                                                                                        (42.032726, -93.611741, '1159')#Mary Greeley Medical Center Ames, IA 50010
                                                                                                                                                        ])
def test_getClosestStopTag(latitude, longitude, expected_closest_stop):
    route_config_elements = ET.fromstring(route_config_xml_response)
    stop_tag = cyridedataparser.get_closest_stop_tag(latitude, longitude, route_config_elements)
    assert expected_closest_stop == stop_tag

@pytest.mark.parametrize('expected_vehicle_data', [({'vehicle' : '1116', 'minutes': 78.0})])
def test_get_next_vehicle_prediction__valid_data(expected_vehicle_data):
    predictions_elements = ET.fromstring(predictions_xml_response)
    vehicle_data = cyridedataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == vehicle_data

@pytest.mark.parametrize('expected_vehicle_data', [(None)])
def test_get_next_vehicle_prediction__no_data(expected_vehicle_data):
    predictions_elements = ET.fromstring(predictions_xml_response_no_data)
    vehicle_data = cyridedataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == vehicle_data

@pytest.mark.parametrize('expected_vehicle_data', [(None)])
def test_get_next_vehicle_prediction__invalid_data(expected_vehicle_data):
    predictions_elements = ET.fromstring(predictions_xml_response_invalid_data)
    vehicle_data = cyridedataparser.get_next_vehicle_prediction(predictions_elements)
    assert expected_vehicle_data == vehicle_data

@pytest.mark.parametrize('vehicle_tag, expected_vehicle_location', [('503', {'lat' : 42.0254, 'lon': -93.65395}),
                                                                                                                                ('111', None)])
def test_get_vehicle_location(vehicle_tag, expected_vehicle_location):
    vehicle_location_elements = ET.fromstring(vehicle_locations_xml_response)
    vehicle_location = cyridedataparser.get_vehicle_location(vehicle_tag, vehicle_location_elements)
    assert expected_vehicle_location == vehicle_location
