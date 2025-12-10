from glaciers import *

# import all functions to run base tests of outputs

def test_datetime():
	file_path = sorted(glob.glob("data/Karakoram/*_vm_*.tif"))
	assert paths_to_datetimeindex(file_path)[0] == '2019-03-18 - 2019-04-03'

def test_midpoint():
	geotiff_list = sorted(glob.glob("data/Karakoram/*_vm_*.tif"))

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
	assert mid_times[0].value == 1553558400000000000

def test_to_ds():
    import xarray as xr

    file_path = "data/Karakoram/*_vm_*.tif"
    assert isinstance(geotiff_to_ds(file_path), xr.Dataset) == True
