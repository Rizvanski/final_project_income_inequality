####################################### Fixed Effects Model #######################################
### Here, using final_data_set, year fixed effects model is used to observe the effect of ###
### financial development on income inequality ###


# packages used
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression


# function used for fitting year fixed effects model
# time fixed effects using linear regression
# imputed mean values for NaN
def fit_fixed_effects_model(data, X, ys, control_vars):
    """Fits multiple linear regression models with time fixed effects, each containing
    different dependent and same independent variables.

    Parameters:
    data (pandas.DataFrame): Data set used for creating the dummy variables.
    X (pandas.DataFrame or numpy.ndarray): Main explanatory variables.
    ys (list of pandas.Series or numpy.ndarray): List of outcome variables.
    control_vars (list): List of control variables.

    Returns:
    models (list of dict): A list of dictionaries containing the fitted regression models, coefficients,
        intercepts and R-squared values for each model.

    """
    models = []
    # getting dummies according to the variable "Year"
    dummies = pd.get_dummies(data["Year"])
    # transforming column names into string type
    dummies.columns = dummies.columns.astype(str)

    for y in ys:
        # Concatenating main explanatory, control and dummy variables
        X_ = pd.concat([X, control_vars, dummies], axis=1)

        # Handling missing values in the data
        # Imputing mean values for NaN in y and X
        imp = SimpleImputer(strategy="mean")
        X_imp = imp.fit_transform(X_)
        y_imp = imp.fit_transform(y.values.reshape(-1, 1))

        # Fitting the time fixed effects model
        model = LinearRegression()
        model.fit(X_imp, y_imp)

        # Extracting statistics of interest
        # Model coefficients (excluding coefficients of dummy variables)
        coeff = len(X.columns) + len(control_vars.columns)
        coeff_interest = model.coef_[:, :coeff]
        # Intercept
        intercept = model.intercept_
        # Coefficient of determination
        rsquared = np.array(model.score(X_imp, y_imp))

        # Adding the results to the list
        results = {
            "model": model,
            "coefficients": coeff_interest,
            "intercept": intercept,
            "rsquared": rsquared,
        }

        models.append(results)

    return models


# function used for baseline regressions
def run_fixed_effects_model(data):
    """Runs multiple linear time fixed effect regression models with specified outcome,
    explanatory and control variables and obtains results from the respective models.

    Parameters:
    data(pandas.DataFrame): Data frame containing the variables used for fitting the model and obtaining the
    respective results.

    Returns:
    results (list): A list of stats models results for the linear time fixed effect models.

    """
    # main explanatory variables
    X = data[["fin_dev_all", "fin_dev_db", "fin_dev_fb"]]
    # outcome variables with leads
    ys = [
        data["fin_diff_all_lead"],
        data["fin_diff_pc_lead"],
        data["fin_diff_peh_lead"],
    ]
    # control variables
    control_vars = data[
        [
            "GDP_nom",
            "CPI",
            "gvt_cs",
            "FSI",
            "GDP_per_cap",
            "agri_gdp",
            "edu_att",
            "fincri_0708",
        ]
    ]
    # fitting the models and obtaining results with the defined variables
    models_baseline = fit_fixed_effects_model(data, X, ys, control_vars)
    return models_baseline


# function used for robustness checks (outcome variables without leads)
def run_fixed_effects_model_robust(data):
    """Runs multiple linear time fixed effect regression models with specified outcome,
    explanatory and control variables and obtains results from the respective models.
    This function is used for robustness checks, where the outcome variables are taken
    without any leads.

    Parameters:
    data(pandas.DataFrame): Data frame containing the variables used for fitting the model and obtaining the
    respective results.

    Returns:
    results (list): A list of stats models results for the linear time fixed effect models.

    """
    # main explanatory variables
    X = data[["fin_dev_all", "fin_dev_db", "fin_dev_fb"]]
    # outcome variables with leads
    ys_robust = [data["fin_diff_all"], data["fin_diff_pc"], data["fin_diff_peh"]]
    # control variables
    control_vars = data[
        [
            "GDP_nom",
            "CPI",
            "gvt_cs",
            "FSI",
            "GDP_per_cap",
            "agri_gdp",
            "edu_att",
            "fincri_0708",
        ]
    ]
    # fitting the models and obtaining results with the defined variables
    models_robust_check = fit_fixed_effects_model(data, X, ys_robust, control_vars)
    return models_robust_check
