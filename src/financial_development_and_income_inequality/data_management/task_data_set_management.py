"""Tasks for managing the creation of the outcome and explanatory variables for the data
set."""

### packages ###

import pandas as pd
import pytask

## folders and function used for creating data set ##
from financial_development_and_income_inequality.config import BLD, SRC
from financial_development_and_income_inequality.data_management.data_set_management import (
    generate_variables,
)

### defining parameter values used in the functions ###

# used for percentage increase calculation
sectors_percentage_increase_calculation = [
    ("fin", "lcph_fin"),  # financial sector
    ("all", "mean_all"),  # all sectors (except finance)
    ("pc", "mean_pr_cst"),  # production and construction sector
    ("peh", "lcph_pseh"),
]  # education and health sector

# used for percentage increase differences calculation
sectors_percentage_increase_diff = ["all", "pc", "peh"]
target_col = "fin"

### pytask usage ###

# input directory
@pytask.mark.depends_on(SRC / "data" / "initial_data_set.pkl")

# output data set
@pytask.mark.produces(
    BLD / "data" / "final_data_set.pkl",
)

# function
def task_create_finaL_data(depends_on, produces):
    """Generates the final version of the data set and stores it in a pickle format,
    using the "generate_variables" function.

    Parameters:
    depends_on (pathlib.Path): The path to the initial data set pickle file.
    produces (pathlib.Path): The path to the final data set pickle file.

    Returns:
    None

    """
    # reading the initial data set
    df = pd.read_pickle(depends_on)
    # function that generates the new variables and final version of the data set
    final_data_set = generate_variables(
        df,
        sectors_percentage_increase_calculation,
        sectors_percentage_increase_diff,
        target_col,
    )
    # exporting the data in the specified folders
    final_data_set.to_pickle(produces)
