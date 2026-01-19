# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/ronjakrg/pepsipy/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                            |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------ | -------: | -------: | ------: | --------: |
| frontend/\_\_init\_\_.py                        |        0 |        0 |    100% |           |
| frontend/dashboard/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| frontend/dashboard/constants.py                 |        7 |        0 |    100% |           |
| frontend/dashboard/import\_maxquant.py          |       69 |       69 |      0% |     5-158 |
| frontend/dashboard/migrations/\_\_init\_\_.py   |        0 |        0 |    100% |           |
| frontend/dashboard/templatetags/\_\_init\_\_.py |        0 |        0 |    100% |           |
| frontend/dashboard/templatetags/utils.py        |       10 |       10 |      0% |      1-18 |
| frontend/dashboard/utils.py                     |       94 |       45 |     52% |75-86, 97-126, 136, 138, 147-148, 176-189 |
| frontend/dashboard/views.py                     |       83 |       68 |     18% |27-130, 134-135, 143-147, 154-161 |
| frontend/project/\_\_init\_\_.py                |        0 |        0 |    100% |           |
| src/pepsipy/\_\_init\_\_.py                     |        2 |        0 |    100% |           |
| src/pepsipy/api.py                              |      118 |       20 |     83% |246, 295-331 |
| src/pepsipy/constants.py                        |       17 |        0 |    100% |           |
| src/pepsipy/features.py                         |      166 |        7 |     96% |98, 100, 102, 105-106, 197, 404 |
| src/pepsipy/plots.py                            |      221 |       42 |     81% |66-73, 78-125, 255, 259, 265, 279, 300, 306, 337, 366, 509, 515, 524, 536-563 |
| src/pepsipy/utils.py                            |       43 |        1 |     98% |        69 |
| **TOTAL**                                       |  **830** |  **262** | **68%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/ronjakrg/pepsipy/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/ronjakrg/pepsipy/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ronjakrg/pepsipy/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/ronjakrg/pepsipy/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fronjakrg%2Fpepsipy%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/ronjakrg/pepsipy/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.