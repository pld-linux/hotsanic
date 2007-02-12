%define		_pver	pre5
%define		_name	HotSaNIC
Summary:	Html Overview to System and Network Information Center
Summary(pl.UTF-8):   HotSaNIC - centrum informacyjne dla systemów uniksowych
Name:		hotsanic
Version:	0.5.0
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/hotsanic/%{name}-%{version}-%{_pver}.tgz
# Source0-md5:	2b005b9ef437abf105a9426cfea51b11
Source1:	%{name}.conf
URL:		http://sourceforge.net/projects/hotsanic/
Requires:	ImageMagick
Requires:	iptables
Requires:	perl >= 1:5.0.0
Requires:	rrdtool
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysinfodir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
HotSaNIC is a Web-based information center for Unix-based systems.
It gives you a graphical overview about certain network and 
system statistics. HotSaNIC is programmed (mainly in Perl 5) 
in a modular way to give you a great flexibility.

%description -l pl.UTF-8
HotSaNIC to oparte na WWW centrum informacyjne dla systemów
uniksowych. Udostępnia graficzny podgląd wybranych statystyk sieci i
systemu. HotSaNIC został napisany (głównie w Perlu 5) w sposób
modularny, dający dużą elastyczność.

%prep
%setup -q -n %{_name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysinfodir}/images \
	$RPM_BUILD_ROOT%{_sysinfodir}/lib \
	$RPM_BUILD_ROOT%{_sysinfodir}/tools \
	$RPM_BUILD_ROOT%{_sysinfodir}/var \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/httpd}

install images/*.gif $RPM_BUILD_ROOT%{_sysinfodir}/images
install lib/*.pm $RPM_BUILD_ROOT%{_sysinfodir}/lib
install tools/*.sh *.pl $RPM_BUILD_ROOT%{_sysinfodir}/tools
install tools/{makeperlheaders,killmod} $RPM_BUILD_ROOT%{_sysinfodir}/tools
cp -r modules $RPM_BUILD_ROOT%{_sysinfodir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi
echo "          NOTICE"
echo "  You have to run setup.pl script"
echo "	to configure what You want to monitor."

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi


%files
%defattr(644,root,root,755)
%doc Documentation/CHANGES Documentation/README Documentation/README.snmp Documentation/TODO
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%dir %{_sysinfodir}
%attr(755,root,http) %{_sysinfodir}/images
%{_sysinfodir}/lib
%{_sysinfodir}/modules
%attr(755,root,http) %{_sysinfodir}/tools
%{_sysinfodir}/var
