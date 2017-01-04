#!/usr/bin/env python
#coding:utf-8
#Frank
import os
import subprocess
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import smtplib

logpath = "/var/log/192.168.1.1.log"
def SendMail(html):
        From = 'auto-push@pyyx.com'
        To = ['huanghuajin@pyyx.com','frank_spr@163.com']
#        subject = 'python email test'
        smtpserver = 'smtp.exmail.qq.com'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "%s %s" % ( '',Header("Firewall monitor","utf-8"))
        msg['From']= From
        msg['To']=",".join(To)
        username = 'auto-push@pyyx.com'
        password = 'Yinxiang001'
        part = MIMEText(html,'html')
        msg.attach(part)
#        print "Send mail......"
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com')
        smtp.login(username,password)
        smtp.sendmail(From, To, msg.as_string())
        smtp.quit()


def monitorLog(logfile):
  popen = subprocess.Popen('tail -f '+ logfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
  pid = popen.pid
 # print 'Popen.pid'+ str(pid)
  while True:
    line = popen.stdout.readline().strip()
    try:
      if len(line) >11:
	
        ipaddr = re.match('10.100.\d{1,3}\.\d{1,3}',line.split()[10])
        if ("logged" in line and ipaddr == None):
      	  SendMail(line)
        else:
	  pass
    except Exception as e:
      print e
if __name__ == '__main__':
  monitorLog(logpath)
  
