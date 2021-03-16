%if 0%{?fedora}
%global with_broadway 1
%endif

%global glib2_version 2.66.0
%global pango_version 1.47.0
%global cairo_version 1.14.0
%global gdk_pixbuf_version 2.30.0
%global wayland_protocols_version 1.20
%global wayland_version 1.14.91
%global epoxy_version 1.4

%global bin_version 4.0.0

# Filter provides for private modules
%global __provides_exclude_from ^%{_libdir}/gtk-4.0

Name:           gtk4
Version:        4.1.2
Release:        1%{?dist}
Summary:        GTK graphical user interface library

License:        LGPLv2+
URL:            https://www.gtk.org
Source0:        https://download.gnome.org/sources/gtk/4.1/gtk-%{version}.tar.xz

BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  pkgconfig(avahi-gobject)
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
BuildRequires:  pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires:  pkgconfig(colord)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(graphene-gobject-1.0)
BuildRequires:  pkgconfig(gstreamer-player-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  pkgconfig(rest-0.7)
BuildRequires:  pkgconfig(sysprof-4)
BuildRequires:  pkgconfig(sysprof-capture-4)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  /usr/bin/xsltproc

# standard icons
Requires: adwaita-icon-theme
# required for icon theme apis to work
Requires: hicolor-icon-theme
# split out in a subpackage
Requires: gtk-update-icon-cache

Requires: cairo%{?_isa} >= %{cairo_version}
Requires: cairo-gobject%{?_isa} >= %{cairo_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: libepoxy%{?_isa} >= %{epoxy_version}
Requires: libwayland-client%{?_isa} >= %{wayland_version}
Requires: libwayland-cursor%{?_isa} >= %{wayland_version}
Requires: pango%{?_isa} >= %{pango_version}

# required to support all the different image formats
Requires: gdk-pixbuf2-modules%{?_isa}

# make sure we have a reasonable gsettings backend
Recommends: dconf%{?_isa}

# Removed in F34
Obsoletes: gtk4-devel-docs < 4.1.2

%description
GTK is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 4 of GTK.

%package devel
Summary: Development files for GTK
Requires: gtk4%{?_isa} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 4 of the GTK widget toolkit.

%prep
%autosetup -p1 -n gtk-%{version}

%build
export CFLAGS='-fno-strict-aliasing -DG_DISABLE_CAST_CHECKS -DG_DISABLE_ASSERT %optflags'
%meson \
        -Dx11-backend=true \
        -Dwayland-backend=true \
%if 0%{?with_broadway}
        -Dbroadway-backend=true \
%endif
        -Dmedia-ffmpeg=disabled \
        -Dmedia-gstreamer=enabled \
        -Dxinerama=enabled \
        -Dsysprof=enabled \
        -Dcolord=enabled \
        -Dsassc=disabled \
        -Dgtk_doc=false \
        -Dman-pages=true \
        -Dinstall-tests=false

%meson_build

%install
%meson_install

%find_lang gtk40
%find_lang gtk40-properties

%if !0%{?with_broadway}
rm $RPM_BUILD_ROOT%{_mandir}/man1/gtk4-broadwayd.1*
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-4.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/%{bin_version}/theming-engines

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f gtk40.lang
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/gtk4-launch
%{_bindir}/gtk4-update-icon-cache
%{_libdir}/libgtk-4.so.1*
%dir %{_libdir}/gtk-4.0
%dir %{_libdir}/gtk-4.0/%{bin_version}
%{_libdir}/gtk-4.0/%{bin_version}/media/
%{_libdir}/gtk-4.0/%{bin_version}/printbackends/
%{_libdir}/gtk-4.0/%{bin_version}/theming-engines/
%{_libdir}/gtk-4.0/modules
%{_libdir}/girepository-1.0
%{_mandir}/man1/gtk4-launch.1*
%{_mandir}/man1/gtk4-update-icon-cache.1*
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.EmojiChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.FileChooser.gschema.xml
%dir %{_datadir}/gtk-4.0
%{_datadir}/gtk-4.0/emoji/
%if 0%{?with_broadway}
%{_bindir}/gtk4-broadwayd
%{_mandir}/man1/gtk4-broadwayd.1*
%endif

%files devel -f gtk40-properties.lang
%{_libdir}/libgtk-4.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk4-builder-tool
%{_bindir}/gtk4-demo
%{_bindir}/gtk4-encode-symbolic-svg
%{_bindir}/gtk4-icon-browser
%{_bindir}/gtk4-query-settings
%{_datadir}/applications/org.gtk.Demo4.desktop
%{_datadir}/applications/org.gtk.IconBrowser4.desktop
%{_datadir}/applications/org.gtk.PrintEditor4.desktop
%{_datadir}/applications/org.gtk.WidgetFactory4.desktop
%{_datadir}/icons/hicolor/*/apps/org.gtk.Demo4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.IconBrowser4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.PrintEditor4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.WidgetFactory4*.svg
%{_bindir}/gtk4-demo-application
%{_bindir}/gtk4-print-editor
%{_bindir}/gtk4-widget-factory
%{_datadir}/gettext/
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo4.gschema.xml
%{_datadir}/gtk-4.0/gtk4builder.rng
%{_datadir}/gtk-4.0/valgrind/
%{_datadir}/metainfo/org.gtk.Demo4.appdata.xml
%{_datadir}/metainfo/org.gtk.IconBrowser4.appdata.xml
%{_datadir}/metainfo/org.gtk.PrintEditor4.appdata.xml
%{_datadir}/metainfo/org.gtk.WidgetFactory4.appdata.xml
%{_mandir}/man1/gtk4-builder-tool.1*
%{_mandir}/man1/gtk4-demo.1*
%{_mandir}/man1/gtk4-demo-application.1*
%{_mandir}/man1/gtk4-encode-symbolic-svg.1*
%{_mandir}/man1/gtk4-icon-browser.1*
%{_mandir}/man1/gtk4-query-settings.1*
%{_mandir}/man1/gtk4-widget-factory.1*

%changelog
* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 4.1.2-1
- Update to 4.1.2
- Disable gtk-doc support as we don't have gi-docgen in Fedora yet
- Remove old obsoletes

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 4.1.1-1
- Update to 4.1.1
- Enable sysprof support

* Fri Feb 19 2021 Kalev Lember <klember@redhat.com> - 4.1.0-3
- Backport upstream patch to fix a settings schema loading issue on Wayland

* Mon Feb 01 2021 Kalev Lember <klember@redhat.com> - 4.1.0-2
- Disable asserts and cast checks

* Sun Jan 31 2021 Kalev Lember <klember@redhat.com> - 4.1.0-1
- Update to 4.1.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Kalev Lember <klember@redhat.com> - 4.0.2-2
- Avoid rebuilding stylesheets with sassc during the build

* Tue Jan 19 2021 Kalev Lember <klember@redhat.com> - 4.0.2-1
- Update to 4.0.2

* Sat Jan 09 2021 Kalev Lember <klember@redhat.com> - 4.0.1-1
- Update to 4.0.1

* Sat Jan 09 2021 Kalev Lember <klember@redhat.com> - 4.0.0-3
- Fix vulkan reference in pc file

* Tue Dec 22 14:13:09 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-2
- Add back gtk4-devel-docs

* Wed Dec 16 2020 Kalev Lember <klember@redhat.com> - 4.0.0-1
- Update to 4.0.0
- Tighten soname globs

* Fri Dec 11 2020 Kalev Lember <klember@redhat.com> - 3.99.5-1
- Update to 3.99.5

* Wed Dec 09 2020 Jeff Law <law@redhat.com> - 3.99.4-3
- Avoid diagnostics for gcc-11 false positive out of bounds accesses

* Sun Nov 15 2020 Jeff Law <law@redhat.com> - 3.99.4-2
- Fix bogus volatile caught by gcc-11

* Thu Nov  5 2020 Kalev Lember <klember@redhat.com> - 3.99.4-1
- Update to 3.99.4

* Fri Oct 16 2020 Kalev Lember <klember@redhat.com> - 3.99.3-1
- Update to 3.99.3

* Thu Oct 01 2020 Kalev Lember <klember@redhat.com> - 3.99.2-2
- Update required pango and glib2 versions

* Tue Sep 29 2020 Kalev Lember <klember@redhat.com> - 3.99.2-1
- Update to 3.99.2

* Mon Sep 28 2020 Jeff Law <law@redhat.com> - 3.99.1-2
- Re-enable LTO as upstream GCC target/96939 has been fixed

* Thu Sep 03 2020 Kalev Lember <klember@redhat.com> - 3.99.1-1
- Update to 3.99.1
- Drop wayland build conditionals

* Mon Aug 17 2020 Jeff Law <law@redhat.com> - 3.99.0-2
- Disable LTO on armv7hl

* Sat Aug 01 2020 Kalev Lember <klember@redhat.com> - 3.99.0-1
- Update to 3.99.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.98.5-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.98.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Kalev Lember <klember@redhat.com> - 3.98.5-1
- Update to 3.98.5

* Tue May 19 2020 Kalev Lember <klember@redhat.com> - 3.98.4-1
- Update to 3.98.4

* Tue Apr 21 2020 Kalev Lember <klember@redhat.com> - 3.98.3-1
- Update to 3.98.3
- Temporarily disable built documentation as we don't have new enough gtk-doc

* Wed Apr 01 2020 Kalev Lember <klember@redhat.com> - 3.98.2-1
- Update to 3.98.2

* Sun Mar 22 2020 Kalev Lember <klember@redhat.com> - 3.98.1-1
- Update to 3.98.1

* Thu Mar 12 2020 Kalev Lember <klember@redhat.com> - 3.98.0-2
- Install missing gtkemojichooser.h (#1806509)

* Tue Feb 11 2020 Kalev Lember <klember@redhat.com> - 3.98.0-1
- Update to 3.98.0
- Use https for source URLs

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.96.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.96.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 3.96.0-1
- Update to 3.96.0
- Use GTK instead of GTK+ in descriptions
- Don't ship installed tests as they are currently broken

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.94.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Kalev Lember <klember@redhat.com> - 3.94.0-1
- Update to 3.94.0
- Remove and obsolete immodules subpackages
- Build new gstreamer media backend

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.92.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 3.92.1-3
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.92.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 3.92.1-1
- Update to 3.92.1
- Enable installed tests

* Tue Aug 08 2017 Kalev Lember <klember@redhat.com> - 3.91.2-1
- Update to 3.91.2

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 3.91.1-1
- Update to 3.91.1

* Wed Jun 14 2017 Kalev Lember <klember@redhat.com> - 3.91.0-2
- Disable installed tests due to file conflicts between gtk3-tests and
  gtk4-tests

* Wed Jun 14 2017 Kalev Lember <klember@redhat.com> - 3.91.0-1
- Initial Fedora packaging
