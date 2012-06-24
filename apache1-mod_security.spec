%define		mod_name	security
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: securing web applications
Summary(pl):	Modu� do apache: ochrona aplikacji webowych
Name:		apache1-mod_%{mod_name}
Version:	1.8.6
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.modsecurity.org/download/mod_security-%{version}.tar.gz
# Source0-md5:	f6bf4724dd0db3d37586b64bc0ee160d
URL:		http://sourceforge.net/projects/mod-acct/
BuildRequires:	apache1-devel
Requires(post,preun):	%{apxs}
Requires:	apache1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir     /etc/httpd

%description
ModSecurity is an open source intrusion detection and
prevention engine for web applications. It operates embedded
into the web server, acting as a powerful umbrella - shielding
web applications from attacks.

%description -l pl
ModSecurity jest otwartym silnikiem wykrywania i zapobiegania 
intruzom dla aplikacji webowych. Oferuje wbudwany w serwer www,
dzia�aj�c jak pot�ny parasol chroni�cy aplikacje webowe przed
atakami.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
cd apache1
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install apache1/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES modsecurity-manual.pdf httpd.conf*
%attr(755,root,root) %{_pkglibdir}/*
