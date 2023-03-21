"""Tasks for compiling the presentation of the project work."""

### packages ###
import shutil

import pytask
from financial_development_and_income_inequality.config import BLD, PAPER_DIR
from pytask_latex import compilation_steps as cs

### document used for compiling the pdf file ###
document = "financial_development_and_income_inequality_pres"


@pytask.mark.latex(
    script=PAPER_DIR / f"{document}.tex",
    document=BLD / "latex" / f"{document}.pdf",
    compilation_steps=cs.latexmk(
        options=(
            "--pdf",
            "--interaction=nonstopmode",
            "--synctex=1",
            "--cd",
            "--quiet",
            "--shell-escape",
        ),
    ),
)
@pytask.mark.task(id=document)
def task_compile_document():
    """Compile the document specified in the latex decorator."""


kwargs = {
    "depends_on": BLD / "latex" / f"{document}.pdf",
    "produces": BLD.parent.resolve() / f"{document}.pdf",
}


@pytask.mark.task(id=document, kwargs=kwargs)
def task_copy_to_root(depends_on, produces):
    """Copy a document to the root directory for easier retrieval."""
    shutil.copy(depends_on, produces)
