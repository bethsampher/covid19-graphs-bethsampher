# Python code compliance

## Instructions

This must be assessed by the pycodestyle and pylint tools. 
Please note your code must conform to the 79 characters line length limit. 
You must use the `pycodestyle` and `pylint` tools and include the output for 
all python code in this file `README_PEP8.md`. 

pycodestyle should not produce any warnings.

It is acceptable to have pylint warnings (for instance missing docstrings for unit tests)
 provided they are justified in README_PEP8.md..

## `pycodestyle -v .` output
```
directory .
checking ./setup.py
directory ./.pytest_cache
directory ./.pytest_cache/v
directory ./.pytest_cache/v/cache
directory ./bin
directory ./out
directory ./out/graphs
directory ./covid19_graphs
checking ./covid19_graphs/command_line_script.py
checking ./covid19_graphs/covid19_processing.py
directory ./covid19_graphs/tests
checking ./covid19_graphs/tests/test_covid19_processing.py
checking ./covid19_graphs/tests/test_parse_command_line_args.py
directory ./.github
directory ./.github/workflows
directory ./.ipynb_checkpoints
directory ./covid19_graphs.egg-info
```

## `pylint covid19_graphs` output
```
************* Module covid19_processing
covid19_graphs/covid19_processing.py:99:8: C0103: Variable name "uk" doesn't conform to snake_case naming style (invalid-name)
covid19_graphs/covid19_processing.py:131:15: W0703: Catching too general exception Exception (broad-except)
```
```
$ pylint *.py
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

## Justification for pylint warnings

uk is an appropriate variable name for data from the UK  
Used Exception rather than anything more specific as there could be a number of different errors when processing data
