Summary:	Complete implementation of an authoritative DNS name server
Name:		nsd
Version:	3.0.6
Release:	%mkrel 1
License:	BSD-like
Group:		System/Servers
URL:		http://open.nlnetlabs.nl/nsd/
Source0:	http://open.nlnetlabs.nl/downloads/nsd/%{name}-%{version}.tar.gz
Source1:	nsd.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	flex
BuildRequires:	openssl-devel
Conflicts:	bind pdns
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
NSD is a complete implementation of an authoritative DNS name server. For
further information about what NSD is and what NSD is not please consult the
REQUIREMENTS document which is a part of this distribution (thanks to Olaf).

%prep

%setup -q 

%build
%serverbuild

%configure2_5x \
    --enable-bind8-stats \
    --enable-plugins \
    --enable-checking \
    --enable-mmap \
    --with-pidfile=/var/run/%{name}/%{name}.pid \
    --with-ssl \
    --with-user=%{name}

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/run/%{name}

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# change .sample to normal config files
mv %{buildroot}%{_sysconfdir}/nsd/nsd.conf.sample %{buildroot}%{_sysconfdir}/nsd/nsd.conf

%pre
%_pre_useradd %{name} %{_sysconfdir}/%{name} /sbin/nologin

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc doc/*
%attr(0711,%{name},%{name}) %dir %{_sysconfdir}/nsd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nsd/nsd.conf
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0711,%{name},%{name}) %dir /var/run/%{name}
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/*/*
