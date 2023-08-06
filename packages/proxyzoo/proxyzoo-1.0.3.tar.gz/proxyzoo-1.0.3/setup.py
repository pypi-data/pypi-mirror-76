import sys
from setuptools import find_packages,setup

install_requires = ['kazoo']

with open("README.rst", "r") as fp:
    proxyzoo_long_description = fp.read()

#text/x-rst
#text/markdown
#text/plain

setup(
    name = 'proxyzoo',
    version = '1.0.3',
    url = "http://git.wadecn.com:18082/bits/proxy-zk",
    author = "xiedx",
    author_email = "40317303@qq.com",
    description = "Haproxy dynamic load balancing",
    long_description = proxyzoo_long_description,
    long_description_content_type = "text/plain",
    license = "MIT",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Communications",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Networking",
    ],
    #py_modules = ['proxyzoo'],
    #package_dir={'': 'proxyzoo'},
    #packages = ['conf', 'haproxy', 'zk'],
    #packages = ['proxyzoo','proxyzoo.conf', 'proxyzoo.haproxy', 'proxyzoo.zk'],
    packages = find_packages(),
    install_requires = install_requires
)