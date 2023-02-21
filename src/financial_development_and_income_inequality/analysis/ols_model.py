####################################### OLS Model #######################################
### Using final_data_set, the effect of financial development   ###
### on income inequality is first estimated using an OLS Model  ###


### packages ###
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression


# function used for fitting OLS model
# note that scikit-learn does not automatically exclude the observations containing the NaN values
# hence means of the respective columns are imputed instead of the NaN values
def fit_ols_model(X, ys, control_vars):
    """Fits multiple OLS regression models, each containing different dependent
    variables and same independent variables and returns a list with statistics of the
    fitted regression models.

    Parameters:
    X (pandas.DataFrame or numpy.ndarray): Main explanatory variables.
    ys (list of pandas.Series or numpy.ndarray): List of outcome variables.
    control_vars (list): List of control variables.

    Returns:
    models (list of dict): A list of dictionaries containing the fitted regression models, coefficients,
        intercepts and R-squared values for each model.

    """
    models = []
    for y in ys:
        # Concatenating main explanatory and control variables
        X_ = pd.concat([X, control_vars], axis=1)

        # Handling missing values in the data
        # Imputing mean values for NaN
        imp = SimpleImputer(strategy="mean")
        X_imp = imp.fit_transform(X_)
        y_imp = imp.fit_transform(y.values.reshape(-1, 1))

        # Fiting the regression model
        model = LinearRegression()
        model.fit(X_imp, y_imp)

        # Extracting model coefficients, intercept, and R-squared values
        coefs = model.coef_
        intercept = model.intercept_
        rsquared = np.array(model.score(X_imp, y_imp))

        # Adding the results to the list
        results = {
            "model": model,
            "coefficients": coefs,
            "intercept": intercept,
            "rsquared": rsquared,
        }

        models.append(results)
    return models


# function used for running baseline regressions
def run_ols_model(data):
    """Runs multiple OLS regression models with specified outcome, explanatory and
    control variables and gets results from the respective models.

    Parameters:
    data(pandas.DataFrame): Data frame containing the variables used for fitting the model and obtaining the
    respective results.

    Returns:
    results (list): A list of stats models results for the OLS models.

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
    models_baseline = fit_ols_model(X, ys, control_vars)
    return models_baseline


# function used for robustness checks (outcome variables without the lead)
def run_ols_model_robust(data):
    """Runs multiple OLS regression models with specified outcome, explanatory and
    control variables and gets results from the respective models. This function is used
    for robustness checks, where the outcome variables are taken without any leads.

    Parameters:
    data(pandas.DataFrame): Data frame containing the variables used for fitting the model and obtaining the
    respective results.

    Returns:
    results (list): A list of stats models results for the OLS models.

    """
    # main explanatory variables
    X = data[["fin_dev_all", "fin_dev_db", "fin_dev_fb"]]
    # outcome variables without leads
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
    models_robust_check = fit_ols_model(X, ys_robust, control_vars)
    return models_robust_check
