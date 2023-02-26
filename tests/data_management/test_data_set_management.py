####################################### Tests for data_set.management.py #######################################
### these test are conducted on the functions located ###
### one test is intentionally marked as xfailed ###

### packages ###
import numpy as np
import pandas as pd
import pytest

### folder and function used for creating the finalized version of the data set ###
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

### this test is done by assuming that the generated outcome variables  ###
### are positive                                                        ###

# test for percentage increase differences
def test_percentage_increase_differences(data):
    """
    Test whether the labor cost percentage increase in the financial sector is larger than
    the rest of the sectors (all (except finance), production and construction and education and finance)
    in the economy.
    """
    results = percentage_increase_differences(
        data,
        sectors_percentage_increase_diff,
        target_col,
    )
    assert (
        np.array(
            results.loc[60:120, ["fin_diff_all", "fin_diff_pc", "fin_diff_peh"]],
        ).all()
        > 0
    ) is True, (
        "sign of fin_diff_all, fin_diff_pc and fin_diff_peh does not match expectation"
    )


# deliberately failing the test (using different time periods), then making it pass
# assuming that the labor cost percentage increase is lower in the financial sector
# @pytest.mark.xfail()
def test_percentage_increase_differences_fail(data):
    """
    Test whether the labor cost percentage increase in the financial sector is larger than
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
        ) is False, "Expected True but False is indicated"


### checking whether the leads from the outcome variables are properly generated ###
### for all quarters in year 1991 there should only be NaN values                ###

# test for leads from outcome variables
def test_create_lead_variables(data):
    """
    Test whether the values for the generated outcome variables are NaN in the last four quarters of 1991.
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

### given that the share of deposits of foreign banks is much smaller, when     ###
### compared with deposits of domestic banks, it is expected that financial     ###


# test for size of financial development variables (fin_dev_fb and fin_dev_db)
# deliberately failing the test
# marking it as failed test
@pytest.mark.xfail()
def test_explanatory_variables(data):
    """
    Test whether the size of the explanatory variables are as expected.
    """
    results3 = explanatory_variables(
        data,
        data[["BDAC", "BDDB", "BDFB"]],
        data["GDP_nom"],
    )
    assert (
        results3.loc[:, "fin_dev_db"] > results3.loc[:, "fin_dev_fb"]
    ).all() is False, "True expected but False indicated"
