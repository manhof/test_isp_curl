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
#This first section is about interpteting the configuration file This seciont includes details on how to confugre the variables that are in the first section and convert them to be used by the tests.

#This section is used for the variables 

config = ConfigParser.ConfigParser()
config.readfp(open('/etc/curl/curl.conf'))
#Varibles
curl_script_frequency= config.get('Section 3','curl_script_frequency')
url_number = config.get('Section 1', 'url_number')
size_per = config.get('Section 6','db_per_test_instance')
test_per_min = int(60/int(config.get('Section 1', 'seconds_per_test')))
local_db_max = config.get('Section 6', 'local_db_max')

max_local_db_lines = int(float(local_db_max)/float(size_per))


#create new csv
mydb = MySQLdb.connect(host=config.get('Section 4','local_database_url_ip'),
    user=config.get('Section 4','local_database_un'),
    passwd=config.get('Section 4','local_database_password'),
    db=config.get('Section 4','local_database_name'))
cursor = mydb.cursor()
cursor.execute("Select count(*) from " + config.get('Section 4','local_table_name'))
number_max_tuple = tuple(cursor.fetchone())
number_max = max(number_max_tuple)
lines_to_delete = int((number_max - max_local_db_lines))
cursor = mydb.cursor()
cursor.execute("Delete From " + config.get('Section 4','local_table_name') +" order by time_id ASC limit " + str(lines_to_delete) )	

mydb.commit()
cursor.close()

