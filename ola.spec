Name:           ola
Version:        0.9.7
Release:        1
Summary:        Open Lighting Architecture
Group:          Applications/Multimedia
License:        GPLv2 and LGPLv2
URL:            https://github.com/OpenLightingProject/ola
Source:         https://github.com/OpenLightingProject/ola/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_buildrootdir}/%{name}-%{version}-%{release}-root
BuildRequires:  libmicrohttpd-devel,cppunit-devel,protobuf-devel,protobuf-compiler,protobuf-python,libftdi-devel,openslp-devel,uuid-devel,libtool,bison,flex,pkgconfig,gcc,gcc-c++,python-devel,avahi-compat-libdns_sd-devel,avahi-devel

%description
The Open Lighting Architecture is a framework for lighting control information.
It supports a range of protocols and over a dozen USB devices. It can run as a
standalone service, which is useful for converting signals between protocols,
or alternatively using the OLA API, it can be used as the back-end for lighting
control software. OLA runs on many different platforms including ARM, which
makes it a perfect fit for low cost Ethernet to DMX gateways.

%package devel
Requires:      ola = %{version}-%{release}, protobuf-devel
Group:         Development/Libraries
Summary:       C/C++ Development files for OLA

%description devel
The OLA C/C++ library

%package -n python2-%{name}
Requires:      ola = %{version}-%{release}, protobuf-python, python(abi) = 2.7
Group:         Development/Libraries
Summary:       Python Development files for OLA
BuildArch:     noarch
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
The OLA python library

%package rdm-tests
Requires:      ola = %{version}-%{release}, python2-%{name}
Group:         Development/Libraries
Summary:       RDM test suite using OLA and python

%description rdm-tests
The rdm test suite for OLA

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf -i
%configure --enable-rdm-tests --enable-shared --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i "s|\$(LN_S) -f \$(bindir)\/|\$(LN_S) -f |g" Makefile
make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH="%buildroot/usr/lib:%buildroot/usr/lib64"
make check %{?_smp_mflags}
find %buildroot -name "*pyc" -delete
find %buildroot -name "*pyo" -delete

%install
rm -rf %buildroot
%make_install
find %buildroot -name "*\.pyc" -delete
find %buildroot -name "*\.pyo" -delete

%clean
rm -rf %buildroot


%files
%{_bindir}/ola*
%{_bindir}/rdmpro_sniffer
%{_bindir}/usbpro_firmware
%{_datadir}/olad/**
%{_datadir}/ola/pids/**
%{_libdir}/libola*\.so\.*
%{_mandir}/man1/**

%files devel
%{_includedir}/ola**
%{_libdir}/libola*\.so
%{_libdir}/pkgconfig/*

%files -n python2-%{name}
%{python2_sitelib}/ola/*\.py
%{python2_sitelib}/ola/rpc/*\.py

%files rdm-tests
%{_bindir}/rdm_model_collector.py
%{_bindir}/rdm_responder_test.py
%{_bindir}/rdm_test_server.py
%{_datadir}/ola/rdm-server/**
%{python2_sitelib}/ola/testing/*\.py
%{python2_sitelib}/ola/testing/rdm/*\.py

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Sat Sep 19 2015 Dave Olsthoorn - 0.9.7-1
- update to 0.9.7
- OLA now requires libusb
* Thu Aug 27 2009 Kevin Deldycke <kevin@deldycke.com> 0.3.1.trunk.20090827-1mdv2009.1
- Rename all project from lla to OLA
- Upgrade to the latest OLA 0.3.1 from the master branch of the git repository
- OLA now requires libmicrohttpd, libcppunit, protobuf and libctemplate
- Disable the --no-undefined option and make all undefined symbols weakly bound
- Add check step
- Rebuild RPM for Mandriva 2009.1
* Mon May 12 2008 Kevin Deldycke <kev@coolcavemen.com> 0.2.3.200710210908-1mdv2008.1
- Ported from Fedora Core 8 ( http://rpms.netmindz.net/FC8/SRPMS.netmindz/lla-0.2.3.200710210908-1.fc8.src.rpm ) to Mandriva 2008.1
* Sun Apr 29 2007 Will Tatam <will@netmindz.net> 0.1.3-1
- Fist Build

