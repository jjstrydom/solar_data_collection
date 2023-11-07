from datetime import datetime
from sun.position import SunAtLatLon
import pytz

def main():
    date = datetime(2023,1,1,12,00)
    print(date.tzinfo)

    lat, lon = 40, -20

    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    print(angles)

if __name__ == '__main__':
    main()
