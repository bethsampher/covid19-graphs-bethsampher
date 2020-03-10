"""module for Covid19Processing class"""
import logging
import os
import pandas as pd
from io import StringIO
import requests
import sys


class Covid19Processing():
    """Downloads and process time series data from
    https://github.com/CSSEGISandData/COVID-19/
    """

    cases_url = ('https://raw.githubusercontent.com/CSSEGISandData/'
                'COVID-19/master/csse_covid_19_data/'
                'csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

    deaths_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/'
                  'master/csse_covid_19_data/csse_covid_19_time_series/'
                  'time_series_19-covid-Deaths.csv')

    recovered_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/'
                     'master/csse_covid_19_data/csse_covid_19_time_series/'
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
        self.cases_data = cases_response.text
        deaths_response = requests.get(self.deaths_url)
        self.deaths_data = deaths_response.text
        recovered_response = requests.get(self.recovered_url)
        self.recovered_data = recovered_response.text

    def filter_data(self, data):
        # TODO write docstring
        all_data = pd.read_csv(StringIO(data))
        china = all_data.loc[all_data['Country/Region'] == 'Mainland China', '1/22/20':].sum().rename('China')
        other = all_data.loc[all_data['Country/Region'] != 'Mainland China', '1/22/20':].sum().rename('Other')
        csv_data = pd.concat([china, other], axis=1)
        csv_data['Total'] = csv_data.sum(axis=1)
        return csv_data

    def process_data(self):
        """processes the stored data into a form for CSV files"""
        self.cases_csv_data = self.filter_data(self.cases_data)
        self.deaths_csv_data = self.filter_data(self.deaths_data)
        self.recovered_csv_data = self.filter_data(self.recovered_data)

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
