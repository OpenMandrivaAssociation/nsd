Summary:	Complete implementation of an authoritative DNS name server
Name:		nsd
Version:	4.0.0
Release:	2
License:	BSD
Group:		System/Servers
URL:		http://www.nlnetlabs.nl/projects/nsd/
Source0:	http://www.nlnetlabs.nl/downloads/%{name}/%{name}-%{version}.tar.gz
Source1:	nsd.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	openssl-devel
BuildRequires:	tcp_wrappers-devel
Conflicts:	bind pdns

%description
NSD is a complete implementation of an authoritative DNS name server. For
further information about what NSD is and what NSD is not please consult the
REQUIREMENTS document which is a part of this distribution (thanks to Olaf).

%prep

%setup -q 

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
%serverbuild

%configure2_5x \
    --localstatedir=/var/lib \
    --enable-bind8-stats \
    --enable-plugins \
    --enable-checking \
    --enable-mmap \
    --enable-dnssec \
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

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_initrddir}

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
%attr(0711,%{name},%{name}) %dir /var/lib/%{name}
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/*/*


%changelog
* Sat Nov 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.2.8-1mdv2012.0
+ Revision: 718430
- 3.2.8

* Wed Mar 16 2011 Stéphane Téletchéa <steletch@mandriva.org> 3.2.7-1
+ Revision: 645332
- update to new version 3.2.7

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-3mdv2011.0
+ Revision: 613107
- the mass rebuild of 2010.1 packages

* Fri Apr 16 2010 Funda Wang <fwang@mandriva.org> 3.2.4-2mdv2010.1
+ Revision: 535272
- rebuild

* Tue Feb 16 2010 Sandro Cazzaniga <kharec@mandriva.org> 3.2.4-1mdv2010.1
+ Revision: 506518
- update to 3.2.4

* Wed Dec 16 2009 Jérôme Brenier <incubusss@mandriva.org> 3.2.3-1mdv2010.1
+ Revision: 479511
- new version 3.2.3

* Mon Jun 01 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.2-1mdv2010.0
+ Revision: 381947
- 3.2.2 (fixes CVE-2009-1755)

* Thu Aug 14 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.1-1mdv2009.0
+ Revision: 271893
- 3.1.1
- fix initscript, spec file and locations

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 3.0.6-4mdv2009.0
+ Revision: 254068
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 3.0.6-2mdv2008.1
+ Revision: 171000
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Nov 06 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-1mdv2008.1
+ Revision: 106401
- 3.0.6
- use the %%serverbuild macro

* Thu Sep 06 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.5-1mdv2008.0
+ Revision: 81124
- 3.0.5


* Thu Jan 11 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.3-1mdv2007.0
+ Revision: 107608
- Import nsd

* Thu Jan 11 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.3-1mdv2007.1
- initial Mandriva package (adapted from fedora)

* Thu Dec 07 2006 Paul Wouters <paul@xelerance.com> 3.0.3-1
- Upgraded to 3.0.3

* Mon Nov 27 2006 Paul Wouters <paul@xelerance.com> 3.0.2-1
- Upgraded to 3.0.2.
- Use new configuration file nsd.conf. Still needs migration script.
  patch from Farkas Levente <lfarkas@bppiac.hu>

* Tue Oct 17 2006 Paul Wouters <paul@xelerance.com> 2.3.6-2
- Bump version for upgrade path

* Fri Oct 13 2006 Paul Wouters <paul@xelerance.com> 2.3.6-1
- Upgraded to 2.3.6
- Removed obsolete workaround in nsd.init
- Fixed spec file so daemon gets properly restarted on upgrade

* Tue Sep 12 2006 Paul Wouters <paul@xelerance.com> 2.3.5-4
- Rebuild requested for PT_GNU_HASH support from gcc
- Removed dbaccess.c from doc section

* Tue Jun 27 2006 Paul Wouters <paul@xelerance.com> - 2.3.5-3
- Bump version for FC-x upgrade path

* Tue Jun 27 2006 Paul Wouters <paul@xelerance.com> - 2.3.5-1
- Upgraded to nsd-2.3.5

* Mon May 08 2006 Paul Wouters <paul@xelerance.com> - 2.3.4-3
- Upgraded to nsd-2.3.4. 
- Removed manual install targets because DESTDIR is now supported
- Re-enabled --checking, checking patch no longer needed and removed.
- Work around in nsd.init for nsd failing to start when there is no ipv6

* Thu Dec 15 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-7
- chkconfig and attribute  changes as proposed by Dmitry Butskoy

* Thu Dec 15 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-6
- Moved pid file to /var/run/nsd/nsd.pid.
- Use _localstatedir instead of "/var"

* Tue Dec 13 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-5
- Added BuildRequires for openssl-devel, removed Requires for openssl.

* Mon Dec 12 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-4
- upgraded to nsd-2.3.3

* Wed Dec 07 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.2-2
- minor cleanups

* Mon Dec 05 2005 Paul Wouters <paul@xelerance.com> - 2.3.2-1
- Upgraded to 2.3.2. Changed post scripts to comply to Fedora
  Extras policies (eg do not start daemon on fresh install)

* Wed Oct 05 2005 Paul Wouters <paul@xelerance.com> - 2.3.1-1
- Initial version

