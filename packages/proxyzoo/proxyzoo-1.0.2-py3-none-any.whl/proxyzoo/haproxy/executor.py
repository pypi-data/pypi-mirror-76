#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
from proxyzoo import utils

'''
---------------------------------------------------------------------
 haproxy backend server 状态属性：
 srv_op_state:                Server operational state (UP/DOWN/...).
                                0 = SRV_ST_STOPPED
                                  The server is down.
                                1 = SRV_ST_STARTING
                                  The server is warming up (up but
                                  throttled).
                                2 = SRV_ST_RUNNING
                                  The server is fully up.
                                3 = SRV_ST_STOPPING
                                  The server is up but soft-stopping
                                  (eg: 404).
 srv_admin_state:             Server administrative state (MAINT/DRAIN/...).
                              The state is actually a mask of values :
                                0x01 = SRV_ADMF_FMAINT
                                  The server was explicitly forced into
                                  maintenance.
                                0x02 = SRV_ADMF_IMAINT
                                  The server has inherited the maintenance
                                  status from a tracked server.
                                0x04 = SRV_ADMF_CMAINT
                                  The server is in maintenance because of
                                  the configuration.
                                0x08 = SRV_ADMF_FDRAIN
                                  The server was explicitly forced into
                                  drain state.
                                0x10 = SRV_ADMF_IDRAIN
                                  The server has inherited the drain status
                                  from a tracked server.
                                0x20 = SRV_ADMF_RMAINT
                                  The server is in maintenance because of an
                                  IP address resolution failure.
                                0x40 = SRV_ADMF_HMAINT
                                  The server FQDN was set from stats socket.
-----------------------------------------------------------------------------
 haproxy backend server 设置状态：
set server <backend>/<server> state [ ready | drain | maint ]
  Force a server's administrative state to a new state. This can be useful to
  disable load balancing and/or any traffic to a server. Setting the state to
  "ready" puts the server in normal mode, and the command is the equivalent of
  the "enable server" command. Setting the state to "maint" disables any traffic
  to the server as well as any health checks. This is the equivalent of the
  "disable server" command. Setting the mode to "drain" only removes the server
  from load balancing but still allows it to be checked and to accept new
  persistent connections. Changes are propagated to tracking servers if any.                                  
'''
class executor:

    def __init__(self, config):
        self.config = config

    def reset(self):
        pidFile = self.config.pidFile
        if( os.path.isfile(pidFile) ):
            command = "kill -9 `cat %s` && rm -fr %s" % (pidFile, pidFile)
            os.system(command)

    def start(self):
        exec = self.config.exec;
        confFile = self.config.confFile
        pidFile = self.config.pidFile

        if( not os.path.exists(exec) ):
            print("exec %s is not exists!" % exec)
            return
        if( not os.path.isfile(confFile) ):
            print("conf file %s is not a exists file!" % exec)
            return

        command = "%s" % exec
        if( os.path.isfile(pidFile) ):
            command += " -sf `cat %s`" % pidFile
        command += " -f  %s" % confFile
        #print("command:%s", command)
        os.system(command)

    def send_command_all(self, command):
        result = []
        for socketFile in self.config.socketFiles:
            result.append(self.send_command(socketFile, command))
        return result

    def send_command(self, socket_file, command):
        haproxy_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        #haproxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #TCP模式
        haproxy_sock.settimeout(10)
        retval = ""
        try:
            haproxy_sock.connect(socket_file)
            haproxy_sock.send(bytes(command, "utf-8"))
            while True:
                buf = haproxy_sock.recv(16)
                if buf:
                    retval += str(buf, encoding = "utf-8")
                else:
                    break
            haproxy_sock.close()
        #except:
        #    retval = ""
        finally:
            haproxy_sock.close()
        return retval

    def init_group_instances(self, group):
        group_name = group.name
        utils.log("初始化group：%s" % group_name)
        idx = 0
        for inst in group.instances:
            idx += 1
            inst_values = inst.split(':')
            server_name =  group_name + str(idx)
            utils.log("激活 %s/%s addr %s port %s" % (group_name, server_name, inst_values[0], inst_values[1]))
            command = "set server %s/%s addr %s port %s\n" % (group_name, server_name, inst_values[0], inst_values[1])
            result = self.send_command_all(command)
            #print(result)
            command = "set server %s/%s state ready\n" % (group_name, server_name)
            result = self.send_command_all(command)
            #print(result)


    def add_instance(self, group, inst):
        # echo "help" | socat stdio /var/lib/haproxy/haproxy.socket
        # echo "show info" | socat stdio /var/lib/haproxy/haproxy.socket
        # set server xxx state ready|maint
        group_name = group.name
        inst_values = inst.split(':')
        for socketFile in self.config.socketFiles:
            servers_slots = self.send_command(socketFile, "show servers state %s\n" % group_name)
            if not servers_slots:
                utils.log("Failed to get %s servers state from socket: %s" % (group_name, socketFile))
                break;
            server_name = ""
            servers_slots = servers_slots.split('\n')
            for server_slot in servers_slots:
                server_infos = server_slot.split(" ")
                if len(server_infos) > 18 and not server_infos[0] == '#':
                    server_op_state = server_infos[5]
                    #server_admin_state = server_infos[6]
                    #server_ip = server_infos[4]
                    #server_port = server_infos[18]
                    if( "0".__eq__(server_op_state) ):
                        server_name = server_infos[3]
                        break
            if( server_name and not "" == server_name ):
                 utils.log("激活 %s/%s addr %s port %s 在%s的进程上" % (group_name, server_name, inst_values[0], inst_values[1], socketFile) )
                 command = "set server %s/%s addr %s port %s\n" % (group_name, server_name, inst_values[0], inst_values[1])
                 result = self.send_command(socketFile, command)
                 #print(result)
                 command = "set server %s/%s state ready\n" % (group_name, server_name)
                 result = self.send_command(socketFile, command)
                 #print(result)
            else:
                utils.log("%s可用的server数量不足: %s" % (group_name, socketFile))

    def remove_instance(self, group, inst):
        # echo "help" | socat stdio /var/lib/haproxy/haproxy.socket
        # echo "show info" | socat stdio /var/lib/haproxy/haproxy.socket
        # set server xxx state ready|maint
        group_name = group.name
        inst_values = inst.split(':')
        for socketFile in self.config.socketFiles:
            servers_slots = self.send_command(socketFile, "show servers state %s\n" % group_name)
            if not servers_slots:
                utils.log("Failed to get %s servers state from socket: %s" % (group_name, socketFile))
                break;
            target_servers = []
            servers_slots = servers_slots.split('\n')
            for server_slot in servers_slots:
                server_infos = server_slot.split(" ")
                if len(server_infos) > 18 and not server_infos[0] == '#':
                    server_name = server_infos[3]
                    #server_op_state = server_infos[5]
                    #server_admin_state = server_infos[6]
                    server_ip = server_infos[4]
                    server_port = server_infos[18]
                    if( server_ip == inst_values[0] and  server_port == inst_values[1] ):
                        target_servers.append(server_name)

            for server_name in target_servers:
                utils.log("下线 %s/%s addr %s port %s 在%s的进程上" % (group_name, server_name, inst_values[0], inst_values[1], socketFile) )
                command = "set server %s/%s state maint\n" % (group_name, server_name)
                result = self.send_command(socketFile, command)
                #print(result)