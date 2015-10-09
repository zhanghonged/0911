#coding=utf-8

passwords={'root:119.29.58.147:22':'XjSRJkd395qTA'}
#passwords={'root:192.168.1.5:22':'hongpan','root:192.168.1.4:22':'backup','root:119.29.58.147:22':'XjSRJkd395qTA'}
#passwords={'root:192.168.1.5:22':'hongpan'}

#kill openfire进程
#cmds=["ps -ef | grep openfire | grep -v grep |awk '{print $2}'","ps -ef | grep openfire | grep -v grep |awk '{print $2}'|xargs kill -9"]

#启动openfire
#cmds=['source /etc/profile; /opt/openfire/bin/openfirectl start']
#cmds=['ifconfig eth0 ; pwd']
cmds=['ifconfig eth0', 'pwd']

