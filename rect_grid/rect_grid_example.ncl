dimensions:
    lat_node = 101 ;
    lon_node = 201 ;
    lat_cell = 100 ;
    lon_cell = 200 ;

variables:

float lat(lat_node) ;
    lat:long_name = "latitude of the nodes" ;
    lat:units = "degrees_north" ;
    lat:standard_name = "latitude" ;

float lon(lon_node) ;
    lon:long_name = "longitude of the nodes" ;
    lon:units = "degrees_east" ;
    lon:standard_name = "longitude" ;

float some_data(lon_cell, lat_cell);
    some_data:long_name = "some data on the cells";    
}
