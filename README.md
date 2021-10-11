### Purpose 

The purpose of this document is to define how the script is used to execute the numbered sql scripts stored in a specified folder.

### Requirements:

Supported Languages: Bash, Python3, PHP, Shell, Ruby, Powershell - No other languages will be accepted

The table where the version is stored is called 'versionTable', and the row with the version is 'version'. This table contains only one column with the actual version.

You will have to use a MySQL database

Script will be executed by using the below format:

## python dbupdate.py -db_script_di <directory with .sql scripts>  -db_username <username for the DB> -db_password <DB password> -db_host  <DB host>  -db_name <DB name>


