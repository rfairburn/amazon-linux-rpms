#!/bin/bash
# Get SRPM for gmp
sudo get_reference_source -p gmp
# Build dependencies so we have them to compile (if needed)
sudo yum -y install rpm-build
sudo yum-builddep /usr/src/srpm/debug/gmp-*.amzn1.src.rpm
# Obtain source to build and build it:
wget https://ftp.gnu.org/gnu/gmp/gmp-6.0.0a.tar.bz2
tar -xjvf gmp-6.0.0a.tar.bz2
cd gmp-6.0.0
./configure --prefix=/opt/gmp6
mkdir /tmp/gmp
# Install into temporary directory for packaging
sudo make DESTDIR=/tmp/gmp install
# You do test your binaries, right?
make test
# Add ld.so.conf file for ldconfig to utilize to the 'package'
mkdir -p /tmp/gmp/etc/ld.so.conf.d
echo /opt/gmp6/lib > /tmp/gmp/etc/ld.so.conf.d/gmp6.conf
# Build the FPM package and say that it provides libgmp.so.10()(64bit) (Required for python-crypto)
echo <<EOF > run-ldconfig.sh
#!/bin/sh
/sbin/ldconfig
EOF
/usr/local/bin/fpm -s dir -t rpm -C /tmp/gmp --name gmp6 --version 6.0.0a --iteration 2 --description "libgpm 6" --provides 'libgmp.so.10()(64bit)' --after-install run-ldconfig.sh .
# Make sure to sign packages
sudo rpm --resign gmp6*.rpm
