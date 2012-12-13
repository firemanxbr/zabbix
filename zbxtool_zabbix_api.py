#!/usr/bin/python
#
# Copyright (C) 2012
#
# Marcelo Barbosa <mr.marcelo.barbosa@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# This is script depend this other source: 
# https://github.com/gescheit/scripts/tree/master/zabbix/
#
# Supported and tested to Zabbix 1.8.15

from zabbix_api import ZabbixAPI

""" Required configuration
server 		= YOUR URL SERVER
sender		= YOUR IP to zabbix_sender
username	= User with privileges API access
password	= Password set to username
templaterbl	= Parameter optional(use monitoring RBL)
"""
server 		= "http://192.168.25.12/zabbix/" 	
sender 		= "192.168.25.12"
username 	= "admin"          
password 	= "zabbix"    
templaterbl 	= "Template RBL"

""" Connection in Zabbix Server API
"""
zapi = ZabbixAPI(server = server, path = "", log_level = 0)
zapi.login(username, password)

""" Zabbix API - Functions supported this script: 
    hostgroup.exists
    hostgroup.get
    hostgroup.create
    template.exists
    template.get
    template.create
    host.exists
    host.get
    host.create
    proxy.get
"""

def HostGroupExists(hostgroup): 
    """ Check this host group exist
    Args: 
	hostgroup (str): name this host group
    Returns:
	True = host group exist
	False = host group not exist 
    Example:
	print HostGroupExists(hostgroup="Your Host Group")
    """
    exists = zapi.hostgroup.exists({
	"name": hostgroup
    })
    return exists 

def HostGroupCreate(hostgroup):
    """ Create new host group
    Args: 
	hostgroup (str): name this new host group
    Returns:
	groupids = id from new host group created
	False = host group exist 
    Example:
	print HostGroupCreate(hostgroup="Your New Host Group")
    """
    if HostGroupExist(hostgroup) == False:
	create = zapi.hostgroup.create({
	    "name": hostgroup
   	})
	result = create['groupids']
    else:  
	result = False
    return result

def TemplateExists(template):
    """ Check this template exist
    Args: 
	template (str): name this template
    Returns:
	True = template exist
	False = template not exist 
    Example:
	print TemplateExists(template="Your Template")
    """
    exists = zapi.template.exists({
	"host": template
    })
    return exists

def TemplateGet(template):
    """ Get this template exist
    Args: 
	template (str): name this template
    Returns:
	templateid = id from template
	False = template not exist 
    Example:
	print TemplateGet(template="Your Template")
    """
    if TemplateExists(template) == True:
	get = zapi.template.get({
	    "output": "extend", 
	    "filter": { 
		"host": [template]
	    }
	})
	result = get[0]['templateid']
    else:
	result = False    
    return result

def TemplateCreate(template, hostgroup):
    """ Create new template
    Args: 
	template (str): name this new template
	hostgroup (str): name this host group to template
    Returns:
	templateids = id from new template created
	False = template exist 
    Example:
	print TemplateCreate(template="Your New Template", hostgroup="Your Host Group to Template")
    """
    if TemplateExists(template) == False:
	create = zapi.template.create({
	    "host": template,
	    "groups": [{
		"groupid": HostGroupGet(hostgroup)
	    }]
	})
	result = create[0]['templateids']
    else:
	result = False
    return result
	
def HostExists(host):
    """ Check this host exist
    Args: 
	host (str): name this host 
    Returns:
	True = host exist
	False = host not exist 
    Example:
	print HostExists(host="Your Host")
    """
    exists = zapi.host.exists({
	"host": host
    })
    return exists

def HostGet(host):
    """ Get this host exist
    Args: 
	host (str): name this host
    Returns:
	hostid = id from host
	False = host not exist 
    Example:
	print HostGet(host="Your Host")
    """
    if HostExists(host) == True:
	get = zapi.host.get({
	    "output": "extend",
	    "filter": {
		"host": [host]
	    }
	})
	result = get[0]['hostid']
    else:
	result = False
    return result

def HostCreate(host, hostgroup, useip, dns, ip, template, port):
    """ Create new host
    Args: 
	host (str): name this new host
	hostgroup (str): name this host group to new host
	useip (bool): 1 - use ip, 0 use dns
	dns (str): name this dns to new host
	ip (str): ip to new host
	template (str): name this template to new host
	port (str): port to new host use
    Returns:
	hostids = id from new host created
	False Host = host exist 
	False Host Group = host group not exist 
	False Template = template not exist 
    Example:
	print HostCreate(host="Your new host", hostgroup="Host Group to new host", useip="1 or 0", dns="Your dns name to new host", ip="ip to new host", template="Template to new host", port="por Zabbix to new host")
    """
    if HostExists(host) == False:
	if HostGroupExists(hostgroup) == True:
	    if TemplateExists(template) == True:
		hostgroup = HostGroupGet(hostgroup)
		template = TemplateGet(template)
		create = zapi.host.create({
		    "host": host,
		    "useip": useip,
		    "dns": dns,
		    "ip": ip,
		    "port": port,
		    "groups":[{
			"groupid": hostgroup
		    }],
		    "templates":[{
			"templateid": template
		    }]
		})
		result = create['hostids']
	    else:
		result = "False Template"
	else:
	    result = "False Host Group"
    else:
	result = "False Host"
    return result

def ProxyHA(getproxy, movetoproxy):
    """ Move hosts from getproxy to movetoproxy
    Args: 
        getproxy (str): get all hosts to proxy
	movetoproxy (str): move all hosts to proxy
    Returns:
	hosts moved to proxy
    Example:
        print ProxyHA(getproxy="proxyname", movetoproxy="proxyname")
    """
    get = zapi.proxy.get({
	"output": "extend"
	})

    if getproxy != "":
	for i in range(len(get)):
	    if get[i]['host'] == getproxy:
		proxyname = get[i]['host']
		proxyid = get[i]['proxyid']

    otherget = zapi.proxy.get({
  	"select_hosts":"extend",
    })
    
    if movetoproxy != "":
	for i in range(len(otherget)):
	    if otherget[i]['proxyid'] == proxyid:

		for y in range(len(otherget[i]['hosts'])):
			print otherget[i]['hosts'][y]['host']
			
			if movetoproxy != "":
				for z in range(len(get)):
				    if get[z]['host'] == movetoproxy:
					movetoproxyid = get[z]['proxyid']
				
				host = otherget[i]['hosts'][y]['host']

				hostid = HostGet(host)

				moreget = zapi.host.update({
				    "hostid": hostid,
				    "proxy_hostid": movetoproxyid
				})			
#END
