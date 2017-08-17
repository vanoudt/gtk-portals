%if 0%{?fedora}
%global with_wayland 1
%global with_broadway 1
%endif

# File conflicts between gtk3-tests and gtk4-tests
%global build_installed_tests 0

%global glib2_version 2.53.0
%global pango_version 1.37.3
%global atk_version 2.15.1
%global cairo_version 1.14.0
%global gdk_pixbuf_version 2.30.0
%global wayland_version 1.9.91
%global wayland_protocols_version 1.9
%global epoxy_version 1.0

%global bin_version 4.0.0

# Filter provides for private modules
%global __provides_exclude_from ^%{_libdir}/gtk-4.0

Name:           gtk4
Version:        3.91.2
Release:        1%{?dist}
Summary:        GTK+ graphical user interface library

License:        LGPLv2+
URL:            http://www.gtk.org
Source0:        http://download.gnome.org/sources/gtk+/3.91/gtk+-%{version}.tar.xz

BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  pkgconfig(atk) >= %{atk_version}
BuildRequires:  pkgconfig(atk-bridge-2.0)
BuildRequires:  pkgconfig(avahi-gobject)
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
BuildRequires:  pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires:  pkgconfig(colord)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(graphene-gobject-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  pkgconfig(rest-0.7)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xrender)
%if 0%{?with_wayland}
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires:  pkgconfig(xkbcommon)
%endif

# standard icons
Requires: adwaita-icon-theme
# required for icon theme apis to work
Requires: hicolor-icon-theme
# split out in a subpackage
Requires: gtk-update-icon-cache

Requires: atk%{?_isa} >= %{atk_version}
Requires: cairo%{?_isa} >= %{cairo_version}
Requires: cairo-gobject%{?_isa} >= %{cairo_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: libepoxy%{?_isa} >= %{epoxy_version}
Requires: pango%{?_isa} >= %{pango_version}
%if 0%{?with_wayland}
Requires: libwayland-client%{?_isa} >= %{wayland_version}
Requires: libwayland-cursor%{?_isa} >= %{wayland_version}
%endif

# required to support all the different image formats
Requires: gdk-pixbuf2-modules%{?_isa}

# make sure we have a reasonable gsettings backend
%if 0%{?fedora}
Recommends: dconf%{?_isa}
%else
Requires: dconf%{?_isa}
%endif

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 4 of GTK+.

%package immodules
Summary: Input methods for GTK+
Requires: gtk4%{?_isa} = %{version}-%{release}
# for im-cedilla.conf
Requires: gtk2-immodules%{?_isa}

%description immodules
The gtk4-immodules package contains standalone input methods that
are shipped as part of GTK+ 4.

%package immodule-xim
Summary: XIM support for GTK+
Requires: gtk4%{?_isa} = %{version}-%{release}

%description immodule-xim
The gtk4-immodule-xim package contains XIM support for GTK+ 4.

%package devel
Summary: Development files for GTK+
Requires: gtk4%{?_isa} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 4 of the GTK+ widget toolkit. If
you plan to develop applications with GTK+, consider installing the
gtk4-devel-docs package.

%package devel-docs
Summary: Developer documentation for GTK+
Requires: gtk4 = %{version}-%{release}

%description devel-docs
This package contains developer documentation for version 4 of the GTK+
widget toolkit.

%if 0%{?build_installed_tests}
%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.
%endif

%prep
%setup -q -n gtk+-%{version}

%build
export CFLAGS='-fno-strict-aliasing %optflags'
%configure \
        --enable-xkb \
        --enable-xinerama \
        --enable-xrandr \
        --enable-xfixes \
        --enable-xcomposite \
        --enable-xdamage \
        --enable-x11-backend \
%if 0%{?with_wayland}
        --enable-wayland-backend \
%endif
%if 0%{?with_broadway}
        --enable-broadway-backend \
%endif
        --enable-colord \
%if 0%{?build_installed_tests}
        --enable-installed-tests
%else
        --disable-installed-tests
%endif

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}

%install
%make_install RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk40
%find_lang gtk40-properties

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gtk4-query-immodules gtk4-query-immodules-%{__isa_bits}
)

echo ".so man1/gtk4-query-immodules.1" > $RPM_BUILD_ROOT%{_mandir}/man1/gtk4-query-immodules-%{__isa_bits}.1

# Remove unpackaged files
find $RPM_BUILD_ROOT -name '*.la' -delete

%if !0%{?with_broadway}
rm $RPM_BUILD_ROOT%{_mandir}/man1/gtk4-broadwayd.1*
%endif

touch $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/%{bin_version}/immodules.cache

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-4.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/%{bin_version}/theming-engines

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun devel
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans devel
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%transfiletriggerin -- %{_libdir}/gtk-4.0/%{bin_version}/immodules
gtk4-query-immodules-%{__isa_bits} --update-cache &>/dev/null || :

%transfiletriggerpostun -- %{_libdir}/gtk-4.0/%{bin_version}/immodules
gtk-query-immodules-4.0-%{__isa_bits} --update-cache &>/dev/null || :

%files -f gtk40.lang
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/gtk4-query-immodules*
%{_bindir}/gtk4-launch
%{_bindir}/gtk4-update-icon-cache
%{_libdir}/libgtk-4.so.*
%dir %{_libdir}/gtk-4.0
%dir %{_libdir}/gtk-4.0/%{bin_version}
%dir %{_datadir}/gtk-4.0
%{_libdir}/gtk-4.0/%{bin_version}/theming-engines
%dir %{_libdir}/gtk-4.0/%{bin_version}/immodules
%{_libdir}/gtk-4.0/%{bin_version}/printbackends
%{_libdir}/gtk-4.0/modules
%{_libdir}/gtk-4.0/immodules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_libdir}/girepository-1.0
%ghost %{_libdir}/gtk-4.0/%{bin_version}/immodules.cache
%{_mandir}/man1/gtk4-query-immodules*
%{_mandir}/man1/gtk4-launch.1*
%{_mandir}/man1/gtk4-update-icon-cache.1*
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.exampleapp.gschema.xml
%if 0%{?with_broadway}
%{_bindir}/gtk4-broadwayd
%{_mandir}/man1/gtk4-broadwayd.1*
%endif

%files immodules
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-viqr.so
%if 0%{?with_broadway}
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-broadway.so
%endif
%config(noreplace) %{_sysconfdir}/gtk-4.0/im-multipress.conf

%files immodule-xim
%{_libdir}/gtk-4.0/%{bin_version}/immodules/im-xim.so

%files devel -f gtk40-properties.lang
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk4-builder-tool
%{_bindir}/gtk4-demo
%{_bindir}/gtk4-encode-symbolic-svg
%{_bindir}/gtk4-icon-browser
%{_bindir}/gtk4-query-settings
%{_datadir}/applications/gtk4-demo.desktop
%{_datadir}/applications/gtk4-icon-browser.desktop
%{_datadir}/applications/gtk4-widget-factory.desktop
%{_datadir}/icons/hicolor/*/apps/gtk4-demo.png
%{_datadir}/icons/hicolor/*/apps/gtk4-demo-symbolic.symbolic.png
%{_datadir}/icons/hicolor/*/apps/gtk4-widget-factory.png
%{_datadir}/icons/hicolor/*/apps/gtk4-widget-factory-symbolic.symbolic.png
%{_bindir}/gtk4-demo-application
%{_bindir}/gtk4-widget-factory
%{_datadir}/gettext/
%{_datadir}/gtk-4.0/gtkbuilder.rng
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo.gschema.xml
%{_mandir}/man1/gtk4-builder-tool.1*
%{_mandir}/man1/gtk4-demo.1*
%{_mandir}/man1/gtk4-demo-application.1*
%{_mandir}/man1/gtk4-encode-symbolic-svg.1*
%{_mandir}/man1/gtk4-icon-browser.1*
%{_mandir}/man1/gtk4-query-settings.1*
%{_mandir}/man1/gtk4-widget-factory.1*

%files devel-docs
%{_datadir}/gtk-doc

%if 0%{?build_installed_tests}
%files tests
%{_libexecdir}/installed-tests/gtk+
%{_datadir}/installed-tests
%endif

%changelog
* Tue Aug 08 2017 Kalev Lember <klember@redhat.com> - 3.91.2-1
- Update to 3.91.2

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 3.91.1-1
- Update to 3.91.1

* Wed Jun 14 2017 Kalev Lember <klember@redhat.com> - 3.91.0-2
- Disable installed tests due to file conflicts between gtk3-tests and
  gtk4-tests

* Wed Jun 14 2017 Kalev Lember <klember@redhat.com> - 3.91.0-1
- Initial Fedora packaging
