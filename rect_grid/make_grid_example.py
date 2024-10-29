
import netCDF4
import numpy as np

import matplotlib.pyplot as plt

# make a little grid:

node_lon = np.linspace(-26, -22, 13)
node_lat = np.linspace(30, 33, 10)

cell_lon = (node_lon[1:] + node_lon[:-1]) / 2
cell_lat = (node_lat[1:] + node_lat[:-1]) / 2


# Define the bounds:
bounds_lon = np.zeros((len(node_lon)-1, 2))
bounds_lon[:, 0] = node_lon[:-1]
bounds_lon[:, 1] = node_lon[1:]

bounds_lat = np.zeros((len(node_lat)-1, 2))
bounds_lat[:, 0] = node_lat[:-1]
bounds_lat[:, 1] = node_lat[1:]

# Some data on the cells:
data = np.random.random_sample((len(node_lon) - 1, len(node_lat) - 1))

# some data on the nodes:
node_data = np.random.random_sample((len(node_lon), len(node_lat)))

# create the file:

with netCDF4.Dataset("rect_grid.nc", mode='w') as ncds:
    ncds.createDimension("node_lon", len(node_lon))
    ncds.createDimension("node_lat", len(node_lat))
    ncds.createDimension("cell_lon", data.shape[0])
    ncds.createDimension("cell_lat", data.shape[1])
    ncds.createDimension("two", 2)

    node_lon_var = ncds.createVariable("node_lon", node_lat.dtype, ("node_lon"))
    node_lon_var[:] = node_lon
    node_lon_var.standard_name = "longitude"
    node_lon_var.units = "degrees_east"
    node_lat_var = ncds.createVariable("node_lat", node_lat.dtype, ("node_lat"))
    node_lat_var[:] = node_lat
    node_lat_var.standard_name = "latitude"
    node_lat_var.units = "degrees_north"

    cell_lon_var = ncds.createVariable("cell_lon", cell_lon.dtype, ("cell_lon"))
    cell_lon_var[:] = cell_lon
    cell_lon_var.standard_name = "longitude"
    cell_lon_var.units = "degrees_east"
    cell_lon_var.bounds = "bounds_lon"

    cell_lat_var = ncds.createVariable("cell_lat", cell_lat.dtype, ("cell_lat"))
    cell_lat_var[:] = cell_lat
    cell_lat_var.standard_name = "latitude"
    cell_lat_var.units = "degrees_east"
    cell_lat_var.bounds = "bounds_lat"


    bounds_lon_var = ncds.createVariable("bounds_lon", node_lat.dtype, ("cell_lon", "two"))
    bounds_lon_var[:] = bounds_lon

    bounds_lat_var = ncds.createVariable("bounds_lat", node_lat.dtype, ("cell_lat", "two"))
    bounds_lat_var[:] = bounds_lat


    # Some data on the cells:

    data_var = ncds.createVariable("data", data.dtype, ("cell_lon", "cell_lat"))
    data_var[:] = data
    data_var.cell_methods="area: mean"
    data_var.coordinates = "cell_lon cell_lat"

    # Some data on the nodes:

    node_data_var = ncds.createVariable("node_data", node_data.dtype, ("node_lon", "node_lat"))
    node_data_var[:] = node_data
    node_data_var.cell_methods="point"
    node_data_var.coordinates = "node_lon node_lat"

# Plot the grid

LAT, LON = np.meshgrid(node_lon, node_lat)

# plt.ion

fig, ax = plt.subplots()
ax.plot(LON.flat, LAT.flat, 'ok')
for lon in node_lon:
    ax.plot((node_lat[0], node_lat[-1]), (lon, lon), 'k')
for lat in node_lat:
    ax.plot((lat, lat), (node_lon[0], node_lon[-1]),  'k')


fig.savefig('basic_grid.png')




