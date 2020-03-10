""" unit tests for covid19_processing """

from mock import patch
import os
import pandas as pd
import pytest

from covid19_graphs.covid19_processing import Covid19Processing


def test_out_dir():
    processing = Covid19Processing('test_dir')
    assert processing.out_dir == 'test_dir'

def test_existing_out_dir():
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        with pytest.raises(SystemExit):
            processing = Covid19Processing('test_dir')

def test_download_from_github():
    processing = Covid19Processing('test_dir')
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = 'Test data'
        mock_get.return_value.status_code = 200
        processing.download_from_github()
        assert processing.cases_data == 'Test data'
        assert processing.deaths_data == 'Test data'
        assert processing.recovered_data == 'Test data'

def test_failed_download_from_github():
    processing = Covid19Processing('test_dir')
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 0
        with pytest.raises(SystemExit):
            processing.download_from_github()

def test_filter_data():
    processing = Covid19Processing('test_dir')
    test_data = 'State,Country/Region,1/22/20,3/3/20\nAnhui,Mainland China,1,990\nBeijing,Mainland China,14,414\n,UK,0,51'
    csv_data = processing.filter_data(test_data)
    expected_data = [[15, 0, 15], [1404, 51, 1455]]
    expected_csv_data = pd.DataFrame(expected_data, columns=['China', 'Other', 'Total'], index=['1/22/20', '3/3/20'])
    assert expected_csv_data.equals(csv_data)

def test_process_data():
    processing = Covid19Processing('test_dir')
    with patch ('covid19_graphs.covid19_processing.Covid19Processing.filter_data') as mock_filter:
        mock_filter.return_value = 'Test CSV data'
        processing.cases_data = 'Test data'
        processing.deaths_data = 'Test data'
        processing.recovered_data = 'Test data'
        processing.process_data()
        assert processing.cases_csv_data == 'Test CSV data'
        assert processing.deaths_csv_data == 'Test CSV data'
        assert processing.recovered_csv_data == 'Test CSV data'

def test_create_out_dir():
    processing = Covid19Processing('test_dir')
    with patch('os.mkdir') as mock_mkdir:
        processing.create_out_dir()
        mock_mkdir.assert_called_once_with('test_dir')

def test_write_csv_files():
    processing = Covid19Processing('test_dir')
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        processing.cases_csv_data = pd.DataFrame(['test data'])
        processing.deaths_csv_data = pd.DataFrame(['test data'])
        processing.recovered_csv_data = pd.DataFrame(['test data'])
        processing.write_csv_files()
        mock_to_csv.assert_any_call('test_dir/cases.csv')
        mock_to_csv.assert_any_call('test_dir/deaths.csv')
        mock_to_csv.assert_any_call('test_dir/recovered.csv')
