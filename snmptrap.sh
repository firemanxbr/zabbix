#!/bin/bash
#
# Copyright (C) 2013
#
# Marcelo Barbosa <firemanxbr@fedoraproject.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

ZABBIX_SERVER="YOUR_IP_ZABBIX_SERVER";
ZABBIX_PORT="YOUR_PORT_ZABBIX_SERVER";

ZABBIX_SENDER="/usr/local/bin/zabbix_sender";

read hostname
read ip
read uptime
read oid
read address
read community
read enterprise

# Device receive snmp trap
if [[ $ip =~ '192.168.0.1' ]]; then
	HOST=device
fi

address=`echo $address|cut -f2 -d' '`
enterprise=`echo $enterprise|cut -f2 -d' '`
str=`echo $oid|cut -f5 -d':'`
KEY=`echo $community|cut -f3 -d':'| cut -f1 -d' '`

$ZABBIX_SENDER -z $ZABBIX_SERVER -p $ZABBIX_PORT -s $HOST -k $KEY -o "$str"
