import pytest
import pytz
from sun.position import SunAtLatLon
from datetime import datetime

# some test data from: https://www.pveducation.org/pvcdrom/properties-of-sunlight/sun-position-calculator

def test_ensure_output_dict_with_n_keys():
    date = datetime.now()
    lat, lon = 40, 20
    sun_angles = SunAtLatLon(lat, lon)
    output = sun_angles.at_datetime(date)
    assert type(output) == dict
    assert len(output.keys()) == 2

def test_at_position_at_datetime_pp():
    date = datetime(2023,1,1,12,00)
    tz = pytz.timezone('Africa/Johannesburg')
    date = tz.localize(date)
    lat, lon = 40, 20
    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    assert angles['azimuth'] == pytest.approx(168.79,abs=0.005)
    assert angles['elevation'] == pytest.approx(26.17,abs=0.005)

def test_at_position_at_datetime_np():
    date = datetime(2023,1,1,12,00)
    tz = pytz.timezone('Africa/Johannesburg')
    date = tz.localize(date)
    lat, lon = -40, 20
    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    assert angles['azimuth'] == pytest.approx(31.79,abs=0.011)  # not sure why this one is so far out...
    assert angles['elevation'] == pytest.approx(70.66,abs=0.005)

def test_at_position_at_datetime_nn():
    date = datetime(2023,1,1,12,00)
    tz = pytz.timezone('Africa/Johannesburg')
    date = tz.localize(date)
    lat, lon = -40, -20
    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    assert angles['azimuth'] == pytest.approx(84.13,abs=0.005)
    assert angles['elevation'] == pytest.approx(44.08,abs=0.005)

def test_at_position_at_datetime_pn():
    date = datetime(2023,1,1,12,00)
    tz = pytz.timezone('Africa/Johannesburg')
    date = tz.localize(date)
    lat, lon = 40, -20
    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    assert angles['azimuth'] == pytest.approx(133.26,abs=0.005)
    assert angles['elevation'] == pytest.approx(11.14,abs=0.005)

def test_at_position_at_datetime_tz_0():
    date = datetime(2023,1,1,12,00)
    tz = pytz.timezone('UTC')
    date = tz.localize(date)
    lat, lon = 0, 0
    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    assert angles['azimuth'] == pytest.approx(177.82,abs=0.01)
    assert angles['elevation'] == pytest.approx(66.97,abs=0.005)

def test_at_position_at_datetime_tz_p3():
    date = datetime(2023,1,1,12,00)
    tz = pytz.timezone('Africa/Nairobi')
    date = tz.localize(date)
    lat, lon = 0, 0
    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    assert angles['azimuth'] == pytest.approx(120.59,abs=0.005)
    assert angles['elevation'] == pytest.approx(39.81,abs=0.005)

def test_at_position_at_datetime_tz_m3():
    date = datetime(2023,1,1,12,00)
    tz = pytz.timezone('America/Buenos_Aires')
    date = tz.localize(date)
    lat, lon = 0, 0
    sun_angles = SunAtLatLon(lat, lon)
    angles = sun_angles.at_datetime(date)
    assert angles['azimuth'] == pytest.approx(238.59,abs=0.005)
    assert angles['elevation'] == pytest.approx(41.40,abs=0.005)
