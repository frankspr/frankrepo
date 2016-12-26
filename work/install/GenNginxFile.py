#coding=utf-8
#Frank
#Date:2016-12-23
#将阿里云上的SLB挂载实例ip写入到backend.conf
import json
from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

clt = client.AcsClient('tablBShBzl4KNW0R', 'ag3ya5SaJjGXHS5QO66JxahzDtUTFN', 'cn-hangzhou')
lb_id = '152b60fc1da-cn-hangzhou-dg-a01'

def get_ecs_info():
  request = DescribeInstancesRequest.DescribeInstancesRequest()
  request.set_accept_format('json')
  request.set_PageSize(50)
  result = json.loads(clt.do_action(request)).get('Instances').get('Instance')
  ecs_dict={}
  for line in result:
    ecs_dict[line['InstanceId']]=line['VpcAttributes']['PrivateIpAddress']['IpAddress']
  return ecs_dict
ecs = get_ecs_info()

def gen():
    request = DescribeLoadBalancerAttributeRequest();
    request.set_LoadBalancerId(lb_id);
    request.set_accept_format('json')
    response_str = clt.do_action(request)
    fp = open('./backend.conf','w')
    fp.write('upstream backend {'+'\n')
    fp.write('	ip_hash;'+'\n')
    if response_str:
        response_obj = json.loads(response_str);
        if response_obj:
            ecs_list = response_obj.get('BackendServers').get('BackendServer');
            for line in  ecs_list:
              print ecs[line['ServerId']][0]
              fp.write('	'+'server '+ecs[line['ServerId']][0]+':8080;'+'\n')
            fp.write('}'+'\n')
    fp.close()
 
 


if __name__ == '__main__':
  gen()
