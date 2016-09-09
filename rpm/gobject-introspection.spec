Name:       gobject-introspection
Summary:    Introspection system for GObject-based libraries
Version:    1.48.0
Release:    1
Group:      Development/Libraries
License:    GPLv2+, LGPLv2+, MIT
URL:        http://live.gnome.org/GObjectIntrospection
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0) >= 1.48.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  python-devel >= 2.5
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  libtool

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package -n python-giscanner
Summary:    Python package for handling GObject introspection data
Group:      Development/Languages
Requires:   %{name} = %{version}-%{release}

%description -n python-giscanner
This package contains a Python package for handling the introspection
data from Python.

%package devel
Summary:    Libraries and headers for gobject-introspection
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   python-giscanner

%description devel
Libraries and headers for gobject-introspection.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
%autogen --disable-static
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

# Die libtool, die.
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-{compiler,generate}
# Mistake in upstream automake
rm -f $RPM_BUILD_ROOT/%{_bindir}/barapp

# Move the python modules to the correct location
mkdir -p $RPM_BUILD_ROOT/%{python_sitearch}
mv $RPM_BUILD_ROOT/%{_libdir}/gobject-introspection/giscanner $RPM_BUILD_ROOT/%{python_sitearch}/

# Trash html documentation
rm -rf $RPM_BUILD_ROOT/%{_datarootdir}/gtk-doc/html

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files -n python-giscanner
%defattr(-,root,root,-)
%{python_sitearch}/giscanner

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{_datadir}/aclocal/introspection.m4
%{_datadir}/gobject-introspection-1.0
%doc %{_mandir}/man1/*.gz
