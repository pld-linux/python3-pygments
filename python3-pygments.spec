#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define module	pygments
Summary:	A generic syntax highlighter as Python 3 module
Summary(pl.UTF-8):	Moduł Pythona 3 do ogólnego podświetlania składni
Name:		python3-%{module}
Version:	2.13.0
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pygments/
Source0:	https://files.pythonhosted.org/packages/source/P/Pygments/Pygments-%{version}.tar.gz
# Source0-md5:	6ccae578d28d18968b30a4711652fd9a
Patch0:		rpmspec.patch
URL:		https://pygments.org/
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python3-modules >= 1:3.6
Requires:	python3-setuptools
Conflicts:	python-pygments < 2.5.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:
- a wide range of common languages and markup formats is supported
- special attention is paid to details that increase highlighting
  quality
- support for new languages and formats are added easily; most
  languages use a simple regex-based lexing mechanism
- a number of output formats is available, among them HTML, RTF, LaTeX
  and ANSI sequences
- it is usable as a command-line tool and as a library
- ... and it highlights even Brainf*ck!

%description -l pl.UTF-8
Pygments to moduł Pythona do podświetlania składni ogólnego
przeznaczenia we wszelkiego rodzaju programach, takich jaka systemy
forów, wiki i inne plikacje wymagające ładnego wyświetlania kodu
źródłowego. Zalety Pygments to:
- obsługiwany szeroki zakres popularnych języków i formatów znaczników
- zwrócenie szczególnej uwagi na szczegóły zwiększające jakość
  podświetlania
- łatwa obsługa nowych języków i formatów; większość języków
  wykorzystuje prosty mechanizm analizy leksykalnej oparty o wyrażenia
  regularne
- dostępność wielu formatów wyjściowych, m.in. HTML, RTF, LaTeX i
  sekwencje ANSI
- możliwość używania z linii poleceń oraz jako biblioteki
- ...a także - podświetla nawet Brainf*cka!

%package apidocs
Summary:	API documentation for Python Pygments module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona Pygments
Group:		Documentation

%description apidocs
API documentation for Python Pygments module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona Pygments.

%prep
%setup -q -n Pygments-%{version}
%patch0 -p1

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pygmentize{,-3}

ln -sf pygmentize-3 $RPM_BUILD_ROOT%{_bindir}/pygmentize

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE README.rst
%attr(755,root,root) %{_bindir}/pygmentize
%attr(755,root,root) %{_bindir}/pygmentize-3
%{py3_sitescriptdir}/pygments
%{py3_sitescriptdir}/Pygments-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,docs,*.html,*.js}
%endif
