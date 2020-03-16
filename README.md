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

