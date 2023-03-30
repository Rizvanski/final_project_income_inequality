"""Tests for the OLS and time fixed effect models."""

### packages ###
import pandas as pd
import pytest

### time fixed effects model function tested ###
from financial_development_and_income_inequality.analysis.fixed_effects_model import (
    run_fixed_effects_model,
)

### OLS model function tested ###
from financial_development_and_income_inequality.analysis.ols_model import (
    run_ols_model,
    run_ols_model_robust,
)

### folder and function used for creating the finalized version of the data set ###
from financial_development_and_income_inequality.config import SRC
from financial_development_and_income_inequality.data_management.data_set_management import (
    generate_variables,
)

### arguments used for the function that creates the finalized version of the data set ###
from financial_development_and_income_inequality.data_management.task_data_set_management import (
    sectors_percentage_increase_calculation,
    sectors_percentage_increase_diff,
    target_col,
)


### finalized version of the data set ###
@pytest.fixture()
def final_data():
    initial_data_set = pd.read_pickle(SRC / "data" / "initial_data_set.pkl")
    final_data_set = generate_variables(
        initial_data_set,
        sectors_percentage_increase_calculation,
        sectors_percentage_increase_diff,
        target_col,
    )
    return final_data_set


### tests for the OLS and time fixed effects models ###
### tests related with the expected signs of the coefficients ###

### fin_dev_db is expected to be positive with OLS model ###
### given that fin_dev_db is much larger than fin_dev_fb ###

# test for expected sign of OLS model
def test_expected_sign_ols(final_data):
    """
    Tests whether the coefficient of financial development contributed to domestic banks is positive.
    """
    # OLS model
    ols_model_results = run_ols_model(final_data)
    # extracting the fin_dev_db coefficient
    coeff_interest = [result["coefficients"][0][1] for result in ols_model_results]
    # testing whether the values are positive
    assert all(coeff > 0 for coeff in coeff_interest)


### sign of fin_dev_db is expected to be faulty with time fixed effect model ###
### the number of clusters is 30, which does not fulfill the rule for thumb ###
### therefore, the model is not applied correctly ###

# marking the test with a decorator
@pytest.mark.xfail()
def test_expected_sign_fixed_effects(final_data):
    """
    Tests whether the coefficient of financial development contributed to domestic banks is positive.
    The coefficient is expected to be faulty and hence this test is intentionally marked as a failed test.
    """
    # time fixed effects model
    fixed_effects_results = run_fixed_effects_model(final_data)
    # extracting the fin_dev_db coefficient
    coeff_interest_fixed_effects = [
        result["coefficients"][0][1] for result in fixed_effects_results
    ]
    # testing whether the values are positive
    assert all(coeff > 0 for coeff in coeff_interest_fixed_effects)


### comparing the sign of the coefficients for baseline and robust models ###
### fin_dev_db is assumed positive in both scenarios ###

# test comparing the results of the ols_model coefficients
def test_compare_coeff(final_data):
    """
    Tests whether the coefficient for financial development contributed to domestic banks is positive in
    both models (OLS and time fixed effects).
    """
    # OLS model baseline regression
    ols_baseline = run_ols_model(final_data)
    # OLS model robustness checks
    ols_robust_checks = run_ols_model_robust(final_data)
    # extracting coefficients (fin_dev_db)
    coeff_baseline = [result["coefficients"][0][1] for result in ols_baseline]
    coeff_robust = [result["coefficients"][0][1] for result in ols_robust_checks]
    # testing whether the values are positive
    assert all(coeff > 0 for coeff in coeff_baseline) and all(
        coeff > 0 for coeff in coeff_robust
    )
