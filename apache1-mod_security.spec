%define		mod_name	security
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: securing web applications
Summary(pl):	Modu³ do apache: ochrona aplikacji WWW
Name:		apache1-mod_%{mod_name}
Version:	1.8.6
Release:	0.4
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.modsecurity.org/download/mod_security-%{version}.tar.gz
# Source0-md5:	f6bf4724dd0db3d37586b64bc0ee160d
URL:		http://www.modsecurity.org/
BuildRequires:	apache1-devel >= 1.3.33-2
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
ModSecurity is an open source intrusion detection and prevention
engine for web applications. It operates embedded into the web server,
acting as a powerful umbrella - shielding web applications from
attacks.

%description -l pl
ModSecurity jest otwartym silnikiem wykrywania i zapobiegania intruzom
dla aplikacji WWW. Operuje w ramach serwera WWW, dzia³aj±c jak
potê¿ny parasol chroni±cy aplikacje WWW przed atakami.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
cd apache1
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install apache1/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES modsecurity-manual.pdf httpd.conf*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
