import pytest
import math
from ..haversineformula import haversine_formula_deg

# Test cases (in order):
# 2115 29th Street NW CedarRapids, IA to 0, 0
# 801 Grand Ave Des Moines, IA to 305 Collins Rd NE CedarRapids, IA
# One nautical mile
# LAX to JFK
# Howe Hall, Iowa State Univ. to Atanasoff Hall, Iowa State Univ.


@pytest.mark.parametrize('lat_one_deg, lon_one_deg, lat_two_deg, lon_two_deg, expected_distance',
    [(41.997713, -91.707896, 0, 0, 10148.682020847635),
        (0, 0, 0, 1.0 / 60, 1.8532511045149815),
        (41.587507, -93.628667, 42.029066, -91.636244, 172.2768120444696),
        (33.941589, -118.40853, 40.641311, -73.778139, 3974.340850996371),
        (42.026913, -93.651913, 42.028884, -93.649569, 0.2924346837435284)])
def test_haversine_formula_deg(lat_one_deg, lon_one_deg, lat_two_deg, lon_two_deg, expected_distance):

    distance = haversine_formula_deg(lat_one_deg, lon_one_deg, lat_two_deg, lon_two_deg)
    assert expected_distance == distance
