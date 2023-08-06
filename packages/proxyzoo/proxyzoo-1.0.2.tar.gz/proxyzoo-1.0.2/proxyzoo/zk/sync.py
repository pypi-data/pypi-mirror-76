import os
import time
import threading
from proxyzoo import utils
from proxyzoo.haproxy.executor import executor
from proxyzoo.haproxy.template import template
from kazoo.client import KazooClient,ChildrenWatch,DataWatch
from kazoo.handlers.threading import KazooTimeoutError

class sync(threading.Thread):
    def __init__(self, lock, config):
        threading.Thread.__init__(self)
        self.name = "zksync-thread-%s" % config.name
        self.lock = lock
        self.config = config
        self.executor = executor(config)
        self.template = template(config)

    def __del__(self):
        if( hasattr(self, "client") and self.client):
            self.client.close()

    def run(self):
        utils.log("开启服务实例步线程：" + self.name)
        self.client = KazooClient(hosts=self.config.zkAddr)
        try:
         self.client.start(timeout=10)
        except KazooTimeoutError:
            utils.log("%s-连接ZK服务器[%s]超时" % (self.name, self.config.zkAddr))
            return
        self.zkpathGroup = {}

        #第一次启动清理pidfile,终止原有实例
        self.lock.acquire()
        #self.executor.reset()
        self.template.write()
        self.executor.start()
        #utils.log("等待haproxy启动...")
        #time.sleep(3)
        self.lock.release()

        for group_name in self.config.groups:
            group = self.config.groups[group_name]
            zkpath = group.zkPath if group.zkPath else self.config.zkPath
            zkpath = zkpath.replace("${app}", group_name)
            zkpath = zkpath.replace("${group}", group_name)
            self.zkpathGroup[zkpath] = group_name
            self.client.ensure_path(zkpath)
            self.watcher(zkpath)

        while True:
            time.sleep(5)
            #print('watching......')

    def watcher(self, zkpath):
        # 获取原子节点列表
        _old_node_list = self.client.get_children(zkpath)

        #if(len(self._old_node_list) > 0):
        group_name = self.zkpathGroup[zkpath] if zkpath in self.zkpathGroup else None
        group = self.config.get_group(group_name) if group_name else None
        utils.log('[%s-%s]初始节点列表：%s' % (self.config.name, group_name, _old_node_list))

        if group:
            group._old_node_list = _old_node_list
            for node in _old_node_list:
                group.add_instance(str(node))

            #获取锁，用于线程同步
            self.lock.acquire()
            self.executor.init_group_instances(group)
            self.lock.release()

        try:
            # 为所要监听的节点开启一个子节点监听器
            ChildrenWatch(client=self.client, path=zkpath, func=self._node_change, send_event=True)
        except Exception as e:
            raise

    def _node_change(self, new_node_list, event):
        # 这里的new_node_list是指当前最新的子节点列表
        if not event: return

        has_change = False
        zkpath = event.path
        group_name = self.zkpathGroup[zkpath] if zkpath in self.zkpathGroup else None
        group = self.config.get_group(group_name) if group_name else None

        if not group:
            utils.log("group_name[%s]未找到对应的配置信息" % group_name)
            return;

        # 当前节点列表与上次拿到的节点列表相等，注意不是长度相等，是列表值和长度都要相等
        if new_node_list == group._old_node_list:
            utils.log('[%s-%s]子节点列表未发生变化' % (self.config.name, group_name))
            return

        if len(new_node_list) > len(group._old_node_list):
            for new_node in new_node_list:
                if new_node not in group._old_node_list:
                    utils.log('[%s-%s]监听到一个新的节点：%s' % (self.config.name, group_name, str(new_node)) )
                    group._old_node_list = new_node_list
                    inst = str(new_node)
                    if group and group.add_instance(inst):
                        self.lock.acquire()
                        self.executor.add_instance(group, inst)
                        self.lock.release()
        else:
            for old_node in group._old_node_list:
                if old_node not in new_node_list:
                    utils.log('[%s-%s]监听到一个删除的节点：%s' % (self.config.name, group_name, str(old_node)) )
                    group._old_node_list = new_node_list
                    inst = str(old_node)
                    if group and group.remove_instance(str(old_node)):
                        self.lock.acquire()
                        self.executor.remove_instance(group, inst)
                        self.lock.release()


