# Analyzing Surge Type Glacial Velocity and the Presence of the Karakoram Anomaly in Select N. Hemisphere Glaciers. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UCB-stat-159-f25/final-group06.git/HEAD)


## Overview
This repo contains an analysis comparing the South Rimo Glacier in the Karakoram with two other “Surge Type” glaciers: the Medvezhiy Glacier in the Pamir mountains of  nearby Tajikistan and the Sít’ Kusá Glacier in Alaska's St. Elias Mountains. The project seeks to answer whether there is evidence of the Karakoram anomaly within this comparison, using statistical analysis of glacial velocity.


## Data Set
The dataset is the [Select Northern Hemisphere Glacier Velocity Maps Using Customized autoRIFT and PlanetScope Imagery, Version 1.](https://nsidc.org/data/nsidc-0801/versions/1) The data set maps five select glaciers using CautoRIFT, “a pipeline that improves temporal coverage during periods of rapid glacier motion by adding pre-processed, daily high-resolution PlanetScope images and customized feature tracking parameters for each glacier to NASA's autonomous Repeat Image Feature Tracking (autoRIFT) algorithm for Sentinel-2 and Landsat imagery. Stable surface masks, area of interest (AOI) and glacier outlines, and ancillary data are also available for each glacier site” (Liu, J., Gendreau, M., Enderlin, E. M. & Aberle, R. (2025). For this project we used three of the five selected glaciers (listed in overview). The data is available via multiple forms of Earthdata download through the [National Snow and Ice Data Center.](https://nsidc.org/data/explore-data) For for increased ease of reproducibility, this project loads the data through the [earthaccess](https://earthaccess.readthedocs.io/en/stable/) Python library. 


## Project Website
The project's MyST website can be accessed [here](https://ucb-stat-159-f25.github.io/final-group06/).


## Repository Structure
The repository is structured as follows:  
`data/`: Contains the raw dataset and processed data files  
`figures/`: Contains the generated figures and plots  
`glaciers/`: Contains the functions and tests  
`eda.ipynb`: Notebook which loads in earth access data and performs initial preprocessing  
`main.ipynb`: Notebook which provides a comparative overview of the analysis and results  
`karakoram_analysis.ipynb`: Notebook containing the analysis of the data for the South Rimo Glacier in the Karakoram  
`non-karakoram_analysis.ipynb`: Notebook containing the analysis of the data for the Medvezhiy Glacier in Tajikistan and the Sít’ Kusá Glacier in Alaska  
`environment.yml`: Environment file with required packages for the project  
`Makefile`: Makefile to build JupyterBook for the repository and manage other tasks  


## Setup and Installation
1. Clone this repository:  
git clone https://github.com/UCB-stat-159-f25/final-group06.git  

2. Create and activate the `glaciers-env` environment:  
conda env create -f environment.yml OR make env  
conda activate glaciers

3. Install the IPython kernel with the `glaciers-env` environment:  
python -m ipykernel install --user --name glaciers-env --display-name "IPython - Glacier"  


## Usage
To make the environment, run:  
make env  

To execute all notebooks, run:  
make all 

To generate notebook pdfs, run:  
myst build `notebook_name`.ipynb --pdf


## Package Structure

The `glaciers` package is a collection of functions that facilitate the conversion, data formatting, and compatibility of the NASA earthaccess filelists for glaciers in the `NSIDC-0801` datasets. The package includes the following functions:  
`paths_to_datetimeindex(paths)`: This function takes in a filepath or list of filepaths and extracts the date information from the name of the file(s). It then converts the them to datetime format and returns the formatted list.  
`midpoint(t)`: This function simply takes in string of a date range and returns its midpoint.   
`geotiff_to_ds(data_path)`: This takes in a filepath or list of filepaths and converts the geotiff list to an xarray dataset with properly defined variable names, and is sorted by the midpoint time of each entry.  

The package uses the following external libraries:  
`glob` to search for filenames  
`xarray` and `rioxarray` for xarrary file usage/compatibility  
`pandas` for dataframe management/creation  
`datetime` for datetime file format usage in the xarrary dataset  
`re` to find certain filepaths by their name from the directory  


## Testing
To run tests, navigate to the root directory of the project and execute the following command:  
pytest  

The function tests exist in `glaciers/tests/test_glaciers.py`. The file contains the following tests:  
`test_datetime()` which tests the `paths_to_datetimeindex(paths)` function above by hardcoding in the true/expected value of the first outputted datetime value and compares the extracted value it obtains by running the function on our Karakoram dataset within the test. It passes if the two values match.  
`test_midpoint()` tests the `midpoint(t)` function above by manually creating an xarray dataset from the Karakoram geotiff list and uses the `midpoint(t)` function to create the midpoint dates for each entry and then sorting by that. The tests passes if the first extracted midpoint time matches the true/expected value that is asserted in the test.  
`test_to_ds()` which tests the `geotiff_to_ds(data_path)` function above. It simply check to ensure that the output of the function is in fact of the filetype Xarray Dataset and passes if it is.


## License
This project is licensed under the BSD 3-Clause License.

