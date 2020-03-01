""" unit tests for covid19_processing """

import mock
import pytest

from covid19_graphs.covid19_processing import Covid19Processing


def test_out_dir():
    processing_with_dir = Covid19Processing('test_dir')
    assert processing_with_dir.out_dir == 'test_dir'

