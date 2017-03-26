import math

def haversine_formula(lat_one_deg, lon_one_deg, lat_two_deg, lon_two_deg):
	
	#Radius of the Earth in km
	earth_radius = 6371.008
	
	#Convert degrees to radians
	lat_one_rad = math.radians(lat_one_deg)
	lon_one_rad = math.radians(lon_one_deg)
	lat_two_rad = math.radians(lat_two_deg)
	lon_two_rad = math.radians(lon_two_deg)

	#Calculate the difference in latitude and longitude
	lat_diff_rad = lat_two_rad - lat_one_rad
	lon_diff_rad = lon_two_rad - lon_one_rad

	#Calculate the haversine of deltaLat and deltaLong
	haversine_lat = math.sin(lat_diff_rad / 2)**2
	haversine_lon = math.sin(lon_diff_rad / 2)**2

	haversine_rhs = haversine_lat + (math.cos(lat_one_rad) * math.cos(lat_two_rad) * haversine_lon)
	distance = 2 * earth_radius * math.asin(math.sqrt(haversine_rhs))

	return distance
	
	
	