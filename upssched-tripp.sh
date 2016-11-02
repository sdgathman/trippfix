#! /bin/sh
#
# This script should be called by upssched via the CMDSCRIPT directive.
# 
# Here is a quick example to show how to handle a bunch of possible
# timer names with the help of the case structure.
#
# This script may be replaced with another program without harm.
#
# The first argument passed to your CMDSCRIPT is the name of the timer
# from your AT lines.

LOG=/var/log/ups.log
TS="$(date '+%Y-%m-%d %H:%M:%S')"

case $1 in
    upsreset)
	logger -t upssched-cmd "The UPS has been gone for awhile, resetting"
	echo "$TS" "NOCOMM" >>$LOG
	;;
    sms-onbatt)
	logger -t upssched-cmd "Sending OnBattery SMS"
	echo "$TS" "SMS" \
		"The Gathman Server has lost power and is on battery.">>$LOG
    	;;
    sms-online)
	logger -t upssched-cmd "Sending OnLine SMS"
	echo "$TS" "SMS" \
		"Power has been restored to the Gathman Server." >>$LOG
    	;;
    *)
	logger -t upssched-cmd "Unrecognized command: $1"
	;;
esac
