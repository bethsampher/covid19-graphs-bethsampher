"""module for Covid19Processing class"""
from datetime import datetime as dt
import os
import sys
from io import StringIO
import pandas as pd
import pycountry_convert as pc
import requests


class Covid19Processing():
    """Downloads and processes time series data from
    https://github.com/CSSEGISandData/COVID-19/

    Produces CSVs and graphs based on numbers of
    reported coronavirus cases, deaths and recoveries
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
        # To be set:
        self.cases_data = None
        self.deaths_data = None
        self.recovered_data = None
        self.cases_csv_data = None
        self.deaths_csv_data = None
        self.recovered_csv_data = None
        self.cases_axes = None
        self.deaths_axes = None
        self.recovered_axes = None

    def download_from_github(self):
        """Downloads the datasets from the COVID19 GitHub repo
        into instance variable storage

        Exits with error message if data is not downloaded
        successfully
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

    @staticmethod
    def get_continent(row):
        """Returns continent of country in dataframe row

        Excludes China and UK from the continents as they
        are reported separately and returns 'Unrecognised'
        for invalid country name
        """
        if row['Country/Region'] in ('China', 'United Kingdom'):
            return ''
        if row['Country/Region'] == 'US':
            country_code = 'US'
        else:
            try:
                country_code = pc.country_name_to_country_alpha2(
                    row['Country/Region'])
            except KeyError:
                return 'Unrecognised'
        continent = pc.country_alpha2_to_continent_code(country_code)
        return continent

    @staticmethod
    def filter_data(data):
        """Returns a dataframe containing data for CSV
        filtered from GitHub data

        Rows are dates and there's a column for each country/
        continent below, unrecognised countries and the total"""
        all_data = pd.read_csv(StringIO(data))
        all_data.insert(2, 'Continent', all_data.apply(
            Covid19Processing.get_continent, axis=1))
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
        filtered_data = pd.concat([china, diamond_princess, uk, asia, europe,
                                   north_america, south_america, africa,
                                   oceania, unrecognised], axis=1)
        filtered_data['Total'] = filtered_data.sum(axis=1)
        return filtered_data

    def store_data_for_csv(self):
        """Stores filtered data for output CSV in
        instance variables

        Exits with error message if data can't be
        processed properly"""
        try:
            self.cases_csv_data = self.filter_data(self.cases_data)
            self.deaths_csv_data = self.filter_data(self.deaths_data)
            self.recovered_csv_data = self.filter_data(self.recovered_data)
        except Exception:
            sys.exit('Error! Data could not be processed')

    def create_out_dir(self):
        """Creates a new output directory out_dir

        This will be used for all files to be written"""
        os.mkdir(self.out_dir)

    def write_csv_files(self):
        """Writes CSV files to out_dir"""
        cases_path = self.out_dir + '/cases.csv'
        self.cases_csv_data.to_csv(cases_path)
        deaths_path = self.out_dir + '/deaths.csv'
        self.deaths_csv_data.to_csv(deaths_path)
        recovered_path = self.out_dir + '/recovered.csv'
        self.recovered_csv_data.to_csv(recovered_path)

    def remove_unrecognised_column(self):
        """Removes unrecognised data so it isn't
        on the graphs"""
        self.cases_csv_data = self.cases_csv_data.drop(
            columns=['Unrecognised'])
        self.deaths_csv_data = self.deaths_csv_data.drop(
            columns=['Unrecognised'])
        self.recovered_csv_data = self.recovered_csv_data.drop(
            columns=['Unrecognised'])

    @staticmethod
    def set_labels(axes):
        """Sets axes labels for graphs"""
        axes.set_xlabel('Date')
        axes.set_ylabel('Reported number')

    def make_axes(self):
        """Creates graphs from cases, deaths and
        recovered data"""
        self.cases_axes = self.cases_csv_data.plot(
            legend=True, title='COVID-19 cases (data from John Hopkins CSSE)',
            grid=True)
        self.set_labels(self.cases_axes)
        self.deaths_axes = self.deaths_csv_data.plot(
            legend=True, title='COVID-19 deaths (data from John Hopkins CSSE)',
            grid=True)
        self.set_labels(self.deaths_axes)
        self.recovered_axes = self.recovered_csv_data.plot(
            legend=True,
            title='COVID-19 recoveries (data from John Hopkins CSSE)',
            grid=True)
        self.set_labels(self.recovered_axes)

    def create_graph_dir(self):
        """Creates a graph dir in our_dir

        For graphs to be put in"""
        os.mkdir(self.out_dir + '/graphs')

    def write_png_files(self):
        """Saves graphs to png files, uses date in path"""
        date = dt.today().strftime('%Y-%m-%d')
        cases_path = f'{self.out_dir}/graphs/{date}-cases.png'
        self.cases_axes.get_figure().savefig(cases_path)
        deaths_path = f'{self.out_dir}/graphs/{date}-deaths.png'
        self.deaths_axes.get_figure().savefig(deaths_path)
        recovered_path = f'{self.out_dir}/graphs/{date}-recovered.png'
        self.recovered_axes.get_figure().savefig(recovered_path)
