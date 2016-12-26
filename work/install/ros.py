#!/usr/bin/env python
#coding:utf-8
#create by hongtengfei at 16/8/5 15:52
#导入包
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkros.request.v20150901 import CreateStacksRequest, DescribeStackDetailRequest
#创建ecs模板
number = int(raw_input("Please input the numbers of esc:"))
template = '''
{
  "ROSTemplateFormatVersion" : "2015-09-01",
  "Description": "创建按量付费的ecs实例",
  "Parameters" : {		
    "ImageId": {
		"Type" : "String",
		"Default": "m-bp10zkx5pckclev4b3ku",
		"Description": "Image_ID，start instance to choose image"
    },
    "InstanceType": {
		"Type": "String",
		"Description": "实例的资源规格",
		"Default": " ecs.n1.xlarge"
    },
    "AllocatePublicIP": {
          "Default": false,
          "Description": " allocate public ip.",
          "Type": "Boolean"
    },
    "SecurityGroupName": {
		"Type": "String",
		"Default": "sg-23b89ts0q",
		"Description": "安全组的名称"
    },
    "SecurityGroupId":{
                "Type": "String",
                "Description": "安全组id",
                "Default": "sg-23b89ts0q"
    },
    "ZoneId": {
		"Description": "可用区 Id",
		"Default": "cn-hangzhou-b",
		"Type": "String"
    },
    "VpcId": {
		"Default": "vpc-2379ch0zm",
		"Type": "String"
    },
    "VSwitchId":{
                "Default": "vsw-23qsejp98",
                "Type": "String"
    },
    "Password": {
		"Type": "String",
		"NoEcho": "true",
		"ConstraintDescription": "passwd",
                "Default": "jhj-ere212edDDVBmml"
    },
    "DiskSize": {
		"Type": "Number",
                "Default": 300
    }, 
    "DiskName": {
		"Type": "String",
                "Default": "-"
    },
    "MinAmount":{
		"Type": "Number",
		"Default": %d 
    },
    "MaxAmount":{
		"Type": "Number",
		"Default": %d 
    }
  },
  "Resources" : {
                "pyyx_esc": {
                          "Type": "ALIYUN::ECS::InstanceGroup",
                          "Properties": {
                                  "ImageId" : {"Ref": "ImageId"},
                                  "InstanceType": {"Ref": "InstanceType"},
                                  "InternetChargeType": "PayByTraffic",
                                  "SystemDisk_Category": "cloud_efficiency",
                                  "IoOptimized": "optimized",
                                  "ZoneId": "cn-hangzhou-b",
                                  "Password": {"Ref": "Password"},
                                  "VSwitchId" : {"Ref": "VSwitchId"},
                                  "VpcId": {"Ref": "VpcId"},
                                  "MinAmount": {"Ref": "MinAmount"},
                                  "MaxAmount": {"Ref": "MaxAmount"},
                                  "AllocatePublicIP": {"Ref": "AllocatePublicIP"}, 
                                  "SecurityGroupId": {
                                          "Ref": "SecurityGroup",
                                          "Ref": "SecurityGroupId"
                                   },
                                  "DiskMappings":[ {
                                        "Description": "300G data_disk",
                                        "Category": "cloud_ssd",
                                        "Size": 300
                                  }]
                           }
                },
		"Attachment": {
			"Type": "ALIYUN::SLB::BackendServerAttachment",
			"Properties": {
				"LoadBalancerId": "152b60fc1da-cn-hangzhou-dg-a01",
				"BackendServerList": 
				{
						"Fn::GetAtt": [
							"pyyx_esc",
							"InstanceIds"
						]
				},
				"BackendServerWeightList": ["0"]
			}

		}
    }
}
''' % (number,number)
def create_aliyun_ros_stack(stack_name,stack_params,id_key,ac_se,region='cn-hangzhou',timeout_mins=60):
	#初始化SDK client
	client = AcsClient(id_key,ac_se,region)
	#初始化request，构建请求
	request = CreateStacksRequest.CreateStacksRequest()
        request.set_headers({'x-acs-region-id': 'cn-hangzhou'})
	create_stack_body = '''{
            "Name": "%s",
            "TimeoutMins": %d,
            "Template": %s,
	    "Parameters": %s 
        }''' % (stack_name, timeout_mins, template,json.dumps(stack_params))
        request.set_content(create_stack_body)
	status,headers,body = client.get_response(request)
        if status == 201:
		result = json.loads(body)
		print result
	else:
		print "Unexpected errors: status=%d,error=%s" % (status,body)
        
if __name__ == '__main__':
    stack_name = raw_input("please input StackName:")
    region_id = "cn-hangzhou"
    id_key,ac_se = 'tablBShBzl4KNW0R', 'ag3ya5SaJjGXHS5QO66JxahzDtUTFN'
    tpl_params = {
	"ImageId": "m-bp1dygvja2gu2u0wwuyd",
	"InstanceType": "ecs.n1.xlarge",
	"SecurityGroupName": "sg-23l9ru2yj"
    }   
    result = create_aliyun_ros_stack(stack_name,tpl_params,id_key,ac_se,region_id)

