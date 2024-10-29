import  netCDF4
import unicodedata

normal_name = "composed\u00E9"
non_normal_name = "separate\u0065\u0301"

# create a netcdef File with two variables.
with netCDF4.Dataset("nfc-norm.nc", 'w') as ds:
    dim = ds.createDimension("a_dim", 10)
    var1 = ds.createVariable(normal_name, float, ("a_dim"))
    var2 = ds.createVariable(non_normal_name, float, ("a_dim"))
    var1[:] = range(10)
    var2[:] = range(10)

    # do the same for attributes:
    var1.test_name = normal_name
    var2.test_name = non_normal_name

# Read it back in, and see if the variable names were normalized
with netCDF4.Dataset("nfc-norm.nc", 'r') as ds:
    # get the vars from their original names
    try:
        norm = ds[normal_name]
        print(f"{normal_name} worked")
    except IndexError:
        print(f"{normal_name} didn't work")

    try:
        non_norm = ds[non_normal_name]
        print(f"{non_normal_name} worked")
    except IndexError:
        print(f"{non_normal_name} didn't work")
        non_norm = ds[unicodedata.normalize('NFC', non_normal_name)]
        print(f"But it  did once normalized!")

    for name in ds.variables.keys():
        assert unicodedata.is_normalized('NFC', name)
    print("All variable names are normalized")

    # how about the attributes?
    assert ds[normal_name].test_name == normal_name
    if ds[unicodedata.normalize('NFC', non_normal_name)].test_name == non_normal_name:
        print("attributes have NOT been normalized")

    if ds[unicodedata.normalize('NFC', non_normal_name)].test_name == unicodedata.normalize('NFC', non_normal_name):
        print("attributes HAVE BEEN normalized")


