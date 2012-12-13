#!/usr/bin/python
#
# Copyright (C) 2012 Unirede Solucoes Corporativas
#  _   _       _              _      
# | | | |_ __ (_)_ __ ___  __| | ___ 
# | | | | '_ \| | '__/ _ \/ _` |/ _ \
# | |_| | | | | | | |  __/ (_| |  __/
#  \___/|_| |_|_|_|  \___|\__,_|\___|
#
# Autor: marcelo.barbosa@unirede.net
#
# This is script depend this other source: 
# https://github.com/gescheit/scripts/tree/master/zabbix/
#
# Supported to Zabbix 1.8.15

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
templaterbl 	= "Template Unirede RBL"

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

def UniHostGroupExists(hostgroup): 
    """ Check this host group exist
    Args: 
	hostgroup (str): name this host group
    Returns:
	True = host group exist
	False = host group not exist 
    Example:
	print UniHostGroupExists(hostgroup="Your Host Group")
    """
    exists = zapi.hostgroup.exists({
	"name": hostgroup
    })
    return exists 

def UniHostGroupCreate(hostgroup):
    """ Create new host group
    Args: 
	hostgroup (str): name this new host group
    Returns:
	groupids = id from new host group created
	False = host group exist 
    Example:
	print UniHostGroupCreate(hostgroup="Your New Host Group")
    """
    if UniHostGroupExist(hostgroup) == False:
	create = zapi.hostgroup.create({
	    "name": hostgroup
   	})
	result = create['groupids']
    else:  
	result = False
    return result

def UniTemplateExists(template):
    """ Check this template exist
    Args: 
	template (str): name this template
    Returns:
	True = template exist
	False = template not exist 
    Example:
	print UniTemplateExists(template="Your Template")
    """
    exists = zapi.template.exists({
	"host": template
    })
    return exists

def UniTemplateGet(template):
    """ Get this template exist
    Args: 
	template (str): name this template
    Returns:
	templateid = id from template
	False = template not exist 
    Example:
	print UniTemplateGet(template="Your Template")
    """
    if UniTemplateExists(template) == True:
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

def UniTemplateCreate(template, hostgroup):
    """ Create new template
    Args: 
	template (str): name this new template
	hostgroup (str): name this host group to template
    Returns:
	templateids = id from new template created
	False = template exist 
    Example:
	print UniTemplateCreate(template="Your New Template", hostgroup="Your Host Group to Template")
    """
    if UniTemplateExists(template) == False:
	create = zapi.template.create({
	    "host": template,
	    "groups": [{
		"groupid": UniHostGroupGet(hostgroup)
	    }]
	})
	result = create[0]['templateids']
    else:
	result = False
    return result
	
def UniHostExists(host):
    """ Check this host exist
    Args: 
	host (str): name this host 
    Returns:
	True = host exist
	False = host not exist 
    Example:
	print UniHostExists(host="Your Host")
    """
    exists = zapi.host.exists({
	"host": host
    })
    return exists

def UniHostGet(host):
    """ Get this host exist
    Args: 
	host (str): name this host
    Returns:
	hostid = id from host
	False = host not exist 
    Example:
	print UniHostGet(host="Your Host")
    """
    if UniHostExists(host) == True:
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

def UniHostCreate(host, hostgroup, useip, dns, ip, template, port):
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
	print UniHostCreate(host="Your new host", hostgroup="Host Group to new host", useip="1 or 0", dns="Your dns name to new host", ip="ip to new host", template="Template to new host", port="por Zabbix to new host")
    """
    if UniHostExists(host) == False:
	if UniHostGroupExists(hostgroup) == True:
	    if UniTemplateExists(template) == True:
		hostgroup = UniHostGroupGet(hostgroup)
		template = UniTemplateGet(template)
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

def UniProxyHA(getproxy, movetoproxy):
    """ Move hosts from getproxy to movetoproxy
    Args: 
        getproxy (str): get all hosts to proxy
	movetoproxy (str): move all hosts to proxy
    Returns:
	hosts moved to proxy
    Example:
        print UniProxyHA(getproxy="proxyname", movetoproxy="proxyname")
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
			"""debug option
			print otherget[i]['hosts'][y]['host']
			"""
			
			if movetoproxy != "":
				for z in range(len(get)):
				    if get[z]['host'] == movetoproxy:
					movetoproxyid = get[z]['proxyid']
				
				host = otherget[i]['hosts'][y]['host']

				hostid = UniHostGet(host)

				moreget = zapi.host.update({
				    "hostid": hostid,
				    "proxy_hostid": movetoproxyid
				})			
#END
