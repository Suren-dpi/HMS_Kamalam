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


    def createpid_table(self,tablename):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("CREATE TABLE")
        # Runner.logwriter("CREATE TABLE")
        try:
            sql = """CREATE TABLE """ + tablename + """ (
                pid int NOT NULL PRIMARY KEY,
                firstname text NOT NULL ,
                lastname text NOT NULL ,
                age int NOT NULL,
                sex text NOT NULL,
                address text NOT NULL,
                city text NOT NULL,
                phone text NOT NULL,
                datetime text NOT NULL
                )"""
            c.execute(sql)
            print("Table Created")
            # run.logwriter("Table Created")
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def createappointment_table(self,tablename):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("CREATE TABLE")
        # Runner.logwriter("CREATE TABLE")
        try:
            sql = """CREATE TABLE """ + tablename + """ (
                Tokenno text NOT NULL,
                Receiptno text NOT NULL PRIMARY KEY,
                Date text NOT NULL,
                Time text NOT NULL,
                Patient text NOT NULL ,
                Age text NOT NULL,
                Sex real NOT NULL,
                Guardian text NOT NULL ,
                Address text NOT NULL,
                Phone text NOT NULL,
                Doctor text NOT NULL,
                Department text NOT NULL,
                Consultationfee NUMERIC  NOT NULL,
                Medicalhistory text NOT NULL
                )"""
            c.execute(sql)
            print("Table Created")
            # run.logwriter("Table Created")
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def createusers_table(self,tablename):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("CREATE TABLE")
        # Runner.logwriter("CREATE TABLE")
        try:
            sql = """CREATE TABLE """ + tablename + """ (
                    empid int NOT NULL PRIMARY KEY,
                    username text NOT NULL ,
                    password varchar(10) NOT NULL,
                    designation varchar(15) NOT NULL
                    )"""
            c.execute(sql)
            print("Table Created")
            # run.logwriter("Table Created")
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def createstaff_table(self,tablename):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("CREATE TABLE")
        # Runner.logwriter("CREATE TABLE")
        try:
            sql = """CREATE TABLE """ + tablename + """ (
                    empid int NOT NULL,
                    empname text NOT NULL PRIMARY KEY ,
                    age int NOT NULL,
                    sex text NOT NULL,
                    designation text NOT NULL,
                    address text NOT NULL,
                    phone text NOT NULL,
                    joiningdate text NOT NULL,
                    exitdate text NULL,
                    datetime text NOT NULL
                    )"""
            c.execute(sql)
            print("Table Created")
            # run.logwriter("Table Created")
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def createlicense_table(self,tablename):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("CREATE TABLE")
        # Runner.logwriter("CREATE TABLE")
        try:
            sql = """CREATE TABLE """ + tablename + """ (
                license_startdate text NOT NULL,
                license_enddate text NOT NULL ,
                license_key text NOT NULL PRIMARY KEY,
                system_key text NOT NULL,
                system_info text NOT NULL,
                key_info text NOT NULL,
                customer_name text NOT NULL,
                customer_address text NOT NULL,
                customer_contactno text NOT NULL,
                customer_email text NOT NULL,
                company_name text NOT NULL,
                company_address text NOT NULL,
                company_contactno text NOT NULL,
                company_email text NOT NULL
                )"""
            c.execute(sql)
            print("Table Created")
            # run.logwriter("Table Created")
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

    def createdoctor_table(self,tablename):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        print("CREATE TABLE")
        # Runner.logwriter("CREATE TABLE")
        try:
            sql = """CREATE TABLE """ + tablename + """ (
                doctor_name text NOT NULL PRIMARY KEY,
                qualification text NOT NULL ,
                department text NOT NULL ,
                joining_date text NOT NULL,
                releving_date text NOT NULL,
                address text NOT NULL,
                contact_no text NOT NULL,
                lastupdated text NOT NULL
                )"""
            c.execute(sql)
            print("Table Created")
            # run.logwriter("Table Created")
        except sqlite3.Error as e:
            print("ERROR - ", e)
            # run.logwriter("ERROR - " + str(e))
        conn.commit()
        conn.close()

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


    # droptable('appointments')
    # createpid_table ("patient_details")

    #
    # pid = 1
    # # insertpid('patient_details',pid,dt,'Suren','33','Male','Ilakkiyampatti','Dharmapuri','9791339138')
    # # viewdata('patient_details')

    # viewdata('appointments')

db = database()
dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# date = datetime.now().strftime('%Y-%m-%d')
# time = datetime.now().strftime('%H:%M:%S')
# db.createappointment_table("appointments")
#db.insertappointment('20','231109049',date,time,'suren','33','male','prakash','dharmapuri','9663044463','Dr.Sugasree','General Medicine','200','diabetic,bp')
# db.createpid_table('patientdetails')
# db.insertpid('1','Suren','prakash','33','Male','Ilakkiyampatti','Dharmapuri','9791339138',dt)
# db.createusers_table('users')
# db.insertusers('KML001','suren','suren@123','admin')
# db.createemp_table('employees')
# # db.insertemployee('KML001','sunil','33','Male','Ilakiyampatti','Dharmapuri','9791339138',dt)
# db.droptable('appointments')
# print(db.execute("select count(*) from patientdetails")[0][0])
# db.createlicense_table('license')
#db.droptable('license')
# db.droptable('doctors')
# db.createdoctor_table('doctors')
# db.insertdoctor('Dr.Vasantharaj','MS','Orthopedics','null','null','null','null',dt)
# db.droptable('admission')
# db.createstaff_table('staffs')
# db.insertstaffs('KHM000','user001','30','Male','office assistant','Dharmapuri','9876543210','2023-11-09','na',dt)
