#!/bin/bash

reset() {
    lsusb | grep 0409:0058 |
    while read x1 bus x2 dev x3; do
      bus="$bus"
      dev="${dev%:}"
      # echo $bus $dev
      /sbin/hubpower "${bus}:${dev}" status | grep Connected | grep Low-Speed |
      while read x1 port x2; do
	/sbin/hubpower "${bus}:${dev}" power "$port" off
	sleep 10
	/sbin/hubpower "${bus}:${dev}" power "$port" on
      done
    done
}

if [ "$1" = "-r" ]; then
  reset
fi

set - `tail -1 /var/log/ups.log`
event="$3"
shift 3
msg="$*"

if [ "$event" = "NOCOMM" ]; then
  logger -t upsreset "RESET UPS" 
  if lsusb | grep 09ae:3016 >/dev/null; then
    : Tripplite is visible on USB bus
  else
    reset
  fi
elif [ "$event" = "SMS" ]; then
  logger -t upsreset "UPS SMS $msg" 
  echo $msg | /usr/local/sbin/sms stuart
fi
