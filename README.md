# IP Checker
Tool to check currently connected IP's using GreyNoise API.
It use classic Unix 'netstat' to gain list of currently connected IP's and scan them using GreyNoise API.

# Installation 
```sh
pip install ip-checker
```
or you can install it from source:

```sh
git clone https://github.com/mickgl/ip-checker.git
python3 setup.py install
```
# Usage

By default IP-Checker runs in background and repeats scan until received kill signal.
To run in default mode:

```sh
ipchecker
```
However there are two other modes: 'log' which also log all scanned adresses in text file and 'no-background' which preforms one scan and exit.

To run in 'log' mode:

```sh
ipchecker --log
```
And to run in 'no-background':

```sh
ipchecker --no-background
```
# Configuration

All configuration is made in 'conf.py' which is (for now) located in site-packages after installation.
You can modify it directly or just use '--cfg' argument to access it from IP-Checker:

```sh
ipchecker --cfg
```

For info about configuration look at 'conf.py'.
