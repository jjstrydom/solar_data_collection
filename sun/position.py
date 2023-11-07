from datetime import datetime, timedelta
import numpy as np
import pytz, tzlocal

sind = lambda degrees: np.sin(np.deg2rad(degrees))
cosd = lambda degrees: np.cos(np.deg2rad(degrees))
arcsind = lambda ratio: np.rad2deg(np.arcsin(ratio))
arccosd = lambda ratio: np.rad2deg(np.arccos(ratio))

class SunAtLatLon():

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    @staticmethod
    def __localize_tz(when):
        if when.tzinfo is None or when.tzinfo.utcoffset(when) is None:
            local_tz = tzlocal.get_localzone()
            tz = pytz.timezone(local_tz._zone.key)
            when = tz.localize(when)
        return when, when.tzinfo.zone

    def at_datetime(self, when: datetime):
        # code implement from 
        # https://www.pveducation.org/pvcdrom/properties-of-sunlight/elevation-angle

        when, tzinfo = self.__localize_tz(when)
        tz = pytz.timezone(tzinfo)
        tz_offset_hours = when.utcoffset().seconds/60/60
        LSTM = 15*tz_offset_hours
        start_of_year = tz.localize(datetime(when.year,1,1,0,0))
        N_dt = (when-start_of_year)
        Nd = N_dt.days + 1
        B = (360/365)*(Nd-81)
        EoT = 9.87*sind(2*B)-7.53*cosd(B)-1.5*sind(B)
        TC = 4*(self.lon - LSTM) + EoT # minutes
        LST = when + timedelta(0,TC*60)
        HRA = 15*(LST.hour + LST.minute/60 + LST.second/60/60 - 12)
        delta = 23.45*sind((360/365)*(Nd-81)) # declanation
        theta = self.lat
        alpha = arcsind(sind(delta)*sind(theta) + cosd(delta)*cosd(theta)*cosd(HRA)) # elevation
        az = arccosd((sind(delta)*cosd(theta) - cosd(delta)*sind(theta)*cosd(HRA))/cosd(alpha)) # azimuth uncorrected
        azimuth = az if HRA <0 else 360 - az
        elevation = alpha

        return {'azimuth':azimuth, 'elevation':elevation}