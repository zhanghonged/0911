#!/usr/bin/env python
#coding=utf-8
import paramiko
import sys,time
import os
import appdeploy
import threading
import help



class run_cmd(threading.Thread):
  def __init__(self,user,passw,host,port,cmds):
    threading.Thread.__init__(self)
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

class tran_put(threading.Thread):
  def __init__(self,user,passw,host,port,local,remote):
    threading.Thread.__init__(self)
    self.user=user
    self.passw=passw
    self.host=host
    self.port=port
    self.local=local
    self.remote=remote
    
  def run(self):
    t = paramiko.Transport((self.host,self.port))
    t.connect(username=self.user,password=self.passw)
    sftp = paramiko.SFTPClient.from_transport(t)
    localpath = self.local
    remotepath = self.remote
    #localpath 为一个目录时，put此目录下所有文件及目录
    if os.path.isdir(localpath):
      for root,dirs,files in os.walk(localpath):
        for f in files:
          localfiles=os.path.join(root,f)
          remotefiles=localfiles.replace(localpath,remotepath)
          try:
            sftp.put(localfiles,remotefiles)
          except Exception,e:
            sftp.mkdir(os.path.split(remotefiles)[0])
            sftp.put(localfiles,remotefiles)
        for d in dirs:
          localdirs=os.path.join(root,d)
          remotedirs=localdirs.replace(localpath,remotepath)
          try:
            sftp.mkdir(remotedirs)
          except Exception,e:
            print e
    #localpath 为一个文件时，put此文件
    if os.path.isfile(localpath):
      localfiles = localpath
      remotefiles = os.path.join(remotepath,localpath.split('/')[-1])
      try:
        sftp.put(localfiles,remotefiles)
      #捕获所有异常
      except Exception,e:
        print e
    t.close()

class tran_get(threading.Thread):
  def __init__(self,user,passw,host,port,remote,local):
    threading.Thread.__init__(self)
    self.user=user
    self.passw=passw
    self.host=host
    self.port=port
    self.local=local
    self.remote=remote

  def run(self):
    t = paramiko.Transport((self.host,self.port))
    t.connect(username=self.user,password=self.passw)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath = self.remote
    localpath = self.local
    try:
      remotefiles=remotepath
      localfiles=os.path.join(localpath,remotefiles.split('/')[-1])
      sftp.get(remotefiles,localfiles)
    #捕获特定异常 IOErro
    except IOError,e:
      print e
    finally:
      t.close



def exect(minfo,ccc):
  if len(sys.argv) > 1:
    if sys.argv[1] == '--help' and len(sys.argv) == 2:
      print help.help()
    if sys.argv[1] == '--version' and len(sys.argv) == 2:
      ver=help.version()
      print "version is %s" %ver
    for j,k in minfo.items():
      user=j.split(':')[0]
      host=j.split(':')[1]
      port=int(j.split(':')[2])
      password=k
      if sys.argv[1] in ['--help','--version'] and len(sys.argv) == 2:
        pass
      elif sys.argv[1] == 'run' and len(sys.argv) == 3:
        print 'exec host is                                                %s ' %host
        print sys.argv[1:]
        r=run_cmd(user,password,host,port,sys.argv[2])
        r.start()
      elif sys.argv[1] == 'put' and len(sys.argv) == 4:
        print 'exec host is                                                %s ' %host
        print sys.argv[1:]
        p=tran_put(user,password,host,port,sys.argv[2],sys.argv[3])
        p.start()
      elif sys.argv[1] == 'get' and len(sys.argv) == 4:
        print 'exec host is                                                %s ' %host
        print sys.argv[1:]
        p=tran_get(user,password,host,port,sys.argv[2],sys.argv[3])
        p.start()
      else:
        print 'Is Wrong,Please input again'
  else:
    for j,k in minfo.items():
      user=j.split(':')[0]
      host=j.split(':')[1]
      port=int(j.split(':')[2])
      password=k
      print 'exec host is                                                %s ' %host
      r=run_cmd(user,password,host,port,ccc)
      r.start()

exect(appdeploy.passwords,appdeploy.cmds)
