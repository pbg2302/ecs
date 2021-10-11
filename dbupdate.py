
from logging import error
import mysql.connector
from mysql.connector import errorcode
import os
import re
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-db_username", "--db_username", dest="db_username", help="User name for the database", required=True)
    parser.add_argument("-db_password", "--db_password", dest="db_password", help="db password for the database", required=True)
    parser.add_argument("-db_host", "--db_host", dest="db_host", help="db hosts name for the database", required=True)
    parser.add_argument("-db_name", "--db_name", dest="db_name", help="database name for the database", required=True)
    parser.add_argument("-db_script_dir", "--db_script_dir", dest="db_script_dir", help="Database script foler", required=True)

    args = parser.parse_args()

    db_username = args.db_username
    db_password = args.db_password
    db_host = args.db_host
    db_name = args.db_name
    db_script_dir = args.db_script_dir

    run_sql_scripts(db_username,db_password,db_host,db_name,db_script_dir)
    
    
def connect_to_database(db_username,db_password,db_host,db_name):
    cnx = mysql.connector.connect(user=db_username,
                                    database=db_name,
                                    password=db_password,
                                    host=db_host)
    return cnx
    
def retrieve_db_verion(db_username,db_password,db_host,db_name):
    mySql_insert_query = """select * from  versiontable"""
    db = connect_to_database(db_username,db_password,db_host,db_name)
    cursor = db.cursor()
    cursor.execute(mySql_insert_query)
    current_versions = cursor.fetchall()
    current_version = max(current_versions)[0]
    return current_version
    
   
def list_sql_scripts(db_username,db_password,db_host,db_name,db_script_dir):
    sql_scripts = []
    path = db_script_dir
    for file in os.listdir(path):
        script_numbers = re.findall(r'\d[0-9].*\.sql', file)
        for script_version in script_numbers:
            sql_scripts.append(script_version)
    return sql_scripts
    
def list_sqlscript_versions(db_username,db_password,db_host,db_name,db_script_dir):
    script_versions = []
    path = db_script_dir
    for file in os.listdir(path):
        script_numbers = re.findall(r'\d[0-9].*\.sql', file)
        for script_number in script_numbers:
            script_num = int(script_number[0:3])
            script_versions.append(script_num)
    return script_versions
    
def run_sql_scripts(db_username,db_password,db_host,db_name,db_script_dir):
    current_version = retrieve_db_verion(db_username,db_password,db_host,db_name)
    script_versions = list_sqlscript_versions(db_username,db_password,db_host,db_name,db_script_dir)
    sql_scripts     = list_sql_scripts(db_username,db_password,db_host,db_name,db_script_dir)
    
    for script_version in script_versions:
        if current_version < script_version:
            print(f"current db version: {current_version} is lower than script version: {script_version}")
            for sql_script in sql_scripts:
                if str(script_version) in sql_script:
                    try:
                        db = connect_to_database(db_username,db_password,db_host,db_name)
                        cursor = db.cursor()
                        t = db_script_dir+'/'+sql_script
                        with open(t,'r') as inserts:
                            query = inserts.read()
                        cursor.execute(query)
                        db.commit()
                        cursor.close()
                        db.close()
                        print("Data inserted successfully into the table")
                        update_version_table(db_username,db_password,db_host,db_name,script_version)
                    except mysql.connector.Error as error:
                        print("query failed {}".format(error))
                    


def update_version_table(db_username,db_password,db_host,db_name,script_version):
    db = connect_to_database(db_username,db_password,db_host,db_name)
    cursor = db.cursor()
    cursor.execute(("""INSERT INTO versiontable
                  VALUES (%s)""" % (script_version)))
    db.commit()
    cursor.close()
    db.close()
    print("Record updated successfully into versiontable table")

if __name__ == "__main__":
    sys.exit(main())
