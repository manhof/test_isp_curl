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
csv_file = config.get('Section 2', 'curl_csv_output')
csv_file1 = csv_file +"1"
epoch_time = int(time.time())

#connecting to database
mydb = MySQLdb.connect(host=config.get('Section 4','local_database_url_ip'),
    user=config.get('Section 4','local_database_un'),
    passwd=config.get('Section 4','local_database_password'),
    db=config.get('Section 4','local_database_name'))
cursor = mydb.cursor()
cursor.execute("Select max(time_id) from " + config.get('Section 4','local_table_name'))
number_max_tuple = tuple(cursor.fetchone())
number_max = max(number_max_tuple)
fieldnames2 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
csv_data = csv.DictReader(file(csv_file1),fieldnames=fieldnames2)
cursor = mydb.cursor()
print number_max
for row in csv_data:
	insert_stmt = (
		"INSERT INTO " + config.get('Section 4','local_table_name') +" (time_id, date, url, user_agent, url_e, http_code, ip_port, download_speed, upload_speed, dns_lookup_time, tcp_connect_time, ssl_connect_time, pretransfer_time, starttransfer_time, total_time) "
		"VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
	)
	input_data = (row['1'], row['2'], row['3'],row['4'],row['5'],row['6'],row['7'],row['8'],row['9'],row['10'],row['11'],row['12'],row['13'],row['14'],row['15'])
	print row['1']	
	if number_max is None:
		cursor.execute(insert_stmt, input_data)	
	elif int(number_max) < int(row['1']):
		cursor.execute(insert_stmt, input_data)
	else:
		print "error with row"
mydb.commit()
cursor.close()
exit()
