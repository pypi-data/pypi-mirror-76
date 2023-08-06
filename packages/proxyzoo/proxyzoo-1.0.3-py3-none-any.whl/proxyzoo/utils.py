#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json;
from time import strftime, localtime

def log(str):
    print("[" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "] " + str)

#加载json文件
def load_jsonfile(cfgPath):
    """"读取配置"""
    with open(cfgPath, 'r') as json_file:
        config = json.load(json_file)
    return config

#解析路径，替换HOME变量
def parse_path(path):
    if(not path or not isinstance(path,str)): return None
    path = path.replace("${HOME}", "~")
    path = path.replace("$HOME", "~")
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return os.path.abspath(os.path.expanduser(path))
