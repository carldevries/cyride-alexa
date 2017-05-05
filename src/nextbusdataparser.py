# Module block comment
from haversineformula import haversine_formula_deg

# get_agency_tag comment


def get_agency_tag(agency_name, agency_list):

    for agency in agency_list:
        if agency.attrib['title'] == agency_name:
            return agency.attrib['tag']

    return None

# get_route_tag comment


def get_route_tags(route_name, route_list):

    # Happy path. The route_name exactly matches an element in the list.
    for route in route_list:
        if route.attrib['title'].lower() == route_name.lower():
            return [route.attrib['tag']]

    # Search for a non perfect match by route name components number, color,
    # and direction. Create an array to hold match counts for each route.
    route_name_components = route_name.split()
    matches = [0 for i in range(len(route_list))]

    # Search each route for each requested route_name_component.  Increase each
    # routes score if a match is made.
    for i in range(len(route_list)):
        title = route_list[i].attrib['title']
        for component in route_name_components:
            if title.count(component) > 0:
                matches[i] = matches[i] + 1

    # Get the maximum number of matches by any route(s).
    max_matches = max(matches)
    selected_matches = []

    # Collect the names of the routes with the maximum matches.
    for i in range(len(matches)):
        if matches[i] == max_matches:
            selected_matches.append(route_list[i].attrib['tag'])

    return selected_matches

# get_closest_stop_tag comment


def get_closest_stop_tag(lat, lon, route_config):

    # closest_stop_tag sed to be initialized to ''.  Try some tests.
    closest_stop_tag = None
    smallest_distance = -1
    route = route_config.find('route')

    if route is not None:
        for stop in route:
            if 'stop' == stop.tag:
                stop_lat = float(stop.attrib['lat'])
                stop_lon = float(stop.attrib['lon'])
                distance = haversine_formula_deg(lat, lon, stop_lat, stop_lon)
                if smallest_distance < 0 or distance < smallest_distance:
                    smallest_distance = distance
                    closest_stop_tag = stop.attrib['tag']

        return closest_stop_tag

    return None

# get_next_vehicle_prediction comment


def get_next_vehicle_prediction(predictions_list):

    for predictions in predictions_list:
        if 'dirTitleBecauseNoPredictions' not in predictions.keys():
            direction = predictions.find('direction')
            if direction is not None:
                prediction_list = direction.findall('prediction')
                vehicle_prediction = None
                for prediction in prediction_list:
                    time = float(prediction.attrib['minutes'])
                    if (vehicle_prediction is None or time < vehicle_prediction['minutes']):
                        vehicle_prediction = {
                                                'vehicle': prediction.attrib['vehicle'],
                                                'minutes': time
                                              }

                return vehicle_prediction

    return None

# get_vehcile_location comment


def get_vehicle_location(vehicle_tag, vehicles):

    for vehicle in vehicles:
        if 'vehicle' == vehicle.tag and vehicle.attrib['id'] == vehicle_tag:
            return {
                        'lat': float(vehicle.attrib['lat']),
                        'lon': float(vehicle.attrib['lon'])
                    }

    return None
