# Handling rectangular grids in CF

a Rectangular grid is defined, for this document, as a grid (or mesh) in which:

- Each cell is rectangular (in a given coordinate system)
- The cells align exactly with the X and Y (or latitude and longitude) directions.

NOTE: This is slightly more complex than a "regular" grid, in which all the cells are the same size -- in this case the width or height of the cells may change, but all the cells in a "row" will have the same height, and all the cells in a "column" have the same width.

A couple more (recursive) definitions:
- node: the corner points of the cells
- cell: region enclosed by nodes

With this definition, you can fully define the grid with a 2 1D vectors, defining the location of the nodes of the grid, e.g.

```
 node_lon = -26, -25.6666666666667, -25.3333333333333, -25,
    -24.6666666666667, -24.3333333333333, -24, -23.6666666666667,
    -23.3333333333333, -23, -22.6666666666667, -22.3333333333333, -22 ;

 node_lat = 30, 30.3333333333333, 30.6666666666667, 31, 31.3333333333333,
    31.6666666666667, 32, 32.3333333333333, 32.6666666666667, 33 ;
```

This fully describes a simple grid:

![plot of rectangular grid](basic_grid.png "rect grid")

In this plot, the dots are the nodes of the grid, and the recrangular boxes are the cells.

## Data associated with the grid.

These types of grids are often used in oceanographic, and other, modeling applications. In that case, the model results can be "located" at different parts of the grid:

### On the nodes:

On the nodes: there is a value associated with each node of the grid.
These are usually "point" values -- that is, they are the value of some parmeter at those particular points.

### On the cells:

Model results are also often associated not with the nodes, but rather with the cells. In this case, there  is one value for each cell, rather than one for each node.
Sometimes those value are defined at a point within the cell (commonly the center),
and sometimes, the value is associated the cell  itself -- for example an average value over the  entire cell.

## Representing this in CF.

CF does not have the concept of a "grid" or "mesh" per-se (except in CF > 1.11, which incorporates the UGRID standard for unstructured meshes).

It does, however, have the concept of coordinates and cells, which can be used to express a rectangular grid.

### Defining the grid:

The nodes can be defined in terms of the latitude and longitude (x,y) arrays. If you set the name of the dimension equal to the name of the variable, CF interprets that as a "coordinate", so we can define the grid as so:

```
dimensions:
    node_lat = 10 ;
    node_lon = 13 ;

variables:

float node_lat(node_lat) ;
    lat:long_name = "latitude of the nodes" ;
    lat:units = "degrees_north" ;
    lat:standard_name = "latitude" ;

float node_lon(node_lon) ;
    lon:long_name = "longitude of the nodes" ;
    lon:units = "degrees_east" ;
    lon:standard_name = "longitude" ;
```

All good.

### Data on the nodes:

Data associated with the nodes of this grid are pretty straightforward.

This is the "standard" data layout originally used by COARDS: CF Sec 5.1

Give them the nodes as coordinates:

```
dimensions:
    node_lat = 10 ;
    node_lon = 13 ;

variables:

float node_lat(node_lat) ;
    lat:long_name = "latitude of the nodes" ;
    lat:units = "degrees_north" ;
    lat:standard_name = "latitude" ;

float node_lon(node_lon) ;
    lon:long_name = "longitude of the nodes" ;
    lon:units = "degrees_east" ;
    lon:standard_name = "longitude" ;

double node_data(node_lon, node_lat) ;
        node_data:cell_methods = "point" ;
        node_data:coordinates = "node_lon node_lat" ;
```

So now there is data associated with positions -- good. And the positions are coordinate variables, which are known to be monotonic. It's defined where all the points are in space, and the 1-D monotonic coordinate variables indicate that the is a rectangular grid, so interpolation, etc, can be done.

### Data on the cells:

There are one fewer cells than nodes in each direction, so you need new dimensions for data on the cells, and then you can define the data arrays for the cells:

```
dimensions:
    node_lat = 10 ;
    node_lon = 13 ;
    cell_lat = 9 ;
    cell_lon = 12 ;

double data(cell_lon, cell_lat) ;
    data:name = "temperature";
    data:units = "C";
```

All good -- but that's not enough to know where these data apply to, or what it means. CF requires "coordinates" to specify that ..

[more to come ....]









