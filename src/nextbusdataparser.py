import haversineformula

def get_agency_tag(agency_name, agency_list):

    for agency in agency_list:
        if agency.attrib['title'] == agency_name:
            return agency.attrib['tag']

    return None

def get_route_tag(route_name, route_list):

    for route in route_list:

        if route.attrib['title'].lower() == route_name.lower():
            return [route.attrib['tag']]

    route_name_components = route_name.split()
    matches = [0 for i in range(len(route_list))]


    for i in range(len(route_list)):
        title = route_list[i].attrib['title']
        for component in route_name_components:
            if title.count(component) > 0:
                matches[i] = matches[i] + 1

    max_matches = max(matches)
    selected_matches = []

    for i in range(len(matches)):
        if matches[i] == max_matches:
            selected_matches.append(route_list[i].attrib['tag'])

    return selected_matches

def get_closest_stop_tag(lat, lon, route_config):

    closest_stop_tag = ''
    smallest_distance = -1
    route = route_config.find('route')

    if route != None:
        for stop in route:
            if 'stop' == stop.tag:
                stop_lat = float(stop.attrib['lat'])
                stop_lon = float(stop.attrib['lon'])
                distance = haversineformula.haversine_formula(lat, lon, stop_lat, stop_lon)
                if smallest_distance < 0 or distance < smallest_distance:
                    smallest_distance = distance
                    closest_stop_tag = stop.attrib['tag']

        return closest_stop_tag

    return None

def get_next_vehicle_prediction(predictions_list):

    for predictions in predictions_list:
        if 'dirTitleBecauseNoPredictions' not in predictions.keys():
            direction = predictions.find('direction')
            if direction is not None:
                prediction_list = direction.findall('prediction')
                vehicle_prediction = None
                for prediction in prediction_list:
                    time = float(prediction.attrib['minutes'])
                    if vehicle_prediction == None or time < vehicle_prediction['minutes']:
                        vehicle_prediction = {
                                                        'vehicle' : prediction.attrib['vehicle'],
                                                        'minutes' : time
                                                        }

                return vehicle_prediction

    return None

def get_vehicle_location(vehicle_tag, vehicles):

    for vehicle in vehicles:
        if 'vehicle' == vehicle.tag and vehicle.attrib['id'] == vehicle_tag:
            return {
                            'lat' : float(vehicle.attrib['lat']),
                            'lon' : float(vehicle.attrib['lon'])
                            }

    return None
