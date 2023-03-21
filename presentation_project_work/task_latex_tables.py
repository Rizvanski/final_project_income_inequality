"""Task for converting the tables into latex format."""

### packages ###
import pandas as pd
import pytask
from financial_development_and_income_inequality.config import BLD

### names of the tables ###
table_names = [
    "fixed_effects_baseline",
    "fixed_effects_robustness_checks",
    "ols_baseline",
    "ols_robustness_checks",
]

### depends and produces folders ###
@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            BLD / "python" / "tables" / f"{table}.csv",
            BLD / "latex" / "tables" / f"{table}.tex",
        )
        for table in table_names
    ],
)

### converting the tables for latex usage
def task_convert_tables(depends_on, produces):
    """Converts csv-file into latex tabular to include in paper."""
    table = pd.read_csv(depends_on)
    with open(produces, "w") as tf:
        tf.write(table.to_latex(na_rep="-", index=False))
