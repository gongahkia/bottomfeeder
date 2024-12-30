import json
from transpiler import (
    generate_latex,
    generate_csv,
    generate_xml,
    generate_hdf5,
    generate_pickle,
    generate_sql,
)


def test_generate_latex():
    """
    tests generation of a valid LaTeX document
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
                "coram": ["Judge Lee", "Judge Tan"],
                "year": 2024,
                "court": "SGHC",
                "paragaph_count": 20,
            }
        },
    ]
    target_filepath = "test_report.tex"
    generate_latex(sample_data, target_filepath)


def test_generate_csv():
    """
    tests generation of a valid CSV file
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
                "coram": ["Judge Lee", "Judge Tan"],
                "year": 2024,
                "court": "SGHC",
                "paragaph_count": 20,
            }
        },
    ]
    target_filepath = "test_report.csv"
    generate_csv(sample_data, target_filepath)


def test_generate_sql():
    """
    tests generation of a valid SQL database
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
                "coram": ["Judge Lee", "Judge Tan"],
                "year": 2024,
                "court": "SGHC",
                "paragaph_count": 20,
            }
        },
    ]
    target_db_name = "test_database.db"
    generate_sql(sample_data, target_db_name)
