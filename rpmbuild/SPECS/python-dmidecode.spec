%define _buildid .99

%global python_sitearch %{sys_python_sitearch}
%global __python %{__sys_python}

%global py26nvr python26-dmidecode-%{version}-%{release}
%global py26builddir %{_builddir}/%{py26nvr}
%global py26doc ../%{py26nvr}

%global py27nvr python27-dmidecode-%{version}-%{release}
%global py27builddir %{_builddir}/%{py27nvr}
%global py27doc ../%{py27nvr}

Summary: Python module to access DMI data
Name: python-dmidecode
Version: 3.10.13
Release: 3%{?_buildid}.c2fo
License: GPLv2+
Group: System Environment/Libraries
URL: http://projects.autonomy.net.au/python-dmidecode/
Source0: http://src.autonomy.net.au/python-dmidecode/%{name}-%{version}.tar.gz
# Upstream source gone. Repository restored from developer tree or source packages.
# Source1: generate-tarball.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libxml2-python26
Requires: libxml2-python27
BuildRequires: libxml2-python26
BuildRequires: libxml2-python27
BuildRequires: libxml2-devel
BuildRequires: python26-devel
BuildRequires: python27-devel

Patch1: SIGILL-catcher.patch
Patch2: dmispec-remove.patch
Patch3: installed-invalid.patch

# Amazon Patches
Patch10: pymap-typo-fix.patch

%description
python-dmidecode is a python extension module that uses the
code-base of the 'dmidecode' utility, and presents the data
as python data structures or as XML data using libxml2.

%package -n python26-dmidecode
Summary: Python module to access DMI data
Requires: libxml2-python26
BuildRequires: libxml2-python26
BuildRequires: python26-devel
Provides: python-dmidecode = %{version}-%{release}
Obsoletes: python-dmidecode <= 3.10.13-3.10.amzn1

%description -n python26-dmidecode
python-dmidecode is a python extension module that uses the
code-base of the 'dmidecode' utility, and presents the data
as python data structures or as XML data using libxml2.

This package is meant to be used with Python 2.6.

%package -n python27-dmidecode
Summary: Python module to access DMI data
Requires: libxml2-python27
BuildRequires: libxml2-python27
BuildRequires: python27-devel

%description -n python27-dmidecode
python-dmidecode is a python extension module that uses the
code-base of the 'dmidecode' utility, and presents the data
as python data structures or as XML data using libxml2.

This package is meant to be used with Python 2.7.

%prep
%setup -q
%patch1 -p1 -b .SIGILL-catcher
%patch2 -p1 -b .dmispec-remove
%patch3 -p1 -b .install-invalid

# Amazon patches
%patch10 -p1 -b .pymap-typo-fix

%build
rm -rf %{py26builddir}
mkdir -p %{py26builddir}
cp -a * %{py26builddir}
pushd %{py26builddir}
sed -i -e 's@share/python-dmidecode@share/python26-dmidecode@' src/{setup.py,config.h,setup-dbg.py}
make build
cd unit-tests
sed -i -e 's@python unit@%{__python26} unit@' Makefile
make
cd ..
popd

rm -rf %{py27builddir}
mkdir -p %{py27builddir}
cp -a * %{py27builddir}
pushd %{py27builddir}
sed -i -e 's@share/python-dmidecode@share/python27-dmidecode@' src/{setup.py,config.h,setup-dbg.py}
make build
cd unit-tests
sed -i -e 's@python unit@%{__python27} unit@' Makefile
make
cd ..
popd

%install
rm -rf $RPM_BUILD_ROOT

pushd %{py26builddir}
%{__python26} src/setup.py install --root $RPM_BUILD_ROOT --install-layout=amzn
popd

pushd %{py27builddir}
%{__python27} src/setup.py install --root $RPM_BUILD_ROOT --install-layout=amzn
popd

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{py26builddir}
rm -rf %{py27builddir}

%files -n python26-dmidecode
%defattr(-,root,root,-)
%doc README doc/README.upstream doc/LICENSE doc/AUTHORS doc/AUTHORS.upstream
%{python26_sitearch}/dmidecodemod.so
%{python26_sitearch}/dmidecode.py
%{python26_sitearch}/dmidecode.py[co]
%{python26_sitearch}/*.egg-info
%{_datadir}/python26-dmidecode/

%files -n python27-dmidecode
%defattr(-,root,root,-)
%doc README doc/README.upstream doc/LICENSE doc/AUTHORS doc/AUTHORS.upstream
%{python27_sitearch}/dmidecodemod.so
%{python27_sitearch}/dmidecode.py
%{python27_sitearch}/dmidecode.py[co]
%{python27_sitearch}/*.egg-info
%{_datadir}/python27-dmidecode/

%changelog
* Thu Apr 02 2015 Robert Fairburn <robert.fairburn@c2fo.com>
- Build for multiple pythons

* Thu Feb 19 2015 Ben Cressey <bcressey@amazon.com>
- build with system python

* Thu Jun 27 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/python-dmidecode-3.10.13-3.el6_4

* Thu Jun 20 2013 Ales Ledvinka <aledvink@redhat.com> - 3.10.13-3
- Attribute installed may appear as duplicate and cause invalid XML.
  Resolves: #975059

* Mon Jun 17 2013 Ales Ledvinka <aledvink@redhat.com> - 3.10.13-2
- Attribute dmispec may cause invalid XML on some hardware.
  Resolves: #975059

* Fri Aug 24 2012 Lee Trager <ltrager@amazon.com>
- Add patch which fixes spelling error

* Thu Dec 8 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/python-dmidecode-3.10.13-1.el6

* Thu Aug 18 2011 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/python-dmidecode-3.10.12-1.el6_1.1

* Wed Jun 29 2011 Roman Rakus <rrakus@redhat.com> - 3.10.13-1
- Update to 3.10.13 release
  Resolves: #621567, #627901, #667363
- Signal handler for SIGILL
  Resolves #646429

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/python-dmidecode-3.10.12-1.el6
- import source package RHEL6/python-dmidecode-3.10.11-1.el6

* Wed May 19 2010 Roman Rakus <rrakus@redhat.com> - 3.10.12-1
- Update to 3.10.12 release
  Resolves: #588387

* Fri May 7 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL5/python-dmidecode-3.10.8-4.el5
- added submodule prep for package python-dmidecode

* Fri Feb 26 2010 Roman Rakus <rrakus@redhat.com> - 3.10.11-2
- Upstream license patch (now GPLv2+)

* Tue Feb 16 2010 Nima Talebi <nima@it.net.au> - 3.10.11-1
- Update to new release

* Tue Jan 12 2010 Nima Talebi <nima@it.net.au> - 3.10.10-1
- Update to new release

* Thu Jan 07 2010 Nima Talebi <nima@it.net.au> - 3.10.9-1
- Update to new release

* Thu Dec 15 2009 Nima Talebi <nima@it.net.au> - 3.10.8-1
- New Upstream release.
- Big-endian and little-endian approved.
- Packaged unit-test to tarball.
- Rewritten unit-test to be able to run as non-root user, where it will not
  try to read /dev/mem.
- Added two dmidump data files to the unit-test.

* Thu Nov 26 2009 David Sommerseth <davids@redhat.com> - 3.10.7-3
- Fixed even more .spec file issues and removed explicit mentioning
  of /usr/share/python-dmidecode/pymap.xml

* Wed Nov 25 2009 David Sommerseth <davids@redhat.com> - 3.10.7-2
- Fixed some .spec file issues (proper Requires, use _datadir macro)

* Wed Sep 23 2009 Nima Talebi <nima@it.net.au> - 3.10.7-1
- Updated source0 to new 3.10.7 tar ball

* Wed Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-6
- Only build the python-dmidecode module, not everything

* Wed Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-5
- Added missing BuildRequres for libxml2-python

* Wed Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-4
- Added missing BuildRequres for python-devel

* Wed Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-3
- Added missing BuildRequres for libxml2-devel

* Wed Jul 13 2009 David Sommerseth <davids@redhat.com> - 3.10.6-2
- Updated release, to avoid build conflict

* Wed Jun 10 2009 David Sommerseth <davids@redhat.com> - 3.10.6-1
- Updated to work with the new XML based python-dmidecode

* Sat Mar  7 2009 Clark Williams <williams@redhat.com> - 2.10.3-1
- Initial build.
