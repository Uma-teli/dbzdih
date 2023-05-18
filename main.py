import os
import json
import requests
import tornado.web
import tornado.autoreload
import sys
import asyncio
#import psycopg2
import hazelcast
import logging







#import matplotlib.pyplot as plt

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))
#port=8000
class landingPage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")
        
class HomePage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")

class Login(tornado.web.RequestHandler):
    def post(self):
        #base_url = 'https://api.eu-gb.apiconnect.appdomain.cloud/m1ganeshtcscom1543928228162-dev/sb/payments/custReg?acctId='
        # 100000001001 is the only working answer
        #headers = {'Content-Type': 'application/json'}
        print("inside login")
        username = str(self.get_body_argument("uname"))
        print(username)
        pwd = str(self.get_body_argument("pass"))
        print(pwd)
        #end_url= base_url+str(self.get_body_argument("accnt"))
        #req = requests.get(end_url, headers=headers, auth=('701e3938-c7c7-4568-9e3b-d474bfb39700', ''), verify=False)
        #json_out = req.json()
        print("json")
        if username =="admin" and pwd == "adminpass":
            print("success")
            self.render("static/indexx.html")
        else:
            print("no")
            self.render("static/trial.html")
        #print(json_out)
        #self.render("static/genericresp.html",msg=json_out['CSRGRES']['CSRGRES']['MESSAGES'],cname=json_out['CSRGRES']['CSRGRES']['CUSTOMER_NAME'],cid=json_out['CSRGRES']['CSRGRES']['CUSTOMER_ID'],date=json_out['CSRGRES']['CSRGRES']['SYS_DATE'],time=json_out['CSRGRES']['CSRGRES']['SYS_TIME'],bloc="regreq")



class basicRevHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/reversal.html")


       

        

       
class AccountList(tornado.web.RequestHandler):
    def post(self):

       
        
        
        headers = {'Content-Type': 'application/json'}
        logging.basicConfig(level=logging.INFO)
        client = hazelcast.HazelcastClient(
                cluster_name="zdih-tcs",
                cluster_members=[
                            "192.86.32.113:6701",
                ])
        
        account=int(self.get_argument('account'))
        print(account)
        #result=client.sql.execute(f"SELECT * FROM TCS001_ACCOUNT WHERE Account_Number= {account} ").result()
        result1=client.sql.execute(f"SELECT * FROM TCS001_TRANSACTION WHERE Account_Number= {account} ").result()
        

        for row in result1:
                print(row.get_object("Account_Number"))
                print(row.get_object("Available_Balance"))
                Account_no=row["Account_Number"]
                balance=row["Available_Balance"]
                self.render("static/result.html",accountno=Account_no,balance=balance,headers=headers,bloc="AccountList")
       
       
        

        
       
        client.shutdown()
       
       


class AccountTransaction(tornado.web.RequestHandler):
    def post(self):
        logging.basicConfig(level=logging.INFO)
        client = hazelcast.HazelcastClient(
            cluster_name="zdih-tcs",
            cluster_members=[

                "192.86.32.113:6701",
                ])
        
        act=int(self.get_argument("act"))
        print(act)
        #damt=int(self.get_argument("damt"))
        #print(damt)

        
       
       

       
        result1=client.sql.execute(f"SELECT * FROM TCS001_TRANSACTION WHERE Account_Number= {act}").result()
        for row in result1:
            print(row.get_object("Available_Balance"))
            print(row.get_object("Account_Number"))
            print(row.get_object("Trans_Amount"))
            print(row.get_object("Bank_Id"))
            print(row.get_object("Description"))
            Account_no=row["Account_Number"]
            balance=row["Available_Balance"]
            transamt=row["Trans_Amount"]
            bankid=row["Bank_Id"]
            desc=row["Description"]


        #balance1=balance+damt
        #client.sql.execute(f"UPDATE TCS001_TRANSACTION SET Available_Balance= {balance1} WHERE Account_Number={act}").result()
        #result3=client.sql.execute(f"SELECT * FROM TCS001_TRANSACTION WHERE Account_Number= {act}").result()
        #for row in result3:
            #print(row.get_object("Available_Balance"))
            #b=row["Available_Balance"]
            

        self.render("static/AccountTransaction.html",Accountno=Account_no,balance=balance,tamt=transamt,bid=bankid,desc=desc,bloc="AccountTransaction")
       
        


            
       

        
       
class AccountDetails(tornado.web.RequestHandler):
    def post(self):
        logging.basicConfig(level=logging.INFO)
        client = hazelcast.HazelcastClient(
            cluster_name="zdih-tcs",
            cluster_members=[

                "192.86.32.113:6701",
                ])
        
        acct=int(self.get_argument("acct"))
        print(acct)
        camt=int(self.get_argument("camt"))
        print(camt)
       
        result1=client.sql.execute(f"SELECT * FROM TCS001_TRANSACTION WHERE Account_Number= {acct}").result()
        for row in result1:
            print(row.get_object("Available_Balance"))
            print(row.get_object("Account_Number"))
            Account_no=row["Account_Number"]
            balance=row["Available_Balance"]



        balance2=balance-camt
        client.sql.execute(f"UPDATE TCS001_TRANSACTION SET Available_Balance= {balance2} WHERE Account_Number={acct}").result()
        result4=client.sql.execute(f"SELECT * FROM TCS001_TRANSACTION WHERE Account_Number= {acct}").result()
        for row in result4:
            print(row.get_object("Available_Balance"))
            b=row["Available_Balance"]

        self.render("static/AccountDetails.html",accountno=Account_no,balance=b,bloc="AccountDetails")
       
            

        #base_url='http//192.867.32.113:16099/zdih/rest/api/v1/accounts='
        #account=str(self.get_body_argument('account'))
        #headers = {'Content-Type': 'application/json'}
        #end_url= base_url+str(self.get_body_argument("account"))
        #req = requests.get(end_url, headers=headers, auth=('ibmuser', 'tcs2041'), verify=False)
        #json_out = req.json()
       # print("json")
        #print(json_out)
        #self.render("static/AccountDetails.html",accountno= json_out[0][0], balance=json_out[0][1] ,ID= json_out[0][2],bloc="AccountDetails") 


        ###cursor=conn.cursor()
        ##records= cursor.fetchall()

        #cursor.close()
        #conn.close()

        #self.render("static/AccountDetails.html",accountno=records[0][0], balance=records[0][1] ,ID=records[0][2],bloc="AccountDetails") 



if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", landingPage),
        (r"/AccountList", AccountList),
        (r"/AccountDetails",AccountDetails),
        (r"/AccountTransaction",AccountTransaction)
        

    ])
    print("commit")
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.listen(port)
    # TODO remove in prod
    #print("inside win")
    #server=HTTPServer(app)
    tornado.autoreload.start()
    print("I'm listening on port specified")
    print(port)
    tornado.ioloop.IOLoop.current().start()
