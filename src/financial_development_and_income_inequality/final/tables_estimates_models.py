####################################### Tables from Estimates for both models #######################################

### packages ###
import numpy as np
import pandas as pd
from tabulate import tabulate

### Functions that generates tables for the OLS model ###
### For these tables, the results from the models, saved in ols_model_estimates.pkl are used ###

# function for generating table with baseline regressions results
def ols_model_table(ols_estimates, row_names):
    """Creates a table with the baseline regression estimates from the OLS model. Tables are created using
    the package 'tabulate'.

    Parameters:
    ols_estimates(dict): Dictionary containing the baseline regression estimates from the OLS model.
    row_names(list): List containing the names of the variables used in the table.

    Returns:
    table_baseline(str): String containing the table with the OLS model coefficients, R-squared value,
       and number of observations, formatted using the 'grid' table format of the 'tabulate' function.
    """
    # extracting the coefficients and r-squared values
    coefficients_baseline = [
        ols_estimates["ols_model_estimates"][i]["coefficients"] for i in range(3)
    ]
    r_squared_baseline = [
        ols_estimates["ols_model_estimates"][i]["rsquared"] for i in range(3)
    ]
    # creating a data frame for the baseline coefficients
    df_baseline = (
        (pd.DataFrame(np.squeeze(coefficients_baseline)))
        .T.rename(
            columns={
                0: "fin_dif_all_lead",
                1: "fin_diff_pc_lead",
                2: "fin_diff_peh_lead",
            },
        )
        .round(3)
    )
    # adding r-squared value and number of observations
    df_baseline.loc["R^2"] = np.round(r_squared_baseline, 3)
    df_baseline.loc["N"] = np.repeat(120, 3)
    table_baseline = tabulate(
        df_baseline,
        headers="keys",
        tablefmt="grid",
        showindex=row_names,
        numalign="center",
    )
    return table_baseline


# function for generating table with robustness checks results (outcome variables without leads)
def ols_modeL_robust_table(ols_estimates, row_names):
    """Creates a table with the robustness checks estimates from the OLS model.

    Parameters:
    ols_estimates(dict): Dictionary containing the robustness checks estimates from the OLS model.
    row_names(list): List containing the names of the variables used in the table.

    Returns:
    table_baseline(str): String containing the table with the OLS model's robustness checks coefficients, R-squared value,
       and number of observations, formatted using the 'grid' table format of the 'tabulate' function.
    """
    # extracting the coefficients and r-squared values (robustness checks)
    coefficients_robust = [
        ols_estimates["ols_model_estimates_robust_checks"][i]["coefficients"]
        for i in range(3)
    ]
    r_squared_robust = [
        ols_estimates["ols_model_estimates_robust_checks"][i]["rsquared"]
        for i in range(3)
    ]
    # creating a data frame for the robustness checks coefficients
    df_robust = (
        (pd.DataFrame(np.squeeze(coefficients_robust)))
        .T.rename(columns={0: "fin_dif_all", 1: "fin_diff_pc", 2: "fin_diff_peh"})
        .round(3)
    )
    # adding r-squared value and number of observations
    df_robust.loc["R^2"] = np.round(r_squared_robust, 3)
    df_robust.loc["N"] = np.repeat(120, 3)
    table_robust = tabulate(
        df_robust,
        headers="keys",
        tablefmt="grid",
        showindex=row_names,
        numalign="center",
    )
    return table_robust


### Functions that generate tables for the time fixed effects model ###
### For these tables, the results from the models, saved in fixed_effects_model_estimates are used ###

# function for generating table with baseline regressions results
def fixed_effects_model_table(fixed_effects_estimates, row_names):
    """Creates a table with the baseline regression estimates from the time fixed effects model.

    Parameters:
    ols_estimates(dict): Dictionary containing the baseline regression estimates from the time fixed effects model.
    row_names(list): List containing the names of the variables used in the table.

    Returns:
    table_baseline(str): String containing the table with the time fixed effects model coefficients, R-squared value,
       and number of observations, formatted using the 'grid' table format of the 'tabulate' function.
    """
    # extracting the coefficients and r-squared values
    coeff_fixed_baseline = [
        fixed_effects_estimates["fixed_effects_model_estimates"][i]["coefficients"]
        for i in range(3)
    ]
    r_squared_fixed_baseline = [
        fixed_effects_estimates["fixed_effects_model_estimates"][i]["rsquared"]
        for i in range(3)
    ]
    # creating a data frame for the baseline coefficients
    df_fixed_baseline = (pd.DataFrame(np.squeeze(coeff_fixed_baseline))).T.rename(
        columns={
            0: "fin_dif_all_lead",
            1: "fin_diff_pc_lead",
            2: "fin_diff_peh_lead",
        },
    )
    # adding r-squared value and number of observations
    df_fixed_baseline.loc["R^2"] = np.round(r_squared_fixed_baseline, 3)
    df_fixed_baseline.loc["N"] = np.repeat(120, 3)
    table_fixed_effects_baseline = tabulate(
        df_fixed_baseline,
        headers="keys",
        tablefmt="grid",
        showindex=row_names,
        numalign="center",
    )
    return table_fixed_effects_baseline


# function for generating table with robustness checks results (outcome variables without leads)
def fixed_effect_modeL_robust_table(fixed_effects_estimates, row_names):
    """Creates a table with the robustness checks regression estimates from the time fixed effects model.

    Parameters:
    ols_estimates(dict): Dictionary containing the robustness checks regression estimates from the time fixed effects model.
    row_names(list): List containing the names of the variables used in the table.

    Returns:
    table_baseline(str): String containing the table with the time fixed effects model's robustness checks coefficients, R-squared value,
       and number of observations, formatted using the 'grid' table format of the 'tabulate' function.
    """
    # extracting the coefficients and r-squared values (robustness)
    coeff_fixed_robust = [
        fixed_effects_estimates["fixed_effects_model_estimates_robust_checks"][i][
            "coefficients"
        ]
        for i in range(3)
    ]
    r_squared_fixed_robust = [
        fixed_effects_estimates["fixed_effects_model_estimates_robust_checks"][i][
            "rsquared"
        ]
        for i in range(3)
    ]
    # creating a data frame for the robustness checks coefficients
    df_fixed_robust = (pd.DataFrame(np.squeeze(coeff_fixed_robust))).T.rename(
        columns={0: "fin_dif_all", 1: "fin_diff_pc", 2: "fin_diff_peh"},
    )
    # adding r-squared value and number of observations
    df_fixed_robust.loc["R^2"] = np.round(r_squared_fixed_robust, 3)
    df_fixed_robust.loc["N"] = np.repeat(120, 3)
    table_fixed_effects_robust = tabulate(
        df_fixed_robust,
        headers="keys",
        tablefmt="grid",
        showindex=row_names,
        numalign="center",
    )
    return table_fixed_effects_robust
