## The Good News

As part of upgrading my home data center, I bought a
new UPS unit with longer runtime and AVR.  The good news is that
the new Tripp Lite SMART1500LCDT has a 50 minute runtime at 18% load (versus 35
minutes with my old APC 1500).  It also has robust AVR (Active Voltage
Regulation) that is confirmed to compensate for switchover to generator power.

## The Bad News

The bad news is that they totally screwed up the USB port needed for
the server to monitor the UPS.  It locks up every few days, and even
resetting the hub controller does not reset it - it ignores the reset
and address assignment requests from the hub, i.e. it does *not* implement
the mandatory reset feature of the USB 2.0 standard.  Reviews indicate that
even their proprietary Windows software is stymied by this defect, but
Windows users accept it as par for the course, naturally.  

## The Workaround

We can reset the USB port on the UPS by turning off power to the port
on a [USB compliant](http://www.makelinux.net/lib/usb/2/USB_2.0_Specification/doc-363) hub.

#### Mandatory All Ports Off State

> Although a self-powered hub is not required to implement power switching, the
> hub MUST support the Powered-off state for all ports. Additionally, the hub
> MUST implement the PortPwrCtrlMask (all bits set to 1B) even though the hub
> has no power switches that can be controlled by the USB System Software.

## The Sad Reality

While most USB microcontrollers used in hubs properly implement one or
both of these options (controlled by configuration pins), unfortunately, it
seems that nearly all actual USB hubs in a box on the market ignore this
mandatory feature, and just hardwire Vcc on all ports to 5V.  I 
am using a Linksys USB2HUB4, other working hubs are listed below.

Copyright (C) 2016 Stuart D. Gathman

Author: Stuart Gathman <stuart at gathman.org>

hub-ctrl.c
==========

Control USB power on a port by port basis on USB hubs with port power switching.

Originally created NIIBE Yutaka and published to Github by Joel Dare on January
31st, 2013.

This only works on USB hubs that have the hardware necessary to allow
software controlled power switching. Most hubs DO NOT include the hardware.

Controlling Power
=================

You can control the power on a port using the following command.

    sudo hub-ctrl -h 3 -P 1 -p 0

That says to control hub 3 (-h 3) port 1 (-P 1) and to turn the power
off (-p 0). You can also use ”-p 1” to turn the power back on.

You can also specify the USB device based on the BUS and DEV numbers. Use the
following command the list the currently connected devices. It's useful to run
this with the device disconnected and then again with the device connected so
that you can tell which device is the one you are trying to target (the Targus
in my case).

    lsusb

Now that we know the BUS and DEV numbers, we can control the power using those
numbers as well. Here's the command for that.

    sudo hub-ctrl -b 001 -d 005 -P1 -p 0

This time we are controlling the device on BUS 001 (-b 001) device 005 (-d 005)
port 1 (-P 1) and turning the power off (-p 0).

Hubs Known to Work
==================

The following is a list of Hubs that are known to have the hardware necessary
to allow power switching.

  - D-Link-DUB-H7-High-Speed-7-Port (Tested with old Silver versions (A3, A4 & A5). Also tested with newer Black version C1).
  - Elecom: U2H-G4S
  - Sanwa Supply: USB-HUB14GPH
  - Targus, Inc.: PAUH212
  - Hawking Technology: UH214
  - B&B Electronics: UHR204
  - Belkin: F5U701
  - Linksys: USB2HUB4

Original Copyright
==================

Copyright (C) 2006 Free Software Initiative of Japan

Author: NIIBE Yutaka  <gniibe at fsij.org>

This file can be distributed under the terms and conditions of the GNU General
Public License version 2 (or later).
