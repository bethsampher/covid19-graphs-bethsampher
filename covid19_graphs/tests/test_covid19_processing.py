""" unit tests for covid19_processing """

from mock import patch
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


