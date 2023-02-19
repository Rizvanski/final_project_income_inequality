############# Creating Outcome and Explanatory Variables #############

### after creating the data set with the python file "data_set_creation", ###
### here the outcome and explanatory variables are generated ###

# packages

# function for generating the outcome and explanatory variables
def generate_variables(
    df,
    sectors_percentage_increase_calculation,
    sectors_percentage_increase_diff,
    target_col,
):
    """Generates variables by calling the functions and stores the variables in the
    "initial_data_set" pandas data frame.

    Parameters:
    df(pandas.DataFrame): Initial data frame used for generating and storing the variables.
    sectors_percentage_increase_calculation(list): List of immutable tuples where each tuple contains two elements:
                   1) The name of the new variable (column).
                   2) The column name in the data frame used for percentage increase calculation.
    sectors_percentage_increase_diff(list): List of sector columns.
    target_col(str): Target sector name (financial sector).

    Returns:
    df(pandas.DataFrame): Pandas data frame where the newly generated variables are stored.

    """
    # mean calculation
    df = mean_calculation(df)
    # percentage increase calculation
    df = percentage_increase_calculation(df, sectors_percentage_increase_calculation)
    # percentage increase difference calculation
    df = percentage_increase_differences(
        df,
        sectors_percentage_increase_diff,
        target_col,
    )
    # one year lead for outcome variables
    df = create_lead_variables(df)
    # main explanatory variables calculation
    df = explanatory_variables(df)
    return df


###                      outcome variables                               ###
### labor cost percentage increase differences between financial sector  ###
### and other sectors in the economy                                     ###

### additionally the mean of labor costs for production and construction is calculated ###

# function for mean calculation
def mean_calculation(df):
    """Calculates mean of labor costs for selected sectors and stores them in a pandas
    data frame.

    Parameters:
    df(pandas.DataFrame): Initial data set.

    Returns:
    df(pandas.DataFrame): Modified data frame where the means for production and construction sector and all sectors (expect finance) are stored.

    """
    df["mean_all"] = df.loc[:, "lcph_prod":"lcph_other"].mean(axis=1)
    df["mean_pr_cst"] = df.loc[:, ["lcph_prod", "lcph_const"]].mean(axis=1)
    return df


### finance sector, all other sectors, production and construction sector,           ###
### education and health sector                                                      ###

# function for percentage increase calculation
def percentage_increase_calculation(df, sectors_percentage_increase_calculation):
    """Calculates labor cost percentage increase for selected sectors and stores the
    variables in the data frame.

    Parameters:
    df(pandas.DataFrame): Initial data frame used for calculating percentage increases and storing the results.
    sectors_percentage_increase_calculation(list): List of immutable tuples where each tuple contains two elements:
                   1) The name of the new variable (column).
                   2) The column name in the data frame used for percentage increase calculation.

    Returns:
    df(pandas.DataFrame): Data frame with additional variables (columns) containing the newly
    generated variables.

    """
    for sector in sectors_percentage_increase_calculation:
        name, col = sector
        a = df.loc[0, col]
        b = df.loc[1:120, col]
        df[name] = ((b - a) / a) * 100
    return df


### Finally, we generate the outcome variables by taking the differences of       ###
### the labor cost percentage increases between financial sector and the other    ###

# function for percentage increase difference calculation
def percentage_increase_differences(df, sectors_percentage_increase_diff, target_col):
    """Calculates percentage increase differences between target sector and other
    sectors and adds the variables in the data frame.

    Parameters:
    df(pandas.DataFrame): Initial data frame containing the variables to be used.
    sectors_percentage_increase_diff(list): List of sector columns.
    target_col(str): Target sector name (financial sector).

    Returns:
    df(pandas.DataFrame): Data frame with added outcome variables.

    """
    for sector in sectors_percentage_increase_diff:
        diff_col = f"{target_col}_diff_{sector}"
        df[diff_col] = df[target_col] - df[sector]
    return df


### Taking a lead for four periods for all of the outcome variables ###

# function for creating a one year (four quarters) lead
def create_lead_variables(df):
    """Creates lead variables for outcome variables (labor cost percentage increase
    differences) and stores them in a pandas data frame.

    Parameters:
    df(pandas.DataFrame):Initial data frame containing the outcome variables.

    Returns:
    df(pandas.DataFrame): Data frame containing the adjusted versions with one year lead
    (four quarters) for outcome variables.

    """
    lead_variables = ["fin_diff_all", "fin_diff_pc", "fin_diff_peh"]
    for variable in lead_variables:
        df[f"{variable}_lead"] = df[variable].shift(-4)
    return df


###                   explanatory variables                        ###
### financial development variables calculated by dividing deposit ###
### liabilities with nominal GDP                                   ###

### overall financial development, financial development contributed to   ###
### domestic banks and financial development contributed to foreign banks ###

# function for calculation of main explanatory variables
def explanatory_variables(df):
    """Generates financial development variables by dividing deposits with nominal GDP
    and stores the newly created variables in a pandas data frame.

    Parameters:
    df(pandas.DataFrame): Initial data frame containing the variables to be used.

    Returns:
    df(pandas.DataFrame): Data frame with additional financial development variables.

    """
    # dictionary containing columns used for calculation and names of new variables
    col_names = {"BDAC": "fin_dev_all", "BDDB": "fin_dev_db", "BDFB": "fin_dev_fb"}

    for col in col_names:
        new_col = col_names[col]
        df[new_col] = df[col] / df["GDP_nom"]
    return df
