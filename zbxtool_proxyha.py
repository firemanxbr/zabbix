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
# This is script depend this other source: zbxtool_zabbix_api.py
#
# Supported and tested to Zabbix 1.8.15

from zbxtool_zabbix_api import *
import sys 

# Main
if __name__ == "__main__":

    if len(sys.argv) == 3:
    	ProxyHA(getproxy=sys.argv[1], movetoproxy=sys.argv[2])
    else: 
	print "Usage: %s proxy_origin proxy_destiny" % sys.argv[0]
        print "Example: %s hostproxy01 hostproxy02" % sys.argv[0]
        sys.exit(0)

# END
