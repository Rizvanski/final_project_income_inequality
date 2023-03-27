# Financial Development and Income Inequality

### Effective Programming Practices for Economists Final Project

### University of Bonn, WS 22/23

### Author

- Haris Rizvanski (e-mail: haris.rizvanski@uni-bonn.de)

### About

This repository contains code for the project work on the topic of: "Financial
Development and Income Inequality". This project work was inspired by multiple papers
that already cover the relationship between financial development and income inequality.
Some examples include:

- Greenwood and Jovanovic (1990). “Financial development, growth,and the distribution of
  income”. In: Journal of political Economy 98.5, Part 1, pp. 1076–1107.
- Zlatko (2013). “Financial sector development and inequality: is there a financial
  Kuznets curve?” In: Journal of International Development 25.7, pp. 897–911.
- Park and Shin (2017). “Economic growth, financial development, and income inequality”.
  In: Emerging Markets Finance and Trade 53.12, pp. 2794–2825.

The data used in this project work is collected from different sources (Deutsche
Bundesbank, Eurostat, European Central Bank) for Germany in the period between 1991 and
2020\. In addition, new variables are generated which are more suitable for this project
work to better capture financial development and income inequality. For more detail
about the calculation of these variables, please refer to the pdf presentation file:
"financial_development_and_income_inequality_pres.pdf".

In total, there are two models applied with this data:

- OLS model
- Year time fixed effects model

Additionally, there are several graphical representations and tables that report the
results from the above models. These tables are transformed and adjusted for future use
in latex documents.

The aim of this project work is to apply the knowledge related with functional
programming practices, which was gained during the course: "Effective Programming
Practices for Economists", in the winter semester of 2022-2023, at the University of
Bonn.

### Requires

For a local machine to run this project, one has to have installed Python, an Anaconda
distribution and a Latex distribution. This project work was tested on Windows 11
operating system using:

- Python 3.11.0
- Anaconda 23.1.0
- MiKTeX 22.1

### Usage

All packages used in this project work can be found in the anaconda environment, named
final-project. In order to install the anaconda environment, one has to move to the root
folder of the repository and type `$ conda env create -f environment.yml`, and to
activate type `$ conda activate final-project`.

For the imports to properly work, one has to navigate through the terminal in the root
of the repository and type `$ conda develop `.

This project work was built using the pytask workflow management system. Once the
repository is cloned to a local machine, one has to type `$ pytask` from the terminal in
the root folder of the project.

### Project Structure

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
All of the source code is contained in the 'src' folder, while the output is generated
in the 'bld' folder. In addition, there is the folder 'presentation_project_work', where
the latex file is compiled and 'tests', where there are several tests for the functions
that create and apply the data.

The 'src' folder contains several subfolders where the data management, analysis and
creation of graphs and tables is performed. Here, the following subfolders can be found:

- 'analysis': includes code for applying the OLS and Time Fixed Effects models.
- 'data': contains the initial data files from which the data set is created.
- 'data_management': includes code for creating the initial and final versions of the
  data sets.
- 'final': contains code for generating graphs and tables of the estimates.

The 'bld' folder contains all of the output generated with the code in the 'src' folder.
Here, the following subfolders can be found:

- 'latex": includes the compiled presentation for the project work and tables converted
  into latex form.
- 'python': contains the generated data sets, estimates of the models, figures and
  tables.
