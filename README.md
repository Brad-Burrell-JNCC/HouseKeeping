# HouseKeeping
This script search for tif file in the GWS and CEDA directories, and compares the filenames, if the filenames match, the files are analysed. Firstly, an MD5 Hash value is generated, if they match the version on GWS is added to the "products_to_delete.txt" file, else the dates are compared. if the new version is on CEDA the GWS version is "products_to_delete.txt" file.
