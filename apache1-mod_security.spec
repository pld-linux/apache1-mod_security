%define		mod_name	security
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: securing web applications
Summary(pl.UTF-8):	Moduł do apache: ochrona aplikacji WWW
Name:		apache1-mod_%{mod_name}
Version:	1.8.7
Release:	0.2
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.modsecurity.org/download/modsecurity-%{version}.tar.gz
# Source0-md5:	0dd48656e451c711358c097dc80e0369
URL:		http://www.modsecurity.org/
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
ModSecurity is an open source intrusion detection and prevention
engine for web applications. It operates embedded into the web server,
acting as a powerful umbrella - shielding web applications from
attacks.

%description -l pl.UTF-8
ModSecurity jest otwartym silnikiem wykrywania i zapobiegania intruzom
dla aplikacji WWW. Operuje w ramach serwera WWW, działając jak potężny
parasol chroniący aplikacje WWW przed atakami.

%prep
%setup -q -n mod%{mod_name}-%{version}

%build
cd apache1
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install apache1/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES modsecurity-manual.pdf httpd.conf*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
