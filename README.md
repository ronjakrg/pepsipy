# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/ronjakrg/thesis-pepsi-package/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                          |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------- | -------: | -------: | ------: | --------: |
| frontend/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| frontend/dashboard/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| frontend/dashboard/migrations/\_\_init\_\_.py |        0 |        0 |    100% |           |
| frontend/dashboard/utils.py                   |       37 |       13 |     65% |48-62, 68-75 |
| frontend/dashboard/views.py                   |       61 |       11 |     82% |56-58, 77, 98-99, 107-111 |
| frontend/project/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| src/pepsi/\_\_init\_\_.py                     |        2 |        0 |    100% |           |
| src/pepsi/calculator.py                       |       64 |       28 |     56% |48-52, 56, 59, 72-74, 94-96, 103-106, 113-117, 123-124, 142-143, 152-153, 163-164 |
| src/pepsi/constants.py                        |       15 |        0 |    100% |           |
| src/pepsi/features.py                         |      103 |       14 |     86% |37-42, 192-209 |
| src/pepsi/plots.py                            |      102 |       89 |     13% |25-68, 82-164, 172-192, 201-217, 235-255, 271-287 |
| src/pepsi/utils.py                            |       17 |        0 |    100% |           |
|                                     **TOTAL** |  **401** |  **155** | **61%** |           |


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