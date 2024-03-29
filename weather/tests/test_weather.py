from weather.weather import Weather
from pandas import DataFrame
import json

data = json.loads('{ \
  "time": ["2023-03-11T00:00", "2023-03-11T01:00", "2023-03-11T02:00", "2023-03-11T03:00", "2023-03-11T04:00", "2023-03-11T05:00", "2023-03-11T06:00", "2023-03-11T07:00", "2023-03-11T08:00", "2023-03-11T09:00", "2023-03-11T10:00", "2023-03-11T11:00", "2023-03-11T12:00", "2023-03-11T13:00", "2023-03-11T14:00", "2023-03-11T15:00", "2023-03-11T16:00", "2023-03-11T17:00", "2023-03-11T18:00", "2023-03-11T19:00", "2023-03-11T20:00", "2023-03-11T21:00", "2023-03-11T22:00", "2023-03-11T23:00", "2023-03-12T00:00", "2023-03-12T01:00", "2023-03-12T02:00", "2023-03-12T03:00", "2023-03-12T04:00", "2023-03-12T05:00", "2023-03-12T06:00", "2023-03-12T07:00", "2023-03-12T08:00", "2023-03-12T09:00", "2023-03-12T10:00", "2023-03-12T11:00", "2023-03-12T12:00", "2023-03-12T13:00", "2023-03-12T14:00", "2023-03-12T15:00", "2023-03-12T16:00", "2023-03-12T17:00", "2023-03-12T18:00", "2023-03-12T19:00", "2023-03-12T20:00", "2023-03-12T21:00", "2023-03-12T22:00", "2023-03-12T23:00", "2023-03-13T00:00", "2023-03-13T01:00", "2023-03-13T02:00", "2023-03-13T03:00", "2023-03-13T04:00", "2023-03-13T05:00", "2023-03-13T06:00", "2023-03-13T07:00", "2023-03-13T08:00", "2023-03-13T09:00", "2023-03-13T10:00", "2023-03-13T11:00", "2023-03-13T12:00", "2023-03-13T13:00", "2023-03-13T14:00", "2023-03-13T15:00", "2023-03-13T16:00", "2023-03-13T17:00", "2023-03-13T18:00", "2023-03-13T19:00", "2023-03-13T20:00", "2023-03-13T21:00", "2023-03-13T22:00", "2023-03-13T23:00"], \
  "temperature_2m": [19.2, 18.8, 17.6, 17.1, 16.4, 16.0, 15.5, 16.1, 19.6, 22.0, 24.0, 25.5, 27.0, 28.3, 28.4, 28.5, 28.2, 27.7, 26.2, 24.2, 22.8, 22.7, 21.7, 20.1, 19.1, 18.4, 18.3, 18.0, 17.6, 17.4, 17.3, 17.6, 19.1, 21.3, 23.5, 25.3, 26.4, 27.0, 27.4, 26.9, 26.7, 25.6, 24.3, 22.3, 19.6, 18.5, 17.2, 16.4, 15.7, 15.1, 15.0, 14.7, 14.6, 14.3, 13.8, 14.4, 16.9, 19.0, 21.1, 23.1, 24.9, 26.2, 26.3, 26.4, 26.3, 25.6, 24.2, 21.2, 18.8, 17.6, 16.8, 16.5], \
  "relativehumidity_2m": [83, 82, 87, 87, 89, 90, 92, 91, 78, 65, 59, 56, 50, 41, 38, 37, 37, 38, 45, 53, 59, 58, 61, 69, 72, 72, 68, 70, 71, 71, 71, 75, 75, 69, 61, 54, 48, 46, 42, 43, 42, 45, 48, 54, 68, 73, 76, 79, 83, 86, 87, 88, 87, 87, 89, 87, 74, 64, 58, 52, 46, 40, 36, 34, 34, 34, 37, 46, 63, 66, 68, 68], "precipitation_probability": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 6, 13, 19, 13, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
  "precipitation": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \
  "surface_pressure": [859.4, 859.0, 859.6, 858.9, 858.8, 858.9, 858.7, 859.3, 861.0, 861.9, 862.1, 862.0, 861.7, 861.0, 860.8, 860.1, 859.9, 859.8, 859.2, 858.8, 859.7, 860.0, 859.9, 859.2, 859.0, 858.7, 859.0, 858.3, 858.4, 858.7, 859.4, 860.3, 861.9, 863.2, 863.7, 863.7, 863.7, 863.7, 863.1, 862.6, 862.3, 862.4, 861.9, 862.1, 862.6, 863.3, 863.6, 863.0, 862.5, 861.7, 862.0, 861.5, 861.4, 861.5, 861.7, 862.5, 863.9, 864.7, 865.1, 865.1, 864.9, 864.4, 864.0, 863.3, 862.8, 862.5, 862.0, 861.5, 861.7, 861.5, 861.5, 861.1], \
  "cloudcover": [57, 3, 0, 0, 0, 0, 0, 0, 0, 3, 4, 30, 25, 6, 27, 25, 14, 42, 52, 75, 77, 81, 68, 71, 35, 2, 5, 58, 52, 48, 40, 37, 48, 53, 49, 75, 47, 77, 76, 78, 77, 100, 100, 67, 37, 26, 12, 18, 25, 27, 41, 41, 34, 10, 23, 37, 31, 28, 29, 24, 26, 52, 71, 59, 40, 21, 24, 26, 25, 6, 0, 0], "cloudcover_low": [36, 3, 0, 0, 0, 0, 0, 0, 0, 0, 4, 30, 25, 6, 27, 25, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 27, 25, 37, 39, 49, 63, 67, 57, 49, 59, 52, 37, 26, 12, 18, 25, 27, 41, 41, 34, 10, 23, 37, 31, 28, 29, 24, 26, 25, 22, 18, 22, 21, 24, 26, 25, 6, 0, 0], \
  "cloudcover_mid": [47, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 13, 42, 52, 72, 77, 81, 68, 71, 35, 2, 5, 58, 52, 48, 40, 37, 36, 39, 37, 58, 12, 55, 68, 42, 49, 27, 59, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 57, 47, 30, 0, 0, 0, 0, 0, 0, 0], "cloudcover_high": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 18, 2, 3, 0, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
  "windspeed_10m": [7.7, 8.2, 6.1, 5.4, 4.9, 4.2, 3.8, 3.2, 3.9, 7.2, 9.2, 9.8, 8.7, 6.5, 5.0, 5.6, 5.4, 4.7, 4.6, 2.8, 3.2, 2.6, 3.1, 4.7, 6.6, 8.4, 10.4, 8.0, 7.2, 8.9, 12.2, 19.4, 21.9, 22.7, 19.5, 18.1, 16.2, 16.0, 13.3, 12.0, 10.8, 13.2, 12.1, 13.2, 14.0, 18.4, 19.2, 17.9, 16.8, 15.5, 13.9, 14.4, 13.4, 12.6, 12.1, 13.6, 17.8, 17.2, 15.4, 13.4, 11.6, 10.0, 11.8, 11.8, 12.0, 12.1, 9.2, 6.5, 5.5, 6.3, 6.3, 8.1], "winddirection_10m": [37, 41, 50, 48, 54, 59, 73, 90, 22, 342, 315, 298, 294, 273, 270, 230, 233, 279, 288, 230, 243, 236, 201, 180, 171, 160, 166, 153, 143, 137, 137, 121, 107, 100, 93, 85, 93, 99, 90, 99, 105, 101, 127, 112, 108, 96, 98, 100, 105, 108, 115, 112, 110, 110, 113, 112, 111, 106, 101, 96, 95, 105, 102, 110, 111, 113, 111, 109, 122, 121, 121, 111], \
  "soil_temperature_0cm": [18.0, 17.4, 16.2, 15.5, 15.0, 14.5, 14.0, 16.9, 23.3, 26.6, 29.4, 32.0, 33.8, 34.8, 33.6, 31.9, 29.8, 27.5, 23.5, 21.2, 19.8, 19.8, 19.1, 18.1, 17.3, 16.7, 16.7, 16.6, 16.1, 15.8, 16.0, 18.0, 21.7, 25.2, 28.7, 31.2, 32.9, 32.1, 31.9, 29.9, 28.2, 25.0, 22.6, 20.5, 18.1, 17.5, 16.3, 15.6, 15.0, 14.3, 14.5, 14.2, 13.9, 13.3, 12.8, 15.4, 20.0, 23.9, 27.7, 31.1, 33.6, 33.9, 31.4, 30.5, 28.6, 25.6, 21.6, 17.9, 16.5, 15.6, 15.0, 14.7]\
  }'
)
                  
def test_init():
    w = Weather(data)
    assert type(w.data) == DataFrame
    for c in w.data.columns:
        assert c in data.keys()
    for k in data.keys():
        assert k in w.data.columns
        assert len(data[k]) == w.data.shape[0]
    assert len(data.keys()) == w.data.shape[1]

def test_func_generator():
    w = Weather(data)
    functions_under_test = [f[4:] for f in dir(w) if f.startswith('get_')]
    for f in functions_under_test:
        assert f in data.keys()

def test_generated_func_outputs():
    w = Weather(data)
    functions_under_test = [f for f in dir(w) if f.startswith('get_')]
    for f in functions_under_test:
        func = getattr(w,f)
        output = func()
        for k, v in output.items():
            assert k in data.keys()
            assert data[k] == v


