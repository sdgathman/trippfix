%global commit          42095e522859059e8a5f4ec05c1e3def01a870a9
%global shortcommit     42095e5
%global checkout        20161103git%{shortcommit}

Name:		nut-tripplite
Version:	0.1
Release:	1%{?dist}
Summary:	Nut workarounds for tripplite UPS

Group:		Applications/System
License:	GPL2+
URL:		https://github.com/sdgathman/trippfix/
Source0:	https://github.com/sdgathman/trippfix/archive/trippfix-%{version}.tar.gz
Source1:	https://github.com/codazoda/hub-ctrl.c/raw/%{commit}/hub-ctrl.c

BuildRequires:	libusb-devel
Requires:	nut-client nut-server incron
# For sms
Requires:	python2

%description
The Tripplite SMART1500LCDT UPS can handle running on a small generator
(unlike many cheap UPSes), but the USB port is braindead and requires
unplugging and plugging back in every few days.  Fortunately, this can
be simulated by removing power from the port on the hub.  To do this, you
will need a hub that actually implements the USB spec.  This package
has scripts for nut to automatically reset the USB port of the UPS
when it dies.  In addition, there is a client for an SMS service to
notify your phone when the power goes out.  (Unrelated - should be
its own package.)

A list of working hubs.

I have tested this with Linksys USB2HUB4.  

Install this if you need your Tripplite SMART1500LCDT to work with nut
for more than a few days.

%prep
%setup -q -n trippfix-%{version}
cp -p %{SOURCE1} .

%build
make LDFLAGS="$RPM_LD_FLAGS -lusb" V=1 hub-ctrl

%install
mkdir -p %{buildroot}%{_sysconfdir}/ups
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/incron.d
install -pm 640 sms.conf %{buildroot}%{_sysconfdir}/ups
install -pm 644 upssched.conf %{buildroot}%{_sysconfdir}/ups/upssched-tripp.conf
install -pm 644 trippfix.conf %{buildroot}%{_sysconfdir}/sysconfig/trippfix
install -pm 644 trippfix.incron %{buildroot}%{_sysconfdir}/incron.d/trippfix

mkdir -p %{buildroot}%{_libexecdir}/trippfix
install -pm 755 upsreset.sh %{buildroot}%{_libexecdir}/trippfix/upsreset
install -pm 755 trippfix.py %{buildroot}%{_libexecdir}/trippfix


mkdir -p %{buildroot}%{_sbindir}
install -pm 755 hub-ctrl %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_bindir}
install -pm 755 sms.py %{buildroot}%{_bindir}/sms
install -pm 755 upssched-tripp.sh %{buildroot}%{_bindir}/upssched.tripp

mkdir -p %{buildroot}%{_var}/log
touch %{buildroot}%{_var}/log/ups.log

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/ups/sms.conf
%{_sysconfdir}/ups/upssched-tripp.conf
%{_sysconfdir}/sysconfig/trippfix
%{_libexecdir}/trippfix
%{_sbindir}/hub-ctrl
%{_bindir}/sms
%config(noreplace) %attr(-,nut,root) %{_var}/log/ups.log

%changelog

* Thu Nov  3 2016 Stuart Gathman <stuart@gathman.org> 0.1-1
- Initial package
