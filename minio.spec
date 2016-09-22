%define		tag	RELEASE.2016-09-11T17-42-18Z
%define		subver	%(echo %{tag} | sed -e 's/[^0-9]//g')
%define		rel	0.1
Summary:	Cloud Storage Server
Name:		minio
Version:	1.1.0
Release:	0.%{subver}.%{rel}
License:	Apache v2.0
Group:		Development/Building
Source0:	https://github.com/minio/minio/archive/%{tag}.tar.gz
# Source0-md5:	30cd2627a897a1ef52439fcd399f068b
URL:		https://www.minio.io/
BuildRequires:	golang >= 1.6
ExclusiveArch:	%{ix86} %{x8664} %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# go stuff
%define _enable_debug_packages 0
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/minio/minio

%description
Minio is an object storage server written in Golang. Minio server,
client and SDK are API compatible with Amazon S3 cloud storage
service.

%prep
%setup -qc

mv %{name}-*/* .

install -d src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}

%build
export GOPATH=$(pwd)
export GOROOT=%{_libdir}/golang
%gobuild -o %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -p %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.md
%attr(755,root,root) %{_sbindir}/minio
