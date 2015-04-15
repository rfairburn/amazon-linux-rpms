%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")}
%endif

%global srcname nzjrs-python-gudev-5fac65a

Summary:        Python (PyGObject) bindings to the GUDev library
Name:           python27-gudev
URL:            http://github.com/nzjrs/python-gudev
# Tar.gz can be downloaded from
# http://github.com/nzjrs/python-gudev/tarball/%{version}
Source0:        %{srcname}.tar.gz

# patch from upstream
Patch0:         0001-Fix-crash-when-freeing-result-of-g_udev_client_query.patch
Version:        147.1
Release:        5.c2fo.1
Group:          Development/Libraries
License:        LGPLv3+
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       libgudev1 >= 147
Requires:       pygobject2
BuildRequires:  python-devel
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  libgudev1-devel >= 147
BuildRequires:  pygobject2-devel
Obsoletes:      python-gudev <= 147.1-4.el6_0.1
Provides:       python-gudev

%description
python-gudev is a Python (PyGObject) binding to the GUDev UDEV library.

%prep
%setup -q -n %{srcname}

# override fuzzy to 1 so that patch can be applied
%patch0 -F1 -p1

%build
sh autogen.sh --prefix %{_prefix} --disable-static
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name gudev.la | xargs rm

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README NEWS
%doc test.py
%{python_sitearch}/*
%{_datadir}/*

%changelog
* Mon Apr 06 2015 Robert Fairburn <robert.fairburn@c2fo.com> - 147.1-5.1
- Python27 for Amazon Linux

* Mon Sep 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 147.1-4.1
- Added upstream patch
- Resolves: rhbz#637084
- Related: rhbz#631789

* Mon Mar 15 2010 Miroslav Suchý <msuchy@redhat.com> 147.1-4
- 572609 - do not strip all debuginfo

* Mon Feb  8 2010 Miroslav Suchý <msuchy@redhat.com> 147.1-3
- initial release
