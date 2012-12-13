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
# This is script depend this other source: unirede_zabbix_api.py

from unirede_zabbix_api import *
import sys 

# Main
if __name__ == "__main__":

    if len(sys.argv) == 3:
    	UniProxyHA(getproxy=sys.argv[1], movetoproxy=sys.argv[2])
    else: 
	print "Usage: %s proxy_origin proxy_destiny" % sys.argv[0]
        print "Example: %s hostproxy01 hostproxy02" % sys.argv[0]
        sys.exit(0)

