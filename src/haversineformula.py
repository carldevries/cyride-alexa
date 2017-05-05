# haversineformula is a module with a single method for calculating the
# great-circle distance between two points on the surface of a sphere.  Note
# the haversine formula becomes less accurate as the two coordinate pairs move
# to opposite sides of the sphere.  The radius used to approximate the distance
# is 6371.008 kilometers.

import math

# haversine_formula_deg calculates the great-circle distance between two
# latitude longitude coordinate pairs.  This function accepts arguments in
# degrees, but converts the values to radians and uses haversine_formula_rad to
# perform the distance calculation.
# Inputs:
#   lat_one_deg - The latitude of of the first coordinate provided as a decimal
#       with degrees as the units.
#   lon_one_deg - The longitude of of the first coordinate provided as a
#       decimal with degrees as the units.
#   lat_two_deg - The latitude of of the second coordinate provided as a
#       decimal with degreees as the units.
#   lon_two_deg - The longitude of of the second coordinate provided as a
#       decimal with degrees as the units.
# Outputs:
#   distance - The great-circle distance between two points in kilometers.


def haversine_formula_deg(lat_one_deg, lon_one_deg, lat_two_deg, lon_two_deg):

    lat_one_rad = math.radians(lat_one_deg)
    lon_one_rad = math.radians(lon_one_deg)
    lat_two_rad = math.radians(lat_two_deg)
    lon_two_rad = math.radians(lon_two_deg)

    return haversine_formula_rad(lat_one_rad, lon_one_rad, lat_two_rad, lon_two_rad)

# haversine_formula_rad calculates the great-circle distance between two
# latitude longitude coordinate pairs.  This function accepts arguments in
# radians, and uses the haversine formula derived from the law of haversines
# to calculate the distance between the two given coordinates.
# Inputs:
#   lat_one - The latitude of of the first coordinate provided as a decimal
#       with radians as the units.
#   lon_one - The longitude of of the first coordinate provided as a
#       decimal with radians as the units.
#   lat_two - The latitude of of the second coordinate provided as a
#       decimal with radians as the units.
#   lon_two - The longitude of of the second coordinate provided as a
#       decimal with radians as the units.
# Outputs:
#   distance - The great-circle distance between two points in kilometers.


def haversine_formula_rad(lat_one, lon_one, lat_two, lon_two):

    # Radius of the Earth in kilometers
    earth_radius = 6371.008

    # Calculate the difference between the latitude and longitude coordinates
    lat_diff = lat_two - lat_one
    lon_diff = lon_two - lon_one

    # Calculate the haversine of lat_diff_rad and lon_diff_rad
    hav_lat = math.pow(math.sin(lat_diff / 2), 2)
    hav_lon = math.pow(math.sin(lon_diff / 2), 2)

    # Evaluate the right hand side of the function and solve for the distance.
    rhs = hav_lat + (math.cos(lat_one) * math.cos(lat_two) * hav_lon)
    distance = 2 * earth_radius * math.asin(math.sqrt(rhs))

    return distance
