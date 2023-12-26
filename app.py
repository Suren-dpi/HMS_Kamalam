from cryptography.fernet import Fernet
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from urllib.parse import unquote
import sqlite3
import uuid
import pandas as pd
import secrets
import string
from email.mime.multipart import MIMEMultipart
import smtplib
import json
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, date
from typing import Union
from jose import JWTError, jwt
from fastapi.responses import FileResponse
from fastapi import Depends, FastAPI, HTTPException, status, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
import uvicorn
import ssl
from db import database
from invoice import receipt
cur_time = lambda:datetime.now().strftime("%Y-%m-%d %H:%M:%S")
path = os.getcwd()
app_path = os.path.abspath(os.path.join(path, os.pardir))

# context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.maximum_version = ssl.TLSVersion.TLSv1_3

JWT_SECRET_KEY = "c6bc49bdde776b55c585cffa3c1e76b74a82d3739478f87375096d8204f1bae6"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "1ebfe97264baf2cc61d512257688687eff56a6178334177c04412917a05907ab"   # should be kept secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(JWT_SECRET_KEY, token_url="/login", use_cookie=True, custom_exception=NotAuthenticatedException())
manager.cookie_name = "access-token"

users_coll = "users"
icemp_coll= "ic_employees"

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/Token_gen",scheme_name="JWT")

class User(BaseModel):
    emp_id: Union[str, None] = None
    username: str
    designation: str

class UserInDB(User):
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class Config:
    def prereq(self):
        year = datetime.now().strftime('%Y')
        cwd = os.getcwd()
        print(cwd)
        if os.path.isdir("/Logs") == False:
            os.mkdir(r"" + cwd + "/Logs")
        os.chdir(r"" + path)

    def get_config(self):
        jsonfilepath = r"" + path + "/config.json"
        with open(jsonfilepath, 'r') as _:
            jsonbody = json.load(_)
        return jsonbody

    def result_log(self,inp):
        conn = self.get_config()
        # outfile = open(path + "/Logs/Result.log", "a", encoding="utf-8")
        outfile = open("/Logs/Result.log", "a", encoding="utf-8")
        outfile.write(cur_time() + ": " +str(inp) + "\n")
        outfile.close()

    def send_mail(self, email,password):
        # The mail addresses and password
        sender_address = 'surenaspect@gmail.com'
        sender_pass = 'puhnpcvenmixxrnd'
        receiver_address = email.split(",")  # should be in list
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = email
        # message['Subject'] = "HR Portal Login"
        # The subject line
        message = 'Subject: {}\n\n{}'.format("HR Portal Login", "Welcome to HR portal \n Your login Password is " + password)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        conf.result_log("Password sent")

    def generate_password(self):
        # define the alphabet
        letters = string.ascii_letters
        digits = string.digits
        special_chars = "!@#$%&*"
        alphabet = letters + digits + special_chars
        # fix password length
        pwd_length = 12
        # generate password meeting constraints
        while True:
            pwd = ''
            for i in range(pwd_length):
                pwd += ''.join(secrets.choice(alphabet))
            if (any(char in special_chars for char in pwd) and
                    sum(char in digits for char in pwd) >= 2):
                break
        return pwd

    def get_paycycle(self):
        today = date.today()
        first = today.replace(day=1)
        last_month = first - timedelta(days=1)
        lm = str(last_month.strftime("%b%y")).lower()
        cm = str(today.strftime("%b%y")).lower()
        paycycle = lm + "_" + cm
        fromdate = str(last_month.strftime("%Y-%m-21"))
        todate = str(today.strftime("%Y-%m-20"))
        daterange = {'paycycle': paycycle, 'fromdate': fromdate, 'todate': todate}
        return daterange

    def get_mac(self):
        mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                for ele in range(0, 8 * 6, 8)][::-1])
        return mac_addr

class Validate:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Token_gen")

    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self,password):
        return self.pwd_context.hash(password)

    def get_user(self, username: str):
        db = sqldb.getuser(username)
        if db:
            user_dict = db
            return UserInDB(**user_dict)

    def authenticate_user(self,username: str, password: str):
        user = self.get_user(username)
        if user is None:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    async def get_current_user(self,token: str = Depends(reuseable_oauth)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def encrypt(self,key, data):
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode('utf-8'))
        return encrypted_data

    def decrypt(self,key, data):
        f = Fernet(key)
        decrypted_data = f.decrypt(data.encode('utf-8'))
        return decrypted_data

    def view_licence(self):
        try:
            key = 'uON5CaIX2ybN-y4at5HyHefXXPIw8Rlb4fMayBRAQhU='
            dbpath = r"" + path + "\\Database\\" + conf.get_config()['database']
            conn = sqlite3.connect(dbpath)
            df = pd.read_sql_query(
                "SELECT license_startdate,license_enddate,system_info,license_key,system_key from license", conn)
            data = df.to_dict('records')[0]
            license_key = data['license_key']
            system_key = data['system_key']
            license_startdate = data['license_startdate']
            license_enddate = val.decrypt(key, license_key)
            system_data = val.decrypt(key, system_key)
            today = datetime.now().strftime('%Y-%m-%d')
            if today <= license_enddate.decode():
                if system_data.decode() == conf.get_mac():
                    return json.dumps({'license_status': 'Active', 'license_startdate':license_startdate,'licence_valid_upto': license_enddate.decode(),
                                       'system_info': system_data.decode()}, indent=4)
                else:
                    return 'Invalid System info'
            else:
                return json.dumps(
                    {'license_status': 'Inactive', 'license_startdate':license_startdate,'licence_valid_upto': license_enddate.decode(),
                     'system_info': system_data.decode()},
                    indent=4)
        except BaseException as e:
            print(str(e))
            return str(e)

class Token_gen:
    def get_userdata(self):
        jsonfilepath = r"" + path + "/Database/user_login.json"
        with open(jsonfilepath, 'r') as _:
            jsonbody = json.load(_)
        return jsonbody

    def create_access_token(self,data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self,data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

app = FastAPI()
val = Validate()
tk = Token_gen()
conf = Config()
sqldb = database()
bill = receipt()
dbpath = r"" + path + "\\Database\\" + conf.get_config()['database']
conn = sqlite3.connect(dbpath)


@manager.user_loader()
def load_user(username: str):
    user = val.get_user(username)
    return user.username

templates = Jinja2Templates(directory="templates")
app.mount("/app/static", StaticFiles(directory="static"), name="static")

# innoviti_users_db = lambda: tk.get_userdata()
innoviti_users_db = lambda: tk.get_userdata()

########## WEB APPLICATION #######################################################################

@app.get('/', response_class=HTMLResponse)
async def login_page(request: Request):
    license = json.loads(val.view_licence())
    print(license)
    systeminfo = conf.get_mac()
    valid_upto = license['licence_valid_upto']
    date = datetime.now().strftime('%Y-%m-%d')
    if valid_upto >= date:
        return templates.TemplateResponse('login.html', {'request': request, 'systeminfo':systeminfo,'licenseinfo':valid_upto})
    else:
        redirect_url = request.url_for('login_invalid') + '?License_Expired'
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

@app.get('/login/msg', response_class=HTMLResponse)
async def login_invalid(request: Request):
    msg = str(request.query_params).replace("+"," ").replace("=","")
    return templates.TemplateResponse('login.html', {'request': request,'msg':msg})

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    print("1qwertyuioolkjhgfdsazxcvbnm")
    redirect_url = request.url_for('login_invalid') + '?Token Expired'
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

@app.post("/login")
async def login_for_access_token(request: Request,username: str = Form(...), password: str = Form(...)):
    conf.result_log(username + " user logged in")
    user = val.authenticate_user(username.lower(), password)
    if not user:
        redirect_url = request.url_for('login_invalid') + '?Invalid Credentials'
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = tk.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        refresh_token = tk.create_refresh_token(data={"sub": user.username}, expires_delta=access_token_expires)
        resp = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        manager.set_cookie(resp, access_token)
        # return {'access_token':access_token}
        return resp

@app.get('/forgot', response_class=HTMLResponse)
async def forgot_page(request: Request):
    conf.result_log("Forgot Password")
    return templates.TemplateResponse('forgot_password.html', {'request': request})

@app.get('/forgot/msg', response_class=HTMLResponse)
async def forgot_invalid(request: Request):
    msg = str(request.query_params).replace("+"," ").replace("=","").replace("%21","!")
    conf.result_log(msg)
    return templates.TemplateResponse('forgot_password.html', {'request': request,'msg':msg})

@app.get('/logout', response_class=HTMLResponse)
async def logout(request: Request, currentuser: User=Depends(manager)):
    try:
        conf.result_log(str(currentuser) + " user logged out")
        resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        manager.set_cookie(resp, "")
        return resp
    except BaseException as e:
        conf.result_log(str(e))

@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request,currentuser: User=Depends(manager)):
    license = json.loads(val.view_licence())
    systeminfo = conf.get_mac()
    valid_from = license['license_startdate']
    valid_upto = license['licence_valid_upto']
    date = datetime.now().strftime('%Y-%m-%d')
    if valid_upto >= date:
        if valid_from < date:
            return templates.TemplateResponse('dashboard.html',
                                              {'request': request, 'user': currentuser, 'systeminfo': systeminfo,
                                               'licenseinfo': valid_upto})
        else:
            redirect_url = request.url_for('login_invalid') + '?License_Not_Activated'
            return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    else:
        redirect_url = request.url_for('login_invalid') + '?License_Expired'
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

#Out Patients
@app.get('/appointment', response_class=HTMLResponse)
async def appointment(request: Request,currentuser: User=Depends(manager)):
    try:
        dbpath = r"" + path + "\\Database\\" + conf.get_config()['database']
        conn = sqlite3.connect(dbpath)
        date = datetime.now().strftime('%Y-%m-%d')
        drs = sqldb.execute("select doctor_name from doctors")
        drs1 = []
        for x in range(len(drs)):
            drs1.append(drs[x][0])
        total_patients = sqldb.execute("select count(*) from appointments")[0][0]
        sql_query = pd.read_sql_query(
            '''select * from appointments where date = '{0}' order by time desc'''.format(date), conn)
        df = pd.DataFrame(sql_query,
                          columns=['Tokenno', 'Receiptno', 'Date', 'Time', 'Patient', 'Age', 'Sex', 'Guardian',
                                   'Doctor', 'Department',
                                   'Consultationfee', 'Medicalhistory'])
        df = df.style.hide(axis='index')
        return templates.TemplateResponse('appointment.html', {'request': request, 'data': df.to_html(), 'drs': drs1,
                                                               'total_patients': total_patients})
    except BaseException as e:
        return templates.TemplateResponse('appointment.html', {'request': request,'error': str(e)})

@app.post('/createappointment', response_class=HTMLResponse)
async def createappointment(request: Request,name: str = Form(...),guardian: str = Form(...),age: str = Form(...),sex: str = Form(...),address: str = Form(...),
                           phone: str = Form(...), dr: str = Form(...),dept: str = Form(...),consfee: str = Form(...),medhist: str = Form(...),currentuser: User=Depends(manager)):
    try:
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        tokenno = sqldb.execute("select count(*) from appointments where doctor = '{0}' and date = '{1}'".format(dr,date))[0][0]
        tokenno += 1
        count = sqldb.execute("select count(*) from appointments where date = '{0}'".format(date))[0][0]
        count += 1
        receiptno = "OP"+str(datetime.now().strftime('%y%m%d'))+(str(count)).zfill(3)
        sqldb.insertappointment(str(tokenno),receiptno,date,time, name, age, sex, guardian,address, phone, dr,dept,consfee,medhist)
        redirect_url = request.url_for('appointment')
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    except BaseException as e:
        print(str(e))
        return templates.TemplateResponse('appointment.html', {'request': request,'error': str(e)})

@app.post('/printreceipt', response_class=HTMLResponse)
async def printreceipt(request: Request,receiptno: str = Form(...),currentuser: User=Depends(manager)):
    try:
        year = datetime.now().strftime('%Y')
        conn = conf.get_config()
        receiptpath = conn['Invoicepath'] + "/Invoice/Outpatient/" + year
        details = sqldb.execute("select * from appointments where receiptno = '{0}'".format(receiptno))[0]
        opdata = list(details)
        opdata.append(currentuser)
        bill.print_receipt(path, opdata)
        # To view the file in the browser, use "inline" for the media_type
        headers = {
            "Content-Disposition": "inline; filename=" + path + "/opd.pdf"
        }
        # Create a FileResponse object with the file path, media type and headers
        response = FileResponse(path + "/opd.pdf", media_type="application/pdf", headers=headers)
        # Return the FileResponse object
        return response
    except BaseException as e:
        return templates.TemplateResponse('appointment.html', {'request': request,'error': str(e)})

#Reports

@app.get('/reports', response_class=HTMLResponse)
async def reports(request: Request,currentuser: User=Depends(manager)):
    return templates.TemplateResponse('report.html', {'request': request})

@app.post('/cashreport', response_class=HTMLResponse)
async def cashreport(request: Request,date: str = Form(...),currentuser: User=Depends(manager)):
    try:
        r2 = pd.read_sql_query(
            "select Date,Doctor as Consulting_Dr,COUNT(Receiptno) as TotalOutPatients,SUM(Consultationfee) as TotalFee from appointments where Date = '{0}' group by Date,Doctor;".format(
                date), conn)
        r3 = pd.read_sql_query(
            "select date as Date,consultingdr as Consulting_Dr,COUNT(ipdno) as TotalInPatients,SUM(payment) as TotalPayments from admission where date = '{0}' and dod !='' group by Date,consultingdr;".format(
                date), conn)
        r2 = r2.style.hide(axis='index')
        r3 = r3.style.hide(axis='index')
        return templates.TemplateResponse('DCR.html',
                                          {'request': request, 'date': date, 'data': r2.to_html(),
                                           'data1': r3.to_html()})
    except BaseException as e:
        print(str(e))
        return templates.TemplateResponse('DCR.html', {'request': request, 'error': str(e)})

@app.post('/monthlycashreport', response_class=HTMLResponse)
async def monthlycashreport(request: Request,month: str = Form(...),currentuser: User=Depends(manager)):
    try:
        r2 = pd.read_sql_query(
            "select Doctor as Consulting_Dr,COUNT(Receiptno) as TotalOutPatients,SUM(Consultationfee) as TotalFee from appointments where Date like '{0}' group by Doctor;".format(
                month + '%'), conn)
        r3 = pd.read_sql_query(
            "select consultingdr as Consulting_Dr,COUNT(ipdno) as TotalInPatients,SUM(payment) as TotalPayments from admission where date like '{0}' group by consultingdr;".format(
                month + '%'), conn)
        r2 = r2.style.hide(axis='index')
        r3 = r3.style.hide(axis='index')
        return templates.TemplateResponse('MCR.html',
                                          {'request': request, 'month': month, 'data': r2.to_html(),
                                           'data1': r3.to_html()})
    except BaseException as e:
        print(str(e))
        return templates.TemplateResponse('MCR.html', {'request': request, 'error': str(e)})

@app.post('/yearlycashreport', response_class=HTMLResponse)
async def yearlycashreport(request: Request,year: str = Form(...),currentuser: User=Depends(manager)):
    try:
        r2 = pd.read_sql_query(
            "select Doctor,COUNT(Receiptno) as TotalOutPatients,SUM(Consultationfee) as TotalFee from appointments where Date like '{0}' group by Doctor;".format(
                year + '%'), conn)
        r3 = pd.read_sql_query(
            "select COUNT(ipdno) as TotalInPatients,SUM(payment) as TotalPayments from admission where date like '{0}'".format(
                year + '%'), conn)
        r2 = r2.style.hide(axis='index')
        r3 = r3.style.hide(axis='index')
        return templates.TemplateResponse('YCR.html',
                                          {'request': request, 'year': year, 'data': r2.to_html(),
                                           'data1': r3.to_html()})
    except BaseException as e:
        print(str(e))
        return templates.TemplateResponse('YCR.html', {'request': request, 'error': str(e)})


# IPD
@app.get('/inpatient', response_class=HTMLResponse)
async def inpatient(request: Request,currentuser: User=Depends(manager)):
    try:
        sql_query = pd.read_sql_query('''select * from admission where dod = '' order by ipdno desc''', conn)
        df = pd.DataFrame(sql_query,
                          columns=['ipdno', 'patient', 'doa', 'age', 'sex', 'roomno', 'guardian', 'mobileno',
                                   'address', 'consultingdr', 'department', 'referreddr'])
        df = df.style.hide(axis='index')
        return templates.TemplateResponse('inpatient.html', {'request': request, 'data': df.to_html()})
    except BaseException as e:
        print(str(e))
        return templates.TemplateResponse('inpatient.html', {'request': request, 'error': str(e)})

@app.get('/ipd_add', response_class=HTMLResponse)
async def ipd_add(request: Request,currentuser: User=Depends(manager)):
    try:
        drs = sqldb.execute("select doctor_name from doctors")
        drs1 = []
        for x in range(len(drs)):
            drs1.append(drs[x][0])
        return templates.TemplateResponse('IPD_Reg.html', {'request': request, 'drs': drs1})
    except BaseException as e:
        print(str(e))
        return templates.TemplateResponse('IPD_Reg.html', {'request': request, 'error': str(e)})

@app.post('/ipd_add_db', response_class=HTMLResponse)
async def ipd_add_db(request: Request,currentuser: User=Depends(manager)):
    try:
        dict_data = {}
        date = datetime.now().strftime('%Y-%m-%d')
        count = sqldb.execute("select count(*) from admission")[0][0]
        count += 1
        ipdno = "IP" + str(datetime.now().strftime('%y%m%d')) + (str(count)).zfill(3)
        byte_data = await request.body()
        str_data1 = byte_data.decode("UTF-8").replace("+", " ")
        str_data = unquote(str_data1)
        list_data = str_data.split("&")
        for x in list_data:
            dt = x.split("=")
            dict_data[dt[0]] = dt[1]
        val = list(dict_data.values())
        val = list((map(str, val)))
        #appending empty discharge date
        val.append('')
        val.append(date)
        val.insert(0, ipdno)
        var_string = ', '.join('?' * len(val))
        qry = 'INSERT INTO admission (ipdno,patient,doa, age, dob,sex,bloodgroup,roomno,guardian,mobileno,maritialstatus,address,consultingdr,department,referreddr,presentcomplaint,familyhistory,remarks,dod,date) VALUES (%s);' % var_string
        sqldb.execute_insert(qry, val)
        redirect_url = request.url_for('inpatient')
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    except BaseException as e:
        print(str(e))
        drs = sqldb.execute("select doctor_name from doctors")
        drs1 = []
        for x in range(len(drs)):
            drs1.append(drs[x][0])
        return templates.TemplateResponse('IPD_Reg.html', {'request': request, 'drs': drs1,'error': str(e)})

@app.post('/printipdform', response_class=HTMLResponse)
async def printipdform(request: Request,ipdno: str = Form(...),currentuser: User=Depends(manager)):
    try:
        year = datetime.now().strftime('%Y')
        condt = conf.get_config()
        receiptpath = condt['Invoicepath'] + "/Invoice/Outpatient/" + year
        sql_query = pd.read_sql_query('''select * from admission where ipdno = '{0}' '''.format(ipdno), conn)
        df = pd.DataFrame(sql_query,
                          columns=['ipdno', 'patient', 'doa', 'age', 'sex', 'bloodgroup', 'roomno', 'guardian', 'mobileno', 'maritialstatus',
                                   'address', 'consultingdr', 'department', 'referreddr','presentcomplaint','familyhistory','remarks'])
        details = df.to_dict('records')[0]
        details['user'] = currentuser
        bill.print_admissionform(ipdno, receiptpath, details)
        # To view the file in the browser, use "inline" for the media_type
        headers = {
            "Content-Disposition": "inline; filename="+path+"/admissionform.pdf"
        }
        # Create a FileResponse object with the file path, media type and headers
        response = FileResponse(path+"/admissionform.pdf", media_type="application/pdf", headers=headers)
        # Return the FileResponse object
        return response
    except BaseException as e:
        return templates.TemplateResponse('inpatient.html', {'request': request, 'error': str(e)})

@app.post('/dissum', response_class=HTMLResponse)
async def reports(request: Request,ipdno2:str = Form(...),currentuser: User=Depends(manager)):
    try:
        ipd_details = list(sqldb.execute('''select * from admission where ipdno = '{0}' '''.format(ipdno2))[0])
        print(ipd_details)
        return templates.TemplateResponse('dischargesummary.html', {'request': request, 'ipd_details': ipd_details})
    except BaseException as e:
        return templates.TemplateResponse('dischargesummary.html', {'request': request, 'error': str(e)})

@app.post('/print_dissum', response_class=HTMLResponse)
async def reports(request: Request,currentuser: User=Depends(manager)):
    try:
        dict_data = {}
        byte_data = await request.body()
        str_data = byte_data.decode("UTF-8").replace("=", ":").replace("&", ",").replace("%40", "@").replace("+", " ")
        list_data = str_data.split(",")
        for x in list_data:
            dt = x.split(":")
            dict_data[dt[0]] = dt[1]
        dict_data['user'] = currentuser
        bill.print_discharge_summary(dict_data)
        # To view the file in the browser, use "inline" for the media_type
        receiptpath = path
        headers = {
            "Content-Disposition": "inline; filename=" + receiptpath + "/dischargesummary.pdf"
        }
        # Create a FileResponse object with the file path, media type and headers
        response = FileResponse(receiptpath + "/dischargesummary.pdf", media_type="application/pdf", headers=headers)
        # Return the FileResponse object
        return response
    except BaseException as e:
        return templates.TemplateResponse('dischargesummary.html', {'request': request, 'error': str(e)})

@app.post('/dischargebill', response_class=JSONResponse)
async def dischargebill(request: Request,ipdno1:str = Form(...),currentuser: User=Depends(manager)):
    try:
        ipd_details = list(sqldb.execute('''select * from admission where ipdno = '{0}' '''.format(ipdno1))[0])
        print(ipd_details)
        category = sqldb.execute("select Category from ipd_category")
        cat1 = []
        for x in range(len(category)):
            cat1.append(category[x][0])
        print(cat1)
        return templates.TemplateResponse('dischargebill.html',
                                          {'request': request, 'ipd_details': ipd_details, 'category': cat1})
    except BaseException as e:
        return templates.TemplateResponse('dischargebill.html', {'request': request, 'error': str(e)})

@app.post('/print_dischargebill', response_class=JSONResponse)
async def print_dischargebill(request: Request,currentuser: User=Depends(manager)):
    try:
        dict_data = {}
        byte_data = await request.body()
        str_data1 = byte_data.decode("UTF-8").replace("=", "|").replace("&", ",").replace("%40", "@").replace("+", " ")
        str_data = unquote(str_data1)
        list_data = str_data.split(",")
        for x in list_data:
            dt = x.split("|")
            dict_data[dt[0]] = dt[1]
        dict_data['user'] = currentuser
        print(dict_data)
        sqldb.execute('''UPDATE admission set dod = '{0}', payment = '{1}' where ipdno = '{2}' '''.format(dict_data['dod'],dict_data['total'],dict_data['ipdno']))
        bill.print_discharge_bill(dict_data)
        # To view the file in the browser, use "inline" for the media_type
        headers = {
            "Content-Disposition": "inline; filename=" + path + "/dischargebill.pdf"
        }
        # Create a FileResponse object with the file path, media type and headers
        response = FileResponse(path + "/dischargebill.pdf", media_type="application/pdf", headers=headers)
        # Return the FileResponse object
        return response
    except BaseException as e:
        return templates.TemplateResponse('dischargebill.html', {'request': request, 'error': str(e)})

# Staff Management
@app.get('/staffs', response_class=HTMLResponse)
async def staffs(request: Request,currentuser: User=Depends(manager)):
    return templates.TemplateResponse('staff.html',
                                      {'request': request, 'empdata':'', 'error':'', 'data': ''})

@app.get('/liststaff', response_class=HTMLResponse)
async def liststaff(request: Request):
    dbpath = r"" + path + "\\Database\\" + conf.get_config()['database']
    conn = sqlite3.connect(dbpath)
    sql_query = pd.read_sql_query('''select * from staffs ''',conn)
    df = pd.DataFrame(sql_query,
                      columns=['empid', 'empname', 'age', 'sex', 'designation', 'address', 'phone', 'joiningdate', 'exitdate'])
    df = df.style.hide(axis='index')
    return templates.TemplateResponse('staff.html',
                                      {'request': request, 'empdata': '', 'error': '', 'data': df.to_html()})

@app.post('/addstaff', response_class=HTMLResponse)
async def addstaff(request: Request,name: str = Form(...),age: str = Form(...),sex: str = Form(...),des: str = Form(...),address: str = Form(...),
                           phone: str = Form(...), jdate: str = Form(...), edate: str = Form(None),currentuser: User=Depends(manager)):
    try:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        count = sqldb.execute("select empid from staffs order by empid desc limit 1")
        if '-1' in count:
            empid = 'KHM0001'
        else:
            empid = 'KMH' + str(int(count[0][0][3:]) + 1).zfill(3)
        out = sqldb.insertstaffs(str(empid), name.capitalize(), age, sex, des, address, phone, jdate, edate, dt)
        redirect_url = request.url_for('liststaff')
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    except BaseException as e:
        print(str(e))
        return templates.TemplateResponse('staff.html',
                                          {'request': request, 'error': str(e)})

@app.get('/viewstaff', response_class=HTMLResponse)
async def viewstaff(request: Request):
    try:
        qry = "select * from  staffs"
        out = sqldb.execute(qry)
        if '-1' in out:
            return templates.TemplateResponse('staff.html',
                                              {'request': request, 'error': 'No Data'})
        else:
            return templates.TemplateResponse('staff.html',
                                              {'request': request, 'empdata': out[0]})
    except BaseException as e:
        print(str(e))
        return str(e)

@app.post('/getstaff', response_class=HTMLResponse)
async def getstaff(request: Request,empid: str = Form(...)):
    try:
        qry = "select * from  staffs where empid = '{0}'".format(empid)
        out = sqldb.execute(qry)
        print(out[0])
        if '-1' in out:
            return templates.TemplateResponse('staff.html',{'request': request, 'error': 'Invalid employee id'})
        else:
            return templates.TemplateResponse('update_staff.html',
                                              {'request': request, 'empdata':out[0]})
    except BaseException as e:
        print(str(e))
        return str(e)

@app.post('/updatestaff', response_class=HTMLResponse)
async def updatestaff(request: Request,empid: str = Form(...),name: str = Form(None),age: str = Form(None),sex: str = Form(None),des: str = Form(None),address: str = Form(None),
                           phone: str = Form(None), jdate: str = Form(None), edate: str = Form(None)):
    try:
        qry1 = "select * from staffs where empid= '{0}'".format(empid)
        out = sqldb.execute(qry1)
        if '-1' in out:
            return templates.TemplateResponse('staff.html',{'request': request, 'error': 'Invalid employee id'})
        else:
            out_list = list(out[0])
            empdata = [empid, name, age, sex, des, address, phone, jdate, edate]
            for i in range(1, len(empdata)):
                if empdata[i] is None:
                    out_list[i] = out_list[i]
                else:
                    out_list[i] = empdata[i]
            qry2 = "update staffs set empname = '{1}',age = '{2}',sex = '{3}',designation = '{4}',address = '{5}',phone = '{6}',joiningdate = '{7}',exitdate = '{8}'  where empid = '{0}'".format(
                *out_list)
            out1 = sqldb.execute(qry2)
            redirect_url = request.url_for('staffs') + '?'+out1
            return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    except BaseException as e:
        print('Error: ' + str(e))
        return str(e)

@app.delete('/deletestaff', response_class=HTMLResponse)
async def deletestaff(request: Request,empid: str = Form(...)):
    try:
        qry = "delete from staffs where empid='{0}'".format(empid)
        out = sqldb.execute(qry)
        return json.dumps(out,indent=4)
    except BaseException as e:
        print(str(e))
        return str(e)


#LICENSE
@app.post('/insert_license', response_class=HTMLResponse)
async def update_license(request: Request):
    try:
        byte_data = await request.body()
        data = json.loads(byte_data)
        key_info = data['key_info']
        license_validaupto = data['license_enddate']
        system_info = data['system_info']
        license_key = val.encrypt(key_info, license_validaupto)
        system_key = val.encrypt(key_info, system_info)
        data['license_key'] = license_key.decode()
        data['system_key'] = system_key.decode()
        sqldb.insertlicense(data['license_startdate'], data['license_enddate'], license_key.decode(), system_key.decode(),
                                  system_info,key_info,data['customer_name'],data['customer_address'],data['customer_contactno'],
                                  data['customer_emailid'],data['company_name'],data['company_address'],data['company_emailid'],data['company_contactno'])
        s = json.dumps(data, indent=4)
        return s
    except BaseException as e:
        return str(e)

@app.post('/update_license', response_class=HTMLResponse)
async def update_license(request: Request):
    try:
        byte_data = await request.body()
        data = json.loads(byte_data)
        key_info = data['key_info']
        license_validaupto = data['license_enddate']
        system_info = data['system_info']
        license_key = val.encrypt(key_info, license_validaupto)
        system_key = val.encrypt(key_info, system_info)
        data['license_key'] = license_key.decode()
        data['system_key'] = system_key.decode()
        sqldb.updatelicense(system_info,data['license_startdate'], data['license_enddate'], license_key.decode(),
                            system_key.decode(),key_info)
        s = json.dumps(data, indent=4)
        return s
    except BaseException as e:
        return str(e)

@app.get('/view_license', response_class=HTMLResponse)
async def view_license(request: Request):
    try:
        dbpath = r"" + path + "\\Database\\" + conf.get_config()['database']
        conn = sqlite3.connect(dbpath)
        df = pd.read_sql_query(
            "SELECT * FROM license",
            conn)
        data = df.to_dict('records')[0]
        return json.dumps(data, indent=4)
    except BaseException as e:
        print(str(e))
        return str(e)

@app.get('/validate_license', response_class=HTMLResponse)
async def view_license(request: Request, key: str = Form(...) ):
    try:
        dbpath = r"" + path + "\\Database\\" + conf.get_config()['database']
        conn = sqlite3.connect(dbpath)
        df = pd.read_sql_query(
            "SELECT license_startdate,license_enddate,system_info,license_key,system_key from license", conn)
        data = df.to_dict('records')[0]
        license_key = data['license_key']
        system_key = data['system_key']
        license_enddate = val.decrypt(key, license_key)
        system_data = val.decrypt(key, system_key)
        today = datetime.now().strftime('%Y-%m-%d')
        if today <= license_enddate.decode():
            if system_data.decode() == conf.get_mac():
                return json.dumps({'license_status': 'Active', 'licence_valid_upto': license_enddate.decode(),
                                   'system_info': system_data.decode()}, indent=4)
            else:
                return 'Invalid System info'
        else:
            return json.dumps(
                {'license_status': 'Inactive', 'licence_valid_upto': license_enddate.decode(),
                 'system_info': system_data.decode()},
                indent=4)
    except BaseException as e:
        print(str(e))
        return str(e)

#user management
@app.post('/create_user', response_class=HTMLResponse)
async def create_user(request: Request, empid: str = Form(...), username: str = Form(...),password: str = Form(...), designation: str = Form(...)):
    try:
        hashed_password = val.get_password_hash(password)
        out = sqldb.execute("INSERT INTO users ( empid, username, password, designation) VALUES ('{0}','{1}','{2}','{3}')".format(empid,username,hashed_password,designation))
        return json.dumps(out,indent=4)
    except BaseException as e:
        print(str(e))
        return str(e)

@app.post('/update_user', response_class=HTMLResponse)
async def update_user(request: Request, empid: str = Form(...), username: str = Form(...),password: str = Form(...), designation: str = Form(...)):
    try:
        hashed_password = val.get_password_hash(password)
        out = sqldb.execute('''update users set empid = '{0}', password = '{2}', designation = '{3}' where username = '{1}' '''.format(empid,username,hashed_password,designation))
        return json.dumps(out, indent=4)
    except BaseException as e:
        print(str(e))
        return str(e)

@app.post('/delete_user', response_class=HTMLResponse)
async def delete_user(request: Request,username: str = Form(...),):
    try:
        out = sqldb.execute("delete from users where username = '{0}'".format(username))
        return json.dumps(out,indent=4)
    except BaseException as e:
        print(str(e))
        return str(e)

@app.get('/view_user', response_class=HTMLResponse)
async def view_user(request: Request):
    try:
        out = sqldb.execute("select * from  users")
        return json.dumps(out,indent=4)
    except BaseException as e:
        print(str(e))
        return str(e)


if __name__ == "__main__":
    conn = conf.get_config()
    conf.prereq()
    #uvicorn.run("web_app:app", host=conn['host'], port=int(conn['port']), log_level="info",reload=True,ssl_keyfile=conn['ssl_keyfile'], ssl_certfile=conn['ssl_certfile'])
    uvicorn.run("app:app", host="127.0.0.1", port=5008, log_level="info", reload=True)
