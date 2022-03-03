from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import threading
import datetime
import pymysql
import certifi
import xlrd
import csv
import os


class MemberData:
    accepted = []
    rejected = []
    max_index = 0

    def getdata(self):
        db = pymysql.connect(host='database-test.cglgkm3wqxbl.eu-west-2.rds.amazonaws.com', user='admin',
                             password='eB8mvRj03r2e', database='gym_data')  # eB8mvRj03r2e

        MemberData.accepted = []
        MemberData.rejected = []

        cursor = db.cursor()
        cursor.execute("SELECT * FROM members")

        data = cursor.fetchall()
        date = str(datetime.datetime.now())
        month = int(date[5:7])
        year = int(date[2:4])
        print(data)
        for d in data:
            if d[5] > self.max_index:
                self.max_index = d[5]
            paid_until = [int(d[4][0:2]), int(d[4][3:5])]
            if paid_until[1] > year or paid_until[0] >= month and paid_until[1] >= year:
                MemberData.accepted.append(d)
            else:
                MemberData.rejected.append(d)

    def new_member(self, fname, lname, phone, membership, paid_until):
        db = pymysql.connect(host='database-test.cglgkm3wqxbl.eu-west-2.rds.amazonaws.com', user='admin',
                             password='eB8mvRj03r2e', database='gym_data')

        cursor = db.cursor()
        cursor.execute("INSERT INTO members VALUES('" + fname + "', '" + lname + "', '" + phone + "', '" + membership + "', '" +
                       paid_until + "', " + str(self.max_index) +", NULL )")
        db.commit()
        self.max_index += 1

    def update_paid(self, fname, lname, paid_until):
        db = pymysql.connect(host='database-test.cglgkm3wqxbl.eu-west-2.rds.amazonaws.com', user='admin',
                             password='eB8mvRj03r2e', database='gym_data')

        cursor = db.cursor()
        cursor.execute("UPDATE members SET paid_until = '"+paid_until+"' WHERE first_name = '" + fname + "' AND second_name = '" + lname + "'")
        db.commit()

    def update_details(self, fname, lname, phone, custom_pay, index):
        db = pymysql.connect(host='database-test.cglgkm3wqxbl.eu-west-2.rds.amazonaws.com', user='admin',
                             password='eB8mvRj03r2e', database='gym_data')

        if not custom_pay.isdecimal():
            if custom_pay[1:].isdecimal():
                custom_pay = custom_pay[1:]
            elif custom_pay[:-1].isdecimal():
                custom_pay = custom_pay[:-1]
            else:
                custom_pay = "NULL"


        cursor = db.cursor()
        cursor.execute("UPDATE members SET first_name = '"+fname+"' , second_name = '"+lname+"' , phone = '"+phone+"' , custom_pay = "+str(custom_pay)+"  WHERE index1 = " + str(index) + " ")
        db.commit()

    def update_membership(self, fname, lname, membership_type):
        db = pymysql.connect(host='database-test.cglgkm3wqxbl.eu-west-2.rds.amazonaws.com', user='admin',
                             password='eB8mvRj03r2e', database='gym_data')

        cursor = db.cursor()
        cursor.execute("UPDATE members SET membership = '"+membership_type+"' WHERE first_name = '" + fname + "' AND second_name = '" + lname + "'")
        db.commit()

    def remove_member(self, fname, lname):
        db = pymysql.connect(host='database-test.cglgkm3wqxbl.eu-west-2.rds.amazonaws.com', user='admin',
                             password='eB8mvRj03r2e', database='gym_data')

        cursor = db.cursor()
        cursor.execute("DELETE FROM members WHERE first_name = '" + fname + "' AND second_name = '" + lname + "'")
        db.commit()

    def email_table(self):

        try:
            date = str(datetime.datetime.now())
            month = str(date[5:7])
            year = str(date[2:4])
            filename = "Monthly_update_"+month+"-"+year+".csv"
            rb = xlrd.open_workbook(filename)
            print('email already sent')
            return False  # in the case email already sent
        except Exception as e:
            if "No such file or directory" in str(e):
                pass  # file not made or sent run function
            else:
                print('error', e)
                return False

        header = ("First Name", "Second Name", "Phone", "Membership", "Paid until", "index", "Custom Pay", "Payment")
        data = []

        for a in MemberData.accepted:
            data.append((a[0], a[1], a[2], a[3], a[4], a[5], a[6], "Paid"))

        for r in MemberData.rejected:
            data.append((r[0], r[1], r[2], r[3], r[4], r[5], r[6], "Not Paid"))

        with open(filename, "w", newline="") as csvfile:
            movies = csv.writer(csvfile)
            movies.writerow(header)
            for x in data:
                movies.writerow(x)
                
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        # Replace with your own gmail account
        gmail = 'service.sailor.opera@gmail.com'
        password = '3E4h4PWQ2dyZ'

        message = MIMEMultipart('mixed')
        message['From'] = 'MMA unit app <{sender}>'.format(sender=gmail)
        message['To'] = 'Imran.farooq27@gmail.com'
        message['Subject'] = 'Monthly update'

        attachmentPath = "./"+filename
        try:
            with open(attachmentPath, "rb") as attachment:
                p = MIMEApplication(attachment.read(), _subtype="csv")
                p.add_header('Content-Disposition', "attachment; filename= " + filename)
                message.attach(p)
        except Exception as e:
            print(str(e))

        context = ssl.create_default_context()
        msg_full = message.as_string()

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(gmail, password)  # "Imran.farooq27@gmail.com"
            cc = ''
            server.sendmail(gmail, "Imran.farooq27@gmail.com".split(";") + (cc.split(";") if cc else []), msg_full)
            server.quit()

        print('email sent')


def initialisation():
    setup = MemberData()
    setup.getdata()
    os.environ['SSL_CERT_FILE'] = certifi.where()
    try:  # solves SSL certificate error
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
    #setup.email_table()
    email_thread = threading.Thread(target=setup.email_table)
    email_thread.start()
    


def reset_table():
    setup = MemberData()
    setup.getdata()

    
#initialisation()

# notes:
# create database gym_data
# CREATE TABLE members(first_name text, second_name text, phone text, membership text)
# INSERT INTO members VALUES('Leeeeroy', 'Jenkinssss','0780085', 'Gym-only')

# cursor.execute("DROP TABLE members")
# cursor.execute("CREATE TABLE members(first_name text, second_name text, phone text, membership text,paid_until text)")
# cursor.execute("INSERT INTO members VALUES('Leeeeroy', 'Jenkinssss','0780085', 'Gym-only', '12/21')")
# cursor.execute("INSERT INTO members VALUES('Leeeeroy1', 'Jenkinssss1','0780086', 'Gym-MMA', '01/22')")
# db.commit()

# memberships: Gym-only, MMA-only, Gym-MMA, None


# db info:
# identifier: database-test
# username: admin
# pword: eB8mvRj03r2e
# host: database-1.cglgkm3wqxbl.eu-west-2.rds.amazonaws.com
# port: 3306
