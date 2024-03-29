# Name: Housekeeping.py
# Author: Bradley Burrell - 202203-Current
# Description: This script search for tif file in the GWS and CEDA directories, and compares the filenames, if the
#              filenames  match, the file are analysed. Firstly, an MD5 Hash value is generated, if  they match the
#              version on GWS is added to the "products_to_delete.txt" file, else the dates are compared. if the new
#              version is on  CEDA the GWS version is "products_to_delete.txt" file.
# REQUIREMENTS:
#  1. Python version 3.10
# CHANGELOG:
#  20221012-BB; Added timecode to start of file and directories. Updated parent directory path.
#  1. Python version 3.10

# READING:
# 1. MD5 Hash: The MD5 message-digest algorithm is widely used hash function producing a 128-bit hash value.  It is used
#              here as a checksum to verify data integrity, but only against unintentional corruption.
#               Reference: https://en.wikipedia.org/wiki/MD5

import datetime
import hashlib
import os
import sys

# ===================================================== Functions ======================================================
def jasmin_list_builder(sen_dir, sen_list, text_file, date):
    """
    The "jasmin_list_builder" uses the sen_dir  to search for valid directory and record all tif found within.

    :param sen_dir: Sentinel Directory, the parent direct containing the sentinel files
    :param sen_list: The list of sentinel tif found
    :param text_file: Output Text file of found sentinel tifs
    :param date: Must have the datetime type
    :return: Return the sen_list with addition Directories appended
    """
    # Pulls YYYY, MM, and DD from the datetime field
    yyyy = date.year
    mm = '{:02d}'.format(date.month)
    dd = '{:02d}'.format(date.day)
    # Check if the directory exists.
    dir_check = os.path.isdir(sen_dir)
    # If dir_check is true (dir exists), checks for tif files, if tif are found they are appended to the list and adds
    # to text file.
    if dir_check is True:
        with open(text_file, 'a') as outfile:
            for file in os.listdir(sen_dir):
                if file.endswith('.tif'):
                    sen_list.append([file, "{}/{}/{}".format(yyyy, mm, dd)]) # TODO: Replace date with full path?
                    outfile.write("{}\n".format(file))
        return sen_list
    # If the dir doesn't exists prints an error message
    elif dir_check is False:
        print("No Directory Found: {}".format(sen_dir))


def md5(file_to_hash, error_log):
    """
    The "md5" functions generates an MD5 hash, this can be used to compare if two file are the same.

    :param file_to_hash: Pathway to the file
    :param error_log: Pathway to error_log
    :return: The MD5 Hash Value of File
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_to_hash, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except PermissionError:
        with open(error_log, 'a') as error_out:
            error_out.write("PermissionError: {}\n".format(file_to_hash))
            error_out.close()
        return None


def housekeeper(gws_dir_list, ceda_dir_list, gws_dir, ceda_dir, products_to_delete_txt, error_log):
    """
    The "housekeeper" is the core function of the Housekeeping.py script, It uses the lists generated by the
    "jasmin_list_builder" to indentify tif with the same name, where they are the same it generates a MD5 Hash to
    compare files. If these files are the same, it compares there creation date

    :param gws_dir_list: List of file on GWS
    :param ceda_dir_list: List of file on CEDA
    :param gws_dir: Path to GWS directory
    :param ceda_dir: Path to CEDA directory
    :param products_to_delete_txt: Path to products_to_delete.txt
    :param error_log: Pathway to error_log Path to errors.txt
    :return:
    """

    gws_file_list = [item[0] for item in gws_dir_list]
    ceda_file_list = [item[0] for item in ceda_dir_list]

    on_gws = set(gws_file_list)  # s1_on_gws
    on_ceda = set(ceda_file_list)  # s1_on_ceda

    on_ceda_not_gws = on_ceda - on_gws  # on_ceda_not_gws

    master_list = gws_dir_list + list(on_ceda_not_gws)
    for entry in master_list:
        filename = entry[0]
        yyyymmdd = entry[1]
        print("{:=^{width}}".format(" Housekeeping - {}".format(filename), width=125))
        gws_path = "{}/{}/{}".format(gws_dir, yyyymmdd, filename)
        ceda_path = "{}/{}/{}".format(ceda_dir, yyyymmdd, filename)
        print("GWS: {}S".format(gws_path))
        print("CEDA: {}S".format(ceda_path))
        if filename in on_gws:
            print("{} Still on GWS".format(filename))
            if filename in on_ceda:
                print("\t{} on GWS and CEDA".format(filename))
                gws_md5 = md5(gws_path, error_log)
                ceda_md5 = md5(ceda_path,error_log)
                if gws_md5 == ceda_md5:
                    print('\t\tIdentical File found in both GWS and CEDA')
                    with open(products_to_delete_txt, 'a') as p2d:
                        p2d.write("{}\n".format(gws_path))
                        p2d.close()
                else:
                    gws_creation_datetime = os.path.getctime(gws_path)
                    ceda_creation_datetime = os.path.getctime(ceda_path)
                    if gws_creation_datetime >= ceda_creation_datetime:
                        print('\t\tNewer Version on GWS')
                    else:
                        print('\t\tNewer Version on CEDA')
                        with open(products_to_delete_txt, 'a') as p2d:
                            p2d.write("{}\n".format(filename))
                            p2d.close()

        else:
            print("{} only on CEDA".format(entry))
        print("\n")


# ===================================================== Main Body ======================================================
print("{:=^{width}}".format(" Starting Housekeeping ", width=125))
start_time = datetime.datetime.now()

# These lines control whether the script will search for S1 and/or S2 tifs. For If "test_s1" is set to True and
# "test_s2" is False the script will search for S1 but not S2.
test_s1 = True
test_s2 = Fals

# Take the date input from System Arguments (expected format YYYY-MM-DD) can converts to <class 'datetime.datetime'>
newd = datetime.datetime.fromisoformat(sys.argv[1]) # Start Date
endd = datetime.datetime.fromisoformat(sys.argv[2]) # End Date

# Creates date code for easy identification 
newd_year = newd.year
newd_month = newd.month
endd_year = endd.year
endd_month = endd.month

datecode = None
if newd_year == endd_year:
    if newd_month == endd_month:
        datecode = "{}{:02d}".format(newd_year, newd_month)
    else:
        datecode = "{0}{1:02d}-{0}{2:02d}".format(newd_year, newd_month, endd_month)
else:
    datecode = "{}{:02d}-{}{:02d}".format(newd_year, newd_month, endd_year, endd_month)

# Pathway to sentinel direct -  Hard coded for JASIN/CEDA
s1_gws_dir = '/gws/nopw/j04/defra_eo/public/s1_ard_update'
s1_ceda_dir = '/neodc/sentinel_ard/data/sentinel_1'
s2_gws_dir = '/gws/nopw/j04/defra_eo/public/s2_ard_update'
s2_ceda_dir = '/neodc/sentinel_ard/data/sentinel_2'


# List to be populated by jasmin_list_builder
s1_gws_dir_list = []
s1_ceda_dir_list = []
s2_gws_dir_list = []
s2_ceda_dir_list = []

# Creates timestamp for files and folders
now = datetime.datetime.now()
datetime_stamp = str(now).split('.')[0].replace('-', '').replace(' ', '').replace(':', '')

# Path to output text files -  Hard code to JASIN/CEDA
parent_dir = "gws/nopw/j04/defra_eo/data/output/sentinel/1/reports/housekeeping"
run_dir = "{}/{}_housekeeping_{}".format(parent_dir, datecode, datetime_stamp)

if not os.path.exists(parent_dir):
      os.mkdir(parent_dir)
if not os.path.exists(run_dir):
      os.mkdir(run_dir)
      
s1_gws_files = "{}/{}_s1_gws_files_{}.txt".format(run_dir, datecode, datetime_stamp)
s1_ceda_files = "{}/{}_s1_ceda_files_{}.txt".format(run_dir, datecode, datetime_stamp)
s2_gws_files = "{}/{}_s2_ceda_files_{}.txt".format(run_dir, datecode, datetime_stamp)
s2_ceda_files = "{}/{}_s2_ceda_files_{}.txt".format(run_dir, datecode, datetime_stamp)
products_to_delete = "{}/{}_products_to_delete_{}.txt".format(run_dir, datecode, datetime_stamp)
errors = "{}/{}_Errors_{}.txt".format(run_dir, datecode, datetime_stamp)
open(products_to_delete, mode='w').close()
open(errors, mode='w').close()



# Incremental works through date between the Start Date and the End Date
while newd <= endd:

    # Pull out date component from the datetime and formats to YYYY, MM, and DD
    year = newd.year
    month = '{:02d}'.format(newd.month)
    day = '{:02d}'.format(newd.day)
    # Use s1_gws_dir, year, month, and day to create path to potential S1 GWS directory
    s1_gws_dir_yyyymmdd = "{}/{}/{}/{}".format(s1_gws_dir, year, month, day)
    # Use s1_ceda_dir, year, month, and day to create path to potential S1 CEDA directory
    s1_ceda_dir_yyyymmdd = "{}/{}/{}/{}".format(s1_ceda_dir, year, month, day)
    # Use s1_gws_dir, year, month, and day to create path to potential S1 GWS directory
    s2_gws_dir_yyyymmdd = "{}/{}/{}/{}".format(s2_gws_dir, year, month, day)
    # Use s1_ceda_dir, year, month, and day to create path to potential S1 CEDA directory
    s2_ceda_dir_yyyymmdd = "{}/{}/{}/{}".format(s2_ceda_dir, year, month, day)

    # If test_s1 is True, i.e. you want to search S1 directories
    if test_s1 is True:
        # Runs jasmin_list_builder to build list of S1 file on the GWS Drive, see function for Details
        jasmin_list_builder(sen_dir=s1_gws_dir_yyyymmdd,
                            sen_list=s1_gws_dir_list,
                            text_file=s1_gws_files,
                            date=newd)
        # Runs jasmin_list_builder to build list of S1 file on the CEDA Drive, see function for Details
        jasmin_list_builder(sen_dir=s1_ceda_dir_yyyymmdd,
                            sen_list=s1_ceda_dir_list,
                            text_file=s1_ceda_files,
                            date=newd)
    if test_s2 is True:
        # Runs jasmin_list_builder to build list of S2 file on the GWS Drive, see function for Details
        jasmin_list_builder(sen_dir=s2_gws_dir_yyyymmdd,
                            sen_list=s2_gws_dir_list,
                            text_file=s2_gws_files,
                            date=newd)
        # Runs jasmin_list_builder to build list of S2 file on the CEDA Drive, see function for Details
        jasmin_list_builder(sen_dir=s2_ceda_dir_yyyymmdd,
                            sen_list=s2_ceda_dir_list,
                            text_file=s2_ceda_files,
                            date=newd)
    # Increase the Date by 1 Day
    newd = newd + datetime.timedelta(days=1)

# If test_s1 is True, i.e. you want to search S1 directories
if test_s1 is True:
    # Runs housekeeper on GWS and CEDA S2 directories to product list of product to be deleted, see function for Details
    housekeeper(gws_dir_list=s1_gws_dir_list,
                ceda_dir_list=s1_ceda_dir_list,
                gws_dir=s1_gws_dir,
                ceda_dir=s1_ceda_dir,
                products_to_delete_txt=products_to_delete,
                error_log=errors)
    # Runs housekeeper on GWS and CEDA S2 directories to product list of product to be deleted, see function for Details
if test_s2 is True:
    housekeeper(gws_dir_list=s2_gws_dir_list,
                ceda_dir_list=s2_ceda_dir_list,
                gws_dir=s2_gws_dir,
                ceda_dir=s2_ceda_dir,
                products_to_delete_txt=products_to_delete,
                error_log=errors)

end_time = datetime.datetime.now()
total_time = end_time - start_time
num_lines = sum(1 for line in open(products_to_delete))
errors_lines = sum(1 for line in open(errors))

print("{:=^{width}}".format(" Completed Housekeeping - Stats", width=125))
print("Runtime            : {}".format(total_time))
print("File to be Deleted : {}".format(num_lines))
print("Errors             : {}".format(errors_lines))
if test_s1 is True:
    print("{:-^{width}}".format(" Sentinel 1 ", width=125))
    num_lines_s1_gws = sum(1 for line in open(s1_gws_files))
    num_lines_s1_ceda = sum(1 for line in open(s1_ceda_files))
    print("\tFile on GWS : {}".format(num_lines_s1_gws))
    print("\tFile on CEDA: {}".format(num_lines_s1_ceda))
if test_s2 is True:
    print("{:-^{width}}".format(" Sentinel 2 ", width=125))
    num_lines_s2_gws = sum(1 for line in open(s2_gws_files))
    num_lines_s2_ceda = sum(1 for line in open(s2_ceda_files))
    print("\tFile on GWS : {}".format(num_lines_s2_gws))
    print("\tFile on CEDA: {}".format(num_lines_s2_ceda))
print("{:=^{width}}".format(" Finished ", width=125))
