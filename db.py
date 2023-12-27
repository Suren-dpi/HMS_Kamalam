import sqlite3
import os
import json
import pandas as pd
from datetime import datetime
path = os.getcwd()


def get_config():
    jsonfilepath = r"" + path + "/config.json"
    with open(jsonfilepath, 'r') as _:
        jsonbody = json.load(_)
    return jsonbody


dbpath = r""+path+"\\Database\\"+get_config()['database']

class database:


    def insertlicense(self, license_startdate, license_enddate, license_key, system_key,system_info,key_info,customer_name,customer_address,
                      customer_contactno,customer_email,company_name, company_address,company_contactno, company_email):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("INSERT TABLE")
        # run.logwriter("INSERT TABLE")
        sql = """INSERT INTO license (license_startdate, license_enddate, license_key, system_key,system_info,key_info,customer_name,customer_address,
                      customer_contactno,customer_email,company_name, company_address,company_contactno, company_email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        try:
            c.execute(sql, (license_startdate, license_enddate, license_key, system_key,system_info,key_info,customer_name,customer_address,
                      customer_contactno,customer_email,company_name, company_address,company_contactno, company_email))
            print("patient data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
            conn.commit()
            conn.close()
            return "license data Inserted to db"
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
            conn.commit()
            conn.close()
            return str(e)

    def updatelicense(self, systeminfo,license_startdate, license_enddate, license_key, system_key,key_info):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("Update TABLE")
        # run.logwriter("INSERT TABLE")
        sql = "UPDATE license  set license_startdate = '{1}', license_enddate = '{2}' , license_key = '{3}' , system_key = '{4}', key_info = '{5}' where system_info = '{0}'".format(systeminfo,license_startdate, license_enddate, license_key,system_key,key_info)
        try:
            c.execute(sql)
            print("patient data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
            conn.commit()
            conn.close()
            return "license data updated to db"
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
            conn.commit()
            conn.close()
            return str(e)

    def insertpid(self, pid, firstname, lastname,age, sex, address, city, phone,datetime):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("INSERT TABLE")
        # run.logwriter("INSERT TABLE")
        sql = """INSERT INTO patientdetails (pid, firstname,lastname, age, sex, address, city, phone,datetime) VALUES (?,?,?,?,?,?,?,?,?)"""
        try:
            c.execute(sql, (pid, firstname, lastname,age, sex, address, city, phone,datetime))
            print("patient data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
            conn.commit()
            conn.close()
            return "patient data Inserted to db"
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
            conn.commit()
            conn.close()
            return str(e)

    def insertappointment(self, tokenno, receiptno, date, time, patient, guardian, age, sex, address, phone, dr,dept,consfee,medhist):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("INSERT TABLE")
        # run.logwriter("INSERT TABLE")
        sql = """INSERT INTO appointments ( tokenno, receiptno, date, time, patient, age, sex, guardian, address, phone, doctor,department,consultationfee,medicalhistory) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        try:
            c.execute(sql, (tokenno, receiptno, date, time, patient, guardian, age, sex, address, phone, dr,dept,consfee,medhist))
            print(str(tokenno) + " data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def insertusers(self,empid,username,password,designation):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("INSERT TABLE")
        # run.logwriter("INSERT TABLE")
        sql = """INSERT INTO users ( empid, username, password, designation) VALUES (?,?,?,?)"""
        try:
            c.execute(sql, (empid,username,password,designation))
            print(str(username) + " data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def updateusers(self,empid,username,password,designation):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("UPDATE TABLE")
        # run.logwriter("INSERT TABLE")
        sql = """UPDATE users set empid = '{0}', password = '{2}', designation = '{3}' where username = '{1}' """.format(empid,username,password,designation)
        try:
            c.execute(sql)
            print(str(username) + " data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def insertstaffs(self,empid,empname,age,sex,designation,address,phone,joiningdate,exitdate,datetime):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("INSERT TABLE")
        # run.logwriter("INSERT TABLE")
        sql = """INSERT INTO staffs ( empid,empname,age,sex,designation,address,phone,joiningdate,exitdate,datetime) VALUES (?,?,?,?,?,?,?,?,?,?)"""
        try:
            c.execute(sql, (empid,empname,age,sex,designation,address,phone,joiningdate,exitdate,datetime))
            out = (str(empname) + " data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
        except sqlite3.Error as e:
            out = "ERROR - "+ str(e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()
        return out

    def insertdoctor(self,doctor_name,qualification,department,joining_date,releving_date,address,contact_no,lastupdated):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("INSERT TABLE")
        # run.logwriter("INSERT TABLE")
        sql = """INSERT INTO doctors (doctor_name,qualification,department,joining_date,releving_date,address,contact_no,lastupdated) VALUES (?,?,?,?,?,?,?,?)"""
        try:
            c.execute(sql, (doctor_name,qualification,department,joining_date,releving_date,address,contact_no,lastupdated))
            print(str(doctor_name) + " data Inserted to db")
            # run.logwriter("Row of data Inserted to table "+ tablename)
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def getuser(self,user):
        conn = sqlite3.connect(dbpath)
        try:
            qry = "SELECT * FROM users where username = '{0}' ".format(user)
            df = pd.read_sql_query(qry, conn)
            df = df.to_dict('records')
            if len(df) >0 :
                return df[0]
            else:
                return df
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " +str(e))
        conn.commit()
        conn.close()

    def execute(self,query):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        c.execute(query)
        data = c.fetchall()
        if not data:
            data = "Rows affected " + str(c.rowcount)
        conn.commit()
        conn.close()
        return data

    def execute_insert(self,query,val):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        c.execute(query, val)
        data = c.fetchall()
        if not data:
            data = "Rows affected " + str(c.rowcount)
        conn.commit()
        conn.close()
        return data

    def droptable(self,tablename):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        # print("DELETE/DROP TABLE")
        try:
            sql = "DROP TABLE " + tablename + ""
            c.execute(sql)
            print("Table Deleted/Dropped Successfully")
            # run.logwriter("Table Deleted/Dropped Successfully")
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def deleterow(self,tablename, condition):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        # print("DELETE ROW FROM TABLE", tablename)
        try:
            sql = "DELETE FROM " + tablename + " WHERE " + condition
            c.execute(sql)
            print("Row(s) deleted from table", tablename)
            # run.logwriter("Row(s) deleted from table"+ tablename )
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - "+ str(e))
        conn.commit()
        conn.close()

    def rowcount(self,tablename):
        i = 0
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        # print("GET ROW COUNT IN TABLE ", tablename)
        try:
            sql = "SELECT * FROM " + tablename
            c.execute(sql)
            data = c.fetchall()
            for rows in data:
                i = i + 1
            print("Row Count", i)
            # run.logwriter("Row Count" + i)
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - "+ str(e))
        conn.commit()
        conn.close()

