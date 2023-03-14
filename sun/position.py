from datetime import datetime, timedelta
from math import sin, cos, asin, acos
import numpy as np

sind = lambda degrees: np.sin(np.deg2rad(degrees))
cosd = lambda degrees: np.cos(np.deg2rad(degrees))
asind = lambda ratio: np.rad2deg(asin(ratio))
acosd = lambda ratio: np.rad2deg(acos(ratio))

class SunAtLatLon():

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def at_datetime(self, when: datetime):
        # code implement from 
        # https://www.pveducation.org/pvcdrom/properties-of-sunlight/elevation-angle
        
        LSTM = 15*np.round((datetime.now()-datetime.utcnow()).seconds/60/60)
        N_dt = (when-datetime(when.year,1,1,0,0))
        Nd = N_dt.days + 1
        B = (360/365)*(Nd-81)
        EoT = 9.87*sind(2*B)-7.53*cosd(B)-1.5*sind(B)
        TC = 4*(self.lon - LSTM) + EoT # minutes
        LST = when + timedelta(0,TC*60)
        HRA = 15*(LST.hour + LST.minute/60 + LST.second/60/60 - 12)
        delta = 23.45*sind((360/365)*(Nd-81)) # declanation
        theta = self.lat
        alpha = asind(sind(delta)*sind(theta) + cosd(delta)*cosd(theta)*cosd(HRA)) # elevation
        az = acosd((sind(delta)*cosd(theta) - cosd(delta)*sind(theta)*cosd(HRA))/cosd(alpha)) # azimuth uncorrected
        azimuth = az if HRA <0 else 360 - az
        elevation = alpha

        return {'azimuth':azimuth, 'elevation':elevation}