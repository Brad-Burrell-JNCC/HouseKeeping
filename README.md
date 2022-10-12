# HouseKeeping
This script search for tif file in the GWS and CEDA directories, and compares the filenames, if the filenames match, the files are analysed. Firstly, an MD5 Hash value is generated, if they match the version on GWS is added to the "products_to_delete.txt" file, else the dates are compared. if the new version is on CEDA the GWS version is "products_to_delete.txt" file.

Full running instruction can be found in [JASMIN Housekeeping Script - Instructions and Documentation.md](https://github.com/Brad-Burrell-JNCC/HouseKeeping/blob/53097beaf887e7170b3a1939e11a3efba7f1a691/JASMIN%20Housekeeping%20Script%20-%20Instructions%20and%20Documentation.md)
