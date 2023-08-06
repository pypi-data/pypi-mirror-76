#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from proxyzoo import utils

DEFAULT_BE_MODE = "http"    #默认backend的模式为http
DEFAULT_BE_BALANCE = "roundrobin"  #默认backend的均衡策略为roundrobin
DEFAULT_BE_SERVER_TEMPLATE = "${group_name} ${min_server}-${max_server} ${ip_port} check inter 2000 rise 1 fall 2 disabled" #默认backend的server模板
DEFAULT_BE_MAX_SERVER = 10  #默认backend的最大server数量

class config:

    def __init__(self, name, zkAddr, zkPath, exec, template, confFile, pidFile, socketFiles, listenerPort, adminPort):
        self.name = name;
        self.zkAddr = zkAddr;
        self.zkPath = zkPath;
        self.exec = utils.parse_path(exec);
        self.template = utils.parse_path(template)
        self.confFile = utils.parse_path(confFile)
        self.pidFile = utils.parse_path(pidFile)
        self.socketFiles = [];
        if(socketFiles):
            for socketFile in socketFiles:
                self.socketFiles.append(utils.parse_path(socketFile))
        self.listenerPort = listenerPort
        self.adminPort = adminPort
        self.groups = {}

    def __str__(self):
        return "config\n name:%s, zk.addr:%s, zk.path:%s " % (self.name, self.zkAddr, self.zkPath)

    def add_group(self, groupname, group):
        self.groups[groupname] = group

    def get_group(self, groupname):
        return self.groups[groupname] if groupname in self.groups else None

    class group:
        def __init__(self, name, zkPath, acls, mode, balance, httpchk, serverTemplate, maxServer, defaultBackend):
            self.name = name
            self.zkPath = zkPath
            self.acls = acls
            self.mode = mode if mode else DEFAULT_BE_MODE
            self.balance = balance if balance else DEFAULT_BE_BALANCE
            self.httpchk = httpchk
            self.serverTemplate = serverTemplate if serverTemplate else DEFAULT_BE_SERVER_TEMPLATE
            self.maxServer = maxServer if maxServer and isinstance(maxServer, int) else DEFAULT_BE_MAX_SERVER
            self.defaultBackend = defaultBackend
            self.instances = []

        def __str__(self):
            return "group\n name:%s, zkPath: %s, acls:%s, mode:%s, balance:%s, httpchk:%s, serverTemplate:%s, defaultBackend:%s, instances:%s " % (self.name, self.zkPath, self.acls, self.mode, self.balance, self.httpchk, self.serverTemplate, self.defaultBackend, self.instances)

        def add_instance(self, instance):
            if(instance and not instance in self.instances):
                self.instances.append(instance)
                return True
            return False

        def remove_instance(self, instance):
            if(instance and instance in self.instances):
                self.instances.remove(instance)
                return True
            return False

        def get_instances(self):
            return self.instances




