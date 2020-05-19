import pandas as pd
import matplotlib.pyplot as plt

class CoronaStats:

    def __init__(self, csv_url):    
        self.population = {'germany': 83019213,  'overall': 7418000000}
        self.csv_url = csv_url
        self.get_clean_data()

    def get_clean_data(self):
        df = pd.read_csv(self.csv_url)
        df = df.drop(columns=['Lat', 'Long'])

        df_group = df.groupby(['Country/Region'])

        germany = df_group.get_group('Germany')

        overall = df.agg(['sum'])
        germany = germany.agg(['sum'])

        self.overall = self.clean_Data(overall, 'overall', ['Country/Region'])
        self.germany = self.clean_Data(germany, 'germany', ['Province/State', 'Country/Region'])

    def clean_Data(self, data_frame, country, drop_columns):
        cleaned_data_frame = data_frame.drop(columns = drop_columns)
        cleaned_data_frame = cleaned_data_frame.T
        
        cleaned_data_frame['related'] = (100/self.population[country]) * cleaned_data_frame['sum']

        return cleaned_data_frame

    def plot_diagram_related(self, filename='confirmed_compared_related'):
        diagram_file = self.plot_diagram('related', 
                                         'Date', 
                                         'Confirmed infections related to population (%)', 
                                         'Confirmed COVID-19 - Related to population', 
                                         filename)
        
        return diagram_file

    def plot_diagram(self, yvalue, xlabel, ylabel, title, filename):
        plt.figure(figsize=(8,5))
        ax = plt.gca()

        self.overall.plot(kind='line', y=yvalue, ax=ax, label="Overall", color='black')
        self.germany.plot(kind='line', y=yvalue, ax=ax, label="Germany", color='red')

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.savefig(filename + '.png', dpi=300)
        
        return filename + '.png' 
    
    def get_actual_infected(self):
        germany_changed = self.germany.tail(2)['sum'][1] - self.germany.tail(2)['sum'][0]
        overall_changed = self.overall.tail(2)['sum'][1] - self.overall.tail(2)['sum'][0]

        germany = '+' if germany_changed > 0 else '-'
        overall = '+' if overall_changed > 0 else '-'

        germany += str(germany_changed)
        overall += str(overall_changed)

        return {
            'germany': [
                self.germany.tail(1)['sum'][0],
                germany
            ],
            'overall': [
                self.overall.tail(1)['sum'][0],
                overall
            ]
        }

    def get_latest_update_date(self):
        [month, day, year] = self.overall.index[-1].split('/', 3)
        date = '.'.join([day, month, '20'+year])
        return date
    
    def get_weekly_growth(self):
        frame = self.germany.tail(7)
        actual = frame['sum'][-1]
        days_before = frame['sum'][0]
        growth_rate = (actual*100/days_before) - 100

        return growth_rate
