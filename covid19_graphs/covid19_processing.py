"""module for Covid19Processing class"""
import os
import sys
from io import StringIO
import pandas as pd
import pycountry_convert as pc
import requests


class Covid19Processing():
    """Downloads and process time series data from
    https://github.com/CSSEGISandData/COVID-19/
    """

    cases_url = ('https://raw.githubusercontent.com/CSSEGISandData/'
                 'COVID-19/master/csse_covid_19_data/'
                 'csse_covid_19_time_series/'
                 'time_series_19-covid-Confirmed.csv')

    deaths_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/'
                  'master/csse_covid_19_data/csse_covid_19_time_series/'
                  'time_series_19-covid-Deaths.csv')

    recovered_url = ('https://raw.githubusercontent.com/'
                     'CSSEGISandData/COVID-19/master/'
                     'csse_covid_19_data/csse_covid_19_time_series/'
                     'time_series_19-covid-Recovered.csv')

    def __init__(self, out_dir):
        if os.path.exists(out_dir):
            sys.exit('Error! Specified output directory already exists')
        else:
            self.out_dir = out_dir

    def download_from_github(self):
        """downloads the datasets from the COVID19 github repo
        into instance variable storage
        """
        cases_response = requests.get(self.cases_url)
        deaths_response = requests.get(self.deaths_url)
        recovered_response = requests.get(self.recovered_url)
        for response in (cases_response, deaths_response, recovered_response):
            if response.status_code != 200:
                sys.exit('Error! Data could not be retrieved')
        self.cases_data = cases_response.text
        self.deaths_data = deaths_response.text
        self.recovered_data = recovered_response.text

    def get_continent(self, row):
        # TODO write docstring
        if row['Country/Region'] in ('China', 'United Kingdom', 'Cruise Ship'):
            return ''
        try:
            if row['Country/Region'] == 'US':
                country_code = 'US'
            else:
                country_code = pc.country_name_to_country_alpha2(
                    row['Country/Region'])
            continent = pc.country_alpha2_to_continent_code(country_code)
            return continent
        except KeyError:
            return 'Unrecognised'

    def filter_data(self, data):
        # TODO write docstring
        all_data = pd.read_csv(StringIO(data))
        all_data.insert(2, 'Continent', all_data.apply(
            self.get_continent, axis=1))
        china = all_data.loc[all_data['Country/Region'] == 'China',
                             '1/22/20':].sum().rename('China')
        diamond_princess = all_data.loc[
            all_data['Country/Region'] == 'Cruise Ship',
            '1/22/20':].sum().rename('Diamond Princess')
        uk = all_data.loc[all_data['Country/Region'] == 'United Kingdom',
                          '1/22/20':].sum().rename('UK')
        asia = all_data.loc[all_data['Continent'] == 'AS',
                            '1/22/20':].sum().rename('Asia')
        europe = all_data.loc[all_data['Continent'] == 'EU',
                              '1/22/20':].sum().rename('Europe')
        north_america = all_data.loc[all_data['Continent'] == 'NA',
                                     '1/22/20':].sum().rename('North America')
        south_america = all_data.loc[all_data['Continent'] == 'SA',
                                     '1/22/20':].sum().rename('South America')
        africa = all_data.loc[all_data['Continent'] == 'AF',
                              '1/22/20':].sum().rename('Africa')
        oceania = all_data.loc[all_data['Continent'] == 'OC',
                               '1/22/20':].sum().rename('Oceania')
        unrecognised = all_data.loc[all_data['Continent'] == 'Unrecognised',
                                    '1/22/20':].sum().rename('Unrecognised')
        csv_data = pd.concat([china, diamond_princess, uk, asia, europe,
                              north_america, south_america, africa, oceania,
                              unrecognised], axis=1)
        csv_data['Total'] = csv_data.sum(axis=1)
        return csv_data

    def process_data(self):
        """processes the stored data into a form for CSV files"""
        try:
            self.cases_csv_data = self.filter_data(self.cases_data)
            self.deaths_csv_data = self.filter_data(self.deaths_data)
            self.recovered_csv_data = self.filter_data(self.recovered_data)
        except Exception:
            sys.exit('Error! Data could not be processed')

    def create_out_dir(self):
        """creates a new output directory out_dir

        This will be used for all files to be written"""
        os.mkdir(self.out_dir)

    def write_csv_files(self):
        """writes CSV files to out_dir"""
        cases_path = self.out_dir + '/cases.csv'
        self.cases_csv_data.to_csv(cases_path)
        deaths_path = self.out_dir + '/deaths.csv'
        self.deaths_csv_data.to_csv(deaths_path)
        recovered_path = self.out_dir + '/recovered.csv'
        self.recovered_csv_data.to_csv(recovered_path)
