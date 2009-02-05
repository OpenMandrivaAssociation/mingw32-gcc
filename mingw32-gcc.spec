%define __os_install_post /usr/lib/rpm/brp-compress %{nil}
%define Werror_cflags %nil

Name:           mingw32-gcc
Version:        4.3.2
Release:        %mkrel 1
Summary:        MinGW Windows cross-compiler (GCC) for C

License:        GPLv2+
Group:          Development/Other
URL:            http://www.mingw.org/
Source0:        ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-core-%{version}.tar.bz2
Source1:        ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-g++-%{version}.tar.bz2
Patch1:         %{name}-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  texinfo
BuildRequires:  mingw32-filesystem >= 39-3
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-runtime
BuildRequires:  mingw32-w32api
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  libgomp-devel
BuildRequires:  glibc-devel

# NB: Explicit mingw32-filesystem dependency is REQUIRED here.
Requires:       mingw32-filesystem >= 39-3
Requires:       mingw32-binutils
Requires:       mingw32-runtime
Requires:       mingw32-w32api
Requires:       mingw32-cpp


%description
MinGW Windows cross-compiler (GCC) for C


%package -n mingw32-cpp
Summary: MinGW Windows cross-C Preprocessor
Group: Development/Other

%description -n mingw32-cpp
MinGW Windows cross-C Preprocessor


%package c++
Summary: MinGW Windows cross-compiler for C++
Group: Development/Other

%description c++
MinGW Windows cross-compiler for C++


%prep
%setup -q -c
%setup -q -D -T -a1
%patch1 -p1


%build
cd gcc-%{version}

mkdir -p build
cd build

languages="c,c++"

CC="%{__cc} ${RPM_OPT_FLAGS}" \
../configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --libexecdir=%{_prefix}/lib \
  --mandir=%{_mandir} \
  --infodir=%{_infodir} \
  --datadir=%{_datadir} \
  --build=%_build --host=%_host \
  --target=%{_mingw32_target} \
  --with-gnu-as --with-gnu-ld --verbose \
  --without-newlib \
  --disable-multilib \
  --with-system-zlib \
  --disable-nls --without-included-gettext \
  --disable-win32-registry \
  --enable-version-specific-runtime-libs \
  --with-sysroot=%{_mingw32_sysroot} \
  --enable-languages="$languages" $optargs

%make all


%install
rm -rf $RPM_BUILD_ROOT

cd gcc-%{version}
cd build
make DESTDIR=$RPM_BUILD_ROOT install

# These files conflict with existing installed files.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty*
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/*

mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ..%{_prefix}/bin/i586-pc-mingw32-cpp \
  $RPM_BUILD_ROOT/lib/i586-pc-mingw32-cpp

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/i586-pc-mingw32-gcc
%{_bindir}/i586-pc-mingw32-gcc-%{version}
%{_bindir}/i586-pc-mingw32-gccbug
%{_bindir}/i586-pc-mingw32-gcov
%{_prefix}/i586-pc-mingw32/lib/libiberty.a
%dir %{_libdir}/gcc/i586-pc-mingw32
%dir %{_libdir}/gcc/i586-pc-mingw32/%{version}
%{_libdir}/gcc/i586-pc-mingw32/%{version}/crtbegin.o
%{_libdir}/gcc/i586-pc-mingw32/%{version}/crtend.o
%{_libdir}/gcc/i586-pc-mingw32/%{version}/crtfastmath.o
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libgcc.a
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libgcov.a
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libssp.a
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libssp.la
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libssp_nonshared.a
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libssp_nonshared.la
%dir %{_libdir}/gcc/i586-pc-mingw32/%{version}/include
%dir %{_libdir}/gcc/i586-pc-mingw32/%{version}/include-fixed
%dir %{_libdir}/gcc/i586-pc-mingw32/%{version}/include/ssp
%{_libdir}/gcc/i586-pc-mingw32/%{version}/include-fixed/README
%{_libdir}/gcc/i586-pc-mingw32/%{version}/include-fixed/*.h
%{_libdir}/gcc/i586-pc-mingw32/%{version}/include/*.h
%{_libdir}/gcc/i586-pc-mingw32/%{version}/include/ssp/*.h
%dir %{_libdir}/gcc/i586-pc-mingw32/%{version}/install-tools
%{_libdir}/gcc/i586-pc-mingw32/%{version}/install-tools/*
%dir %{_libexecdir}/gcc/i586-pc-mingw32/%{version}/install-tools
%{_libexecdir}/gcc/i586-pc-mingw32/%{version}/install-tools/*
%{_mandir}/man1/i586-pc-mingw32-gcc.1*
%{_mandir}/man1/i586-pc-mingw32-gcov.1*


%files -n mingw32-cpp
%defattr(-,root,root)
/lib/i586-pc-mingw32-cpp
%{_bindir}/i586-pc-mingw32-cpp
%{_mandir}/man1/i586-pc-mingw32-cpp.1*
%dir %{_libdir}/gcc/i586-pc-mingw32
%dir %{_libdir}/gcc/i586-pc-mingw32/%{version}
%{_libexecdir}/gcc/i586-pc-mingw32/%{version}/cc1


%files c++
%defattr(-,root,root)
%{_bindir}/i586-pc-mingw32-g++
%{_bindir}/i586-pc-mingw32-c++
%{_mandir}/man1/i586-pc-mingw32-g++.1*
%{_libdir}/gcc/i586-pc-mingw32/%{version}/include/c++/
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libstdc++.a
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libstdc++.la
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libsupc++.a
%{_libdir}/gcc/i586-pc-mingw32/%{version}/libsupc++.la
%{_libexecdir}/gcc/i586-pc-mingw32/%{version}/cc1plus
%{_libexecdir}/gcc/i586-pc-mingw32/%{version}/collect2
