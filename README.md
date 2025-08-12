# PEPSI: **PEP**tide **S**equence **I**nformation

[![CI](https://github.com/ronjakrg/thesis-pepsi-package/actions/workflows/ci.yml/badge.svg)](https://github.com/ronjakrg/thesis-pepsi-package/actions/workflows/ci.yml)
[![Coverage badge](https://github.com/ronjakrg/thesis-pepsi-package/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/ronjakrg/thesis-pepsi-package/tree/python-coverage-comment-action-data/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> [!NOTE]
> This repository is still a work in progress.

PEPSI is an open-source Python package that provides methods for computing a wide range of peptide features, including sequence composition, charge, hydrophobicity, and other physicochemical properties. All features can be calculated on an entire dataset or on a single peptide sequence of interest. Additionally, PEPSI offers a selection of visualisations, such as hydropathy profile or amino acid classification.
This work was conducted as part of the project 'Veni, Vidi, Visualization: Improving Analysis Communication for a Million-Dollar Machine' at the Data Analytics and Computational Statistics Chair, Hasso Plattner Institute.

| 💻 Python package | 📊 Web-based dashboard] | Miscellaneous |
|-------------------|-------------------------|-------|
| [Installation](#installation)<br>[Usage](#usage) | [Installation](#installation-1)<br>[Usage](#usage-1) | [Third-party resources](#third-party-resources)<br>[License](#license) |

# 💻 Python package
## Installation
> [!CAUTION]
> The release of the package on PyPI is still pending. See related [issue](https://github.com/pypi/support/issues/6869) for any updates.

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

1. Make sure you have a virtual environment manager installed, e.g., [Conda](https://www.anaconda.com/docs/getting-started/miniconda/install/) (recommended), or any other manager such as venv or Poetry.
2. Clone this repository and enter the frontend folder<br>
   ```
   git clone https://github.com/ronjakrg/thesis-pepsi-package.git
   cd thesis-pepsi-package/frontend
   ```
3. Create a virtual environment and install all necessary requirements<br>
   ```
   conda create pepsi
   conda activate pepsi
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
<img width="2240" height="1400" alt="Screenshot of dashboard" src="https://github.com/user-attachments/assets/e61d6bd7-6826-4323-8e2f-7a416edfdd5b" />

<br><br>
## Third-party resources
| Type    | Name                                                           | DOI                                                                  | Saved in                                     |
|---------|----------------------------------------------------------------|----------------------------------------------------------------------|----------------------------------------------|
| Dataset | Urinary peptidomics in youths with and without type 1 diabetes | [10.1074/mcp.RA119.001858](https://doi.org/10.1074/mcp.RA119.001858) | - `/data/peptides.csv`<br>- `/data/metadata.csv` |
| Code    | Isoelectric Point Calculator 2.0                               | [10.1093/nar/gkab295](https://doi.org/10.1093/nar/gkab295)           | - `/src/pepsi/external/ipc-2.0.1`               |

## License
This project is licensed under the [MIT License](./LICENSE).
