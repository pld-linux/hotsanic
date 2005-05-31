%define		_pver	pre5
%define		_name	HotSaNIC
Summary:	Html Overview to System and Network Information Center
Summary(pl):	-
Name:		hotsanic
Version:	0.5.0
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://heanet.dl.sourceforge.net/sourceforge/hotsanic/%{name}-%{version}-%{_pver}.tgz
# Source0-md5:	2b005b9ef437abf105a9426cfea51b11
URL:		http://sourceforge.net/projects/hotsanic/
BuildRequires:	ImageMagick-devel
BuildRequires:	iptables
BuildRequires:  perl-devel >= 1:5.0.0
BuildRequires:  rrdtool
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HotSaNIC is a Web-based information center for Unix-based systems.
It gives you a graphical overview about certain network and 
system statistics. HotSaNIC is programmed (mainly in Perl 5) 
in a modular way to give you a great flexibility of which items yo

%description -l pl

%prep
%setup -q -n %{_name}

%build
#%configure
#%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8}

install doc/man/* $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Documentation/CHANGES Documentation/README Documentation/README.snmp Documentation/TODO
