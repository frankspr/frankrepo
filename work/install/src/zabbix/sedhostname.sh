#!/bin/bash
HOSTNAME=`uname -n`
/bin/sed -i "s/Hostname=base/Hostname=$HOSTNAME/g" /usr/local/zabbix-agent/etc/zabbix_agentd.conf
