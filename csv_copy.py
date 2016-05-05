#!/usr/bin/python
import ConfigParser
import os
#from crontab import CronTab
import shutil
import time
from datetime import datetime
import calendar
import sys
import MySQLdb
import csv
import codecs

#This first section is about interpteting the configuration file This seciont includes details on how to confugre the variables that are in the first section and convert them to be used by the tests.

#This section is used for the variables 

config = ConfigParser.ConfigParser()
config.readfp(open('/etc/curl/curl.conf'))
#Varibles
csv_file = config.get('Section 2', 'curl_csv_output')
csv_file1 = str(csv_file) +"1"
epoch_time = int(time.time())
variable = 0
with open(csv_file, 'rU') as csvfile:
	fieldnames = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
	curlreader = csv.DictReader((line.replace('\0','') for line in csvfile),fieldnames=fieldnames)
	with open(csv_file1, 'w') as result:
		make_new = csv.writer(result)
		for row in curlreader :
			date_object = datetime.strptime(row['1'], "%m/%d/%y %H:%M:%S.%f")
			variable = variable + 1
			try:
				make_new.writerow((epoch_time, date_object,row['2'],row['3'],row['4'],int(row['5']),row['6'],float(row['7']),float(row['8']),float(row['9']),float(row['10']),float(row['11']),float(row['12']),float(row['13']),float(row['14']),float(row['15'])))
			except ValueError:
				break
#print variable
sed_string = "sed -i\"\" '1," + str(variable) +"d' "+ csv_file
#print sed_string
os.system(sed_string)
exit()


