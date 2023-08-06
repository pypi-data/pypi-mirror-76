#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from multiprocessing import Process
from proxyzoo import utils

class response(Process):
    def __init__(self, client_socket, config_all):
        Process.__init__(self)
        self.client_socket = client_socket
        self.config_all = config_all

    def run(self):
        """
        处理客户端请求
        """
        client_socket = self.client_socket

        # 获取客户端请求数据
        request_data = client_socket.recv(1024)
        #print("request data:", request_data)
        request_lines = request_data.splitlines()
        #for line in request_lines:
        #    print(line)

        # 解析请求报文
        request_start_line = request_lines[0]
        # 提取用户请求的文件名及请求方法
        file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)
        method = re.match(r"(\w+) +/[^ ]* ", request_start_line.decode("utf-8")).group(1)
        #print("file_name: %s" % file_name)

        # 构造响应数据
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Cache-Control: no-cache, no-store, must-revalidate\r\nPragma: no-cache\r\nExpires: -1\r\nContent-Type:application/json;charset=utf-8\r\n"  #text/plain
        response_body = "{}"

        #使用正则表达式解析URL参数
        re_cfg_name = re.match(r"/([^/]*)", file_name)
        re_group_name = re.match(r"/[^/]*/([^/]*)", file_name)
        #print("re_cfg_name:%s, re_app_name:%s" % (re_cfg_name, re_app_name))
        cfg_name = re_cfg_name.group(1) if re_cfg_name else None
        group_name = re_group_name.group(1) if re_group_name else None
        utils.log("cfg_name:%s group_name:%s" % (cfg_name, group_name))

        if( "/" == file_name ):
            response_body = self.build_all()
        elif( cfg_name and cfg_name in self.config_all ):
            if( group_name and group_name in self.config_all[cfg_name].groups ):
                response_body = self.build_group(cfg_name, group_name)
            else:
                response_body = self.build_cfg(cfg_name)
        else:
            response_start_line = "HTTP/1.1 403 Forbidden\r\n"

        response = response_start_line + response_headers + "\r\n" + response_body
        #向客户端返回响应数据
        client_socket.send(bytes(response, "utf-8"))
        #关闭客户端连接
        client_socket.close()

    def build_all(self):
        str = "{"
        l = len(self.config_all); idx = 0
        for cfg_name in self.config_all:
            str += "\"" + cfg_name + "\":"
            str += self.build_cfg_body(cfg_name)
            idx += 1
            if idx < l: str += ","
        str += "}"
        return str

    def build_cfg(self, cfg_name):
        str = "{"
        if cfg_name in self.config_all:
            str += "\"" + cfg_name + "\":"
            str += self.build_cfg_body(cfg_name)
        str += "}"
        return str

    def build_group(self, cfg_name, group_name):
        str = "{"
        if cfg_name in self.config_all:
            str += "\"" + cfg_name + "\":"
            str += "{"
            if group_name in self.config_all[cfg_name].groups:
                str += "\"" + group_name + "\":"
                str += self.build_group_body(cfg_name, group_name)
            str +="}"
        str += "}"
        return str

    def build_cfg_body(self, cfg_name):
         str = ""
         if( cfg_name in self.config_all ):
            cfg = self.config_all[cfg_name]
            str = "{"
            l = len(cfg.groups); idx = 0
            for group_name in cfg.groups:
                str += "\"" + group_name + "\":"
                str += self.build_group_body(cfg_name, group_name)
                idx += 1
                if idx < l: str += ","
            str += "}"
         else:
             str = "{}"
         return str

    def build_group_body(self, cfg_name, group_name):
        str = ""
        if( cfg_name in self.config_all and group_name in self.config_all[cfg_name].groups):
            group = self.config_all[cfg_name].groups[group_name]
            str = "{"
            str += "\"instances:\"["
            l = len(group.instances); idx = 0
            for inst in group.instances:
                str += "\"" + inst + "\""
                idx += 1
                if idx < l: str += ","
            str += "]}"
        else:
            str = "{}"
        return str