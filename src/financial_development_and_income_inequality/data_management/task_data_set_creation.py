"""Tasks for managing the creation of the initial data set."""

### packages ###

import pandas as pd
import pytask

## folders and function used for creating data set ##
from financial_development_and_income_inequality.config import BLD, SRC
from financial_development_and_income_inequality.data_management.data_set_creation import (
    data_creation,
)


# input directory
@pytask.mark.depends_on(SRC / "data" / "data_initial_files/")

# output data set
@pytask.mark.produces(
    [
        BLD / "python" / "data" / "initial_data_set.pkl",
        SRC / "data" / "initial_data_set.pkl",
    ],
)
def task_create_initial_data_set(depends_on, produces):
    """Creates and stores the initial data set, using the function data_creation.

    Parameters:
    depends_on (pathlib.Path): The path to the directory where the initial data files are located.
    produces (pathlib.Path): The paths to the initial data set pickle files.

    Returns:
    None

    """
    # empty DataFrame
    dataframe = pd.DataFrame()

    # importing the function from data_set_creation.py
    initial_data_set = data_creation(dataframe, data_dir=depends_on)

    # exporting the data in the specified folders
    initial_data_set.to_pickle(produces[0])
    initial_data_set.to_pickle(produces[1])
