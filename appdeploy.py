#coding=utf-8

#passwords={'root:192.168.1.5:22':'hongpan','root:192.168.1.4:22':'backup'}
passwords={'root:192.168.1.5:22':'hongpan'}

#kill openfire进程
#cmds=["ps -ef | grep openfire | grep -v grep |awk '{print $2}'","ps -ef | grep openfire | grep -v grep |awk '{print $2}'|xargs kill -9"]

#启动openfire
cmds=['source /etc/profile; /opt/openfire/bin/openfirectl start']
