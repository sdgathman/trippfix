#!/usr/bin/python

import sys
import logging
import smtplib
import tempfile
from email.Message import Message
from email.Utils import getaddresses,parseaddr
from suds.client import Client
from ConfigParser import RawConfigParser

logging.basicConfig(level=logging.INFO)

# FIXME: need to read these from config

config = RawConfigParser()
config.read('/etc/ups/sms.conf')

PHONE = dict(config.items('phone'))
EMAIL = dict(config.items('email'))
USERID = config.get('main','userid')
FROM = config.get('main','from')

class SMSError(Exception): pass

class SMS(object):
  client = Client('http://smsgateway.ca/SendSMS.asmx?WSDL')
  def __init__(self,key):
    self.key = key
    self.remaining = None
  def sendMsg(self,cell,msg,ref=''):
    res = self.client.service.SendMessageWithReferenceExtended(
    	cell, msg, self.key, ref)
#   MessagesRemaining = "8"
#   MessageID = "2171881"
#   QueuedSuccessfully = "True"
#   ErrorMessage = ""
    self.remaining = int(res.MessagesRemaining)
    if not res.QueuedSuccessfully:
      raise SMSError(res.ErrorMessage)
    return int(res.MessageID)
  def getSent(self,cnt=10):
    res = self.client.service.GetSentMessages(self.key, cnt)
#   CreditsDeducted = "1"
#   Reference = ""
#   Sent = "True"
#   QueueDate = "2009-06-19 16:03:50.267000"
#   MessageID = "2123455"
#   SendDate = "2009-06-19 16:03:56.830000"
#   Status = "Success"
#   Body = "..."
#   CellNumber = "5711234567"
    return res.SMSOutgoingMessage

  def getRecv(self,cnt=10):
    res = self.client.service.GetIncomingMessages(self.key, cnt)
    if not res: return res
#   OutgoingMessageID = "2123456"
#   Reference = ""
#   MessageNumber = "116297"
#   PhoneNumber = "5711234567"
#   Message = "Ok. I love you."
#   ReceivedDate = "2009-06-19 16:06:25.243000"
    return res.SMSIncomingMessage

def sendEmail(to,subj,txt):
  msg = Message()
  msg.set_type('text/plain')
  msg.add_header('Subject',subj)
  msg.add_header('From',FROM)
  msg.add_header('To',to)
  realname,fromaddr = parseaddr(FROM)
  msg.set_payload(txt)
  with open('/var/log/email.log','at') as fp:
    fp.write(msg.as_string(True)+'\n')
  toaddrs = [addr for name,addr in getaddresses([msg['to']])]
  server = smtplib.SMTP('localhost')
  #server.set_debuglevel(1)
  server.sendmail(fromaddr, toaddrs, msg.as_string())
  server.quit()

if __name__ == '__main__':
  sms = SMS(USERID)

  if len(sys.argv) > 1:
    msg = ' '.join(sys.stdin.read().split())
    name = sys.argv[1]
    if name in PHONE:
      cell = PHONE[name]
    else:
      cell = name
    if len(msg) > 160:
      print "Message too long (%d)." % len(msg)
    else:
      res = sms.sendMsg(cell, msg)
      print "id %d, %d units remaining"%(res,sms.remaining)
      if name in EMAIL:
        sendEmail(EMAIL[name],'SMS %d'%res,msg)
  else:
    for m in sms.getRecv():
      print "%8s %8s %8s %10s %s" % (
        m.OutgoingMessageID,
        m.Reference,
        m.MessageNumber,
        m.PhoneNumber,
        m.ReceivedDate )
      print "> ",m.Message
    for m in sms.getSent():
      print "%1s %8s %1s%1s %8s %10s %s" % (
        m.CreditsDeducted, m.Reference, m.Sent, m.Status[:1],
	m.MessageID, m.CellNumber, m.SendDate
      )
      print "> ",m.Body
