#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import configparser

def ini2json(cfgpath):
    """
    读取配置文件为json
    :param cfgpath: 配置文件路径，eg: config.ini
    """
    config = {}
    conf = configparser.ConfigParser()
    conf.read(cfgpath, encoding="utf-8")
    sections = conf.sections()
    for item in sections:
        config.setdefault(item,{})
        config[item].update(dict(conf.items(item)))
    return config



