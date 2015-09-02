#!/usr/bin/env python
#coding=utf-8
import paramiko
import sys
import os
import appdeploy

class run_cmd():
  def __init__(self,user,passw,host,port,cmds):
    self.user=user
    self.passw=passw
    self.host=host
    self.port=port
    self.cmds=cmds
    print user,passw,host,port,cmds
  def run(self):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(self.host,port=self.port,username=self.user,password=self.passw)
    #print type(cmds)
    #如果命令是列表形式
    if isinstance(self.cmds,list):
      for i in xrange(len(self.cmds)):
        print 'cmd is "%s" **********************************************' %self.cmds[i]
        stdin,stdout,stderr=ssh.exec_command(self.cmds[i])
        for i in stdout.readlines():
          print i,
        for i in stderr.readlines():
          print i,
    else:
      stdin,stdout,stderr=ssh.exec_command(self.cmds)
      for i in stdout.readlines():
        print i,
      for i in stderr.readlines():
        print i
    ssh.close()

#t=run_cmd('root','hongpan','192.168.1.5',22,'ifconfig br0')
#t.run()

class uad():
  def __init__(self,user,passw,host,port,local,remote):
    self.user=user
    self.passw=passw
    self.host=host
    self.port=port
    self.local=local
    self.remote=remote
    
  def tran_put(self):
    t = paramiko.Transport((self.host,self.port))
    t.connect(username=self.user,password=self.passw)
    sftp = paramiko.SFTPClient.from_transport(t)
    localpath = self.local
    remotepath = os.path.join(self.remote,self.local.split('/')[-1])
    sftp.put(localpath,remotepath)
    t.close()

  def tran_get(self):
    t = paramiko.Transport((self.host,self.port))
    t.connect(username=self.user,password=self.passw)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath = self.local
    localpath = os.path.join(self.remote,remotepath.split('/')[-1])
    print 'remotepath is %s' %remotepath
    print 'localpath is %s' %localpath
    sftp.get(remotepath,localpath)
    t.close()



def exect(minfo,ccc):
  for j,k in minfo.items():
    user=j.split(':')[0]
    host=j.split(':')[1]
    port=int(j.split(':')[2])
    password=k
    print 'exec host is                                                %s ' %host
    if len(sys.argv) > 1:
      if sys.argv[1] == 'run' and len(sys.argv) == 3:
        print sys.argv[1:]
        r=run_cmd(user,password,host,port,sys.argv[2])
        r.run()
      elif sys.argv[1] == 'put' and len(sys.argv) == 4:
        print sys.argv[1:]
        p=uad(user,password,host,port,sys.argv[2],sys.argv[3])
        p.tran_put()
      elif sys.argv[1] == 'get' and len(sys.argv) == 4:
        print sys.argv[1:]
        p=uad(user,password,host,port,sys.argv[2],sys.argv[3])
        p.tran_get()
      else:
        print 'Is Wrong,Please input again'
    else:
      r=run_cmd(user,password,host,port,ccc)
      r.run()

exect(appdeploy.passwords,appdeploy.cmds)


'''
#下面是用关键字参数实现exect函数的代码片段 **kwargs
def exect(minfo,**kw):
  for j,k in minfo.items():
    user=j.split(':')[0]
    host=j.split(':')[1]
    port=int(j.split(':')[2])
    password=k
    cmd=kw
    print cmd
    print 'exec host is                                                %s ' %host
    if len(sys.argv) == 1 or sys.argv[1] == 'run':
      run(user,password,host,port,cmd['cmds'])
    elif sys.argv[1] == 'put':
      tran_put(user,password,host,port,cmd['local'],cmd['remote'])
    elif sys.argv[1] == 'get':
      tran_get(user,password,host,port,cmd['remote'],cmd['local'])

def zhixing():
  if len(sys.argv) > 1:
    if sys.argv[1] == 'run' and len(sys.argv) == 3:
      print sys.argv[1:]
      exect(appdeploy.passwords,cmds=sys.argv[2])
    elif sys.argv[1] == 'put' and len(sys.argv) == 4:
      print sys.argv[1:]
      exect(appdeploy.passwords,local=sys.argv[2],remote=sys.argv[3])
    elif sys.argv[1] == 'get' and len(sys.argv) == 4:
      print sys.argv[1:]
      exect(appdeploy.passwords,remote=sys.argv[2],local=sys.argv[3])
    else:
      print 'Is Wrong!'
  else:
    exect(appdeploy.passwords,cmds=appdeploy.cmds)

zhixing()
'''
