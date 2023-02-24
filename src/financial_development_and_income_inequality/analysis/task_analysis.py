"""Tasks used for saving the results from the core analyses of the OLS_model and time
fixed effects model.
"""

### packages ###
import pickle

import pandas as pd
import pytask

### functions and folders used for the task file ###
from financial_development_and_income_inequality.analysis.fixed_effects_model import (
    run_fixed_effects_model,
    run_fixed_effects_model_robust,
)
from financial_development_and_income_inequality.analysis.ols_model import (
    run_ols_model,
    run_ols_model_robust,
)
from financial_development_and_income_inequality.config import BLD


# input directory
@pytask.mark.depends_on(BLD / "data" / "final_data_set.pkl")

# output directory
@pytask.mark.produces(
    [
        BLD / "python" / "models" / "ols_model_estimates.pkl",
        BLD / "python" / "models" / "fixed_effects_model_estimates.pkl",
    ],
)
def task_store_model_estimates(depends_on, produces):
    """Stores the model estimates in a pickle format. The estimates for both the ols
    model and fixed effects model are stored in two separate pickle files.

    Parameters:
    depends_on (pathlib.Path): The path to the directory where the data set is stored.
    produces (pathlib.Path): The paths to the estimates pickle files.

    Returns:
    None

    """
    # loading final_data_set
    data = pd.read_pickle(depends_on)
    # OlS model statistics
    ols_model_estimates = {
        "ols_model_estimates": run_ols_model(data),
        "ols_model_estimates_robust_checks": run_ols_model_robust(data),
    }
    # Fixed effects model statistics
    fixed_effects_model_estimates = {
        "fixed_effects_model_estimates": run_fixed_effects_model(data),
        "fixed_effects_model_estimates_robust_checks": run_fixed_effects_model_robust(
            data,
        ),
    }
    with open(produces[0], "wb") as f:
        pickle.dump(ols_model_estimates, f)
    with open(produces[1], "wb") as f:
        pickle.dump(fixed_effects_model_estimates, f)
