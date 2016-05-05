#!/usr/bin/python

import ConfigParser
import os
from crontab import CronTab
#This first section is about interpteting the configuration file This seciont includes details on how to confugre the variables that are in the first section and convert them to be used by the tests.

#This section is used for the variables 

config = ConfigParser.ConfigParser()
config.readfp(open('/etc/curl/curl.conf'))
url_number = config.get('Section 1', 'url_number')
url_number = int(url_number)
tests_per_min = int(60/int(config.get('Section 1', 'seconds_per_test')))
user_agent_string = config.get('Section 1', 'user_agent_string')
wait_time = int(config.get('Section 1','seconds_per_test'))
test_script = open(config.get('Section 2', 'big_curl_script_location'), 'w')
curl_file = config.get('Section 2', 'curl_script_location')
csv_file = config.get('Section 2', 'curl_csv_output')
curl_script_frequency = int(config.get('Section 3', 'curl_script_frequency'))
db_script_frequency = int(config.get('Section 4', 'local_db_update'))
cron_user = str(config.get('Section 3', 'cron_user'))
remote_db_script_frequency = int(config.get('Section 5', 'remote_db_update'))
#This is to write the test file
test_script.write('#!/bin/bash\n') # the first line required to call bash

for y in range (tests_per_min,0,-1):
	for x in range (url_number,0, -1):
		
		x = str(x)
		try:
			test_script.write( 'nohup ' +' '+ curl_file +' '+ config.get('Section 1', 'url' + (x)) +' '+ user_agent_string +' '+ csv_file +' &'+ '\n')

		except ConfigParser.NoOptionError:
			print "missing url" + (x)
			break
	wait_time2= str(wait_time)
	test_script.write( 'sleep ' + wait_time2 + '\n')

test_script.close()
os.chmod(config.get('Section 2', 'big_curl_script_location'), 0777)
print test_script
#time to create cron jobs
tab = CronTab(user= cron_user)
cmd_curl = config.get('Section 2', 'big_curl_script_location')
tab.remove_all(comment='CurlScript')
cron_job_curl = tab.new(cmd_curl, comment='CurlScript')
cron_job_curl.minute.every(curl_script_frequency)
tab.write()

#2

tab = CronTab(user= cron_user)
cmd_curl = config.get('Section 4', 'local_db_file_location')
tab.remove_all(comment='db_update')
cron_job_curl = tab.new(cmd_curl, comment='db_update')
cron_job_curl.minute.every(db_script_frequency)
tab.write()

#3
tab = CronTab(user= cron_user)
cmd_curl = config.get('Section 5', 'remote_upload_file_location')
tab.remove_all(comment='remote_db_update')
cron_job_curl = tab.new(cmd_curl, comment='remote_db_update')
cron_job_curl.minute.every(remote_db_script_frequency)
tab.write()
#4

#curl_script_frequency= config.get('Section 3','curl_script_frequency')
#size_per = config.get('Section 6','db_per_test_instance')
#test_per_min = int(60/int(config.get('Section 1', 'seconds_per_test')))
#local_db_max = config.get('Section 6', 'local_db_max')

#local_db_delete_frequency=int((int(local_db_max)/ (float(test_per_min) *float(size_per)*float(url_number))))
#print local_db_delete_frequency
#local_db_delete_frequency_day= int(local_db_delete_frequency /(60*24))
#print local_db_delete_frequency_day

#local_db_delete_frequency_hour= int(((local_db_delete_frequency-local_db_delete_frequency_day*60*24)/60))
#print local_db_delete_frequency_hour

#local_db_delete_frequency_min= (local_db_delete_frequency % 60)
#print local_db_delete_frequency_min

#tab = CronTab(user= cron_user)
#cmd_curl = config.get('Section 6', 'local_db_delete_file_location')
#tab.remove_all(comment='local_rm_db_update')
#cron_job_curl = tab.new(cmd_curl, comment='local_rm_db_update')
#if local_db_delete_frequency_day != 0:
#	cron_job_curl.day.every(local_db_delete_frequency_day)

#if local_db_delete_frequency_hour != 0:
#	cron_job_curl.hour.every(local_db_delete_frequency_hour)

#if local_db_delete_frequency_min != 0:
#	cron_job_curl.minute.every(local_db_delete_frequency_min)
#
tab.write()
print tab.render ()
exit