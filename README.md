# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/ronjakrg/thesis-pepsi-package/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                          |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------- | -------: | -------: | ------: | --------: |
| frontend/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| frontend/dashboard/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| frontend/dashboard/migrations/\_\_init\_\_.py |        0 |        0 |    100% |           |
| frontend/dashboard/utils.py                   |       66 |       11 |     83% |80-87, 108, 119, 131, 133 |
| frontend/dashboard/views.py                   |       62 |       10 |     84% |57-59, 96-97, 105-109 |
| frontend/project/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| src/pepsi/\_\_init\_\_.py                     |        2 |        0 |    100% |           |
| src/pepsi/calculator.py                       |       85 |       37 |     56% |59-64, 70, 73, 94-96, 120-122, 125-127, 134-137, 140-145, 152-156, 162-163, 186-187, 197-202, 213-217 |
| src/pepsi/constants.py                        |       16 |        0 |    100% |           |
| src/pepsi/features.py                         |      128 |        3 |     98% |37-42, 222 |
| src/pepsi/plots.py                            |      167 |      150 |     10% |28-75, 90-173, 181-201, 210-226, 235-269, 287-313, 329-348, 359-474 |
| src/pepsi/utils.py                            |       17 |        2 |     88% |     47-48 |
|                                     **TOTAL** |  **543** |  **213** | **61%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/ronjakrg/thesis-pepsi-package/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/ronjakrg/thesis-pepsi-package/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ronjakrg/thesis-pepsi-package/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/ronjakrg/thesis-pepsi-package/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fronjakrg%2Fthesis-pepsi-package%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/ronjakrg/thesis-pepsi-package/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.