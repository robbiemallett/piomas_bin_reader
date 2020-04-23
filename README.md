# piomas_bin_reader
Python code to read raw binaries from UW PSC website and save as NetCDF4

Code in the jupyter notebook and .py files are identical.

Place raw data in the 'binaries' directory, run the code and it will output a netcdf file in 'output' directory.

This netcdf is self-describing and has the grid coordinates within it.

While the code attributes describe the 'sea ice thickness' variable, 
the code works for other variables too (just rename the strings)
