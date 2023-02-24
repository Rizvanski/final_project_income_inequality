"""Task file related with generating plots for the ols and time fixed effects models."""

### packages ###
import pandas as pd
import pytask

### folders and functions used for the task file ###
from financial_development_and_income_inequality.config import BLD
from financial_development_and_income_inequality.final.descriptive_statistics_plots import (
    foreign_banks_increase_plot,
    gen_scatter_plots,
    labor_cost_increase_plot,
)


# input file
@pytask.mark.depends_on(BLD / "python" / "data" / "final_data_set.pkl")

# output files
@pytask.mark.produces(
    [
        BLD / "python" / "figures" / "labor_cost_increase.png",
        BLD / "python" / "figures" / "foreign_banks_presence.png",
        BLD / "python" / "figures" / "scatter_plot1.png",
        BLD / "python" / "figures" / "scatter_plot2.png",
        BLD / "python" / "figures" / "scatter_plot3.png",
        BLD / "python" / "figures" / "scatter_plot4.png",
        BLD / "python" / "figures" / "scatter_plot5.png",
        BLD / "python" / "figures" / "scatter_plot6.png",
        BLD / "python" / "figures" / "scatter_plot7.png",
        BLD / "python" / "figures" / "scatter_plot8.png",
        BLD / "python" / "figures" / "scatter_plot9.png",
    ],
)
def task_generate_plots(depends_on, produces):
    """Creates and stores several plots depicting the descriptive statistics of the data.

    Parameters:
    depends_on (pathlib.Path): The path to the directory where the finalized version of the data set is stored.
    produces (pathlib.Path): The paths to the directory where plots are stored in a "png" format.

    Returns:
    None

    """
    # loading final_data_set
    data = pd.read_pickle(depends_on)
    # generating plots using the functions
    # labor cost increase
    labor_cost_increase = labor_cost_increase_plot(data)
    # foreign banks presence
    foreign_banks_presence = foreign_banks_increase_plot(data)
    # scatter plots showing the relationship between outcome and explanatory variables
    scatter_plots = gen_scatter_plots(data)
    # saving the plots in the specified output directory
    labor_cost_increase.savefig(produces[0])
    foreign_banks_presence.savefig(produces[1])
    for i, fig in enumerate(scatter_plots):
        fig.savefig(produces[i + 2])
