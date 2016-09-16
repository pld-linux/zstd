Summary:	Zstandard - fast lossless compression algorithm
Summary(pl.UTF-8):	Zstandard - szybki, bezstratny algorytm kompresji
Name:		zstd
Version:	1.0.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/Cyan4973/zstd/releases
Source0:	https://github.com/Cyan4973/zstd/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ca9a01cd81265ac235acdf611a25122e
Patch0:		%{name}-noquiet.patch
Patch1:		%{name}-no32.patch
Patch2:		%{name}-noclean.patch
URL:		https://github.com/Cyan4973/zstd
BuildRequires:	gcc >= 5:3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md images
%attr(755,root,root) %{_bindir}/unzstd
%attr(755,root,root) %{_bindir}/zstd
%attr(755,root,root) %{_bindir}/zstdcat
%attr(755,root,root) %{_libdir}/libzstd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzstd.so.1
%{_mandir}/man1/unzstd.1*
%{_mandir}/man1/zstd.1*
%{_mandir}/man1/zstdcat.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzstd.so
%{_includedir}/zbuff.h
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_pkgconfigdir}/libzstd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libzstd.a
