#!/usr/bin/python

import ConfigParser
import os
from crontab import CronTab
import MySQLdb
import yum
import sys
import subprocess
import shutil
#This first section is about interpteting the configuration file This seciont includes details on how
# to confugre the variables that are in the first section and convert them to be used by the tests.
#Running this script will Re-Iniate the table, so if it does exists it will be deleted. There will be a prompt asking for you input to continue

#This section is used for the variables 

config = ConfigParser.ConfigParser()
config.readfp(open('/etc/curl/curl.conf'))
#url_number = config.get('Section 1', 'url_number')
#url_number = int(url_number)
#tests_per_min = int(60/int(config.get('Section 1', 'seconds_per_test')))
#user_agent_string = config.get('Section 1', 'user_agent_string')
#wait_time = int(config.get('Section 1','seconds_per_test'))
test_script = open(config.get('Section 2', 'big_curl_script_location'), 'w')
curl_file = config.get('Section 2', 'curl_script_location')
csv_file = config.get('Section 2', 'curl_csv_output')
curl_csv_directory = config.get('Section 2', 'curl_csv_directory')
#curl_script_frequency = int(config.get('Section 3', 'curl_script_frequency'))
#db_script_frequency = int(config.get('Section 4', 'local_db_update'))
#cron_user = str(config.get('Section 3', 'cron_user'))
#remote_db_script_frequency = int(config.get('Section 5', 'remote_db_update'))
local_db_upload_file = config.get('Section 4', 'local_db_upload')
local_db_copy_file = config.get('Section 4', 'local_db_copy')
local_db_user= str(config.get('Section 4', 'local_database_un'))
local_db_password= str(config.get('Section 4', 'local_database_password'))
local_database_url_ip= str(config.get('Section 4', 'local_database_url_ip'))
local_database_name= str(config.get('Section 4', 'local_database_name'))
local_table_name= str(config.get('Section 4', 'local_table_name'))
remote_upload_file_location= config.get('Section 5', 'remote_upload_file_location')

# This section of the script is done to install the base hardware that is required to run the scripts
# and store the data locally
# This includes making sure that a database exists,and if not installing that database.

#This section is a check to see if there is a local datbase with the correct parameters installed. If 
#not it will install the correct database
#if the table you are trying to use for this iniation script exists the table will be overwritten. 
#if you would like to create a new table for this test please change in the config file
try
	mydb = MySQLdb.connect(host=local_database_url_ip,
	    	user=local_db_user,
	    	passwd=local_db_password,
    		db=local_database_name)
	cursor = mydb.cursor()
	cursor.execute("Select table_name from information_schema.tables WHERE table_name = '" + local_table_name + "'")
	table_exists_results = cursor.fetchone()
	if table_exists_results:
		print "Table Exists"
		delete_question = raw_input("Would you like to Continue? Process Will Delete Table!(y/n): ")
		if "y" is not in delete_question:
			exit
		else:
			cursor.execute("DROP TABLE" + local_table_name)
			mydb.commit()
			cursor.close()
	else:
		print "Table Doesn't Exists. Will attempt to create one"
except MySQLdb.Error:
	print "Can't Connect to DB. Will attempt to install one"

#This section here is to run yum to install a new database. This will default to using mariadb
	yb=yum.YumBase()
	inst = yb.rpmdb.returnPackages()
	installed=[x.name for x in inst]
	packages=['mariadb']

	for package in packages:
        	if package in installed:
	                print('{0} is already installed'.format(package))
	        else:
        	        print('Installing {0}'.format(package))
        	        kwarg = {
        	                'name':package
        	        }
        	        yb.install(**kwarg)
        	        yb.resolveDeps()
        	        yb.buildTransaction()
        	        yb.processTransaction()
			start_db_command = ["/usr/bin/service mariadb start"]
			persistant_db_command = ["chkconfig mariadb on"]
			subprocess.call(start_db_command, shell=True)
			subprocess.call(persistant_db_command, shell=True)
			
	
#This will pull us out of our loops. The next steps will be to create the table
#this is done by connecting to the local db creating the table with the required rows for the service

mydb = MySQLdb.connect(host=local_database_url_ip,
    	user=local_db_user,
    	passwd=local_db_password,
	db=local_database_name)
cursor = mydb.cursor()

build_table= (
	"Create Table " + local_table_name + 
	" (id int(10) NOT NULL auto_increment, "
	"time_id int(10) NOT NULL, "
	"date datetime NOT NULL, "
	"url varchar(250) NOT NULL, "
	"user_agent varchar(250) default NULL, "
	"url_e varchar(250) NOT NULL, "
	"http_code int(3) NOT NULL, "
	"ip_port varchar(50) NOT NULL, "
	"download_speed int(10) NOT NULL, "
	"upload_speed int(10) NOT NULL, "
	"dns_lookup_time decimal(6,3) NOT NULL, "
	"tcp_connect_time decimal(6,3) NOT NULL, " 
	"ssl_connect_time decimal(6,3) NOT NULL, "
	"pretransfer_time decimal(6,3) NOT NULL, "
	"redirect_time decimal(6,3) NOT NULL, "
	"starttransfer_time decimal(6,3) NOT NULL, "
	"total_time decimal(6,3) NOT NULL, "
	"PRIMARY KEY (id)"
)


cursor.execute( build_table)

#building the indexes for the local table

build_index1 = ("Create Index url ON " + local_table_name + "(url)")
cursor.execute(build_index1)


build_index2 = ("Create Index user_agent ON " + local_table_name + "(user_agent)")
cursor.execute(build_index2)

build_index3 = ("Create Index date ON " + local_table_name + "(date)")
cursor.execute(build_index3)

mydb.commit()
cursor.close()


#now we have a local db built. The next steps are to move the required files to their required locations

shutil.copyfile(csv_copy.py, local_db_copy_file)
shutil.copyfile(datbase_upload, local_db_upload_file)
shutil.copyfile(curl2.sh, curl_file)
shutil.copyfile(remote_database_upload.py, curl_file)


#creating temp curl folder
os.makedirs(curl_csv_directory)



print "Please Run curltest12.py to start the inital load of testing"

exit
