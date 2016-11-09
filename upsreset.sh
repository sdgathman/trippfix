#!/bin/bash

# Manually configured script to power cycle a port on a hub that supports PPPS

CONFIG="/etc/sysconfig/trippfix"
PORT=""	
TRIPPID="09ae:3016"	# Tripplite SMART1500LCDT
HUBID="0409:0058"	# Linksys USB2HUB4
DELAY="10"
CONTACT=""

test -s "$CONFIG" && . "$CONFIG"

reset() {
    port="$1"
    if test -z "$port"; then
      logger -t upsreset "PORT not set in $CONFIG"
      return 1
    fi
    # Find Linksys USB2HUB4
    lsusb | grep "$HUBID" |
    while read x1 bus x2 dev x3; do
      let bus="$bus"
      let dev="${dev%:}"
      # echo $bus $dev
      logger -t upsreset "Turning off port $port on ${bus}:${dev}"
      /sbin/hub-ctrl -b "${bus}" -d "${dev}" -P "$port" -p 0
      sleep "$DELAY"
      logger -t upsreset "Turning on port $port on ${bus}:${dev}"
      /sbin/hub-ctrl -b "${bus}" -d "${dev}" -P "$port" -p 1
    done
}

if [ "$1" = "-r" ]; then
  reset "$PORT"
  exit
fi

set - `tail -1 /var/log/ups.log`
event="$3"
shift 3
msg="$*"

if [ "$event" = "NOCOMM" ]; then
  if lsusb | grep "$TRIPPID" >/dev/null; then
    logger -t upsreset "UPS $TRIPPID active on USB" 
  else
    logger -t upsreset "RESET UPS $TRIPPID" 
    reset "$PORT"
  fi
elif [ "$event" = "SMS" ]; then
  logger -t upsreset "UPS SMS $msg" 
  if test -n "$CONTACT"; then
    echo "$msg" | sms stuart
  else
    logger -t upsreset "CONTACT not set in $CONFIG"
    exit 1
  fi
fi
