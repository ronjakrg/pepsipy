# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/ronjakrg/pepsipy/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                            |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------ | -------: | -------: | ------: | --------: |
| frontend/\_\_init\_\_.py                        |        0 |        0 |    100% |           |
| frontend/dashboard/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| frontend/dashboard/migrations/\_\_init\_\_.py   |        0 |        0 |    100% |           |
| frontend/dashboard/templatetags/\_\_init\_\_.py |        0 |        0 |    100% |           |
| frontend/dashboard/templatetags/utils.py        |        8 |        8 |      0% |      1-16 |
| frontend/dashboard/utils.py                     |       71 |       31 |     56% |73-82, 93-122, 132, 134, 143-144 |
| frontend/dashboard/views.py                     |       65 |       53 |     18% |23-103, 107-108, 116-120 |
| frontend/project/\_\_init\_\_.py                |        0 |        0 |    100% |           |
| src/pepsipy/\_\_init\_\_.py                     |        2 |        0 |    100% |           |
| src/pepsipy/api.py                              |      117 |       18 |     85% |   286-321 |
| src/pepsipy/constants.py                        |       16 |        0 |    100% |           |
| src/pepsipy/features.py                         |      141 |        1 |     99% |       153 |
| src/pepsipy/plots.py                            |      212 |       37 |     83% |63-70, 75-122, 244, 248, 254, 268, 287, 293, 323, 353, 491, 500, 509 |
| src/pepsipy/utils.py                            |       34 |        1 |     97% |        69 |
|                                       **TOTAL** |  **666** |  **149** | **78%** |           |


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