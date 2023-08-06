### 一、这是什么

haproxy-zk 是一个基于haproxy+zookeeper+python实现的动态软负载，主要实现的功能是：使用python实现的守护进程从zookeeper（简称zk）里同步应用实例注册到zk里的实例IP:端口地址信息，根据指定的haproxy模板生成对应的haproxy配置，并使用生成的配置启动haproxy负载进程；当zk里的实例信息发生变化时(应用实例重启、发布)，守护进程将haproxy进程对应的后端服务进行实时激活和优雅下线，实现系统不间断接入。


优点：

 1.支持haproxy多进程模式，保障高并发的性能

 2.支持haproxy的HTTP和TCP模式，能对多种服务提供接入支持

 3.可以在haproxy自定义模板中对已有的第三方系统或子模块做配置实现统一接入

 3.使用socket通信与haproxy进程交互实现优雅下线，无需重启haproxy进程，不会中断已有连接。

 5.守护进程提供REST-HTTP查询接口，支持活动实例信息的实时查询

 6.仅需与zk通信，无需在应用节点安装其它组件，对于已经在zk实现实例注册的应用很容易做接入适配。

 7.haproxy、python和zk对于不同指令集的硬件平台支持性好


缺点：

 1.与zookeeper绑定，对于未使用zookeeper做实例注册的应用需要做改造



### 二、环境说明
#### 1.开发环境
##### 1) Python环境

本项目基于 python3 开发，需要python3环境支持，开发环境建议安装Anaconda包，可以免去很多第三方依赖包安装。Anaconda当前支持Windows、Mac和Linxu(x86,Power) 平台。

Anaconda 下载地址：https://www.anaconda.com/download/

安装Anaconda 后，需要设置本机环境变量（以Windows为例）

假设Anaconda的安装路径是“ANACONDA3_HOME”，在Windows环境变量的“Path”中添加以下路径：

```
ANACONDA3_HOME
ANACONDA3_HOME\Scripts
ANACONDA3_HOME\Library\bin
```
设置完成后，在命令行下输入```python -V``` 测试python环境是否可以正常使用

安装kazoo插件

从本工程的 ```docs/3rd``` 目录下获取```kazoo-2.8.0-py2.py3-none-any.whl```

打开其所在的目录，执行命令 ``` pip install kazoo-2.8.0-py2.py3-none-any.whl ``` 完成插件安装

##### 2) IDE使用

由于Python是脚本语言，对IDE的依赖不大，不过还是推荐开发IDE使用IntelliJ IDEA

通过IDEA的```File -> Open``` 菜单直接打开本工程目录即可

##### 3) 编译打包

编译打包需要依赖setuptools模块，安装Anaconda 后自带

打包只需要在工程根目录下执行：
```
python setup.py sdist bdist_wheel || true
```
执行完成后会在工程的```dist```目录下生成```proxyzoo-1.0.tar.gz``` 和```proxyzoo-1.0-py3-none-any.whl```包，将包上传到服务器环境执行安装即可

#### 2.运行环境

##### 1) Python环境
服务器运行环境也可以直接安装对应的Anaconda版，但是考虑到Anaconda的Linux版本支持有限，且Anaconda的安装包很大。可能还是需要自行安装python3环境。

Python3下载地址： https://www.python.org/downloads/

安装依赖包
```
yum -y install gcc  
yum install readline-devel -y
yum install openssl-devel -y
yum install libffi-devel -y
yum install zlib-devel bzip2-devel -y
```

Python3编译安装
```
tar -xvf Python-3.8.2.tgz       #解压Python安装包
cd Python-3.8.2
./configure --prefix=/home/proxy/support/python3  #配置安装路径
make && make install   #执行编译安装
ln -s /home/proxy/support/python3/bin/python3 /home/proxy/support/python3/bin/python #将python3软链接到python
ln -s /home/proxy/support/python3/bin/pip3 /home/proxy/support/python3/bin/pip #将pip3软链接到pip
```
如果需要同时使用python2和python3版本，则可以不做软链接。

编辑当前用户的 .bash_profile文件，设置PATH环境变量
```
export PATH=.:$HOME/support/python3/bin:$PATH:$HOME/.local/bin:$HOME/bin
```
执行 ```source ~/.bash_profile```使环境变量生效

执行以下命令，检查python安装和环境变量是否成功生效

```
which python
python -V
pip -V
```

安装依赖模块:kazoo, six，将kazoo和six的安装文件上传到主机

#whl方式安装

```
pip install six-1.14.0-py2.py3-none-any.whl  #安装six插件包
pip install kazoo-2.8.0-py2.py3-none-any.whl #安装kazoo插件包
pip install proxyzoo-1.0-py3-none-any.whl    #安装proxyzoo插件包
```
tar.gz包安装，如果pip命令安装有问题无法解决，可以使用tar.gz包安装插件。tar.gz包先将插件包上传解压，进入解压目录后执行
```
python setup.py install
```

安装完成后，启动守护进程（以工程docs/example）例子为例

```bash
cd ~/bin
./web-pzdaemon.py start
./esb-pzdaemon.py start
```

##### 2) Haproxy版本

综合考虑新特性支持和稳定性，Haproxy版本选择2.0长期支持版本(支持到2024年第二季度)，写这篇文档时候的最新版本是2.0.17，下载地址:http://www.haproxy.org/   （需要科学下载）

Haproxy1.X 编译

```
解压haproxy源码包
cd 源码解压目录
make TARGET=linux26   #执行编译，uname -r 查看内核版本，linux内核版本大于2.6.28可以使用 TARGET=linux2628
```

Haproxy2.X 编译

```
解压haproxy源码包
cd 源码解压目录
make TARGET=linux-glibc-legacy ARCH=x86_64
#haproxy2.x TARGET可选参数值：linux-glibc, linux-glibc-legacy, solaris, freebsd, openbsd, netbsd,cygwin, haiku, aix51, aix52, osx, generic, custom
#CentOS6使用linux-glibc-legacy CentOS7可以使用linux-glibc
```

Haproxy不需要特别安装，编译后在编译目录下会生成编译出来的应用程序，拷贝出来即可

##### 3) Zookeeper版本
对Zookeeper版本并无特别要求


### 三、配置说明
#### 1.JSON配置
Python守护进程启动时，会加载一个全局JSON配置，这个JSON配置包含了zk连接配置、haproxy对应的应用转发配置、以及haproxy其它如监听端口、模板路径、进程id文件路径等关键属性配置。一个典型的全局JSON配置如下：
```json
{
  "ngboss": {
    "zk.addr": "10.238.99.212:21810",
    "zk.path": "/wade-web/${group}/instances",
    "groups": {
      "web-ngboss" : {
        "httpchk": "GET /probe.jsp",
        "default_backend": true
      },
      "web-basecentre": {
        "zk.path": "/wade-web/${group}/instances",
        "acls": ["path_beg -i /basecentre", "path_beg -i /testcentre"],
        "mode": "http",
        "balance": "roundrobin",
        "httpchk": "GET /basecentre/probe.jsp",
        "server-template": "${group_name} 1-${max_server} 0.0.0.0:0 check inter 2000 rise 1 fall 2 disabled",
        "max_server": 20
      }
     },
    "exec": "${HOME}/sbin/haproxy",
    "template": "${HOME}/etc/haproxy.web.conf.template",
    "conf_file": "${HOME}/etc/haproxy.web.ngboss.conf",
    "pid_file": "${HOME}/logs/haproxy.web.ngboss.pid",
    "socket_files": ["${HOME}/logs/haproxy.web.ngboss.socket1","${HOME}/logs/haproxy.web.ngboss.socket2"],
    "listener_port": 8080,
    "admin_port": 20001
  }
}
```
其中：

 1."ngboss" 是配置分组，同一组配置连接相同的zk地址，对应一个haproxy监听实例，一个全局JSON配置里可以配置多组配置；通常全局JSON配置按接入类型分开，例如：web接入配置为```web.config.json```，esb接入配置为```esb.config.json```，svc接入配置为```svc.config.json```，每一类接入需要单独配置一个守护进程控制类。而在```web.config.json```里又可以配置多组接入配置，如ngboss接入一组，esop接入一组。同一个JSON文件里的每一组接入配置，守护进程都会启动一个线程来做应用实例信息同步和变更。

 2."zk.addr" 配置该组连接的zk服务地址，地址格式为```ip:port```多个地址使用```,```号分隔

 3.“zk.path” 配置该组接入配置下应用实例信息在zk上的注册路径，其中 ```${group}``` 匹配应用分组名

 3.“groups”为该组接入配置下的应用设置，应用名会用于组配置里的 "zk.path" 替换```${group}```变量和生成 haproxy配置时的backend名字，应用配置详细说明如下：

​    1) "zk.path" 应用实例信息在zk上的注册路径，不配置时，则使用接入组上的"zk.path"路径(根据应用名替换```${group}```变量)

​    2) "acls" 应用接入的匹配规则，按haproxy的acl语法编写，通常web应用需要按路径匹配，支持多acl匹配。

​    3) "mode" 应用对应haproxy后端 backend的模式，可以配置为 “http” 或 "tcp"，默认不配置为 "http"

​    4) "balance" 应用对应haproxy后端backend的负载均衡策略，默认不配置为 "roundrobin"

​    5) "httpchk" 对应haproxy后端backend的http健康检查请求方法和路径设置，不配置则使用TCP探测

​    6) "server-template" 对应haproxy后端backend的实例节点模板配置，默认不配置则为 ```${group_name} 1-${max_server} ${ip_port} check inter 2000 rise 1 fall 2 disabled``` 其中 ```${group_name}``` 为应用名，```${max_server}``` 为haproxy后端backend的实例节点的最大初始化数量，特别注意：模板一定要添加```disabled```关键字，避免proxy启动时启用模板实例。

​    7) "max_server" 应用对应haproxy后端backend的实例节点的最大初始化数量，默认不设置为10，该值理论上应该配置为：应用程序部署的最大实例进程数+批量灰度发布或容器滚动发布每次操作的实例数量，为了保险起见，建议配置为：应用程序部署的最大实例进程数x2 。且应用程序部署的最大实例进程数需要考虑到扩容增长的数量，从而尽量避免需要修改该配置和重启负载。

 4."exec"  为haproxy执行文件的路径，可以使用```${HOME}```来代替用户家目录

 5."template" 为该接入组使用的haproxy模板配置，可以使用```${HOME}```来代替用户家目录

 6.“conf_file” 为该接入组动态生成的haproxy配置文件路径，可以使用```${HOME}```来代替用户家目录

 7."pid_file" 为该接入组对应haproxy实例的进程id号存储文件路径，用于haproxy的-sf模式重启，可以使用```${HOME}```来代替用户家目录

 8."socket_files" 为该接入组对应的haproxy实例进程对应的 socket通信文件，由于haproxy多个nproc进程间是独立的，因此当nproc大于1时需要对应多个socket通信文件。所以反过来使用 "socket_files"配置来配置nproc的值，如果"socket_files"配置的数量大于1，则会将haproxy的nproc设置为 "socket_files"的数量值。

 9."listener_port" 为该接入组对应haproxy实例的监听(接入)端口

10. “admin_port” 为该接入组对应haproxy实例的管理端口

#### 2.HAProxy模板

一个通用的haproxy模板内容如下：

```
global
    maxconn 20000
    log 127.0.0.1 local0 info
    daemon
    quiet
    nbproc $nbproc
    pidfile $pid_file
$sockets

defaults
    mode            http
    option          httplog
    option          dontlognull
    option          forwardfor
    maxconn         20000
    timeout connect 5000ms
    timeout client  600000ms
    timeout server  600000ms

frontend public
    bind            *:$listener_port
    mode            http

$acl

$use_backend
$default_backend

$backend

listen admin_stats
    bind 0.0.0.0:$admin_port
    mode http
    option httplog
    maxconn 10
    stats refresh 5s
    stats uri /ha-stats
    stats realm Haproxy Manager
    stats auth admin:admin
    stats hide-version
    stats admin if TRUE
```

通常只有需要修改连接参数、接入模式（http|tcp）的时候，才需要对模板做修改。

对于web应用接入，也有可能需要对已有的第三方系统或子模块做配置实现统一接入，这时可以在haproxy里做预配置，例如在模板里加入静态资源 /static 路径的资源请求接入：

```
global
    maxconn 20000
    log 127.0.0.1 local0 info
    daemon
    quiet
    nbproc $nbproc
    pidfile $pid_file
$sockets

defaults
    mode            http
    option          httplog
    option          dontlognull
    option          forwardfor
    maxconn         20000
    timeout connect 5000ms
    timeout client  600000ms
    timeout server  600000ms

frontend public
    bind            *:$listener_port
    mode            http

    acl static path_beg -i /static
$acl

    use_backend static if static
$use_backend
$default_backend

backend static
     mode            http
     balance         roundrobin

     server  web-static-node01 10.238.99.212:9000 check inter 2000 rise 1 fall 2

$backend

listen admin_stats
    bind 0.0.0.0:$admin_port
    mode http
    option httplog
    maxconn 10
    stats refresh 5s
    stats uri /ha-stats
    stats realm Haproxy Manager
    stats auth admin:admin
    stats hide-version
    stats admin if TRUE

```



#### 3.守护进程

守护进程是在Python程序里fork出子进程常驻后台来实时监测接收zk上应用实例的注册信息变化，并通过socket通信对haproxy进程后端服务做上下线操作。

每一类型的接入(一个JSON配置文件)需要对应设置一个守护进程控制类，守护进程控制类用于控制守护进程的停启，查询守护进程状态。

一个守护进程控制类```web-daemon.py```编写的内容如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-i

import os
import sys
from proxyzoo.daemon import daemon
from proxyzoo import utils
from proxyzoo import launcher

PZ_CONFIG = "${HOME}/etc/web.config.json"          #proxyzoo配置文件路径
PZDAEMON_PID = "${HOME}/logs/web-pzdaemon.pid"     #守护进程pid文件的绝对路径
PZDAEMON_LOG= "${HOME}/logs/web-pzdaemon.log"      #守护进程日志文件的绝对路径
PZDAEMON_ERR= "${HOME}/logs/web-pzdaemon.err"  #守护进程启动过程中的错误日志
HTTP_SERVER_PORT = 21000      #HTTP接口服务端口

class pzdaemon(daemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=22, verbose=1):
        daemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name  # 派生守护进程类的名称

    def run(self, *args, **kwargs):
        #启动处理程序，启动时传入配置文件路径
        launcher.start(PZ_CONFIG, HTTP_SERVER_PORT)

if __name__ == '__main__':
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)

    pidfile = utils.parse_path(PZDAEMON_PID)
    stdout = utils.parse_path(PZDAEMON_LOG)
    stderr = utils.parse_path(PZDAEMON_ERR)

    pzd = pzdaemon("web-pzdaemon", pidfile, stdout=stdout, stderr=stderr, verbose=1)

    if sys.argv[1] == 'start':
        pzd.start()
    elif sys.argv[1] == 'stop':
        pzd.stop()
    elif sys.argv[1] == 'restart':
        pzd.restart()
    elif sys.argv[1] == 'status':
        alive = pzd.is_running()
        if alive:
            print('process [%s] is running ......' % pzd.get_pid())
        else:
            print('daemon process [%s] stopped' % pzd.name)
    else:
        print('invalid argument!')
        print(help_msg)


```

要点：

 1.在守护进程控制类里，定义全局常量设置JSON配置类路径，守护进程PID文件路径，HTTP服务 监听端口、日志输出文件和错误输出文件。

 2.守护进程控制类的 pzdaemon类继承 proxyzoo.daemon 类，实现run方法，在run方法里调用proxyzoo.launcher的sart方法，传入JSON配置文件路径和HTTP服务监听地址，启动对应接入组的zk监听、haproxy实例以及HTTP服务。

 3.在守护进程控制类的主方法里初始化pzdaemon实例类，并接受脚本执行传入参数， 执行对应的启动、停止、重启或状态查询方法。

守护进程控制类执行

```
#直接执行
./web-pzdaemon.py start   #启动web类接入守护进程和haproxy实例
./web-pzdaemon.py stop    #停止web类接入守护进程(haproxy实例不停止)
./web-pzdaemon.py restart  #重启web类接入守护进程和haproxy实例
./web-pzdaemon.py status   #查看web类接入守护进程状态

#使用python命令执行
python web-pzdaemon.py start   #启动web类接入守护进程和haproxy实例
python web-pzdaemon.py stop    #停止web类接入守护进程(haproxy实例不停止)
python web-pzdaemon.py restart  #重启web类接入守护进程和haproxy实例
python web-pzdaemon.py status   #查看web类接入守护进程状态
```



### 四、HTTP查询接口

HTTP查询接口是用于对动态软负载接入组的实例信息做实时查询，常用于对实例的缓存刷新等维护操作。

前面已经说明了HTTP服务的启动端口在守护进程类里设置，守护进程类启动后，可以对HTTP服务的端口发起访问，访问请求为HTTP GET，访问地址格式为：```http://守护进程启动主机IP:HTTP服务端口/```

默认不加任何参数会返回对应JSON配置里所有组的所有应用类和下的实例信息，例如，测试环境执行```curl http://10.238.99.210:21000``` 返回结果如下：

```json
{
	"ngboss": {
		"web-ngboss": {
			"instances:" ["10.238.99.246:32800", "10.238.99.243:32784"]
		},
		"web-basecentre": {
			"instances:" ["10.238.99.246:32799"]
		},
		"web-cpmcentre": {
			"instances:" ["10.238.99.243:32783"]
		},
		"web-csfproxy": {
			"instances:" ["10.238.99.244:32804"]
		},
		"web-customercentre": {
			"instances:" ["10.238.99.244:32806"]
		},
		"web-invoicecentre": {
			"instances:" []
		},
		"web-iupc": {
			"instances:" ["10.238.99.246:32797"]
		},
		"web-ordercentre": {
			"instances:" ["10.238.99.246:32798", "10.238.99.245:32805"]
		},
		"web-resourcecentre": {
			"instances:" ["10.238.99.244:32805"]
		},
		"web-treasury": {
			"instances:" ["10.238.99.245:32804"]
		}
	},
	"ecbusi": {
		"web-ecgateway": {
			"instances:" ["10.238.99.245:32803"]
		},
		"web-basecentre": {
			"instances:" ["10.238.99.246:32799"]
		},
		"web-cpmcentre": {
			"instances:" ["10.238.99.243:32783"]
		},
		"web-csfproxy": {
			"instances:" ["10.238.99.244:32804"]
		},
		"web-customercentre": {
			"instances:" ["10.238.99.244:32806"]
		},
		"web-invoicecentre": {
			"instances:" []
		},
		"web-iupc": {
			"instances:" ["10.238.99.246:32797"]
		},
		"web-ordercentre": {
			"instances:" ["10.238.99.246:32798", "10.238.99.245:32805"]
		},
		"web-resourcecentre": {
			"instances:" ["10.238.99.244:32805"]
		},
		"web-treasury": {
			"instances:" ["10.238.99.245:32804"]
		}
	}
}
```

通过 ```http://守护进程启动主机IP:HTTP服务端口/组名``` 访问，返回对应组下的所有应用实例，例如，测试环境执行```curl http://10.238.99.210:21000/ngboss``` 返回结果如下：

```json
{
	"ngboss": {
		"web-ngboss": {
			"instances:" ["10.238.99.246:32800", "10.238.99.243:32784"]
		},
		"web-basecentre": {
			"instances:" ["10.238.99.246:32799"]
		},
		"web-cpmcentre": {
			"instances:" ["10.238.99.243:32783"]
		},
		"web-csfproxy": {
			"instances:" ["10.238.99.244:32804"]
		},
		"web-customercentre": {
			"instances:" ["10.238.99.244:32806"]
		},
		"web-invoicecentre": {
			"instances:" []
		},
		"web-iupc": {
			"instances:" ["10.238.99.246:32797"]
		},
		"web-ordercentre": {
			"instances:" ["10.238.99.246:32798", "10.238.99.245:32805"]
		},
		"web-resourcecentre": {
			"instances:" ["10.238.99.244:32805"]
		},
		"web-treasury": {
			"instances:" ["10.238.99.245:32804"]
		}
	}
}
```

通过 ```http://守护进程启动主机IP:HTTP服务端口/组名/应用名``` 访问，返回对应组对应用下的所有应用实例，例如，测试环境执行```curl http://10.238.99.210:21000/ngboss/web-ngboss``` 返回结果如下：

```json
{
	"ngboss": {
		"web-ngboss": {
			"instances:" ["10.238.99.246:32800", "10.238.99.243:32784"]
		}
	}
}
```

