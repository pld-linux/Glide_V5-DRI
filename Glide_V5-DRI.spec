#
# Conditional build:
%bcond_without	glide3_sdk	# don't build glide3x SDK here
#
%define snapdate 20010309
%define	rel	15
Summary:	Glide runtime for 3Dfx Voodoo4 and Voodoo5 boards
Summary(ko.UTF-8):	3Dfx 부두 벤쉬/3 비디오카드용 Glide 런타임 라이브러리
Summary(pl.UTF-8):	Biblioteki Glide dla kart 3Dfx Voodoo4 i Voodoo5
Name:		Glide_V5-DRI
Version:	3.10.0
Release:	0.%{snapdate}.%{rel}
Epoch:		1
License:	3dfx Glide General Public License, 3Dfx Interactive Inc.
Group:		X11/Libraries
Source0:	cvs://anonymous@cvs.glide.sourceforge.net:/cvsroot/glide/glide3x-%{snapdate}.tar.gz
# Source0-md5:	42a8e093221b2360ec96191ae0e13ce0
Patch0:		glide-ia64.patch
Patch1:		glide-ac-workaround.patch
Patch2:		glide-h3.patch
Patch3:		glide-h5.patch
Patch4:		glide-am16.patch
Patch5:		glide-gcc33.patch
Patch6:		glide-ioctl.patch
Patch7:		glide-morearchs.patch
Patch8:		glide-gcc4.patch
Patch9:		glide-no_redefine_macro.patch
Patch10:	glide-format.patch
Patch11:	glide-include.patch
URL:		http://glide.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86dga-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Provides:	Glide3-DRI
Obsoletes:	Glide_V3-DRI
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows the user to use a 3dfx Interactive Voodoo4 or
Voodoo5 card under Linux with DRI support. The source support DRI or
non-DRI versions of Glide.

%description -l pl.UTF-8
Ta biblioteka pozwala użytkownikowi na używanie kart 3dfx Interactive
Voodoo4 lub Voodoo5 pod Linuksem z DRI. Ta wersja zawiera wsparcie dla
wersji Glide z DRI i bez DRI.

%package devel
Summary:	Development headers for Glide 3.x
Summary(pl.UTF-8):	Pliki nagłówkowe Glide 3.x
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	Glide3x_SDK >= %{epoch}:%{version}
Provides:	Glide3-DRI-devel
Obsoletes:	Glide_V3-DRI-devel

%description devel
This package includes the headers files, documentation, and test files
necessary for developing applications that use the 3Dfx Interactive
Voodoo4 or Voodoo5 cards.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe, dokumentacje, oraz pliki tekstowe
wymagane przez aplikacje deweloperskie, które używają kart 3Dfx
Interactive Voodoo4 lub Voodoo5.

%package static
Summary:	Static Glide 3.x library
Summary(pl.UTF-8):	Statyczne biblioteki Glide 3.x
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	Glide3-DRI-static
Obsoletes:	Glide_V3-DRI-static

%description static
This package includes the static Glide3 library for Voodoo4 or
Voodoo5.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki Glide3 dla Voodoo4 lub
Voodoo5.

%package -n Glide3x_SDK
Summary:	Development libraries for Glide 3.x
Summary(pl.UTF-8):	Część Glide 3.x przeznaczona dla programistów
Group:		Development/Libraries
Conflicts:	Glide_SDK

%description -n Glide3x_SDK
This package includes the header files and test files necessary for
developing applications that use any of the 3D accelerators in the
3Dfx Interactive Voodoo line utilizing Glide 3.x interface.

%description -n Glide3x_SDK -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i pliki testowe potrzebne do
tworzenia aplikacji korzystających z akceleratorów 3D serii 3Dfx
Interactive Voodoo przy użyciu interfejsu Glide 3.x.

%prep
%setup -q -n glide3x-%{snapdate}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p2
%patch -P9 -p1
%patch -P10 -p1
%patch -P11 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake} -i
%configure \
	--enable-fx-dri-build \
	--enable-fx-glide-hw=h5 \
	--enable-fx-debug=no \
%ifarch i586 i686 athlon
	--enable-amd3d
%endif

%{__make} -j1 -f makefile.autoconf all \
	GLIDE_DEBUG_GCFLAGS="%{rpmcflags} -fno-expensive-optimizations %{!?debug:-fomit-frame-pointer -ffast-math}" \
	GLIDE_DEBUG_GDEFS="%{!?debug:-DBIG_OPT} %{?debug:-DGDBG_INFO_ON -DGLIDE_DEBUG}" \
	LINK_LIBS="-lX11 -lXext -lXxf86dga -lXxf86vm -lm" \
	PREPROCESSOR='cpp -I. -x assembler-with-cpp'

%install
rm -rf $RPM_BUILD_ROOT

# something is recompiled - use GCFLAGS too
%{__make} -f makefile.autoconf install \
	GLIDE_DEBUG_GCFLAGS="%{rpmcflags} -fno-expensive-optimizations %{!?debug:-fomit-frame-pointer -ffast-math}" \
	GLIDE_DEBUG_GDEFS="%{!?debug:-DBIG_OPT} %{?debug:-DGDBG_INFO_ON -DGLIDE_DEBUG}" \
	LINK_LIBS="-lX11 -lXext -lXxf86dga -lXxf86vm -lm" \
	DESTDIR=$RPM_BUILD_ROOT

# used by tdfx_dri.so from XFree86
ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3-v5.so
# used by ???
ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3x_V5.so
# used by dlopen in X driver
ln -sf libglide3.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglide3x.so

%if %{with glide3_sdk}
# Install the examples and their source, no binaries
install -d $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
install h5/glide3/tests/makefile.linux $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests/makefile
install h5/glide3/tests/*.3df $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
install h5/glide3/tests/test??.c $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
install h5/glide3/tests/tldata.inc $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
install h5/glide3/tests/tlib.[ch] $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests
gzip -9nf $RPM_BUILD_ROOT%{_examplesdir}/glide3x-%{version}/tests/*.3df
%else
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/glide3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc glide_license.txt
%attr(755,root,root) %{_libdir}/libglide3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglide3.so.3
%attr(755,root,root) %{_libdir}/libglide3-v5.so
%attr(755,root,root) %{_libdir}/libglide3x.so
%attr(755,root,root) %{_libdir}/libglide3x_V5.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglide3.so
%{_libdir}/libglide3.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libglide3.a

%if %{with glide3_sdk}
%files -n Glide3x_SDK
%defattr(644,root,root,755)
%{_includedir}/glide3
%{_examplesdir}/glide3x-%{version}
%endif
