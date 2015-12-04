from bottle import route, run, request


from bottle import get, run
import bottle
from bottle import error
from bottle import static_file
import mysql.connector
import pymongo
import cgi
import re
import datetime
import random
import hmac
import user
import sys
import os
from Crypto.PublicKey import RSA
from Crypto import Random

from server_sync import add_new

i=0


@bottle.post('/newNode')
def insert_entry():
    postdata = request.body.read()
    print postdata #this goes to log file only, not to client
    name,location=postdata.split("=",1)
    pwd="pwd"+name+location
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    public_key=key.publickey()
    enc_data=public_key.encrypt(pwd,32)
    print enc_data
    cnx=mysql.connector.connect(user="ideate",password='password',database='one')
    cursor=cnx.cursor()
    try:
      add_entry=("INSERT INTO data (name,location,pwd) VALUES (%s,%s,%s)")
      entry_data=(name,location,pwd)
      cursor.execute(add_entry,entry_data)
      cursor.close()
      cnx.commit()
	    #q="SELECT uid from data WHERE name='"+name+"' and pwd='"+pwd+"';"
	    #cursor1.execute(q)
	    #result=cursor1.fetchone()
	    #cnx.commit()
	    #cursor1.close()
      cnx.close()
		
	    #tirtha 28/11
	    #add_new(name, pwd)
	    #sending uid and pwd to client
      return pwd	
	
    except:
        print ("Error inserting post")
	      #return "Invalid"



@bottle.post('/login') 
def do_login(): 
	postdata=request.body.read()
	uid,pwd=postdata.split("=",1)
	print uid+" "+pwd
	cnx=mysql.connector.connect(user="ideate",password='password',database='one')
    	cursor=cnx.cursor()
	cursor.execute("select uid,pwd from data where uid="+uid+" and pwd='"+pwd+"'")
	result=cursor.fetchone()
	if result : 
		return "1" 
	else: 
		return "0"




run(host='localhost', port=8080, debug=True)
