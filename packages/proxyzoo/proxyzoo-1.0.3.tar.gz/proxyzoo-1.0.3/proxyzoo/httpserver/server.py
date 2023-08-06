#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import threading
from proxyzoo import utils
from proxyzoo.httpserver.response import response

class server(threading.Thread):
    def __init__(self, config_all):
        threading.Thread.__init__(self)
        self.config_all = config_all
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __del__(self):
        if( hasattr(self, "server_socket") and self.server_socket):
            self.server_socket.close()

    def run(self):
        utils.log("启动HTTP服务，端口：%d" % self.port)
        self.server_socket.listen(128)
        while True:
            client_socket, client_address = self.server_socket.accept()
            #print("[%s, %s]用户连接上了" % client_address)
            handle_client_process = response(client_socket, self.config_all)
            handle_client_process.start()
            client_socket.close()

    def bind(self, port):
        self.port = port
        self.server_socket.bind(("", port))


if __name__ == "__main__":
    s = server({})
    s.bind(8000)
    s.start()