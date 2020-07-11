#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import re
import ipaddress

from .logs_help import Logger

logger = Logger("debug",name=os.path.split(os.path.splitext(os.path.abspath(__file__))[0])[-1])

def net2ip(net_str,_all=False,_error=False):
    """
    拆分网段为IP
    :param net_str: 传入合法网段，eg: 192.168.1.0/24 or 192.168.1.1-33 or 192.168.1.5-192.168.1.8
    :param _all: 是否包含网络地址和广播地址 eg: False
    :param _error: 是否包含无法处理地址 eg: False
    """
    _list = []
    if re.search(r"^\d+\.\d+\.\d+\.\d+-\d+$",net_str):
        net,a,b = re.findall(r"(\d+\.\d+\.\d+\.)(\d+)-(\d+)",net_str)[0]
        if any([int(n) > 255 for n in [a,b]]):
            logger.error(f"error ip_net > 255:{net_str}")
            if _error:
                _list.append(net_str)
            return _list
        for i in range(int(a),int(b)+1):
            _list.append(net+str(i))
    elif re.search(r"^\d+\.\d+\.\d+\.\d+-\d+\.\d+\.\d+\.\d+$",net_str):
        a,b,c,d,e,f,g,h = re.findall(r"(\d+)\.(\d+)\.(\d+)\.(\d+)-(\d+)\.(\d+)\.(\d+)\.(\d+)",net_str)[0]
        if any([int(n) > 255 for n in [a,b,c,d,e,f,g,h]]):
            logger.error(f"error:{net_str} > 255")
            if _error:
                _list.append(net_str)
            return _list
        for i in range(int(a),int(e)+1):
            for j in range(int(b),int(f)+1):
                for k in range(int(c),int(g)+1):
                    for l in range(int(d),int(h)+1):
                        _list.append(f"{i}.{j}.{k}.{l}")
    else:
        try:
            for ip in ipaddress.ip_network(net_str).hosts():
                _list.append(ip.compressed)
            if _all:
                _list.append(ipaddress.ip_network(net_str).network_address.compressed)
                _list.append(ipaddress.ip_network(net_str).broadcast_address.compressed)
        except Exception:
            logger.error(f"error ip_net :{net_str}", exc_info=True)
            if _error:
                _list.append(net_str)
    return list(set(_list))