"""Task file for generating tables with the estimates from the ols and time fixed effects models."""

### packages ###
import pandas as pd
import pytask

### folders and functions used for the task file ###
from financial_development_and_income_inequality.config import BLD
from financial_development_and_income_inequality.final.tables_estimates_models import (
    fixed_effect_modeL_robust_table,
    fixed_effects_model_table,
    ols_modeL_robust_table,
    ols_model_table,
)

### defining parameter values used in the functions ###
# names of the independent variables (including coefficient of determination and number of observations)
row_names = [
    "fin_dev_all",
    "fin_dev_db",
    "fin_dev_fb",
    "GDP_nom",
    "CPI",
    "gvt_cs",
    "FSI",
    "GDP_per_cap",
    "agri_gdp",
    "edu_att",
    "fincri_0708",
    "R^2",
    "N",
]

# input files
@pytask.mark.depends_on(
    [
        (BLD / "python" / "models" / "ols_model_estimates.pkl"),
        (BLD / "python" / "models" / "fixed_effects_model_estimates.pkl"),
    ],
)

# output files
@pytask.mark.produces(
    [
        BLD / "python" / "tables" / "ols_baseline.csv",
        BLD / "python" / "tables" / "ols_robustness_checks.csv",
        BLD / "python" / "tables" / "fixed_effects_baseline.csv",
        BLD / "python" / "tables" / "fixed_effects_robustness_checks.csv",
    ],
)
def task_generate_tables(depends_on, produces):
    """Creates and stores tables from the OLS and time fixed effects models.

    Parameters:
    depends_on (pathlib.Path): The paths to the directory where the estimates from both models are located.
    produces (pathlib.Path): The paths to the directory where tables are stored in a "txt" format.

    Returns:
    None

    """
    # loading the estimates results from both models
    ols_estimates = pd.read_pickle(depends_on[0])
    fixed_effects_estimates = pd.read_pickle(depends_on[1])
    # creating the tables using the functions
    # OLS model
    ols_baseline = ols_model_table(ols_estimates, row_names)
    ols_robustness_checks = ols_modeL_robust_table(ols_estimates, row_names)
    # Fixed effects model
    fixed_effects_baseline = fixed_effects_model_table(
        fixed_effects_estimates,
        row_names,
    )
    fixed_effects_robustness_checks = fixed_effect_modeL_robust_table(
        fixed_effects_estimates,
        row_names,
    )
    # saving the files in an "csv" format
    outputs = [
        ols_baseline,
        ols_robustness_checks,
        fixed_effects_baseline,
        fixed_effects_robustness_checks,
    ]
    for i, output in enumerate(outputs):
        with open(produces[i], "w") as f:
            f.write(str(output))
