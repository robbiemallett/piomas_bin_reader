#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import struct
import xarray as xr


# In[2]:


grids = {}

for i in ['lon','lat']:

    grid = np.array(pd.read_csv(f'grids/{i}grid.dat',header=None, delim_whitespace=True))

    flat_grid = grid.ravel()

    shaped_grid = flat_grid.reshape(360,120)
    
    grids[i] = shaped_grid


# In[3]:


def process_piomass(year):
    
    binary_dir = f'binaries/heff.H{year}'
    
    ############################################################
    
    # Read File
    
    with open(binary_dir, mode='rb') as file:
    
        fileContent = file.read()
        data = struct.unpack("f" * (len(fileContent)// 4), fileContent)
        
    ############################################################
    
    # Put it in a 3D array
        
        native_data = np.full((12,360,120),np.nan)

        for month in range(1,13):
            
            start = (month-1)*(360*120)
            end = month*(360*120)
            thickness_list = np.array(data[start:end])
            
            gridded = thickness_list.reshape(360,120)
            native_data[month-1,:,:] = gridded
            
          
    ############################################################
        
    # Output to NetCDF4
        
        ds = xr.Dataset( data_vars={'thickness':(['t','x','y'],native_data)},

                         coords =  {'lon':(['x','y'],grids['lon']),
                                    'lat':(['x','y'],grids['lat']),
                                    'month':(['t'],np.array(range(1,13)))})
        
        ds.attrs['data_name'] = 'Monthly mean Piomass sea ice thickness data'
        
        ds.attrs['description'] = """Sea ice thickness in meters on the native 360x120 grid, 
                                    data produced by University of Washington Polar Science Center"""
        
        ds.attrs['year'] = f"""these data are for the year {year}"""
        
        ds.attrs['citation'] = """When using this data please use the citation: 
                                Zhang, Jinlun and D.A. Rothrock: Modeling global sea 
                                ice with a thickness and enthalpy distribution model 
                                in generalized curvilinear coordinates,
                                Mon. Wea. Rev. 131(5), 681-697, 2003."""
        
        ds.attrs['code to read'] = """  # Example code to read a month of this data 
    
                                        def read_month_of_piomass(year,month): 
    
                                            data_dir = 'output/' 

                                            with xr.open_dataset(f'{data_dir}{year}.nc') as data: 

                                                ds_month = data.where(int(month) == data.month, drop =True) 

                                                return(ds_month)"""
        
        ds.attrs['python author'] = """Robbie Mallett wrote this python code. If there's a problem with it, 
                                        email him at robbie.mallett.17@ucl.ac.uk"""
                                
        
        

        output_dir = f'output/'

        ds.to_netcdf(f'{output_dir}{year}.nc','w')
        


# In[4]:


for year in range(1993,1994):
    
    process_piomass(year)


# In[ ]:




