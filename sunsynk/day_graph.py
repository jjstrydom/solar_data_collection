from sunsynk.resource import Resource
import pandas as pd
from warnings import warn

class DayGraph(Resource):
    def __init__(self, graphs, date):
        for graph in graphs:
            graph_label = graph['label'].lower()
            df = pd.DataFrame(graph['records'])[['time', 'value']]
            df['time'] = str(date) + ' ' + df['time'].astype(str)
            df['time'] = pd.to_datetime(df['time'])
            if graph_label == 'pv':
                self.solar_production = df
            elif graph_label == 'battery':
                self.battery = df
            elif graph_label == 'soc':
                self.state_of_charge = df
            elif graph_label == 'load':
                self.consumption = df
            elif graph_label == 'grid':
                self.grid_usage = df
            else:
                warn(f'Found unknown graph {graph_label}')

    def get_solar_production(self):
        return self.solar_production.to_dict()
    
    def get_battery(self):
        return self.battery.to_dict()
    
    def get_state_of_charge(self):
        return self.state_of_charge.to_dict()
    
    def get_consumption(self):
        return self.consumption.to_dict()
    
    def get_grid_usage(self):
        return self.grid_usage.to_dict()
    
