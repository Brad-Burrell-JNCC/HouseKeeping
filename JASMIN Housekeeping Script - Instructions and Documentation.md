
# JASMIN Housekeeping Script
A python script to identify sentinel scenes to be deleted

## Summary

This script search for tif file in the GWS and CEDA directories, and compares the filenames, if the filenames match, the files are analysed. Firstly, an MD5 Hash value is generated, if they match the version on GWS is added to the "products_to_delete" file, else the dates are compared. If the new version is on CEDA the GWS version is "products_to_delete" file.

## Requirements

Python 3.8 (Tested on: 3.8.12 | packaged by conda-forge | (default, Oct 12 2021, 21:59:51))

 - datetime
 - hashlib
 - os
 - sys

## Setup

Create a new folder in your user area on JASMIN, copy the script into the folder. Please make sure your JASMIN and CEDA accounts are linked.

## Running Instructions

To run the “Housekeeping.py” please follow these instruction

### Step 1

Open and sign into MobaXterm

### Step 2

Start New Terminal

### Step 3

Enter the following command into JAMSIN, to login
~~~
ssh -A login2.jasmin.ac.uk
~~~
Press the ‘Enter’ key

### Step 4

Enter the following command into JAMSIN, 
~~~
ssh sci8.jasmin.ac.uk 
~~~
to sign into a machine using (Please note you can uses any “sci” machine, “sci8” is used as any example:

Press the ‘Enter’ key

### Step 5
The Housekeeping script take a long time to run, by entering the following command you will be able to close MobaXterm  and the script will keep running:
~~~
screen
~~~
The will clear all text currently in your terminal. This step is optional, but advisable. 

### Step 6

Enter the following command into JAMSIN, to load the correct JASPY module (This module meets all the requirements laid out in section 2.) using:
~~~
module load jaspy/3.8/r20211105
~~~

Press the ‘Enter’ key

### Step 7

Change directory to where the python script is located, for example:

~~~
cd code/ard/
~~~

Press the ‘Enter’ key

### Step 8

To run the script enter the command from the text box, altering the {start-date} {end-date} to your desired dates. 

~~~
 python Housekeeping.py {start-date} {end-date}
~~~

Press the ‘Enter’ key

### Step 9

After the script has run, go to the housekeeping directory;
~~~
cd /gws/nopw/j04/defra_eo/data/output/sentinel/1/reports/housekeeping
~~~
Press the ‘Enter’ key

### Step 10

Check for you housekeeping runs directory
~~~
ls
~~~
Press the ‘Enter’ key

It will be named like this. The name is comprised for 3 section broken by underscores.

> 201801_housekeeping_20220923100216

The first section in a  'datecode' in, i.e. the time period you where house keeping for in yyyymm. Please note if this is great than one month the 'datecode' will be long and in this format yyyymm-yyyymm.

The second identifies it as a housekeeping directory.

The third is the runs timestamp, i.e. the time you ran the script in yyyymmddhhmmss format.

### Step 11

Enter the housekeeping directory. 

Double click on the directory in the terminal window to select it. 

Type in 'cd ' then left click and press enter.

### Step 12
You should have 4 text file in the directory. Entry the below command to check.
~~~
ls
~~~
Press the ‘Enter’ key

You should have 
>201801_products_to_delete_20220923100216.txt  
>201801_s1_ceda_files_20220923100216.txt  
>201801_s1_gws_files_20220923100216.txt
>201801_Errors_20220923100216.txt

If you are missing any, contact Brad Burrell or Rachel King for advise.
