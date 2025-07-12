# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/ronjakrg/thesis-pepsi-package/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                          |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------- | -------: | -------: | ------: | --------: |
| frontend/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| frontend/dashboard/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| frontend/dashboard/migrations/\_\_init\_\_.py |        0 |        0 |    100% |           |
| frontend/dashboard/utils.py                   |       37 |       13 |     65% |48-62, 68-75 |
| frontend/dashboard/views.py                   |       69 |       18 |     74% |56-58, 77, 98-104, 108-109, 117-121 |
| frontend/project/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| src/pepsi/\_\_init\_\_.py                     |        2 |        0 |    100% |           |
| src/pepsi/calculator.py                       |       80 |       36 |     55% |55-60, 66, 69, 86-88, 109-111, 114-116, 123-126, 129-134, 141-145, 151-152, 172-173, 183-188, 199-200 |
| src/pepsi/constants.py                        |       15 |        0 |    100% |           |
| src/pepsi/features.py                         |      110 |       14 |     87% |38-43, 201-218 |
| src/pepsi/plots.py                            |      111 |       96 |     14% |26-67, 81-163, 171-191, 200-216, 224-235, 253-271, 287-302 |
| src/pepsi/utils.py                            |       13 |        0 |    100% |           |
|                                     **TOTAL** |  **437** |  **177** | **59%** |           |


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