Summary:	Metadata Anonymisation Toolkit
Name:		mat2
Version:	0.12.3
Release:	1
License:	LGPLv3+
Group:		File tools
URL:		https://mat.boum.org/
Source0:	https://0xacab.org/jvoisin/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
#Source1:	https://0xacab.org/jvoisin/%{name}/uploads/289306e110d1425db0d3ce017065f73b/%{name}-%{version}.tar.gz.asc
BuildArch:	noarch

BuildRequires:	pkgconfig(python3)
BuildRequires:	perl(Image::ExifTool)
BuildRequires:	python3dist(mutagen)
BuildRequires:	python3dist(pycairo)
BuildRequires:	python3dist(setuptools)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) 
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	%{_lib}rsvg-gir2.0
BuildRequires:	ffmpeg-devel
BuildRequires:	bubblewrap
BuildRequires:	imagemagick
BuildRequires:	librsvg

Requires:	bubblewrap
Requires:	perl-Image-ExifTool

%description
Metadata consist of information that characterizes data.
Metadata are used to provide documentation for data products.
In essence, metadata answer who, what, when, where, why, and how about
every facet of the data that are being documented.

Metadata within a file can tell a lot about you.
Cameras record data about when a picture was taken and what
camera was used. Office documents like PDF or Office automatically adds
author and company information to documents and spreadsheets.
Maybe you don't want to disclose those information.

This is precisely the job of mat2: getting rid, as much as possible, of
metadata.

mat2 provides a command line tool, and graphical user interfaces via a service
menu for Dolphin, the default file manager of KDE, and an extension for
Nautilus, the default file manager of GNOME.

%files
%license LICENSE
%doc README.md CHANGELOG.md
%doc doc/comparison_to_others.md
%doc doc/implementation_notes.md
%doc doc/threat_model.md
%{_bindir}/%{name}
%{py_sitedir}/lib%{name}/
%{py_sitedir}/%{name}-%{version}-py%{python_version}.egg-info/
%{_iconsdir}/hicolor/*/apps/%{name}.{png,svg}
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/kservices5/ServiceMenus/%{name}.desktop
%{_datadir}/nautilus-python/extensions/%{name}.py
%{_mandir}/man1/%{name}.1.*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%py_build

%install 
%py_install

# icons
for d in 16 32 48 64 72 128 256 512
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	rsvg-convert -f png -h ${d} -w ${d} data/%{name}.svg \
			-o %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
#	convert -background none -size "${d}x${d}" sources/pics/vector-logo/%{sname}-logo.svg \
#			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
#	pixmap
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -size 32x32 data/%{name}.svg %{buildroot}%{_datadir}/pixmaps/%{name}.xpm
#	scalable
install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
install -pm 0644 data/%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

# contextual menu
# 	dolphin 
install -dm 0755 %{buildroot}%{_datadir}/kservices5/ServiceMenus/
install -pm 0755 dolphin/mat2.desktop %{buildroot}%{_datadir}/kservices5/ServiceMenus/
#	nautilus
install -dm 0755 %{buildroot}%{_datadir}/nautilus-python/extensions/
install -pm 0755 nautilus/mat2.py %{buildroot}%{_datadir}/nautilus-python/extensions/

# manual
install -dm 0755 %{buildroot}%{_mandir}/man1/
install -pm 0644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/

%check
# run tests
PYTHONPATH=%{buildroot}%{py_sitedir} %python -m unittest discover -v || :

