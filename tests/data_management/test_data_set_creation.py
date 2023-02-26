####################################### Tests for data_set_creation.py #######################################
### these tests are conducted on the functions located    ###

### packages ###
import glob
import os

import pandas as pd
import pytest

### folder and function indicating the directory of initial data files ###
from financial_development_and_income_inequality.config import SRC

### functions tested ###
from financial_development_and_income_inequality.data_management.data_set_creation import (
    load_csv_data_deposits,
    load_csv_data_labor_costs,
)
from pandas.testing import assert_series_equal


@pytest.fixture()
def directory_initial_data_files():
    data_initial_files = SRC / "data" / "data_initial_files"
    return data_initial_files


### checking whether the length of the variables is the   ###
### same given that there are 9 different csv files       ###

# test for length of variables
def test_length_variables(directory_initial_data_files):
    """
    Tests whether the length of the variables is the same for each variable.
    In total, there are nine variables created by load_csv_data_labor_costs function.
    """
    # calling the necessary files (using a wildcard)
    filenames = glob.glob(str(directory_initial_data_files / "BBNZ1.Q.DE.N.H.09*.A"))
    # expected length of the variables
    expected_len = 120

    for filename in filenames:
        result = load_csv_data_labor_costs(filename)
        assert (
            len(result) == expected_len
        ), f"Expected length {expected_len}, but got {len(result)} for file {filename}"


### checking for numeric format in the values of the variables ###

# test for numeric values
def test_numeric_values(directory_initial_data_files):
    """
    Tests whether the values of each variable are numerical (float).
    """
    # calling the csv files used in the function
    fileitems = glob.glob(str(directory_initial_data_files / "BBNZ1.Q.DE.N.H.09*.A"))
    # expected type of the variables
    expected_type = "float64"

    for fileitem in fileitems:
        result = load_csv_data_labor_costs(fileitem)
        assert (
            result.dtype == expected_type
        ), f"Expected type {expected_type}, but got {result.dtype} for filename {fileitem}"


### checking whether mean values for each quarter of randomly ###
### chosen years for deposits are calculated correctly        ###

### first, the mean values for each quarter of the respective ###
### years are calculated by hand, then using the functions    ###
### the values are matched and tested                         ###

# test for matching expected and actual results (BDAC)
def test_expected_values(directory_initial_data_files):
    """
    Tests whether the mean values are calculated correctly. On the left hand side, we have the results for randomly chosen years,
    given from the function, whereas on the right hand side we have the corresponding values which are calculated manually.
    """
    results1 = pd.Series(
        load_csv_data_deposits(
            os.path.join(directory_initial_data_files, "BBK01.OU0001.csv"),
            range(509, 869),
            "BBK01.OU0001",
        ),
    ).round(2)
    expected_values_1996 = pd.Series(
        [1031.65, 1048.43, 1055.25, 1113.18],
        index=range(20, 24),
    )
    expected_values_2006 = pd.Series(
        [1989.33, 2042.79, 1981.70, 2012.35],
        index=range(60, 64),
    )
    expected_values_2016 = pd.Series(
        [1697.39, 1709.08, 1718.10, 1730.59],
        index=range(100, 104),
    )
    # checking equality of values 1996 (all quarters)
    assert_series_equal(results1[20:24], expected_values_1996)
    # checking equality of values 2006 (all quarters)
    assert_series_equal(results1[60:64], expected_values_2006)
    # checking equality of values 2016 (all quarters)
    assert_series_equal(results1[100:104], expected_values_2016)


# test for matching expected and actual results (BDFB)
def test_expected_values1(directory_initial_data_files):
    """
    Tests whether the mean values are calculated correctly. Using assert_series_equal and pd.Series, the mean values obtained from the
    function for randomly selected years are tested and matched with manually calculated corresponding values.
    """
    results2 = pd.Series(
        load_csv_data_deposits(
            os.path.join(directory_initial_data_files, "BBK01.OU1664.csv"),
            range(5, 365),
            0,
        ),
    ).round(2)
    expected_values_1995 = pd.Series([42.85, 176.1, 44.98, 45.6], index=range(16, 20))
    expected_values_2005 = pd.Series([75.08, 83.41, 77.93, 81.10], index=range(56, 60))
    expected_values_2015 = pd.Series(
        [104.65, 118.23, 133.14, 141.82],
        index=range(96, 100),
    )
    # checking equality of values 1995 (all quarters)
    assert_series_equal(results2[16:20], expected_values_1995)
    # checking equality of values 2005 (all quarters)
    assert_series_equal(results2[56:60], expected_values_2005)
    # checking equality of values 2015 (all quarters)
    assert_series_equal(results2[96:100], expected_values_2015)
