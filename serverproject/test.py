# -*- coding: GBK -*-
import sys
import cPickle

sys.path.append('.')
sys.path.append('./common')
sys.path.append('./network')
sys.path.append('./common_server')
sys.path.append('./database')

from login import loginServer

log = loginServer()
print log.userPasswordConfirm('Client1','163')
print log.createAccount('test001','000')






