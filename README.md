# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/ronjakrg/thesis-pepsi-package/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                          |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------- | -------: | -------: | ------: | --------: |
| frontend/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| frontend/dashboard/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| frontend/dashboard/migrations/\_\_init\_\_.py |        0 |        0 |    100% |           |
| frontend/dashboard/utils.py                   |       55 |        8 |     85% |78-85, 110 |
| frontend/dashboard/views.py                   |       63 |       11 |     83% |57-59, 79, 98-99, 107-111 |
| frontend/project/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| src/pepsi/\_\_init\_\_.py                     |        2 |        0 |    100% |           |
| src/pepsi/calculator.py                       |       83 |       37 |     55% |57-62, 68, 71, 90-92, 113-115, 118-120, 127-130, 133-138, 145-149, 155-156, 178-179, 189-194, 205-209 |
| src/pepsi/constants.py                        |       15 |        0 |    100% |           |
| src/pepsi/features.py                         |      122 |        3 |     98% |37-42, 208 |
| src/pepsi/plots.py                            |      111 |       96 |     14% |26-67, 81-163, 171-191, 200-216, 224-235, 253-271, 287-302 |
| src/pepsi/utils.py                            |       13 |        0 |    100% |           |
|                                     **TOTAL** |  **464** |  **155** | **67%** |           |


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