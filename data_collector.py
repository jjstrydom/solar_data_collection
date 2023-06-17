import asyncio
import os
from dotenv import load_dotenv
from sunsynk.client import SunsynkClient
from datetime import date
import json
import pandas as pd

try:
    load_dotenv()
except:
    print("load_dotenv failed!")

def results_to_df(results, result_name):
    df = pd.DataFrame(results)
    df.columns = [result_name + '_' + c for c in df.columns]
    return df

def process_time(df, colname):
    df[colname] = df[colname].apply(str)
    return df

def process_data(df, name):
    return process_time(results_to_df(df, name), f'{name}_time').to_dict()

async def main():
    sunsynk_username = os.getenv('SUNSYNK_USERNAME')
    sunsynk_password = os.getenv('SUNSYNK_PASSWORD')

    collection_date = date(2023,3,11)

    async with SunsynkClient(sunsynk_username, sunsynk_password) as client:
        plants = await client.get_plants()
        for plant in plants: 
            measurements = await client.get_historic_graph_data(plant.id, collection_date)

    date_str = collection_date.strftime('%Y_%m_%d')

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
    with open(f"{date_str}.txt",'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)
    print('Done!')

asyncio.run(main())