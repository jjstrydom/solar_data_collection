import asyncio
import os
from dotenv import load_dotenv
from sunsynk.client import SunsynkClient
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

def process_data(df:pd.DataFrame, name:str) -> dict:
    return process_time(results_to_df(df, name), f'{name}_time').to_dict()

def get_all_dates_between(start_date:date, end_date:date) -> list[date]:
    days_difference = (end_date - start_date).days
    return [start_date + timedelta(days=d) for d in range(days_difference)]

def get_all_data_files():
    return glob.glob('data/*_*_*.txt')

def get_all_data_file_dates() -> list[date]:
    data_files = get_all_data_files()
    return [datetime.strptime(d[5:-4], '%Y_%m_%d').date() for d in data_files]

def get_dates_to_download(starting_from:date) -> list[date]:
    list_of_dates = get_all_dates_between(starting_from, datetime.utcnow().date())
    list_of_data_dates = get_all_data_file_dates()
    dates_to_download = list(set(list_of_dates) - set(list_of_data_dates))
    return dates_to_download

async def main(collection_date:date, sunsynk_username:str, sunsynk_password:str) -> None:
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
    with open(f"data/{date_str}.txt",'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)
    print('Done!')

if __name__ == "__main__":
    sunsynk_username = os.getenv('SUNSYNK_USERNAME')
    sunsynk_password = os.getenv('SUNSYNK_PASSWORD')
    # dates_to_download = get_dates_to_download(starting_from=date(2022,9,21))
    dates_to_download = get_dates_to_download(starting_from=date(2023,6,10))
    for date_to_download in dates_to_download:
        asyncio.run(main(date_to_download, sunsynk_username, sunsynk_password))