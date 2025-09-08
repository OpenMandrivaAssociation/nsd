Summary:	Complete implementation of an authoritative DNS name server
Name:		nsd
Version:	4.13.0
Release:	1
License:	BSD
Group:		System/Servers
URL:		https://www.nlnetlabs.nl/projects/nsd/
Source0:	http://www.nlnetlabs.nl/downloads/%{name}/%{name}-%{version}.tar.gz
Source1:	nsd.init
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	tcp_wrappers-devel
Conflicts:	bind pdns

%description
NSD is a complete implementation of an authoritative DNS name server. For
further information about what NSD is and what NSD is not please consult the
REQUIREMENTS document which is a part of this distribution (thanks to Olaf).

%prep
%autosetup -p1
# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
%serverbuild

%configure \
	--localstatedir=/var/lib \
	--enable-bind8-stats \
	--enable-plugins \
	--enable-checking \
	--enable-mmap \
	--enable-dnssec \
	--disable-dnstap \
	--enable-ipv6 \
	--enable-tsig \
	--enable-nsig \
	--with-pidfile=/var/run/%{name}/%{name}.pid \
	--with-dbfile=/var/lib/%{name}/nsd.db \
	--with-difffile=/var/lib/%{name}/ixfr.db \
	--with-xfrdfile=/var/lib/%{name}/xfrd.state \
	--with-ssl \
	--with-user=%{name}

# antiborker
perl -pi -e "s|^piddir = .*|piddir = /var/run/%{name}|g" Makefile
perl -pi -e "s|^dbdir = .*|dbdir = /var/lib/%{name}|g" Makefile

%make_build

%install
%make_install

install -d %{buildroot}%{_initrddir}

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# change .sample to normal config files
mv %{buildroot}%{_sysconfdir}/nsd/nsd.conf.sample %{buildroot}%{_sysconfdir}/nsd/nsd.conf

mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/%{name}.conf <<'EOF'
u %{name} - "NSD" %{_sysconfdir}/%{name} %{_bindir}/nologin
EOF

%files 
%defattr(-,root,root,-)
%doc doc/*
%attr(0711,%{name},%{name}) %dir %{_sysconfdir}/nsd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nsd/nsd.conf
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0711,%{name},%{name}) %dir /var/run/%{name}
%attr(0711,%{name},%{name}) %dir /var/lib/%{name}
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/*/*
%{_sysusersdir}/nsd.conf
