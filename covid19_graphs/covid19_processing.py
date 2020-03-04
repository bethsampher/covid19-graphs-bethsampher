"""module for Covid19Processing class"""
import logging
import pandas as pd
from io import StringIO
import requests


class Covid19Processing():
    """Downloads and process time series data from
    https://github.com/CSSEGISandData/COVID-19/
    """

    data_url = ('https://raw.githubusercontent.com/CSSEGISandData/'
                'COVID-19/master/csse_covid_19_data/'
                'csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

    def __init__(self, out_dir):
        self.out_dir = out_dir
        # TODO add instance variables to store the data here
        # TODO decide on how we are going to store

    def download_from_github(self):
        """downloads the datasets from the COVID19 github repo
        into instance variable storage
        """
        response = requests.get(self.data_url)
        self.status_code = response.status_code
        self.data = response.text
        return self.status_code

    def process_data(self):
        """processes the stored data into a form for CSV files"""
        all_data = pd.read_csv(StringIO(self.data))
        china = all_data.loc[all_data['Country/Region'] == 'Mainland China', '1/22/20':].sum().rename('China')
        other = all_data.loc[all_data['Country/Region'] != 'Mainland China', '1/22/20':].sum().rename('Other')
        csv_data = pd.concat([china, other], axis=1)
        csv_data['Total'] = csv_data.sum(axis=1)
        self.csv_data = csv_data

    def create_out_dir(self, out_dir):
        """creates a new output directory out_dir

        This will be used for all files to be written"""
        # TODO decide on what happens if the directory already exists!
        logging.debug(f'create_out_dir to be written, {out_dir}')  # TODO

    def write_csv_files(self, out_dir):
        """writes CSV files to out_dir"""
        logging.debug(f'write_csv_files to be written, {out_dir}')  # TODO
