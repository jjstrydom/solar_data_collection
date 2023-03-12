from sunsynk.resource import Resource
import pandas as pd
from warnings import warn

class DayGraph(Resource):
    def __init__(self, graphs, date):
        for graph in graphs:
            graph_label = graph['label'].lower()
            df = pd.DataFrame(graph['records'])[['time', 'value']]
            df['time'] = str(date) + ' ' + df['time'].astype(str)
            pd.to_datetime(df['time'])
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
        return self.solar_production
    
    def get_battery(self):
        return self.battery
    
    def get_state_of_charge(self):
        return self.state_of_charge
    
    def get_consumption(self):
        return self.consumption
    
    def get_grid_usage(self):
        return self.grid_usage
    
