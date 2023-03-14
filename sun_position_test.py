from datetime import datetime
from sun.position import SunAtLatLon


date = datetime(2023,3,13,12,10)
lat, lon = -25.8932, 28.2185

sun_angles = SunAtLatLon(lat, lon)
angles = sun_angles.at_datetime(date)
print(angles)

