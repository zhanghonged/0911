#!/usr/bin/env python
import time,sys


logdate=time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
def wlog(cont):
  if len(sys.argv) > 1:
    b=sys.argv[1]
  else:
    b='empty'
  log=open('%s_%s.txt' % (logdate,b) ,'a')
  try:
    log.write('%s\n' %cont)
  finally:
    log.close()
