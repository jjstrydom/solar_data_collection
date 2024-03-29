import pandas as pd

class Weather:

    def __init__(self, data):
        self.data = pd.DataFrame(data)
        for key in data.keys():
            if key.lower() != 'time':
                self.__create_get_function(key)

    def get_full_data_frame(self):
        return self.data

    def __create_get_function(self,item):
        def get_something():
            return(self.data[['time',item]].to_dict(orient='list'))
        setattr(self, f'get_{item}', get_something)