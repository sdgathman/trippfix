#!/usr/bin/python2

## @trippfix Workaround broken USB port on Tripplite SMART1500LCDT
#
# The USB port on the Tripplite hangs after 4 days or so.  It can be
# reset by removing and reinserting the USB cable.  If it is plugged
# into a port on a real USB 2.0 hub (a rare beast - most leave out
# the mandatory power control features to save a few pennies), then
# turning the port power off, then on again will also reset the USB port.
#
# First we find the bus, parent device, and port of the UPS.  Then
# we use hubpower (or hub-ctrl) to turn the power off, wait a few seconds,
# then turn it on again.
#
# When the Tripplite hangs, it disappears from the USB bus, so we have
# to save the parent hub and port while it is working.

# Bus=05 Lev=02 Prnt=12 Port=03 Cnt=01 Dev#= 19 Spd=1.5  MxCh= 0
def parse_attr(v):
  last_key = None
  d = {}
  for s in v.split(' '):
    if s.find('=') > 0:
      last_key,v = s.split('=',1)
      d[last_key] = v
      continue
    if last_key:
      d[last_key] = ' '.join((d[last_key],s))
  return d

class USBDev(object):

  def __init__(self,s=None):
    self.attrs = {}
    if s: self.parse(s)

  def _parse_tree(self,d):
    self.bus = int(d['Bus'])
    self.lev = int(d['Lev'])
    self.parent = int(d['Prnt'])
    self.port = int(d['Port'])
    self.cnt = int(d['Cnt'])
    self.dev = int(d['Dev#'])
    self.chans = int(d['MxCh'])
    self.speed = float(d['Spd'])

  def _parse_prod(self,d):
    self.vendor = int(d['Vendor'],16)
    self.prodid = int(d['ProdID'],16)
    self.rev = d['Rev']
    
  def parse(self,s):
    for ln in s.split('\n'):
      if not ln: continue
      t,v = ln.split(':',1)
      d = parse_attr(v)
      if t == 'T':
        self._parse_tree(d)
      elif t == 'P':
        self._parse_prod(d)
      elif t == 'S':
	for k in d.keys():
	  self.attrs[k] = d[k]

def find_dev(vend,prod,serial=None):
  with open("/proc/bus/usb/devices",'r') as fp:
    for s in fp.read().split('\n\n'):
      if not s: continue
      u = USBDev(s)
      if serial and u.attrs['SerialNumber'] != serial: continue
      if u.vendor == vend and u.prodid == prod:
        return u

def main(argv):
  u = find_dev(0x09ae,0x3016)
  print '/sbin/hubpower %d:%d power %d off # %s' % (
  	u.bus,u.parent,u.port+1,u.attrs['Product'])

if __name__ == '__main__':
  import sys
  main(sys.argv[1:])
