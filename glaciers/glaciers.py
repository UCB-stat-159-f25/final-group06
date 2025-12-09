"""
glacier.py

Version 0.1.0
December 5, 2025
Ethan Briel, Param Gandhi, Eden Lange, and Char Tomlinson

This module provides tools for date conversion and data formatting as well as 
reading in data included in the repository. 


"""

import glob
import xarray as xr
import rioxarray
import pandas as pd
import numpy as np
from datetime import datetime
import re
import matplotlib.pyplot as plt
import os

def paths_to_datetimeindex(paths):
    """
    Extract the FIRST date from each filename and return a pandas.DatetimeIndex.
    string_slice should give the full date range substring.
    Example substring: '20190606-20190622'
    """
    labels = []
    for p in paths:
        fname = p.split('/')[-1]
        dates = re.findall(r"\d{8}", fname)
        if len(dates) < 2:
            raise ValueError(f"File does not contain two dates: {fname}")
        start = pd.to_datetime(dates[0]).strftime("%Y-%m-%d")
        end = pd.to_datetime(dates[1]).strftime("%Y-%m-%d")
        labels.append(f"{start} - {end}")
    return labels

def midpoint(t):
    nums = re.findall(r"\d{4}\d{2}\d{2}", t.replace("-", ""))
    
    if len(nums) == 2:
        d1 = pd.to_datetime(nums[0])
        d2 = pd.to_datetime(nums[1])
        return d1 + (d2 - d1) / 2
    else:
        return pd.NaT


def geotiff_to_ds(geotiff_list, time):
	"""
	geotiff_list: geotiff_list = glob.glob(data_path) where data_path is the string data path for desired glacier data

    time: result of using the paths_to_datetimeindex function
	"""
		
	# Create variable used for time axis
	time_var = xr.Variable('time', time)
		
	# Load in and concatenate all individual GeoTIFFs
	geotiffs_da = xr.concat(
		[rioxarray.open_rasterio(i) for i in geotiff_list],
		dim=time_var
	)
		
	# Covert our xarray.DataArray into a xarray.Dataset
	geotiffs_ds = geotiffs_da.to_dataset('band')
		
	# Rename the variable to a more useful name
	geotiffs_ds = geotiffs_ds.rename({1: 'x_vel', 2: 'y_vel', 3: 'vel_magnitude'})
		
	# Print the output
	return(geotiffs_ds)

