import asyncio
import os
from dotenv import load_dotenv
from sunsynk.client import SunsynkClient
from weather.client import WeatherClient
from datetime import date, timedelta, datetime
import json
import pandas as pd
import glob

try:
    load_dotenv()
except:
    print("load_dotenv failed!")

def results_to_df(results:dict, result_name:str) -> pd.DataFrame:
    df = pd.DataFrame(results)
    df.columns = [result_name + '_' + c for c in df.columns]
    return df

def process_time(df:pd.DataFrame, colname:str) -> pd.DataFrame:
    df[colname] = df[colname].apply(str)
    return df

def process_data(data:dict, name:str) -> dict:
    if name in data.keys():
        data['value'] = data.pop(name)
    return process_time(results_to_df(data, name), f'{name}_time').to_dict()

def get_all_dates_between(start_date:date, end_date:date) -> list[date]:
    days_difference = (end_date - start_date).days
    return [start_date + timedelta(days=d) for d in range(days_difference)]

def get_all_data_files(suffix:str = None):
    if suffix is None:
        glob.glob(f'data/*_*_*.txt')
    else:
        return glob.glob(f'data/*_*_*_{suffix}.txt')

def get_all_data_file_dates(suffix:str) -> list[date]:
    data_files = get_all_data_files(suffix)
    return [datetime.strptime(d[5:-4-len(suffix)-1], '%Y_%m_%d').date() for d in data_files]

def get_dates_to_download(starting_from:date, suffix) -> list[date]:
    list_of_dates = get_all_dates_between(starting_from, datetime.utcnow().date())
    list_of_data_dates = get_all_data_file_dates(suffix)
    dates_to_download = list(set(list_of_dates) - set(list_of_data_dates))
    return dates_to_download

def store_data(data, date_str, suffix):
    with open(f"data/{date_str}_{suffix}.txt",'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

async def main_solar(collection_date:date, sunsynk_username:str, sunsynk_password:str, suffix:str) -> None:
    date_str = collection_date.strftime('%Y_%m_%d')

    async with SunsynkClient(sunsynk_username, sunsynk_password) as client:
        plants = await client.get_plants()
        for plant in plants: 
            measurements = await client.get_historic_graph_data(plant.id, collection_date)
    
    battery = measurements.get_battery()
    consumption = measurements.get_consumption()
    grid_usage = measurements.get_grid_usage()
    solar_production = measurements.get_solar_production()
    state_of_charge = measurements.get_state_of_charge()
    data = {
        'battery': process_data(battery, 'battery'),
        'consumption' : process_data(consumption, 'consumption'),
        'grid_usage' : process_data(grid_usage, 'grid_usage'),
        'solar_production' : process_data(solar_production, 'solar_production'),
        'state_of_charge' : process_data(state_of_charge, 'state_of_charge'),
    }
    store_data(data, date_str, suffix)
    print(f'Solar for {date_str}: Done!')

async def main_weather(collection_date:date, suffix:str):
    date_str = collection_date.strftime('%Y_%m_%d')

    async with WeatherClient() as client:
        weather = await client.get_data(collection_date, collection_date)
    
    temperature_2m = weather.get_temperature_2m()
    relativehumidity_2m = weather.get_relativehumidity_2m()
    precipitation_probability = weather.get_precipitation_probability()
    precipitation = weather.get_precipitation()
    surface_pressure = weather.get_surface_pressure()
    cloudcover = weather.get_cloudcover()
    cloudcover_low = weather.get_cloudcover_low()
    cloudcover_mid = weather.get_cloudcover_mid()
    cloudcover_high = weather.get_cloudcover_high()
    windspeed_10m = weather.get_windspeed_10m()
    winddirection_10m = weather.get_winddirection_10m()
    soil_temperature_0cm = weather.get_soil_temperature_0cm()
    data = {
        'temperature_2m' : process_data(temperature_2m, 'temperature_2m'),
        'relativehumidity_2m' : process_data(relativehumidity_2m, 'relativehumidity_2m'),
        'precipitation_probability' : process_data(precipitation_probability, 'precipitation_probability'),
        'precipitation' : process_data(precipitation, 'precipitation'),
        'surface_pressure' : process_data(surface_pressure, 'surface_pressure'),
        'cloudcover' : process_data(cloudcover, 'cloudcover'),
        'cloudcover_low' : process_data(cloudcover_low, 'cloudcover_low'),
        'cloudcover_mid' : process_data(cloudcover_mid, 'cloudcover_mid'),
        'cloudcover_high' : process_data(cloudcover_high, 'cloudcover_high'),
        'windspeed_10m' : process_data(windspeed_10m, 'windspeed_10m'),
        'winddirection_10m' : process_data(winddirection_10m, 'winddirection_10m'),
        'soil_temperature_0cm' : process_data(soil_temperature_0cm, 'soil_temperature_0cm'),
    }
    store_data(data, date_str, suffix)
    print(f'Weather for {date_str}: Done!')

if __name__ == "__main__":
    starting_date = date(2022,9,21)
    # starting_date = date(2023,6,12)
    solar_suffix = 'solar'
    weather_suffix = 'weather'
    try:
        os.mkdir('data')
    except FileExistsError:
        print('data direcory exists, no need to create')
    sunsynk_username = os.getenv('SUNSYNK_USERNAME')
    sunsynk_password = os.getenv('SUNSYNK_PASSWORD')
    # solar_dates_to_download = get_dates_to_download(starting_from=date(2022,9,21))
    solar_dates_to_download = get_dates_to_download(starting_from=starting_date, suffix=solar_suffix)
    weather_dates_to_download = get_dates_to_download(starting_from=starting_date, suffix=weather_suffix)
    for date_to_download in solar_dates_to_download:
        asyncio.run(main_solar(date_to_download, sunsynk_username, sunsynk_password, solar_suffix))
    for date_to_download in weather_dates_to_download:
        asyncio.run(main_weather(date_to_download, weather_suffix))