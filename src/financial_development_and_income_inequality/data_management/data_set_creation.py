####################################### Data Set Creation #######################################

### data_dir indicates the directory where the initial data files are located ###

### packages ###

import os

import numpy as np
import pandas as pd

### Creating the Data Frame ###

# function that creates the initial data frame
def data_creation(dataframe, data_dir):
    """Creates the final data set by concatenating multiple data frames that contain the
    necessary variables. All of the duplicated columns are dropped.

    Parameters:
    dataframe(pandas.DataFrame): Initial empty data frame used for creating and storing the variables.
    data_dir(str): A string representing the directory where the initial data files can be found. This
    string is used as an argument only in the functions that load csv or excel files.

    Returns:
    dataframe_final(pandas.DataFrame): Finalized data frame containing all of the variables.

    """
    dataframes = [
        indicator_variables(dataframe),
        store_labor_costs(dataframe, data_dir),
        store_deposits(dataframe, data_dir),
        control_variables_deutsche_bundesbank(dataframe, data_dir),
        control_variables_eurostat(dataframe, data_dir),
        control_variable_ecb(dataframe, data_dir),
        control_fin_crisis(dataframe),
    ]
    # concatenating data frames which contain the variables
    dataframe_final = pd.concat(dataframes, axis=1)
    # dropping all duplicated columns
    dataframe_final = dataframe_final.loc[:, ~dataframe_final.columns.duplicated()]
    return dataframe_final


### indicator variables ###

# function that creates indicator variables
def indicator_variables(dataframe):
    """Creates indicator variables for the data set.

    Parameters:
    dataframe(pandas.DataFrame): Initial empty pandas data frame used to store the indicator variables.

    Returns:
    dataframe(pandas.DataFrame): Pandas data frame with newly created indicator variables.

    """
    dataframe["Country"] = np.repeat(["Germany"], 120)
    dataframe["Year"] = np.repeat(list(range(1991, 2021)), 4)
    dataframe["Quarter"] = np.tile(list(range(1, 5)), 30)
    return dataframe


### Unit Labor Costs per Hour Across Sectors, data gathered from Deutsche BundesBank ###
### measured in billion Euros ###

# function that loads csv data and selects exact rows and columns
def load_csv_data_labor_costs(filename):
    """Loads data from a csv file and returns it as a numeric list (float).

    Parameters:
    filename (str): The name of the csv file (without the ".csv" extension).

    Returns:
    data (list): A list of numerical values from the specified csv file.

    """
    file = pd.read_csv(filename + ".csv")
    data = pd.to_numeric(list(file.iloc[range(6, 126), 1]))

    return data


# function that stores the data from the function load_csv_data_labor_costs
def store_labor_costs(dataframe, data_dir):
    """Stores newly created labor costs variables in pandas data frame.

    Parameters:
    dataframe(pandas.DataFrame): Data frame to which the variables will be stored.
    data_dir(str): A string representing the directory where the initial data files can be found.

    Returns:
    dataframe(pandas.DataFrame): Pandas data frame with newly created labor cost variables.

    """
    codes = ["0939", "0931", "0933", "0934", "0948", "0940", "0938", "0941", "0947"]
    varnames = [
        "lcph_fin",
        "lcph_prod",
        "lcph_const",
        "lcph_wsrt",
        "lcph_inco",
        "lcph_reest",
        "lcph_bsns",
        "lcph_pseh",
        "lcph_other",
    ]

    for i in range(len(codes)):
        code = codes[i]
        varname = varnames[i]
        filename = os.path.join(data_dir, "BBNZ1.Q.DE.N.H.") + code + ".A"
        dataframe[varname] = load_csv_data_labor_costs(filename)
    return dataframe


### Deposit liabilities for domestic, foreign banks ###
### monthly measured values in billion Euros ###
### mean for three consecutive months is taken ###

# function that loads data for deposits and calculates the mean
def load_csv_data_deposits(file_name, row_range, target_col):
    """Processes a CSV file and returns the mean value of every 3 elements.

    Parameters:
    file_name (str): The path and name of the CSV file to be processed.
    row_range (iterable): The rows to be processed in the CSV file.
    target_col (int or str): The target column to be processed in the CSV file.
    dataframe (pandas.DataFrame): The dataframe to which the processed data will be assigned.

    Returns:
    processed_data (list): The mean value of every 3 elements in the target column.

    """
    df = pd.read_csv(
        file_name,
        header=None if file_name.endswith("BBK01.OU1664.csv") else 0,
    )
    col = pd.to_numeric(df.loc[row_range, target_col])
    processed_data = list(col.groupby(np.arange(len(col)) // 3).mean())
    return processed_data


# function that stores the data from load_csv_data_deposits
def store_deposits(dataframe, data_dir):
    """Stores newly created bank deposits variables in pandas data frame.

    Parameters:
    dataframe(pandas.DataFrame): Data frame where the variables are stored.
    data_dir(str): A string representing the directory where the initial data files can be found.

    Returns:
    dataframe(pandas.DataFrame): Data frame where the newly created variables are stored.

    """
    # bank deposits for all categories

    dataframe["BDAC"] = load_csv_data_deposits(
        os.path.join(data_dir, "BBK01.OU0001.csv"),
        range(509, 869),
        "BBK01.OU0001",
    )
    # bank deposits for foreign banks
    dataframe["BDFB"] = load_csv_data_deposits(
        os.path.join(data_dir, "BBK01.OU1664.csv"),
        range(5, 365),
        0,
    )
    # bank deposits for domestic banks
    dataframe["BDDB"] = dataframe["BDAC"] - dataframe["BDFB"]
    return dataframe


### Control Variables ###
### Data Gathered from Deutsche BundesBank ###

# function that reads csv data and stores newly created control variables
def control_variables_deutsche_bundesbank(dataframe, data_dir):
    """Reads CSV files and stores newly created control variables in pandas data frame.
    The CSV files are obtained from Deutsche Bundesbank.

    Parameters:
    dataframe(pandas.DataFrame): Data Frame where the variables are stored.
    data_dir(str): A string representing the directory where the initial data files can be found.

    Returns:
    dataframe(pandas.DataFrame): Data Frame where the newly created control variables are stored.

    """
    # number of foreign banks in Germany (saving the values with integer type)
    dataframe["fb_num"] = (
        pd.read_csv(os.path.join(data_dir, "Number of Foreign Banks.csv"))[272:632]
        .iloc[::3, 1]
        .values.astype(int)
    )
    # GDP nominal
    dataframe["GDP_nom"] = list(
        pd.read_csv(os.path.join(data_dir, "BBNZ1.Q.DE.N.G.0000.A.csv"))
        .iloc[range(6, 126), 1]
        .astype(float),
    )
    # Government consumption
    dataframe["gvt_cs"] = (
        list(
            pd.read_csv(os.path.join(data_dir, "BBNZ1.Q.DE.N.G.0106.A.csv"))
            .iloc[range(6, 126), 1]
            .astype(float),
        )
        / dataframe["GDP_nom"]
    )
    # Consumer Price Index
    dataframe["CPI"] = (
        pd.read_csv(os.path.join(data_dir, "BBDP1.M.DE.Y.VPI.C.A00000.I15.A.csv"))
        .iloc[range(4, 364), 1]
        .astype(float)
        .groupby(np.arange(360) / 3)
        .mean()
    )
    return dataframe


### Data Gathered from Eurostat ###

# function that reads csv and excel data and stores newly created control variables
def control_variables_eurostat(dataframe, data_dir):
    """Reads CSV and excel data and stores newly created control variables. The CSV and
    excel files are obtained from Eurostat.

    Parameters:
    dataframe(pandas.DataFrame): Data frame where the variables are stored.
    data_dir(str): A string representing the directory where the initial data files can be found.

    Returns:
    dataframe(pandas.DataFrame): Data frame with newly created control variables.

    """
    # GDP per capita (converting the value measurement from millions to billions)
    dataframe["GDP_per_cap"] = (
        pd.read_csv(
            os.path.join(data_dir, "namq_10_pc__custom_4327625_page_linear.csv.gz"),
        )
        .loc[:, "OBS_VALUE"]
        .astype(float)
    ) / 1000
    # Share of agricultural sector in nominal GDP
    dataframe["agri_gdp"] = (
        pd.read_csv(
            os.path.join(data_dir, "namq_10_a10__custom_4327784_page_linear.csv.gz"),
        )
        .loc[:, "OBS_VALUE"]
        .astype(float)
    )
    # Population by education attainment level
    edu_att = (
        pd.read_excel(
            os.path.join(
                data_dir,
                "edat_lfse_03__custom_4306995_page_spreadsheet.xlsx",
            ),
        )
        .loc[11, :]
        .dropna()
    )
    # filtering the list to include only numeric values
    edu_att = [value for value in edu_att if isinstance(value, (int, float))]
    # creating the variable
    dataframe["edu_att"] = np.repeat(np.insert(edu_att, [0, 6], np.nan, axis=0), 4)
    return dataframe


### Data Gathered from European Central Bank ###

# function that reads an csv file and stores a control variable (financial stress index of Germany)
def control_variable_ecb(dataframe, data_dir):
    """Reads an CSV file and creates a new control variable named "FSI". The CSV file is
    obtained from the European Central Bank.

    Parameters:
    dataframe(pandas.DataFrame): Data frame where the new control variable "FSI" is stored.
    data_dir(str): A string representing the directory where the initial data files can be found.

    Returns:
    dataframe(pandas.DataFrame): Data frame with a newly created control variable "FSI".

    """
    # defining the column names
    col_names = [
        "Year and Month",
        "Monthly Values",
        "Observed Status",
        "Quarterly Values",
    ]
    # loading the csv file and re-indexing
    financial_stress_data = pd.read_csv(
        os.path.join(data_dir, "Financial Stress Index Germany.csv"),
        names=col_names,
    ).loc[::-1]
    # creating the control variable (financial stress index Germany)
    dataframe["FSI"] = (
        pd.to_numeric(financial_stress_data.loc[365:6, "Monthly Values"])
        .groupby(np.arange(360) // 3)
        .mean()
    )
    return dataframe


### Control Variable indicating the period for Global Financial Crisis ###

# function that creates a dummy variable indicating the global financial crisis
def control_fin_crisis(dataframe):
    """Creates a dummy variable indicating period of the Global Financial Crisis in
    2007-08.

    Parameters:
    dataframe(pandas.DataFrame): Data frame used for storage of the control variable.

    Returns:
    dataframe(pandas.DataFrame): Data frame with a new control variable ("fincri_0708").

    """
    # starting from 3. quarter in 2007 until 4.quarter 2008
    dataframe["fincri_0708"] = np.where(
        (
            (dataframe["Year"] == 2008)
            | ((dataframe["Year"] == 2007) & (dataframe["Quarter"] >= 3))
        ),
        1,
        0,
    )
    return dataframe
