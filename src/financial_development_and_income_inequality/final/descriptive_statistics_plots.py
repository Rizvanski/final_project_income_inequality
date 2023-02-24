####################################### Descriptive Statistics Plots #######################################

### packages ###
import matplotlib.pyplot as plt

### Plots depicting rising income inequality in Germany ###

# function for plotting labor cost percentage increase
def labor_cost_increase_plot(data):
    """Generates a plot depicting the higher percentage increase of the financial sector,
    when compared with other sectors in the economy.

    Parameters:
    data(pandas.DataFrame): Data frame used to obtain the variables used for plotting.

    Returns:
    fig_labor_costs(matplotlib.figure): The figure object containing the generated plot.
    """
    fig_labor_costs, ax = plt.subplots()
    for column, label in [
        ("fin", "Finance"),
        ("pc", "Production and Construction"),
        ("peh", "Education and Health"),
        ("all", "All Sectors"),
    ]:
        ax.plot(data["Year"], data[column], label=label)
    ax.set(
        xlabel="Year",
        ylabel="Percentage Increase",
        title="Labor Cost Percentage Increase Across Sectors",
    )
    ax.legend()
    return fig_labor_costs


# function for plotting the increased number of foreign branches in Germany
def foreign_banks_increase_plot(data):
    """Generates a plot depicting the increased presence of foreign banks in Germany.

    Parameters:
    data(pandas.DataFrame): Data frame containing the variable used to generate the plot.

    Returns:
    fig_foreign_banks(matplotlib.pyplot figure): Figure containing the generated plot.

    """
    # choosing every third year for both variables
    years = data.loc[range(1, 120, 12), "Year"]
    banks = data.loc[range(1, 120, 12), "fb_num"]
    # empty figure object
    fig_foreign_banks = plt.figure()
    # number of foreign branches in Germany plot
    plt.bar(years, banks)
    plt.xlabel("Year")
    plt.ylabel("Number of Foreign Branches")
    plt.title("Number of Foreign Branches in Germany")
    return fig_foreign_banks


### Plots depicting bi-variate relationships between outcome and explanatory variables ###

# function showing the bi-variate relationship between financial development and labor cost percentage increase differences
def gen_scatter_plots(data):
    """Generates multiple scatter plots depicting the bi-variate relationship between financial development
    and income inequality, using several variables.

    Parameters:
    df(pandas.DataFrame): Data frame which contains the variables used for generating the plots.

    Returns:
    fig_scatter_plots (list): List of figures containing the scatter plots amongst selected variables.
    """
    # defining the variables used for the scatter plots
    x_variables = ["fin_dev_all", "fin_dev_db", "fin_dev_fb"]
    y_variables = ["fin_diff_all", "fin_diff_pc", "fin_diff_peh"]

    # empty list to store figures
    fig_scatter_plots = []

    # scatter plots
    # creating a nested loop to create all possible combinations
    for _i, x_var in enumerate(x_variables):
        for _j, y_var in enumerate(y_variables):
            # creating a new figure for each plot
            fig = plt.figure()
            # defining which variables to be plotted
            plt.scatter(data[x_var], data[y_var], color="blue")
            # labeling
            plt.xlabel(f"Indicator of Financial Development ({x_var})", color="darkred")
            plt.ylabel(f"Indicator of Income Inequality ({y_var})", color="darkred")
            plt.title(f"Bivariate Relationship between {x_var} and {y_var}")
            # adding the figure to the list
            fig_scatter_plots.append(fig)

    return fig_scatter_plots
