%define _buildid .100

%global py26nvr python26-crypto-%{version}-%{release}
%global py26builddir %{_builddir}/%{py26nvr}
%global py26doc ../%{py26nvr}

%global py27nvr python27-crypto-%{version}-%{release}
%global py27builddir %{_builddir}/%{py27nvr}
%global py27doc ../%{py27nvr}

%bcond_without tests # with

%global upstream_name pycrypto

Name: python-crypto
Version: 2.6.1
Release: 1%{?_buildid}.c2fo
Summary: Cryptography library for Python
Group: Development/Libraries
License: Public Domain and Python
URL: http://www.pycrypto.org/
Source0:	http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
Patch0:		python-crypto-2.4-optflags.patch
Patch1:		python-crypto-2.4-fix-pubkey-size-divisions.patch
Patch2:		python-crypto-2.6-gmp6.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python26
BuildRequires: python27

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

%package -n python26-crypto
Summary: Cryptography library for Python
BuildRequires:	python26-devel
BuildRequires:  gmp6 >= 6.0
BuildRequires:	python26-tools
Provides: python-crypto = %{version}-%{release}
Provides: pycrypto = %{version}-%{release}
Provides: pycrypto%{?_isa} = %{version}-%{release}
Provides: python-crypto%{?_isa} = %{version}-%{release}
Obsoletes: python-crypto <= 2.6.1-1.7.amzn1
Obsoletes: python-crypto <= 2.6.1-1.99.gmp6

%description -n python26-crypto
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

This package is meant to be used with Python 2.6.

%package -n python27-crypto
Summary: Cryptography library for Python
BuildRequires:	python27-devel
BuildRequires:  gmp6 >= 6.0
BuildRequires:	python27-tools

%description -n python27-crypto
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

This package is meant to be used with Python 2.7.

%prep
%setup -q -n %{upstream_name}-%{version}
# Use distribution compiler flags rather than upstream's
%patch0 -p1

# Fix divisions within benchmarking suite:
%patch1 -p1

# Use gmp6
%patch2 -p1

%build
export ac_cv_func_malloc_0_nonnull="yes"
rm -rf %{py26builddir}
mkdir -p %{py26builddir}
cp -a * %{py26builddir}
pushd %{py26builddir}
CFLAGS="$RPM_OPT_FLAGS -I/opt/gmp6/include" LDFLAGS="-L/opt/gmp6/lib" %{__python26} setup.py build 
popd

rm -rf %{py27builddir}
mkdir -p %{py27builddir}
cp -a * %{py27builddir}
pushd %{py27builddir}
CFLAGS="$RPM_OPT_FLAGS -I/opt/gmp6/include" LDFLAGS="-L/opt/gmp6/lib" %{__python27} setup.py build 
popd

%install
rm -rf %{buildroot}

pushd %{py26builddir}
%{__python26} setup.py install -O1 --skip-build --root %{buildroot} --install-layout=amzn
popd
find %{buildroot}%{python26_sitearch} -name '*.so' -exec chmod -c g-w {} \;

pushd %{py27builddir}
%{__python27} setup.py install -O1 --skip-build --root %{buildroot} --install-layout=amzn
popd
find %{buildroot}%{python27_sitearch} -name '*.so' -exec chmod -c g-w {} \;

%check
export ac_cv_func_malloc_0_nonnull="yes"
%if %{with tests}
pushd %{py26builddir}
CFLAGS="$RPM_OPT_FLAGS -I/opt/gmp6/include" LDFLAGS="-L/opt/gmp6/lib" %{__python26} setup.py test

PYTHONPATH=%{buildroot}%{python26_sitearch} %{__python26} pct-speedtest.py

popd
pushd %{py27builddir}
CFLAGS="$RPM_OPT_FLAGS -I/opt/gmp6/include" LDFLAGS="-L/opt/gmp6/lib" %{__python27} setup.py test

PYTHONPATH=%{buildroot}%{python27_sitearch} %{__python27} pct-speedtest.py

popd
%endif

%clean
rm -rf %{buildroot}
rm -rf %{py26builddir}
rm -rf %{py27builddir}

%files -n python26-crypto
%doc README TODO ACKS ChangeLog %{py26doc}/LEGAL/ COPYRIGHT %{py26doc}/Doc/
%{python26_sitearch}/*

%files -n python27-crypto
%doc README TODO ACKS ChangeLog %{py27doc}/LEGAL/ COPYRIGHT %{py27doc}/Doc/
%{python27_sitearch}/*

%changelog
* Tue Mar 31 2015 Robert Fairburn <robert.fairburn@c2fo.com>
- Build against gmp6

* Wed Feb 4 2015 Jamie Anderson <jamieand@amazon.com>
- Build for multiple pythons

* Mon Oct 28 2013 Lee Trager <ltrager@amazon.com>
- import source package F18/python-crypto-2.6.1-1.fc18

* Fri Oct 18 2013 Paul Howarth <paul@city-fan.org> - 2.6.1-1
- Update to 2.6.1
  - Fix PRNG not correctly reseeded in some situations (CVE-2013-1445)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Lee Trager <ltrager@amazon.com>
- import source package F18/python-crypto-2.6-4.fc18

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 2.6-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.6-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 7 2012 Cristian Gafton <gafton@amazon.com>
- import source package F16/python-crypto-2.3-6.fc16
- import source package F16/python-crypto-2.3-5.fc16
- import source package F16/python-crypto-2.3-4.fc15
- import source package F16/python-crypto-2.3-2.fc14.1
- import source package F16/python-crypto-2.1.0-2.fc14
- import source package F16/python-crypto-2.0.1-20

* Thu May 24 2012 Paul Howarth <paul@city-fan.org> - 2.6-1
- Update to 2.6
  - Fix insecure ElGamal key generation (launchpad bug #985164, CVE-2012-2417)
  - Huge documentation cleanup
  - Added more tests, including test vectors from NIST 800-38A
  - Remove broken MODE_PGP, which never actually worked properly
  - A new mode, MODE_OPENPGP, has been added for people wishing to write
    OpenPGP implementations (see also launchpad bug #996814)
  - Fix: getPrime with invalid input causes Python to abort with fatal error
    (launchpad bug #988431)
  - Fix: Segfaults within error-handling paths (launchpad bug #934294)
  - Fix: Block ciphers allow empty string as IV (launchpad bug #997464)
  - Fix DevURandomRNG to work with Python3's new I/O stack
  - Remove automagic dependencies on libgmp and libmpir; let the caller
    disable them using args
  - Many other minor bug fixes and improvements
- Drop upstream patches

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.5-2
- Add upstream fixes for issues found by Dave Malcolm's experimental static
  analysis tool (#790584)

* Mon Jan 16 2012 Paul Howarth <paul@city-fan.org> - 2.5-1
- Update to 2.5
  - Added PKCS#1 encryption schemes (v1.5 and OAEP); we now have a decent,
    easy-to-use non-textbook RSA implementation
  - Added PKCS#1 signature schemes (v1.5 and PSS); v1.5 required some
    extensive changes to Hash modules to contain the algorithm-specific ASN.1
    OID, and to that end we now always have a (thin) Python module to hide the
    one in pure C
  - Added 2 standard Key Derivation Functions (PBKDF1 and PBKDF2)
  - Added export/import of RSA keys in OpenSSH and PKCS#8 formats
  - Added password-protected export/import of RSA keys (one old method for
    PKCS#8 PEM only)
  - Added ability to generate RSA key pairs with configurable public
    exponent e
  - Added ability to construct an RSA key pair even if only the private
    exponent d is known, and not p and q
  - Added SHA-2 C source code (fully from Lorenz Quack)
  - Unit tests for all the above
  - Updates to documentation (both inline and in Doc/pycrypt.rst)
  - Minor bug fixes (setup.py and tests)
- Upstream no longer ships python-3-changes.txt

* Sat Jan  7 2012 Paul Howarth <paul@city-fan.org> - 2.4.1-2
- Rebuild with gcc 4.7

* Mon Nov  7 2011 Paul Howarth <paul@city-fan.org> - 2.4.1-1
- Update to 2.4.1
  - Fix "error: Setup script exited with error: src/config.h: No such file or
    directory" when installing via easy_install

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.4-2.1
- Rebuild with new gmp without compat lib

* Tue Oct 25 2011 Paul Howarth <paul@city-fan.org> - 2.4-2
- Add python3-crypto subpackage (based on patch from Dave Malcolm - #748529)

* Mon Oct 24 2011 Paul Howarth <paul@city-fan.org> - 2.4-1
- Update to 2.4
  - Python 3 support! PyCrypto now supports every version of Python from 2.1
    through to 3.2
  - Timing-attack countermeasures in _fastmath: when built against libgmp
    version 5 or later, we use mpz_powm_sec instead of mpz_powm, which should
    prevent the timing attack described by Geremy Condra at PyCon 2011
  - New hash modules (for Python ≥ 2.5 only): SHA224, SHA384 and SHA512
  - Configuration using GNU autoconf, which should help fix a bunch of build
    issues
  - Support using MPIR as an alternative to GMP
  - Improve the test command in setup.py, by allowing tests to be performed on
    a single sub-package or module only
  - Fix double-decref of "counter" when Cipher object initialization fails
  - Apply patches from Debian's python-crypto 2.3-3 package:
    - fix-RSA-generate-exception.patch
    - epydoc-exclude-introspect.patch
    - no-usr-local.patch
  - Fix launchpad bug #702835: "Import key code is not compatible with GMP
    library"
  - More tests, better documentation, various bugfixes
- Update patch for imposing our own compiler optimization flags
- Drop lib64 patch, no longer needed
- No longer need to fix up permissions and remove shellbangs

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 2.3-5.1
- Rebuild with new gmp

* Wed May 11 2011 Paul Howarth <paul@city-fan.org> - 2.3-5
- Upstream rolled new tarball with top-level directory restored
- Nobody else likes macros for commands

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 2 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/python-crypto-2.0.1-22.el6

* Wed Sep 29 2010 jkeating - 2.3-3
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 David Malcolm <dmalcolm@redhat.com> - 2.3-2
- Add "-fno-strict-aliasing" to compilation flags

* Fri Aug 27 2010 Paul Howarth <paul@city-fan.org> - 2.3-1
- Update to 2.3
  - Fix NameError when attempting to use deprecated getRandomNumber() function
  - _slowmath: Compute RSA u parameter when it's not given to RSA.construct;
    this makes _slowmath behave the same as _fastmath in this regard
  - Make RSA.generate raise a more user-friendly exception message when the
    user tries to generate a bogus-length key
- Add -c option to %%setup because upstream tarball has dropped the top-level
  directory
- Run benchmark as part of %%check if we have python 2.4 or later
- BR: python2-devel rather than just python-devel
- Add patch to make sure we can find libgmp in 64-bit multilib environments

* Tue Aug  3 2010 Paul Howarth <paul@city-fan.org> - 2.2-1
- Update to 2.2
  - Deprecated Crypto.Util.number.getRandomNumber()
  - It's been replaced by getRandomNBitInteger and getRandomInteger
  - Better isPrime() and getPrime() implementations
  - getStrongPrime() implementation for generating RSA primes
  - Support for importing and exporting RSA keys in DER and PEM format
  - Fix PyCrypto when floor division (python -Qnew) is enabled
  - When building using gcc, use -std=c99 for compilation
- Update optflags patch

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 9 2010 Cristian Gafton <gafton@amazon.com>
- import source package RHEL6/python-crypto-2.0.1-20.el6
- import source package RHEL6/python-crypto-2.0.1-19.1
- setup complete for package python-crypto

* Tue Feb 16 2010 Paul Howarth <paul@city-fan.org> - 2.1.0-1
- Update to 2.1.0 (see ChangeLog for details)
- Remove patches (no longer needed)
- Use new upstream URLs
- Upstream has replaced LICENSE with LEGAL/ and COPYRIGHT
- Clarify that license is mostly Public Domain, partly Python
- Add %%check section and run the test suite in it
- Remove upstream's fiddling with compiler optimization flags so we get
  usable debuginfo
- Filter out unwanted provides for python shared objects
- Tidy up egg-info handling
- Simplify %%files list
- Pacify rpmlint as much as is reasonable
- Add dist tag

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-17
- Use patches in upstream git to fix #484473

* Fri Feb 13 2009 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-16.1
- add patch to fix #485298 / CVE-2009-0544

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15.1
- Oops, actually apply the patch
- Modify patch so modules remain compatible with PEP 247

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15
- Add patch to hashlib instead of deprecated md5 and sha modules (#484473)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.1-14.1
- Rebuild for Python 2.6

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-13
- provide pycrypto

* Sat Feb 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-12
- rebuilt

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-11
- egg-info file in python_sitearch and not in python_sitelib

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-10
- ship egg-file

* Tue Aug 21 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-9
- Remove the old and outdated python-abi hack

* Fri Aug 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- Update License field due to the "Licensing guidelines changes"

* Mon Jun 04 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.1-8
- Fix libdir handling so it works on more arches than x86_64

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-7
- Fix typo

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-6
- Remove dist
- rebuild, because the older version was much bigger, as it was build when
  distutils was doing static links of libpython

* Sat Dec 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-5
- Rebuild for python 2.5

* Thu Sep 07 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-4
- Don't ghost pyo files (#205408)

* Tue Aug 29 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-3
- Rebuild for Fedora Extras 6

* Mon Feb 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-2
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0.1-1
- Update to 2.0.1
- Use Dist
- Drop python-crypto-64bit-unclean.patch, similar patch was applied 
  upstream

* Thu May 05 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-4
- add python-crypto-64bit-unclean.patch (#156173)

* Mon Mar 21 2005 Seth Vidal <skvidal at phy.duke.edu> - 0:2.0-3
- iterate release for build on python 2.4 based systems

* Sat Dec 18 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-2
- Fix build on x86_64: use python_sitearch for files and patch source
  to find gmp

* Thu Aug 26 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-0.fdr.1
- Update to 2.00

* Fri Aug 13 2004 Ville Skytta <ville.skytta at iki.fi> - 0:1.9-0.fdr.6.a6
- Don't use get_python_version(), it's available in Python >= 2.3 only.

* Thu Aug 12 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.5.a6
- Own dir python_sitearch/Crypto/

* Wed Aug 11 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.4.a6
- Match python spec template more

* Sat Jul 17 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.3.a6
- Own _libdir/python/site-packages/Crypto/

* Wed Mar 24 2004 Panu Matilainen <pmatilai@welho.com> 0.3.2-0.fdr.2.a6
- generate .pyo files during install
- require exact version of python used to build the package
- include more docs + demos
- fix dependency on /usr/local/bin/python
- use fedora.us style buildroot
- buildrequires gmp-devel
- use description from README

* Sun Jan 11 2004 Ryan Boder <icanoop@bitwiser.org>  0.3.2-0.fdr.1.a6
- Initial build.
