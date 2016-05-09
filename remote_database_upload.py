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
csv_file = config.get('Section 5', 'remote_db_csv_location')
site_id = config.get('Section 5', 'phone_number')
#this section is used to delete the tmp file
os.system('rm -rf ' + csv_file)

mydb = MySQLdb.connect(host=config.get('Section 5','remote_database_url_ip'),
    user=config.get('Section 5','remote_database_un'),
    passwd=config.get('Section 5','remote_database_password'),
    db=config.get('Section 5','remote_database_name'))

#Get max of old data
cursor = mydb.cursor()
max_time_statement = (
	"SELECT time_id from " + config.get('Section 5','remote_table_name')+
	" WHERE site='" + site_id +"' "
	"ORDER BY ID DESC LIMIT 1"
)

cursor.execute(max_time_statement)
try:
	number_max_tuple = tuple(cursor.fetchone())
	number_max = max(number_max_tuple)
except TypeError:
	number_max = 0
cursor.close()
print "create new csv"

mydb1 = MySQLdb.connect(host=config.get('Section 4','local_database_url_ip'),
    user=config.get('Section 4','local_database_un'),
    passwd=config.get('Section 4','local_database_password'),
    db=config.get('Section 4','local_database_name'))
cursor1 = mydb1.cursor()

outfile_statement = (
	"SELECT * INTO OUTFILE'"+csv_file+"'"
	"FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' "
	"LINES TERMINATED BY '\n' FROM " + config.get('Section 4', 'local_table_name')
	)
if number_max is None:
	cursor1.execute(outfile_statement)
	cursor1.close()
else:
	print number_max
	delete_statement = (
		"Delete from "+ config.get('Section 4', 'local_table_name')+ " "
		"where time_id <= '"+ str(int(number_max))+"'"
	)
	cursor1.execute(delete_statement)
	mydb1.commit
	cursor1.close()
	print "delete worked"
	print outfile_statement			
	cursor3 = mydb1.cursor()
	cursor3.execute(outfile_statement)
	cursor3.close()
print "connect to remote server"
mydb2 = MySQLdb.connect(host=config.get('Section 5','remote_database_url_ip'),
    user=config.get('Section 5','remote_database_un'),
    passwd=config.get('Section 5','remote_database_password'),
    db=config.get('Section 5','remote_database_name'))
cursor2 = mydb2.cursor()
fieldnames2 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
csv_data = csv.DictReader(file(csv_file),fieldnames=fieldnames2)
print number_max
for row in csv_data:
	insert_stmt = (
		"INSERT INTO " + config.get('Section 5','remote_table_name') +"(site, time_id, date, url, user_agent, url_e, http_code, ip_port, download_speed, upload_speed, dns_lookup_time, tcp_connect_time, ssl_connect_time, pretransfer_time,redirect_time, starttransfer_time, total_time)"
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	)
	input_data = (site_id, row['2'], row['3'],'"'+row['4']+'"',row['5'],row['6'],row['7'],row['8'],row['9'],row['10'],row['11'],row['12'],row['13'],row['14'],row['15'], row['16'],row['17'])
	print row['2']	
	if number_max is None:
		cursor2.execute(insert_stmt, input_data)	
		print 0
	elif int(number_max) < int(row['2']):
		cursor2.execute(insert_stmt, input_data)
		print 1
	else:
		print 2
mydb2.commit()
cursor2.close()
exit()

