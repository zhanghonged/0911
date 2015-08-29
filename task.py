#!/usr/bin/env python
#coding=utf-8
import paramiko
import sys
import os
import appdeploy



def run(user,passw,host,port,cmds):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(host,port=port,username=user,password=passw)
  #print type(cmds)
  if isinstance(cmds,list):
    for i in xrange(len(cmds)):
      print 'cmd is "%s" **********************************************' %cmds[i] 
      stdin,stdout,stderr=ssh.exec_command(cmds[i])
      for i in stdout.readlines():
        print i,
      for i in stderr.readlines():
        print i,
  else:
    stdin,stdout,stderr=ssh.exec_command(cmds)
    for i in stdout.readlines():
      print i,
  ssh.close()

def tran_put(user,passw,host,port,local,remote):
  t = paramiko.Transport((host,port))
  t.connect(username=user,password=passw)
  sftp = paramiko.SFTPClient.from_transport(t)
  localpath = local
  remotepath = os.path.join(remote,local.split('/')[-1])
  sftp.put(localpath,remotepath)
  t.close()

def tran_get(user,passw,host,port,remote,local):
  t = paramiko.Transport((host,port))
  t.connect(username=user,password=passw)
  sftp = paramiko.SFTPClient.from_transport(t)
  remotepath = remote
  localpath = os.path.join(local,remotepath.split('/')[-1])
  print localpath
  sftp.get(remotepath,localpath)
  t.close()

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
