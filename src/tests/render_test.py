import json
import render
import pytest
from pytest_mock import patch
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show


def test_bokeh_visualise_valid_data():
    """
    tests bokeh_visualise with valid JSON data
    """
    sample_data = [
        {
            "case_123": {
                "coram": ["Judge Doe"],
                "year": 2023,
                "court": "SGCA",
                "paragaph_count": 10,
            }
        },
        {
            "case_456": {
                "coram": ["Judge Lee"],
                "year": 2024,
                "court": "SGHC",
                "paragaph_count": 20,
            }
        },
    ]
    target_filepath = "test_output.html"
    with patch("bokeh.plotting.show") as mock_show:
        render.bokeh_visualise(sample_data, target_filepath)
        mock_show.assert_called_once_with(figure())


def test_bokeh_visualise_empty_data():
    """
    tests bokeh_visualise with empty JSON data
    """
    sample_data = []
    target_filepath = "test_output.html"
    with pytest.raises(ValueError):
        render.bokeh_visualise(sample_data, target_filepath)
