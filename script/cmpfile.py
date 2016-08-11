#!/usr/bin/python
#coding:utf-8
#检查git仓库文件对比线上的文件
import os,hashlib,datetime
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#global_DirOld = ""
#global_DirNew = ""
global_FilesList = []

#输入要比对的文件路径

StaticDir = '/data/test_static'
TempDir = '/tmp/test_static'
#while not os.path.exists(global_DirOld):	 
#global_DirNew = unicode(raw_input(u"请输入要检测文件的目录："),"utf-8")

#将数据保存到文件中
def SaveToFile(filePath,content):
    try:
        f = open(filePath,"a+")
        f.write(content.encode("utf-8") + "\n")
        f.close()
    except Exception,ex:
        print "Error:" + str(ex)

#计算文件的MD5值
def CalcMD5(filepath):
    try:
        #以二进制的形式打开
        with open(filepath,'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            return hash
    except Exception,ex:
        print "Error:" + str(ex)
        return None

#遍历目录下的所有文件
def GetAllSubFiles():
    global global_FilesList
    for dir in os.walk(StaticDir):
        for file in dir[2]:
            filePath = dir[0] + os.sep + file
            global_FilesList.append(filePath[len(StaticDir)+1:])

#列出新增文件和变动的文件
def ListChangedFiles():
    global TempDir,StaticDir,global_FilesList
    print "变动或新增的文件："
    for file in global_FilesList:
        filePathOld = TempDir + os.sep + file
        filePathNew = StaticDir + os.sep + file
        if not os.path.exists(filePathOld) or CalcMD5(filePathOld)!=CalcMD5(filePathNew):
            content = "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ "]" + filePathNew
            print filePathNew
	    #cmd = 'cp -rfv '+ filePathNew + ' '+TempDir+'/'
	    #os.system(cmd)
            #print content
            SaveToFile("ChangedFiles.txt",content)

if __name__=="__main__":
#    InputDirPath()
    GetAllSubFiles()
    ListChangedFiles()

