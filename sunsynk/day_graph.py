from sunsynk.resource import Resource
import pandas as pd
from warnings import warn

class DayGraph(Resource):
    def __init__(self, graphs, date):
        self.cols_to_select = ['time', 'value']
        for graph in graphs:
            graph_label = graph['label'].lower()
            df = pd.DataFrame(graph['records'])[self.cols_to_select]
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

    def return_empty(self):
        data = dict()
        for key in self.cols_to_select:
            data[key] = []
        return data

    def get_solar_production(self):
        if hasattr(self, 'solar_production'):
            return self.solar_production.to_dict()
        return self.return_empty()
    
    def get_battery(self):
        if hasattr(self, 'battery'):
            return self.battery.to_dict()
        return self.return_empty()
    
    def get_state_of_charge(self):
        if hasattr(self, 'state_of_charge'):
            return self.state_of_charge.to_dict()
        return self.return_empty()
    
    def get_consumption(self):
        if hasattr(self, 'consumption'):
            return self.consumption.to_dict()
        return self.return_empty()
    
    def get_grid_usage(self):
        if hasattr(self, 'grid_usage'):
            return self.grid_usage.to_dict()
        return self.return_empty()
