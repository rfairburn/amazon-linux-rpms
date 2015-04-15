%define name ethtool
%define version 0.11
%define unmangled_version 0.11
%define release 2

%global srcname ethtool

Summary: Python module to interface with ethtool
Name: python27-%{name}
Version: %{version}
Release: c2fo.%{release}
Source0: %{srcname}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Vendor: Harald Hoyer, Arnaldo Carvalho de Melo, David Sommerseth <davids@redhat.com>
Url: http://fedoraproject.org/wiki/python-ethtool
Provides: python-ethtool


%description
UNKNOWN

%prep
%setup -n %{srcname}-%{unmangled_version}

%build
env CFLAGS="$RPM_OPT_FLAGS" %{__python27} setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Mon Apr 06 2015 Robert Fairburn <robert.fairburn@c2fo.com> 0.11-2
- Python27 for Amazon Linux
