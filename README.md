# PEPSI: PEPtide Sequence Information

[![CI](https://github.com/ronjakrg/thesis-pepsi-package/actions/workflows/ci.yml/badge.svg)](https://github.com/ronjakrg/thesis-pepsi-package/actions/workflows/ci.yml)
[![Coverage badge](https://github.com/ronjakrg/thesis-pepsi-package/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/ronjakrg/thesis-pepsi-package/tree/python-coverage-comment-action-data/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

PEPSIPy (**PEP**tide **S**equence **I**nformation for **Py**thon) is an open-source Python library that provides methods for computing a wide range of peptide features, including sequence composition, charge, hydrophobicity, and other physicochemical properties. All features can be calculated on an entire dataset or on a single peptide sequence of interest. Additionally, PEPSI offers a selection of visualisations, such as hydropathy profile or amino acid classification. <br>
This work was conducted as part of the project 'Veni, Vidi, Visualization: Improving Analysis Communication for a Million-Dollar Machine' at the Data Analytics and Computational Statistics Chair, Hasso Plattner Institute.

| 💻 Python library | 📊 Web-based dashboard | Miscellaneous |
|-------------------|------------------------|---------------|
| [Installation](#installation)<br>[Usage](#usage) | [Installation](#installation-1)<br>[Usage](#usage-1) | [Third-party resources](#third-party-resources)<br>[License](#license) |

# 💻 Python library
## Installation

1. Make sure you have [pip](https://pip.pypa.io/en/stable/installation/) installed
2. Update pip in your console <br>
   ```python -m pip install --upgrade pip```
3. Install PEPSI <br>
   ```pip install pepsi```
4. Import and use PEPSI in your project!

## Usage
1. Initialize a calculator instance
   ```
   import pandas as pd
   from pepsi import Calculator
   calc = Calculator(
      dataset=pd.read_csv("data/peptides.csv"),
      metadata=pd.read_csv("data/metadata.csv"),
      seq="SVIDQSRVLNLGPITR",
   )
   ```
2. Select desired features and plots with related parameters
   ```
   calc.set_feature_params(
      gravy=True,
      molecular_weight=True,
   )
   calc.set_plot_params(
      hydropathy_profile=True,
      classification=True,
      classification_classify_by="charge",
   )
   ```
3. Compute and show results
   ```
   print(calc.get_features())
   plots = calc.get_plots()
   for plot in plots:
      plot.show()
   ```

# 📊 Web-based dashboard
## Installation

1. Make sure you have a virtual environment manager available, e.g., [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) (recommended), or any other manager such as Conda or Poetry.
2. Clone this repository and enter the frontend folder<br>
   ```
   git clone https://github.com/ronjakrg/pepsipy.git
   cd pepsipy/frontend
   ```
3. Create and activate a virtual environment and install all necessary requirements<br>
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Start the server<br>
   ```
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/` in the browser of your choice to use the PEPSI Dashboard!

## Usage
1. Select a dataset and a metadata file (must be uploaded to the `/data` folder) and a peptide sequence of interest.
2. Select desired features and plots with related parameters
3. Click on 'Calculate' and inspect results

<img width="2240" height="1400" alt="Screenshot of PEPSI Dashboard" src="https://github.com/user-attachments/assets/48d29756-8d5d-44d0-b187-278f37278940" />

<br><br>
## Third-party resources
| Type    | Name                                                           | DOI                                                                  | Saved in                                     |
|---------|----------------------------------------------------------------|----------------------------------------------------------------------|----------------------------------------------|
| Dataset | Urinary peptidomics in youths with and without type 1 diabetes | [10.1074/mcp.RA119.001858](https://doi.org/10.1074/mcp.RA119.001858) | - `/data/peptides.csv`<br>- `/data/metadata.csv` |
| Code    | Isoelectric Point Calculator 2.0                               | [10.1093/nar/gkab295](https://doi.org/10.1093/nar/gkab295)           | - `/src/pepsi/external/ipc-2.0.1`               |

## License
This project is licensed under the [MIT License](./LICENSE).
