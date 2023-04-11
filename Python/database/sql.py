import mysql.connector
'conda install mysql-connector-python'
import pandas as pd

def load_data(file_name):
    data=pd.read_csv(file_name,sep=';',error_bad_lines=False)
    return data

def create_database(columns):
    mydb=mysql.connector.connect(host='localhost',
                                 user='root',
                                 passwd='root',
                                 charset='utf8')
    mycursor=mydb.cursor()
    mycursor.execute("CREATE DATABASE if not exists WG")
    mycursor.execute("USE WG")
    mycursor.execute("CREATE TABLE IF NOT exists wg "+"("+columns+")")
    mycursor.execute("LOAD DATA LOCAL INFILE 'warranty.csv' INTO TABLE wg FIELDS TERMINATED BY ','")


if __name__=="__main__":
    data=load_data()
    columns=','.join([column.replace('.','')+' TINYTEXT' for column in data.columns])
    create_database(columns)
    print('Done')