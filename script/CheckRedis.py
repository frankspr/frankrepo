#  coding=utf-8

# create by taotao at 7/22/16 3:45 PM  

# before start. you need to sudo pip install aliyun-python-sdk-r-kvstore
import sys
import json
import datetime
import time
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider



YOUR_ACCESSKEY = 'tablBShBzl4KNW0R'
YOUR_ACCESSKEY_SECRET = 'ag3ya5SaJjGXHS5QO66JxahzDtUTFN.huang'
REGION_ID_FIXED = 'cn-hangzhou'
product_name_for_redis = 'R-kvstore'
domain_name_for_redis = 'r-kvstore.aliyuncs.com'
metric_used_memory = 'UsedMemory'
#instance_id = '780006a9ab164e0a'
clt = client.AcsClient(YOUR_ACCESSKEY, YOUR_ACCESSKEY_SECRET, REGION_ID_FIXED)


def time_to_utc_convert(utc_datetime):
    return utc_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

# need to execute the shell in sudo python let it update configuration file first time.
r_kvstore_init_ready = False
for item in region_provider.product_list:
    if item.get(product_name_for_redis):
        r_kvstore_init_ready = True

if r_kvstore_init_ready is False:
    region_provider.modify_point(product_name_for_redis, REGION_ID_FIXED, domain_name_for_redis)


def build_describe_region_request():
    kvstore_package = __import__('aliyunsdkr-kvstore.request.v20150101.DescribeRegionsRequest')
    request = kvstore_package.request.v20150101.DescribeRegionsRequest.DescribeRegionsRequest()
    request.set_accept_format('json')
    return request


def build_describe_monitor_items():
    kvstore_package = __import__('aliyunsdkr-kvstore.request.v20150101.DescribeMonitorItemsRequest')
    request = kvstore_package.request.v20150101.DescribeMonitorItemsRequest.DescribeMonitorItemsRequest()
    request.set_accept_format('json')
    return request


def build_monitor_items(instance_id, monitor_key):
    kvstore_package = __import__(
        'aliyunsdkr-kvstore.request.v20150101.DescribeMonitorValuesRequest')
    request = kvstore_package.request.v20150101.DescribeMonitorValuesRequest.DescribeMonitorValuesRequest()
    request.set_accept_format('json')
    request.set_InstanceIds(instance_id)
    request.set_MonitorKeys(monitor_key)
    return request


def build_history_monitor_items(instance_id, monitor_key, start_time, end_time,
                                interval_time='01m'):
    kvstore_package = __import__(
        'aliyunsdkr-kvstore.request.v20150101.DescribeHistoryMonitorValuesRequest')
    request = kvstore_package.request.v20150101.DescribeHistoryMonitorValuesRequest.DescribeHistoryMonitorValuesRequest()
    request.set_accept_format('json')
    request.set_InstanceId(instance_id)
    request.set_MonitorKeys(monitor_key)
    request.set_StartTime(start_time)
    request.set_EndTime(end_time)
    # 01m, 05m, 15m, 60m
    request.set_IntervalForHistory(interval_time)
    return request


def convert_response_to_json(response_string):
    if response_string:
        response_json = json.loads(response_string)
        return response_json


def check_describe_region_ready():
    region_response_str = clt.do_action(build_describe_region_request())
    assert region_response_str is not None
    region_result = convert_response_to_json(region_response_str)
    assert region_result.get('RegionIds') is not None
    print region_response_str

# this api will list the monitor items you want.
def describe_monitor_items():
    monitor_items_response_str = clt.do_action(build_describe_monitor_items())
    items = convert_response_to_json(monitor_items_response_str)
    return items

# this api will get the current value of the metric
def monitor_redis_metric(instance_id, metric):
    request = build_monitor_items(instance_id=instance_id, monitor_key=metric)
    response = clt.do_action(request)
    items = convert_response_to_json(response)
    print items

# this api will list the history metric in the past hour.
def monitor_redis_history_metric(instance_id, metric):
    now = datetime.datetime.utcnow()
    end_time = time_to_utc_convert(now)
#    start_time_ts = now - datetime.timedelta(hours=1)
    start_time_ts = now - datetime.timedelta(minutes=1)
    start_time = time_to_utc_convert(start_time_ts)
    request = build_history_monitor_items(instance_id=instance_id, monitor_key=metric,
                                          start_time=start_time, end_time=end_time)
    response = clt.do_action(request)
    items = convert_response_to_json(response)
    items = json.loads(items['MonitorHistory'])
    MemUsed = (items.values()[0]['UsedMemory'])/1024/1024
    print '%.2f' % MemUsed


# check_describe_region_ready()
# items = describe_monitor_items()


# monitor_redis_metric(instance_id=instance_id, metric=metric_used_memory)
if __name__ == '__main__':
	instance_id = sys.argv[1]
	monitor_redis_history_metric(instance_id=instance_id, metric=metric_used_memory)
