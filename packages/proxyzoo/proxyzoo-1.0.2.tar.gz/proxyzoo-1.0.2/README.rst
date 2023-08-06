proxyzoo is a dynamic soft load based on haproxy+zookeeper+python.
The main function is:
  the daemon implemented by python synchronizes the application instance registration from zookeeper (zk) to the instance IP: port address information in zk
  Generate the corresponding haproxy configuration according to the specified haproxy template, and use the generated configuration to start the haproxy load process
  when the instance information in zk changes (application instance restart, release), the daemon will perform the backend service corresponding to the haproxy process Real-time activation and graceful offline,
  realizing uninterrupted system access
Online documentation is at http://git.wadecn.com:18082/bits/proxy-zk.
Bugs can be reported to http://git.wadecn.com:18082/bits/proxy-zk.  The code can also be found there.