from datetime import datetime
# from suncalc import get_position, get_times
from sun.position import SunAtLatLon


date = datetime(2023,3,13,12,10)
lon, lat = 28.2, -25.7

sun_angles = SunAtLatLon(lat, lon)
angles = sun_angles.at_datetime(date)
print(angles)

