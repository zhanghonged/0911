#!/usr/bin/env python

def version():

  return '1.0.1'



def help():
  return '''

--version Display version number.

default,read the appdeploy.py host informatin. appdeploy.passwords.
no argv:  run the appdeploy.cmds.
run [cmds]  
;the "cmds" can be a separate command, or can be multiple commands separated by ';'  example "cd /opt ; pwd"
get [remotefiles] [localpath]
put [remotefiles/remotepath] [localpath]
 
        '''

