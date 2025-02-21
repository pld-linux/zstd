#
# Conditional build:
%bcond_without	asm		# disable assembler

Summary:	Zstandard - fast lossless compression algorithm
Summary(pl.UTF-8):	Zstandard - szybki, bezstratny algorytm kompresji
Name:		zstd
Version:	1.5.7
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/facebook/zstd/releases
Source0:	https://github.com/facebook/zstd/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	619a019adbbc4536e7fb93cdbb01af3e
URL:		https://github.com/facebook/zstd
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libstdc++-devel
BuildRequires:	lz4-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{arm}
%define		archcflags	-DMEM_FORCE_MEMORY_ACCESS=1
%endif

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression
ratio.

%description -l pl.UTF-8
Zstd (skrót od Zstandard) to szybki, bezstratny algorytm kompresji, do
zastosowwań przy kompresji w czasie rzeczywistym ze współczynnikiem
kompresji zbliżonym do biblioteki zlib.

%package devel
Summary:	Header files for Zstd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Zstd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Zstd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Zstd.

%package static
Summary:	Static Zstd library
Summary(pl.UTF-8):	Statyczna biblioteka Zstd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Zstd library.

%description static -l pl.UTF-8
Statyczna biblioteka Zstd.

%prep
%setup -q

%build
CC="%{__cc}" \
CXX="%{__cxx}" \
CFLAGS="%{rpmcflags} %{rpmcppflags} %{?archcflags}" \
CXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} allmost manual \
	V=1 \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	%{!?with_asm:ZSTD_NO_ASM=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	V=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libzstd.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libzstd.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libzstd.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE CHANGELOG README.md
%attr(755,root,root) %{_bindir}/unzstd
%attr(755,root,root) %{_bindir}/zstd
%attr(755,root,root) %{_bindir}/zstdcat
%attr(755,root,root) %{_bindir}/zstdgrep
%attr(755,root,root) %{_bindir}/zstdless
%attr(755,root,root) %{_bindir}/zstdmt
%attr(755,root,root) /%{_lib}/libzstd.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libzstd.so.1
%{_mandir}/man1/unzstd.1*
%{_mandir}/man1/zstd.1*
%{_mandir}/man1/zstdcat.1*
%{_mandir}/man1/zstdgrep.1*
%{_mandir}/man1/zstdless.1*

%files devel
%defattr(644,root,root,755)
%doc doc/{zstd_compression_format.md,zstd_manual.html,images}
%attr(755,root,root) %{_libdir}/libzstd.so
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_pkgconfigdir}/libzstd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libzstd.a
