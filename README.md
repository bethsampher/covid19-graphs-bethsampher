![Python application](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/workflows/Python%20application/badge.svg)

# A tool to download and plot Covid-19 disease outbreak data

Uses data from [John Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)

## Installing the `covid19_graphs` package (for developers)

To install the `covid19_graphs` package first git clone this repo
then 
```
cd REPO_DIR
pip install -e . 
```
To test your installation run the `covid19_graphs` command line script.
```
covid19_graphs -h
```
You should get an output like
```
$ covid19_graphs -h
usage: covid19_graphs [-h] [-g] [-d] OUT_DIR

tool to download and process COVID-19 data

positional arguments:
  OUT_DIR      directory for output files

optional arguments:
  -h, --help   show this help message and exit
  -g, --graphs option to specify for graphs
  -d, --debug  turn on debug message logging output
```

## Using the script

covid19_graphs must be run with the name of an output directory to be created, OUT_DIR. Output files will be put in here.   
If a directory with the same name already exists, the script will exit with an error message informing you of this.  
The script will also exit with an error message if the data is not retrieved successfully from [John Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series), or if this data cannot be processed.    
For help use the **-h** option.

Other options that can be specified are: 
* **--graphs, -g**  
   Outputs png files of graphs from the data
* **--debug, -d**  
   For developers, logs output

## Example output files

Output CSVs produced by running the script on 16/03/20 (data for the 16th was not yet available when the script was run):  
```
$ covid19_graphs -g out
```
* [out/cases.csv](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/cases.csv)
* [out/deaths.csv](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/deaths.csv)
* [out/recovered.csv](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/recovered.csv)   

Output graphs (found in the graphs directory within the specified output directory):
* out/graphs/cases.png  
   ![Cases graph](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/graphs/2020-03-16-cases.png)
* out/graphs/deaths.png  
  ![Deaths graph](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/graphs/2020-03-16-deaths.png)
* out/graphs/recovered.png  
  ![Recovered graph](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/graphs/2020-03-16-recovered.png)

## Advanced features

* Use of pandas
* Use of mocking in tests
* Error handling

## Testing

Command line is tested in [tests/test_parse_command_line_args.py] (https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/covid19_graphs/tests/test_parse_command_line_args.py) and most methods in covid19_processing.py are tested in [tests/test_covid19_processing.py](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/covid19_graphs/tests/test_covid19_processing.py):

```
$ pytest -v

============================================================================== test session starts ===============================================================================
platform darwin -- Python 3.7.4, pytest-5.2.1, py-1.8.0, pluggy-0.13.0 -- /Users/bs15/opt/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/bs15/ARU/ISE/covid19-graphs-bethsampher
plugins: arraydiff-0.3, remotedata-0.3.2, mock-2.0.0, doctestplus-0.4.0, openfiles-0.4.0, cov-2.8.1
collected 16 items

covid19_graphs/tests/test_covid19_processing.py::test_out_dir PASSED                                                                                                       [  6%]
covid19_graphs/tests/test_covid19_processing.py::test_existing_out_dir PASSED                                                                                              [ 12%]
covid19_graphs/tests/test_covid19_processing.py::test_download_from_github PASSED                                                                                          [ 18%]
covid19_graphs/tests/test_covid19_processing.py::test_download_from_github_fail PASSED                                                                                     [ 25%]
covid19_graphs/tests/test_covid19_processing.py::test_get_continent PASSED                                                                                                 [ 31%]
covid19_graphs/tests/test_covid19_processing.py::test_filter_data PASSED                                                                                                   [ 37%]
covid19_graphs/tests/test_covid19_processing.py::test_store_data_for_csv PASSED                                                                                            [ 43%]
covid19_graphs/tests/test_covid19_processing.py::test_store_data_for_csv_fail PASSED                                                                                       [ 50%]
covid19_graphs/tests/test_covid19_processing.py::test_create_out_dir PASSED                                                                                                [ 56%]
covid19_graphs/tests/test_covid19_processing.py::test_write_csv_files PASSED                                                                                               [ 62%]
covid19_graphs/tests/test_covid19_processing.py::test_remove_unrecongnised_column PASSED                                                                                   [ 68%]
covid19_graphs/tests/test_covid19_processing.py::test_create_graph_dir PASSED                                                                                              [ 75%]
covid19_graphs/tests/test_parse_command_line_args.py::test_supply_output_dir PASSED                                                                                        [ 81%]
covid19_graphs/tests/test_parse_command_line_args.py::test_with_empty_args_raises_error PASSED                                                                             [ 87%]
covid19_graphs/tests/test_parse_command_line_args.py::test_with_invalid_option_raises_error PASSED                                                                         [ 93%]
covid19_graphs/tests/test_parse_command_line_args.py::test_supply_2_strings_raises_error PASSED                                                                            [100%]

=============================================================================== 16 passed in 2.78s ===============================================================================
```

For set_labels, make_axes and write_png_files, I took a more manual approach by running:
```
$ covid19_processing -g out
```
I then opened the png files and checked the graphs look correct, which they do here:
![Cases graph](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/graphs/2020-03-16-cases.png)
![Deaths graph](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/graphs/2020-03-16-deaths.png)
![Recovered graph](https://github.com/ARU-Bioinf-ISE/covid19-graphs-bethsampher/blob/master/out/graphs/2020-03-16-recovered.png)
