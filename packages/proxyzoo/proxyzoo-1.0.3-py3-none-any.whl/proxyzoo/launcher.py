#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from proxyzoo import utils
from proxyzoo.conf.config import config
from proxyzoo.zk.sync import sync
from proxyzoo.httpserver.server import server

def start(configPath, httpServerPort=21000):
    cfgPath = utils.parse_path(configPath)
    cfgJson = utils.load_jsonfile(cfgPath)

    #判断并设置默认服务端口
    httpServerPort = httpServerPort if isinstance(httpServerPort, int) else 21000

    lock = threading.Lock()
    threads = []
    config_all = {}
    for name in cfgJson:
        item = cfgJson[name];
        cfg = config(name,
                    item['zk.addr'],
                    item['zk.path'],
                    item['exec'],
                    item['template'],
                    item['conf_file'],
                    item['pid_file'],
                    item['socket_files'],
                    item['listener_port'],
                    item['admin_port'],
               )
        for group_name in item["groups"]:
            group_item = item["groups"][group_name]
            zkPath = group_item['zk.path'] if 'zk.path' in group_item else None
            acls = group_item['acls'] if 'acls' in group_item else None
            mode = group_item['mode'] if 'mode' in group_item else None
            balance = group_item['balance'] if 'balance' in group_item else None
            httpchk = group_item['httpchk'] if 'httpchk' in group_item else None
            serverTemplate = group_item['server-template'] if 'server-template' in group_item else None
            maxServer = group_item['max_server'] if 'max_server' in group_item else None
            defaultBackend = True.__eq__(group_item['default_backend']) if 'default_backend' in group_item else False
            cfg_group = config.group(group_name, zkPath, acls, mode, balance, httpchk, serverTemplate, maxServer, defaultBackend)
            #print(cfg_group)
            cfg.add_group(group_name, cfg_group)

        config_all[name] = cfg

        t = sync(lock, cfg)
        t.start()
        threads.append(t)

    #启动HTTP服务
    s = server(config_all)
    s.bind(httpServerPort)
    s.start()

    threads.append(s)

    for t in threads:
        t.join()

if __name__ == '__main__':
    start('./conf/config.json')