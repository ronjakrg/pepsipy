# PEPSI: **PEP**tide **S**equence **I**nformation

[![CI](https://github.com/ronjakrg/thesis-pepsi-package/actions/workflows/ci.yml/badge.svg)](https://github.com/ronjakrg/thesis-pepsi-package/actions/workflows/ci.yml)
[![Coverage badge](https://github.com/ronjakrg/thesis-pepsi-package/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/ronjakrg/thesis-pepsi-package/tree/python-coverage-comment-action-data/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> [!NOTE]
> This repository is still a work in progress.

PEPSI is an open-source Python package that provides methods for computing a wide range of peptide features, including sequence composition, charge, hydrophobicity, and other physicochemical properties. All features can be calculated on an entire dataset or on a single peptide sequence of interest. Additionally, PEPSI offers a selection of visualisations, such as hydropathy profile or amino acid classification.
This work was conducted as part of the project 'Veni, Vidi, Visualization: Improving Analysis Communication for a Million-Dollar Machine' at the Data Analytics and Computational Statistics Chair, Hasso Plattner Institute.

## ⚙️ Setup & Installation
### PEPSI Package

1. Make sure to have pip installed (Tutorial available [here](https://pip.pypa.io/en/stable/installation/))
2. Update pip in your console <br>
   ```python -m pip install --upgrade pip```
3. Install PEPSI <br>
   ```pip install pepsi```
4. Import and use PEPSI in your project! ✨ For more details, see section **How to use PEPSI**

### PEPSI Dashboard
1. Make sure to have conda installed (Tutorial available [here](https://www.anaconda.com/docs/getting-started/miniconda/install/)
2. Clone this repository and enter the frontend folder<br>
   ```
   git clone https://github.com/ronjakrg/thesis-pepsi-package.git
   cd thesis-pepsi-package/frontend
   ```
3. Create a virtual environment and install necessary requirements<br>
   ```
   conda create pepsi
   conda activate pepsi
   pip install -r requirements.txt
   ```
4. Start the server<br>
   ```
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/` in the browser of your choice to use the PEPSI Dashboard! ✨ For more details, see section **How to use PEPSI**

## 📌 How to use PEPSI
(Coming soon!)



This project is licensed under the [MIT License](./LICENSE).
