"""Tests for data set management where the explanatory and outcome variables are generated."""

### these test are conducted on the functions used ###
### for generating the explanatory and outcome variables ###

### packages ###
import numpy as np
import pandas as pd
import pytest

### folder used for creating the finalized version of the data set ###
from financial_development_and_income_inequality.config import SRC

### functions tested ###
from financial_development_and_income_inequality.data_management.data_set_management import (
    create_lead_variables,
    explanatory_variables,
    generate_variables,
    percentage_increase_differences,
)

### arguments used for the function that creates the finalized version of the data set ###
from financial_development_and_income_inequality.data_management.task_data_set_management import (
    sectors_percentage_increase_calculation,
    sectors_percentage_increase_diff,
    target_col,
)


### finalized version of the data set ###
@pytest.fixture()
def data():
    initial_data = pd.read_pickle(SRC / "data" / "initial_data_set.pkl")
    final_data = generate_variables(
        initial_data,
        sectors_percentage_increase_calculation,
        sectors_percentage_increase_diff,
        target_col,
    )
    return final_data


###             tests for outcome variables                             ###

### checking whether the labor cost percentage increase for financial   ###
### sector is larger the the rest of the sectors                        ###

### this test is done by assuming that the generated outcome variables  ###
### are positive                                                        ###

# test for percentage increase differences
def test_percentage_increase_differences(data):
    """
    Tests whether the labor cost percentage increase in the financial sector is larger than
    the rest of the sectors (all (except finance), production and construction and education and health)
    in the economy.
    """
    results = percentage_increase_differences(
        data,
        sectors_percentage_increase_diff,
        target_col,
    )
    assert (
        np.array(results.loc[60:120, ["fin_diff_all", "fin_diff_pc", "fin_diff_peh"]])
    ).all() > 0, "labor cost percentage increase in financial sector is not larger when compared with the other sectors in the economy"


# deliberately failing the test (using different time periods), then making it pass
# assuming that the labor cost percentage increase is lower in the financial sector
# @pytest.mark.xfail()
def test_percentage_increase_differences_fail(data):
    """
    Tests whether the labor cost percentage increase in the financial sector is larger than
    the rest of the sectors (all (except finance), production and construction and education and finance)
    in the economy, for different periods.
    """
    results1 = percentage_increase_differences(
        data,
        sectors_percentage_increase_diff,
        target_col,
    )
    with pytest.raises(AssertionError):
        assert (
            np.array(
                results1.loc[40:60, ["fin_diff_all", "fin_diff_pc", "fin_diff_peh"]],
            ).all()
            > 0
        ) is False, "Expected True but False is indicated"
    with pytest.raises(AssertionError):
        assert (
            np.array(
                results1.loc[20:40, ["fin_diff_all", "fin_diff_pc", "fin_diff_peh"]],
            ).all()
            > 0
        ) is False


### checking whether the leads from the outcome variables are properly generated ###
### for all quarters in year 2020 NaN values are expected                        ###

# test for leads from outcome variables
def test_create_lead_variables(data):
    """
    Tests whether the values for the generated outcome variables are NaN in the last four quarters of 1991.
    """
    results2 = create_lead_variables(data)
    actual_values = np.array(
        results2.loc[
            (results2["Year"] == 2020) & (results2["Quarter"] >= 1),
            ["fin_diff_all_lead", "fin_diff_pc_lead", "fin_diff_peh_lead"],
        ],
    )
    expected_values = np.full((4, 3), np.nan)
    assert (
        actual_values.all() == expected_values.all()
    ), f"Expected values{expected_values} but got {actual_values}"


###               test for explanatory variables                                ###
### checking whether the financial development variables are generated properly ###

### given that the share of deposits from domestic banks is much larger, when          ###
### compared with deposits of foreign banks, the variable is expected to be larger     ###


# test for size of financial development variables (fin_dev_db and fin_dev_fb)
def test_explanatory_variables(data):
    """
    Tests whether the size of the explanatory variables are as expected. Financial development
    contributed to domestic banks variable (fin_dev_db) is expected to be larger.
    """
    # generating the explanatory variables
    exp_variables = explanatory_variables(data)
    # testing whether fin_dev_db is larger
    assert (
        exp_variables.loc[:, "fin_dev_db"] > exp_variables.loc[:, "fin_dev_fb"]
    ).all(), "fin_dev_db is not larger than fin_dev_fb in all of its values"
