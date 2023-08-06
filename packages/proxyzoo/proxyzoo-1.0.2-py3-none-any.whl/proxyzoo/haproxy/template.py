#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os;
from string import Template

class template:
    space_chars = 4 * ' ';

    def __init__(self, config):
        self.config = config;
        tplPath = config.template;
        try:
            tplFile = open(tplPath, 'r')
            self.tplContent = tplFile.read();
            tplFile.close()
        except IOError:
            print("template file open faild, file path:%" % tplPath)

    def write(self):
        tpl = Template(self.tplContent)

        nbproc = 1
        sockets = []
        acl = [];
        use_backend = []
        backend = []
        default_backend = ""

        if( len(self.config.socketFiles) > 0 ):
            nbproc = len(self.config.socketFiles)
            idx = 0
            for socketFile in self.config.socketFiles:
                idx += 1
                sockets.append("\n%sstats socket %s mode 600 level admin process %d" % (template.space_chars, socketFile, idx))

        if( len(self.config.groups) > 0 ):
            for group_name in self.config.groups:
                group = self.config.groups[group_name]
                #default backend
                if( group.defaultBackend ):
                    default_backend = "\n%sdefault_backend %s" % (template.space_chars, group_name)

                 #acl
                if( group.acls and len(group.acls) > 0 ):
                    idx = 0
                    for acl_value in group.acls:
                        idx +=1
                        acl_name = group_name + str(idx)
                        #acl
                        acl.append("\n%sacl %s %s" % (template.space_chars, acl_name, acl_value) )
                        #use_backend
                        use_backend.append("\n%suse_backend %s if %s" % (template.space_chars, group_name, acl_name) )

                #backend
                backend.append("\n\nbackend %s" % group_name)
                backend.append("\n%smode %s" % (template.space_chars, group.mode) )
                backend.append("\n%sbalance %s" % (template.space_chars, group.balance) )
                if group.httpchk:
                    backend.append("\n%soption httpchk %s" % (template.space_chars, group.httpchk) )
                backend.append("\n%sserver-template %s" % (template.space_chars, group.serverTemplate) )
                #for inst in group.instances:
                #    backend.append("\n%sserver %s-%s %s check inter 2000 rise 1 fall 2 " % (template.space_chars, group_name, inst, inst))


        output = tpl.substitute({
            "nbproc": nbproc,
            "pid_file": self.config.pidFile,
            "sockets": ''.join(sockets),
            "acl": ''.join(acl),
            "use_backend": ''.join(use_backend),
            "default_backend": default_backend,
            "backend": ''.join(backend),
            "listener_port": self.config.listenerPort,
            "admin_port": self.config.adminPort
        })

        handle = open(self.config.confFile, 'w')
        handle.write(output)
        handle.close()
