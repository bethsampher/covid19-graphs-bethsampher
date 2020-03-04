""" unit tests for covid19_processing """

from mock import patch
import pandas as pd
import pytest

from covid19_graphs.covid19_processing import Covid19Processing


def test_out_dir():
    processing_with_dir = Covid19Processing('test_dir')
    assert processing_with_dir.out_dir == 'test_dir'

def test_download_from_github():
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = 'Test info'
        mock_get.return_value.status_code = 200
        processing = Covid19Processing('test_dir')
        response = processing.download_from_github()
        assert response == 200
        assert processing.data == 'Test info'
        assert processing.status_code == 200

def test_process_data():
    processing = Covid19Processing('test_dir')
    test_data = 'State,Country/Region,1/22/20,3/3/20\nAnhui,Mainland China,1,990\nBeijing,Mainland China,14,414\n,UK,0,51'
    processing.data = test_data
    processing.process_data()
    expected_rows = [[15, 0, 15], [1404, 51, 1455]]
    expected_col_names = ['China', 'Other', 'Total']
    expected_row_names = ['1/22/20', '3/3/20']
    expected_csv_data = pd.DataFrame(data=expected_rows, columns=expected_col_names, index=expected_row_names)
    assert expected_csv_data.equals(processing.csv_data)

