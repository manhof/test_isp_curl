# test_isp_curl
These programs are used to simulate webpage testing on a large scale

Once you download this folder the first steps to get this setup is to modify the curl.conf file to configure where you would like the files to be placed. This can be done in Section 2 of the configuration file


#curltestconfigscript.py
This script (must be run as root) will move the various scripts to the folders required for running the program. This will use the information found within Section 2 of the configuration file to place the files. This script will also create a local database to be used by the testing service. If a db service is not installed, it will be, and will be set to run on boot. This testing tool is setup to run using MariaDB. Once complete you will need to run curltest12.py to iniatiate the testing. Before this is done you should enter the required parameters located within the curl.conf file. 

Once the configuration file has been updated, you need to make a directory called /etc/curl/ and copy the curl.conf file to this directory.


#curltest12.py

This script is done to build the acutal scripts which are running the tests, as well as scheduling when the tests will occur. Th. This script will schedule these tasks under the cron of the cron_user field in the configuration file. It will also direct all outputs to log files within the /tmp directory. THIS SCRIPT MUST BE RUN AS ROOT. 

#Overall Testing Stragety

There are 4 scripts that are run for this testing procedure.

1) isp_curl_script.sh is the testing which occurs, and it outputs to a temporary file

2) csv_copy.py & datbase_upload.py are responsible for uploading the data to the local directory

3) remote_database_upload.py is responisble for uploading the data to a back end database. This allows for tests to be run at various locations are report the metrics back to a centralized service.
