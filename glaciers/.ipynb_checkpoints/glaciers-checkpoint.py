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
    Extract the FIRST date range from each filename and return a pandas.DatetimeIndex.
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


def geotiff_to_ds(data_path):
	"""
	data_path: path to stored data in string format
		example: "data/Karakoram/*_vm*.tif"
	"""

	geotiff_list = glob.glob(data_path)
		
	# Create variable used for time axis
	time_var = xr.Variable('time', paths_to_datetimeindex(geotiff_list))
		
	# Load in and concatenate all individual GeoTIFFs
	geotiffs_da = xr.concat(
		[rioxarray.open_rasterio(i) for i in geotiff_list],
		dim=time_var
	)
		
	# Covert our xarray.DataArray into a xarray.Dataset
	geotiffs_ds = geotiffs_da.to_dataset('band')
		
	# Rename the variable to a more useful name
	geotiffs_ds = geotiffs_ds.rename({1: 'x_vel', 2: 'y_vel', 3: 'vel_magnitude'})
		
	#Adding midpoint time for sorting
	mid_times = [midpoint(t) for t in geotiffs_ds.time.values]
	geotiffs_ds = geotiffs_ds.assign_coords(mid_time=("time", mid_times))
	geotiffs_ds = geotiffs_ds.sortby("mid_time")
		
	# Print the output
	return(geotiffs_ds)

