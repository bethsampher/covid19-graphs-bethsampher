""" unit tests for covid19_processing """

from mock import patch
import pandas as pd
import pytest

from covid19_graphs.covid19_processing import Covid19Processing


def test_out_dir():
    """Tests out_dir is set"""
    processing = Covid19Processing('test_dir')
    assert processing.out_dir == 'test_dir'


def test_existing_out_dir():
    """Tests script exits if out_dir already exists"""
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        with pytest.raises(SystemExit):
            Covid19Processing('test_dir')


def test_download_from_github():
    """Tests download_from_github method"""
    processing = Covid19Processing('test_dir')
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = 'Test data'
        mock_get.return_value.status_code = 200
        processing.download_from_github()
        assert processing.cases_data == 'Test data'
        assert processing.deaths_data == 'Test data'
        assert processing.recovered_data == 'Test data'


def test_download_from_github_fail():
    """Tests script exits if download unsuccessful
    (success code not 200)"""
    processing = Covid19Processing('test_dir')
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 0
        with pytest.raises(SystemExit):
            processing.download_from_github()


def test_get_continent():
    """Tests get_continent"""
    assert Covid19Processing.get_continent(pd.Series(
        {'Country/Region': 'China'})) == ''
    assert Covid19Processing.get_continent(pd.Series(
        {'Country/Region': 'US'})) == 'NA'
    assert Covid19Processing.get_continent(pd.Series(
        {'Country/Region': 'Italy'})) == 'EU'
    assert Covid19Processing.get_continent(pd.Series(
        {'Country/Region': 'Unknown'})) == 'Unrecognised'


def test_filter_data():
    """Tests filter_data"""
    test_data = ('State,Country/Region,1/22/20,3/3/20\n'
                 'Anhui,China,1,990\nBeijing,China,14,414\n'
                 ',United Kingdom,0,51\n,Italy,0,2502\n'
                 ',Germany,0,196\n,Unknown,10,20')
    filtered_data = Covid19Processing.filter_data(test_data)
    expected_data = [[15, 0, 0, 0, 0, 0, 0, 0, 0, 10, 25],
                     [1404, 0, 51, 0, 2698, 0, 0, 0, 0, 20, 4173]]
    expected_cols = ['China', 'Diamond Princess', 'UK', 'Asia',
                     'Europe', 'North America', 'South America',
                     'Africa', 'Oceania', 'Unrecognised', 'Total']
    expected_filtered_data = pd.DataFrame(expected_data, columns=expected_cols,
                                          index=['1/22/20', '3/3/20'])
    assert expected_filtered_data.equals(filtered_data)


def test_store_data_for_csv():
    """Tests store_data_for_csv"""
    processing = Covid19Processing('test_dir')
    with patch('covid19_graphs.covid19_processing.'
               'Covid19Processing.filter_data') as mock_filter:
        mock_filter.return_value = 'Test CSV data'
        processing.cases_data = 'Test data'
        processing.deaths_data = 'Test data'
        processing.recovered_data = 'Test data'
        processing.store_data_for_csv()
        assert processing.cases_csv_data == 'Test CSV data'
        assert processing.deaths_csv_data == 'Test CSV data'
        assert processing.recovered_csv_data == 'Test CSV data'


def test_store_data_for_csv_fail():
    """Tests script exits if filter_data fails"""
    processing = Covid19Processing('test_dir')
    with patch('covid19_graphs.covid19_processing.'
               'Covid19Processing.filter_data') as mock_filter:
        mock_filter.side_effect = Exception
        processing.cases_data = 'Test data'
        processing.deaths_data = 'Test data'
        processing.recovered_data = 'Test data'
        with pytest.raises(SystemExit):
            processing.store_data_for_csv()


def test_create_out_dir():
    """Tests create_out_dir"""
    processing = Covid19Processing('test_dir')
    with patch('os.mkdir') as mock_mkdir:
        processing.create_out_dir()
        mock_mkdir.assert_called_once_with('test_dir')


def test_write_csv_files():
    """Tests write_csv_files"""
    processing = Covid19Processing('test_dir')
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        processing.cases_csv_data = pd.DataFrame(['test data'])
        processing.deaths_csv_data = pd.DataFrame(['test data'])
        processing.recovered_csv_data = pd.DataFrame(['test data'])
        processing.write_csv_files()
        mock_to_csv.assert_any_call('test_dir/cases.csv')
        mock_to_csv.assert_any_call('test_dir/deaths.csv')
        mock_to_csv.assert_any_call('test_dir/recovered.csv')
