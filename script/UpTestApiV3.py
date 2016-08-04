#!/usr/bin/python
#Version 1.0
#
#coding:utf-8
import sys
import getopt
import time
import os
import ConfigParser
import hashlib
import pickle
import config.Config as c
import modules.function as f
import modules.Readfile as rf
import shutil
import subprocess

BASEDIR = os.path.split(os.path.realpath(__file__))[0]
os.chdir(BASEDIR)
CURRENTPATH = os.getcwd()
#help
def Usage():
	info = """
	Info of Exec Script


	"""
	print info
#define config class 	
class Config:
	"""
	Info of config.ini
	"""
	def __init_(self,path):
		self.path = path
		self.cf = ConfigParSer.ConfigParser()
		self.cf.read(self.path)
	def get(self,field,key):
		result = ""
		try:
			result = self.cf.get(field,key)
		except:
			result = ""
		return result
	def set(self,field,key,value):
		try:
			self.cf.set(field,key,value)
			cf.write(open(self.path,'w'))
		except:
			return False
		return True
def read_config(config_file_path,field,key):
	cf = ConfigParser.ConfigParser()
	try:
		cf.read(config_file_path)
		result = cf.get(field,key)
	except:
		sys.exit(1)
	return result



staticdir = str(read_config(BASEDIR+'/etc/config.ini','dirconf','StaticDir'))
AppDir = str(read_config(BASEDIR+'/etc/config.ini','dirconf','AppDir'))
last_pyyxversion = str(read_config(BASEDIR + '/etc/config.ini','versionconf','lastpyyxversion_test'))
last_staticversion = str(read_config(BASEDIR + '/etc/config.ini','versionconf','laststatictestversion'))
statictmpfile = str(read_config(BASEDIR + '/etc/config.ini','versionconf','statictmpfile'))
inifile = str(read_config(BASEDIR + '/etc/config.ini','versionconf','inifile'))
javabin = str(read_config(BASEDIR + '/etc/config.ini','javaevnconf','javabin'))
os.chdir(staticdir)
#print os.getcwd()

def CalcSha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        return hash

def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        return hash

#check version 
testVer = False
while ( not testVer):
	userType = raw_input("Please type push test version: ")
	res = f.testGitVersion(userType,AppDir)
	if (not res ):
		f.echo('Your type version '+userType+' is not exist.',2)
	else:
		testVer = True
		VERSION = userType
		print VERSION,testVer

#get time 
nowTime = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
tagInfo = VERSION+'-'+nowTime;

#pull appcode
os.chdir(AppDir)
cmd = 'git fetch '
f.command(cmd)
cmd = 'git checkout '+ VERSION
f.command(cmd)
cmd ='git pull origin '+ VERSION
f.command(cmd)
#############  get log commit version
#
#
#
os.chdir(BASEDIR)

if (not os.path.isfile(last_pyyxversion)):
        cmd = 'touch '+last_pyyxversion
        f.command(cmd)
        os.chdir(AppDir)
        cmd = 'git log --pretty=format:"%H"|tail -1'
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        out = p.communicate()[0]
        pyyxlastversion = out.strip()
else:
        fp = open(last_pyyxversion)
        pyyxlastversion = fp.read().strip()
        fp.close
os.chdir(AppDir)
cmd = 'git log --pretty=format:"%H"|head -1'
p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
out = p.communicate()[0]
pyyxcurrentversion = out.strip()
print '''
_____________________________________________________________________
pyyx version info:

	pyyx currentversion: %s
	                                          
	pyyx last version: %s
_____________________________________________________________________
''' % (pyyxcurrentversion,pyyxlastversion)

if (pyyxcurrentversion != pyyxlastversion):

	#get the diff file
	cmd = 'git diff '+pyyxcurrentversion+' '+pyyxlastversion+' --name-only'+' '+'|'+'xargs -i cp -rf --parents {}'+' '+BASEDIR+'/tmp/pyyxtmpfile/'
#	print cmd
	os.system(cmd)
	#use ansible push the files
	optinfo = raw_input("""
	\033[32m Please choose Push content:
	y ) push api	
	n ) exit
	\033[0m
	"""
	)
	
	optlist = ('y','n')
	if (optinfo == 'y'):
			cmd = '/usr/bin/ansible-playbook -i '+BASEDIR+'/config/hostslist '+BASEDIR+'/config/apideploy.yml -e"environ=api site=test version='+tagInfo+'"'
			f.command(cmd)
	if (optinfo == 'n'):
			print 'No push and exit.'
			sys.exit(2)
	if (optinfo not in optlist):
		print '\033[31m Input is wrong,no this option, \033[0m',optinfo
		sys.exit()
	
	#write the version info to the file
	os.chdir(BASEDIR)
	cmd = 'echo '+pyyxcurrentversion+'>'+last_pyyxversion
	f.command(cmd)
	print '__________________________________________Done________________________________________________________'
	#push appcode to server list
else:
	print "pyyx notthing to upgrade."
	print "________________________"










