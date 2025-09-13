#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.18
%define		qtver		5.15.2
%define		kfname		kiconthemes

Summary:	Icon GUI utilities
Name:		kf6-%{kfname}
Version:	6.18.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	79e50bd245c84a30cd59d12fb261a80a
URL:		https://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-breeze-icons-devel >= %{version}
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-karchive-devel >= %{version}
BuildRequires:	kf6-kconfigwidgets-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	kf6-kitemviews-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Svg >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-karchive >= %{version}
Requires:	kf6-kconfigwidgets >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-ki18n >= %{version}
Requires:	kf6-kitemviews >= %{version}
Requires:	kf6-kwidgetsaddons >= %{version}
#Obsoletes:	kf5-%{kfname} < %{version}
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
This library contains classes to improve the handling of icons in
applications using the KDE Frameworks. Provided are:

- KIconDialog: Dialog class to let the user select an icon from the
  list of installed icons.
- KIconButton: Custom button class that displays an icon. When
  clicking it, the user can change it using the icon dialog.
- KIconEffect: Applies various colorization effects to icons, which
  can be used to create selected/disabled icon images.

Other classes in this repository are used internally by the icon theme
configuration dialogs, and should not be used by applications.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/qlogging-categories6/kiconthemes.categories
%attr(755,root,root) %{_bindir}/kiconfinder6
%ghost %{_libdir}/libKF6IconThemes.so.6
%attr(755,root,root) %{_libdir}/libKF6IconThemes.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/kiconthemes6widgets.so
%dir %{_libdir}/qt6/plugins/kiconthemes6
%dir %{_libdir}/qt6/plugins/kiconthemes6/iconengines
%attr(755,root,root) %{_libdir}/qt6/plugins/kiconthemes6/iconengines/KIconEnginePlugin.so
%{_datadir}/qlogging-categories6/kiconthemes.renamecategories
%attr(755,root,root) %{_libdir}/libKF6IconWidgets.so.*.*
%ghost %{_libdir}/libKF6IconWidgets.so.6
%dir %{_libdir}/qt6/qml/org/kde/iconthemes
%{_libdir}/qt6/qml/org/kde/iconthemes/iconthemesplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/iconthemes/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/iconthemes/libiconthemesplugin.so
%{_libdir}/qt6/qml/org/kde/iconthemes/qmldir

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KIconThemes
%{_includedir}/KF6/KIconWidgets
%{_libdir}/cmake/KF6IconThemes
%{_libdir}/libKF6IconThemes.so
%{_libdir}/libKF6IconWidgets.so
