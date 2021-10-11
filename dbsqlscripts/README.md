### Purpose 

The purpose of this document is to define how the script is used to execute the numbered sql scripts stored in a specified folder.

### Requirements:

Supported Languages: Bash, Python3, PHP, Shell, Ruby, Powershell - No other languages will be accepted

The table where the version is stored is called 'versionTable', and the row with the version is 'version'. This table contains only one column with the actual version.

You will have to use a MySQL database

Script will be executed by using the below format:

## python dbupdate.py -db_script_di /d/KeepLearning/Learning/dbsqlscripts  -db_username prem -db_password prem@123 -db_host 127.0.0.1 -db_name versiondb


