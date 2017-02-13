#!/usr/bin/python 
#coding:utf-8


from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeRegionsRequest
import datetime
import json
import time
import sys
import os
import string
import re
import time 
import xlwt
import copy

date = time.strftime("%Y-%m-%d-%H-%M-%S")
filename = "/tmp/%s_rds_slowlog.xls" % date
Action = 'DescribeSlowLogRecords'
Key = 'DescribeSlowLogRecords' 
Opt = 'Slowlog'
row = 0
title = ['instance','ParseRowCounts','HostAddress',\
'ExecutionStartTime','QueryTimes','LockTimes','SQLText']
#获取utc时间时间间隔24hour
UtStartTime = datetime.datetime.utcnow()
mm = datetime.timedelta(minutes=1440)
StartD = UtStartTime.strftime('%Y-%m-%dT%H:%MZ')
EndD = (UtStartTime - mm).strftime('%Y-%m-%dT%H:%MZ')

print "startD:%s" % StartD
print "endD:%s" % EndD

mysql_instance = {
                'rm-bp1m6fg4jqgd8c4d6':'p_mysql_single',
                'rm-bp19iseb9wo335ic4':'p_mysql_stat',
                'rds283x305zml16st5c1':'mysql_test',
                'rds86m8fl5c58df2f55e':'mysql_d',
                'rm-bp101k2t0885wm35s':'p_mysql_imp_a',
                'rm-bp198emri0f6kk3k5':'p_mysql_imp_b',
                'rm-bp14b0sy7o28f89i4':'p_mysql_imp_c',
                'rm-bp1lcao98lj19z9nf':'p_mysql_imp_d',
                'rdsh981111il84bkp90b':'p_mysql_user_a',
                'rdso0387bf5bb5s28wt9':'p_mysql_user_b',
                'rdsu9ym3i55m26l1i29w':'p_mysql_user_c',
                'rds9t8x9vmkl9922k87z':'p_mysql_user_d'
}
mail_to_user = ['hongtengfei@pyyx.com','dengxiangyu@pyyx.com',\
                'zhanglei@pyyx.com','xiaoyouqiang@pyyx.com',\
                'liuhaitao@pyyx.com','mayi@pyyx.com']

#mail_to_user = ['dengxiangyu@pyyx.com']


def Request_aliyunapi_getusage(InId,Action,Key,Opt):
    SQLSlowRecord = []
    totalrecordcount = 0
    try:
        clt = client.AcsClient('tablBShBzl4KNW0R',\
        'ag3ya5SaJjGXHS5QO66JxahzDtUTFNdeng','cn-hangzhou')
        request=DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        request.set_action_name(Action)
        request.set_query_params(dict(DBInstanceId=InId,key=Key,\
        StartTime=EndD,EndTime=StartD))
        result = eval(clt.do_action(request))
        total = result['TotalRecordCount']
        print 'slowlog total number : %s' % total
        if total > 0 and total < 100:
            print 'slowlog number 0-100'
            request.set_query_params(dict(DBInstanceId=InId,\
            key=Key,StartTime=EndD,EndTime=StartD,PageSize=100,PageNumber=1))
            result = eval(clt.do_action(request))
            SQLSlowRecord.extend(result['Items']['SQLSlowRecord']) 
        elif total != 0 and total > 100 :
            print 'slowlog number more than 100'
            PageNumber = total / 100
            print "pagenumber is %s" % PageNumber
            i = 0
            if PageNumber > 30:
                PageNumber = 30
            for i in range(1,PageNumber):
                request.set_query_params(dict(DBInstanceId=InId,\
                key=Key,StartTime=EndD,EndTime=StartD,PageSize=100,PageNumber=i))
                result = eval(clt.do_action(request)) 
                SQLSlowRecord.extend(result['Items']['SQLSlowRecord']) 
                i = i + 1 
                print i
        else:
            PageNumber = 0
        return SQLSlowRecord   #return slowrecord list
    except Exception as e:
        print e 
        print -1 
#        sys.exit(1)
     
def write_excel(slowrecord):
    style = xlwt.easyxf('font: bold 1')
    global row
    row = row + 1
    merge_now = copy.deepcopy(row) + 1 
    #print "merge_now %s" % merge_now 
    merge_done = len(slowrecord) + merge_now -1
    #print "merge_done %s" % merge_done

    for x,y in enumerate(slowrecord): 
        row = row + 1
        for i,j in enumerate(title[1:]):
            cloumn = i + 1
            if j == 'SQLText' and len(y[j]) >=  32767:
                sheet.write(row,cloumn,y[j][:30000].replace('\n',''))
                sheet.write(row,cloumn+1,y[j][30000:].replace('\n',''))
            elif j == 'SQLText':
                sheet.write(row,cloumn,y[j].replace('\n',''))
            elif j == 'ExecutionStartTime':
                utc_time = y[j]
                utc_timestamp = time.mktime(time.strptime(utc_time,'%Y-%m-%dT%H:%M:%SZ'))
                local_timestamp = int(utc_timestamp + 28800)
                tmp_timestamp = time.localtime(local_timestamp) 
                local_time_str = time.strftime('%Y-%m-%d %H:%M:%S',tmp_timestamp)
                sheet.write(row,cloumn,local_time_str) 
            else:
                sheet.write(row,cloumn,y[j])
    sheet.write_merge(merge_now,merge_done,0,0,mysql_instance[InId],style)


def S_Mail(user):
    cmd = "echo '%s_rds_slowlog'|mail -s 'rds_slowlog' -a %s %s" % (date,filename,user)
    print cmd
    os.system(cmd)


if __name__=='__main__':
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('rds_slowlog') 
    title = ['instance','ParseRowCounts','HostAddress',\
    'ExecutionStartTime','QueryTimes','LockTimes','SQLText']
    sec_col = sheet.col(1)
    thr_col = sheet.col(2)
    four_col = sheet.col(3)
    six_col = sheet.col(6)
    sec_col.width = 256*20
    thr_col.width = 256*40
    four_col.width = 256*20
    six_col.width = 256*100

    for x,y in enumerate(title):
        sheet.write(row,x,y)

    for InId in mysql_instance.keys(): 
        print InId
        slowrecord = Request_aliyunapi_getusage(InId,Action,Key,Opt)
        if slowrecord:
            write_excel(slowrecord) 
        else:
            pass

    workbook.save(filename)
    for user in mail_to_user:
   	S_Mail(user)
