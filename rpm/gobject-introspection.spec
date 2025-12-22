Name:       gobject-introspection
Summary:    Introspection system for GObject-based libraries
Version:    1.86.0
Release:    1
License:    GPLv2+, LGPLv2+, MIT
URL:        https://github.com/sailfishos/gobject-introspection
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0) >= 2.82.0
BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  meson

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package -n python-giscanner
Summary:    Python package for handling GObject introspection data
Requires:   %{name} = %{version}-%{release}

%description -n python-giscanner
This package contains a Python package for handling the introspection
data from Python.

%package devel
Summary:    Libraries and headers for gobject-introspection
Requires:   %{name} = %{version}-%{release}
Requires:   python-giscanner

%description devel
Libraries and headers for gobject-introspection.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%meson -Dcairo=disabled -Ddoctool=disabled -Dgtk_doc=false -Dpython=%{__python3}
%meson_build

%install
%meson_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files -n python-giscanner
%{_libdir}/gobject-introspection/giscanner

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{_datadir}/aclocal/introspection.m4
%{_datadir}/gobject-introspection-1.0
%doc %{_mandir}/man1/*.gz
