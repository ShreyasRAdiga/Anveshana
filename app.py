

import math
import random
import logging
import json
import re
import openpyxl
from urllib import request, response
from flask import *
from flask import session
from flask_mail import *
from flask_bootstrap import *
from flask_session import Session
from flask_mongoengine import MongoEngine
import os
import pandas as pd
from flask import send_from_directory



'''os.environ['API_USER'] = 'teamekyam@outlook.com'
os.environ['API_PASSWORD'] = 'EkyamJNN'''

os.environ['API_USER']='support.anveshana@jnnce.ac.in'
os.environ['API_PASSWORD']='P5A=9DUeZUUy4mC&1'

app = Flask(__name__)
DB_URI = "mongodb+srv://user:anve321@cluster0.fguhnfv.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

'''app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('API_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('API_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False'''

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get('API_USER')
app.config["MAIL_PASSWORD"] = os.environ.get('API_PASSWORD')

db = MongoEngine()
mail = Mail(app)
db.init_app(app)
Session(app)


class Flag(db.Document):
    key = db.StringField()
    value = db.StringField()
  
class User(db.Document):
    email = db.StringField()
    password = db.StringField()
    name = db.StringField()
    mobile=db.StringField()
    type = db.StringField(default='none')
    verified=db.StringField(default='False')
    telegram= db.StringField(default='none')
    var1=db.StringField(default='none')
    var2=db.StringField(default='none')
class Participant1(db.Document):
    regNo=db.StringField()
    teamName=db.StringField()
    participant1=db.StringField()
    participant2=db.StringField()
    email1 = db.StringField()
    email2 = db.StringField()
    usn1=db.StringField()
    usn2=db.StringField()
    phone1=db.StringField()
    phone2=db.StringField()
    amount=db.StringField()
    utr=db.StringField()
    accomodation=db.StringField()
    event=db.StringField()
    var1=db.StringField(default='none')
    var2=db.StringField(default='none')
    
class Participant2(db.Document):
    regNo=db.StringField()
    teamName=db.StringField()
    participant1=db.StringField()
    email1 = db.StringField()
    usn1=db.StringField()
    phone1=db.StringField()
    amount=db.StringField()
    utr=db.StringField()
    accomodation=db.StringField()
    event=db.StringField()
    var1=db.StringField(default='none')
    var2=db.StringField(default='none')

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')


def sendEmail(recipientsArr,subject,msgBody):
    try:
        msg = Message(subject, sender='support.anveshana@jnnce.ac.in',recipients=recipientsArr)
        msg.body = msgBody
        msg.html = msgBody
        mail.send(msg)
        return 1
    except:
        return 0

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("registerpage.html")
    else:
        try:
            if(request.form['password'] == request.form['agpassword']):
                data = {
                    "name": request.form['name'].strip(),
                    "email": request.form['email'].strip(),
                    "mobile":request.form['mno'].strip(),
                    "password": request.form['password'],
                    }
                data = json.dumps(data)
                record = json.loads(data)
                d = User(name=record['name'], email=record['email'],mobile=record['mobile'],password=record['password'])
                m=User.objects(email=request.form['email'])
                email=request.form['email'].strip()
                name=request.form['name'].strip()
                if m:
                    for doc in m:
                        if doc['verified']=='False':
                            otp = generateOTP()
                            msg="Dear <b>%s</b>,<br>This message is sent from ANVESHANA web application.<br> Your OTP for confirming your registration is <b>%s</b><br> Regards. <br><b>Team ANVESHANA</b>" % ( name, otp)
                            if(sendEmail([email],'OTP for ANVESHANA Site - '+str(otp),msg)):
                                pass
                            else:
                                return render_template("registerpage.html", error="ERROR : SERVER ERROR CONTACT THE ADMIN.")
                            try:
                                m.delete()
                                d.save()
                                g=Flag.objects(key=record['email'])
                                if g:
                                    g.delete()
                                m=Flag(key=record['email'],value=str(otp))
                                m.save()
                                resp = make_response(render_template("otpConfirm.html",confirm="Confirm your account first by entering the OTP sent to your registered email - "+str(record['email']+" for any changes in the email contact the admin.")))
                                resp.set_cookie('user',record['email'])
                                return resp
                            except:
                                return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
                        else:
                            return render_template("login.html", error="ERROR : YOUR ACCOUNT EXISTS YOU CAN LOGIN.")
                else:
                    otp = generateOTP()
                    msg="Dear <b>%s</b>,<br>This message is sent from ANVESHANA web application.<br> Your OTP for confirming your registration is <b>%s</b><br> Regards. <br><b>Team ANVESHANA</b>" % ( name, otp)
                    if(sendEmail([email],'OTP for ANVESHANA Site - '+str(otp),msg)):
                        pass
                    else:
                        return render_template("registerpage.html", error="ERROR : SERVER ERROR CONTACT THE ADMIN.")
                    try:
                        d.save()
                        m=Flag(key=record['email'],value=str(otp))
                        m.save()
                        resp = make_response(render_template("otpConfirm.html"))
                        resp.set_cookie('user',record['email'])
                        return resp
                    except:
                        return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
            else:
                return render_template("registerpage.html", error="ERROR : PASSWORD MISMATCH.")
        except:
            return render_template("login.html",error="ERROR : SERVER ERROR.")
@app.route('/confirmOTP',methods=['GET','POST'])
def otpConfirm():
    otpf=request.form['otp']
    try:
        otp1=Flag.objects(key=request.cookies.get('user'))
        m=json.dumps(otp1)
        m=m[1:len(m)-1]
        s=json.loads(m)
        otp=str(s['value'])
        d=User.objects(email=request.cookies.get('user'))
        m=json.dumps(d)
        m=m[1:len(m)-1]
        s=json.loads(m)
        if(otp==str(otpf)):
            d.update(verified="True")
            otp1.delete()
            msg="Dear <b>%s</b>,<br>This message is sent from ANVESHANA web application.<br> Your request has been sent to the ADMIN. Please wait for email confirmation of your account authenticaation.<br> <br> Regards. <br><b>Team ANVESHANA</b>" % ( s['name'])
            if(sendEmail([s['email'],'navaneethtth@gmail.com','support.anveshana@jnnce.ac.in'],'Request Received',msg)):
                pass
                return render_template("login.html", done="SUCCESS : REQUEST ACCEPTED WAIT FOR EMAIL CONFIRMATION FOR YOUR ACCEPT.")

        else:
            d.delete()
            otp1.delete()
            return render_template("registerpage.html", error="ERROR : OTP MISMATCH REGISTER AGAIN.")
    except:
        return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        
        u = User.objects(email=username)
        
        if not u:
            return render_template("login.html",error="ERROR : USER ACCOUNT DOESN'T EXIST.")
        else:
            m=json.dumps(u)
            m=m[1:len(m)-1]
            s=json.loads(m)
            if(password == s['password']):
                resp = make_response(redirect('/home'))
                name = s['name']
                email = s['email']
                type =s['type']
                resp.set_cookie('user', name)
                resp.set_cookie('email', email)
                resp.set_cookie('type', type)
                session["name"]=name
                return resp
            else:
                return render_template("login.html", error="ERROR : WRONG PASSWORD.")     
            '''if(password == s['password'] and s['type']=='ADMIN'):
                resp = make_response(redirect('/confirmUser'))
                name = s['name']
                type = s['type']
                resp.set_cookie('user', name)
                resp.set_cookie('type', type)
                resp.set_cookie('email',s['email'])
                session["name"]=name
                return resp'''
@app.route('/forgotPass',methods=['GET','POST'])
def forgotPass():
    if request.method=="GET":
        return render_template("forgotPass.html")
    else:
        try:
            email=str(request.form['email'].strip())
            otp = generateOTP()
            msg="Dear <b>%s</b>,<br>This message is sent from EKAYM web application.<br> Your OTP for confirming your identity is <b>%s</b><br> Regards. <br><b>Team EKYAM</b>" % ( name, otp)
            if(sendEmail([email],'OTP for EKYAM Website - '+str(otp),msg)):
                pass
            else:
                return render_template("registerpage.html", error="ERROR : SERVER ERROR CONTACT THE ADMIN.")
            try:
                d=Flag.objects(key=email)
                if(d):
                    d.delete()
                m=Flag(key=record['email'],value=str(otp))
                m.save()
                resp = make_response(render_template("otpConfirm.html"))
                resp.set_cookie('user',record['email'])
                return resp
            except:
                return render_template("registerpage.html", error="ERROR : SERVER ERROR.")
        except:
            return render_template("login.html",error="ERROR : USER ACCOUNT DOESN'T EXIST.")

        

@app.route('/', methods=['GET', 'POST'])
def participantlogin():
    return redirect("/login")
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method=="GET":
        d=Participant1.objects()
        m=Participant2.objects()
        if(request.cookies.get('user') and request.cookies.get('type')=='user'):
            return render_template("userHome.html",d=d,m=m)
        elif(request.cookies.get('user') and request.cookies.get('type')=='admin'):
            return render_template("adminHome.html",d=d,m=m)
        else:
            return render_template("login.html",error="ERROR : UNAUTHORIZED LOGIN.")
    else:
        if(request.cookies.get('user') and request.cookies.get('type')=='admin'):
            f = request.files['file']
            data_xls = pd.read_excel(f)
            app.logger.error(data_xls)
            if(request.form.get('check')=="True"):
                for i in range(len(data_xls)):
                    if(data_xls.values[i,2]=="DB Maniac" ):
                        data = {
                            "regNo": data_xls.values[i,4],
                            "teamName":data_xls.values[i,3],
                            "participant1":data_xls.values[i,5],
                            "email1":data_xls.values[i,7],
                            "usn1":data_xls.values[i,6],
                            "phone1":data_xls.values[i,8],
                            "amount":data_xls.values[i,23],
                            "utr":data_xls.values[i,24],
                            "accomodation":data_xls.values[i,27],
                            "event":data_xls.values[i,2],
                            
                            }
                        data = json.dumps(data)
                        record = json.loads(data)
                        d = Participant2(regNo=str(record['regNo']), teamName=record['teamName'],participant1=record['participant1'],email1=record['email1'],usn1=record['usn1'],phone1=str(record['phone1']),amount=str(record['amount']),utr=str(record['utr']),accomodation=record['accomodation'],event=record['event'])
                        d.save()
                    else:
                        data = {
                            "regNo": data_xls.values[i,4],
                            "teamName":data_xls.values[i,3],
                            "participant1":data_xls.values[i,11],
                            "participant2":data_xls.values[i,17],
                            "email1":data_xls.values[i,13],
                            "email2": data_xls.values[i,19],
                            "usn1":data_xls.values[i,12],
                            "usn2":data_xls.values[i,18],
                            "phone1":data_xls.values[i,14],
                            "phone2":data_xls.values[i,20],
                            "amount":data_xls.values[i,23],
                            "utr":data_xls.values[i,24],
                            "accomodation":data_xls.values[i,27],
                            "event":data_xls.values[i,2],
                            
                            }
                        data = json.dumps(data)
                        record = json.loads(data)
                        d = Participant1(regNo=str(record['regNo']), teamName=record['teamName'],participant1=record['participant1'],participant2=record['participant2'],email1=record['email1'],email2=record['email2'],usn1=record['usn1'],usn2=record['usn2'],phone1=str(record['phone1']),phone2=str(record['phone2']),amount=str(record['amount']),utr=str(record['utr']),accomodation=record['accomodation'],event=record['event'])
                        try:
                            d.save()
                        except:
                            continue
            else:
                if(request.cookies.get('user') and request.cookies.get('type')=='admin'):
                    m1=Participant1.objects()
                    m2=Participant2.objects()

                    for i in m1:
                        i.delete()
                    for i in m2:
                        i.delete()
                    f = request.files['file']
                    data_xls = pd.read_excel(f)
                    app.logger.error(data_xls)
                    for i in range(len(data_xls)):
                        if(data_xls.values[i,2]=="DB Maniac" ):
                            data = {
                                "regNo": data_xls.values[i,4],
                                "teamName":data_xls.values[i,3],
                                "participant1":data_xls.values[i,5],
                                "email1":data_xls.values[i,7],
                                "usn1":data_xls.values[i,6],
                                "phone1":data_xls.values[i,8],
                                "amount":data_xls.values[i,23],
                                "utr":data_xls.values[i,24],
                                "accomodation":data_xls.values[i,27],
                                "event":data_xls.values[i,2],
                                
                                }
                            data = json.dumps(data)
                            record = json.loads(data)
                            d = Participant2(regNo=str(record['regNo']), teamName=record['teamName'],participant1=record['participant1'],email1=record['email1'],usn1=record['usn1'],phone1=str(record['phone1']),amount=str(record['amount']),utr=str(record['utr']),accomodation=record['accomodation'],event=record['event'])
                            d.save()
                        else:
                            data = {
                                "regNo": data_xls.values[i,4],
                                "teamName":data_xls.values[i,3],
                                "participant1":data_xls.values[i,11],
                                "participant2":data_xls.values[i,17],
                                "email1":data_xls.values[i,13],
                                "email2": data_xls.values[i,19],
                                "usn1":data_xls.values[i,12],
                                "usn2":data_xls.values[i,18],
                                "phone1":data_xls.values[i,14],
                                "phone2":data_xls.values[i,20],
                                "amount":data_xls.values[i,23],
                                "utr":data_xls.values[i,24],
                                "accomodation":data_xls.values[i,27],
                                "event":data_xls.values[i,2],
                                
                                }
                            data = json.dumps(data)
                            record = json.loads(data)
                            d = Participant1(regNo=str(record['regNo']), teamName=record['teamName'],participant1=record['participant1'],participant2=record['participant2'],email1=record['email1'],email2=record['email2'],usn1=record['usn1'],usn2=record['usn2'],phone1=str(record['phone1']),phone2=str(record['phone2']),amount=str(record['amount']),utr=str(record['utr']),accomodation=record['accomodation'],event=record['event'])
                            try:
                                d.save()
                            except:
                                continue
                else:
                    return render_template("login.html",error="ERROR : UNAUTHORIZED ACCESS REQUEST.")


            return redirect("/home")
                    

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method=="GET":
        if(request.cookies.get('user') and request.cookies.get('type')=='admin'):
            m=User.objects(type='none')
            return render_template("verify.html",data=m)
        
        else:
            return render_template("login.html",error="ERROR : UNAUTHORIZED LOGIN.")       
@app.route('/remove', methods=['GET'])
def remove():
    if request.method=="GET":
        if(request.cookies.get('user') and request.cookies.get('type')=='admin'):
            m1=Participant1.objects()
            m2=Participant2.objects()

            for i in m1:
                i.delete()
            for i in m2:
                i.delete()
            return redirect("/home")
        
        else:
            return render_template("login.html",error="ERROR : UNAUTHORIZED ACCESS REQUEST.")      
    
@app.route('/verifya/id=<id>', methods=['POST'])
def verifya(id):
    if(request.cookies.get('user') and request.cookies.get('type')=='admin'):
        u=User.objects(email=str(id))
        m=json.dumps(u)
        m=m[1:len(m)-1]
        s=json.loads(m)
        l=User(email = s['email'], password = s['password'] ,name =s['name'] , mobile=s['mobile'] , type ="user" , verified="True")
        u.delete()
        l.save()
        msg="Dear <b>%s</b>,<br>This message is sent from ANVESHANA web application.<br> Your request to access ANVESHANA website has been <strong>accepted</strong> by the ADMIN. Now you can login to your account.<br> <br> Regards. <br><b>Team ANVESHANA</b>" % ( s['name'])
        sendEmail([s['email']],'Request Accepted',msg)
        return redirect("/verify")

@app.route('/verifyr/id=<id>', methods=[ 'POST'])
def verifyr(id):
    if(request.cookies.get('user') and request.cookies.get('type')=='admin'):
        u=User.objects(email=str(id))
        m=json.dumps(u)
        m=m[1:len(m)-1]
        s=json.loads(m)
        u.delete()
        msg="Dear <b>%s</b>,<br>This message is sent from ANVESHANA web application.<br> Your request to access ANVESHANA website has been <strong>declined</strong> by the ADMIN. Sorry for the inconvenience.<br> <br> Regards. <br><b>Team ANVESHANA</b>" % ( s['name'])
        sendEmail([s['email']],'Request Declined',msg)
        return redirect("/verify")
        
            

if __name__ == "__main__":
    app.run(debug=True)
