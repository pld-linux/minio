%define		tag	RELEASE.2016-03-21T21-08-51Z
%define		subver	%(echo %{tag} | sed -e 's/[^0-9]//g')
%define		rel	0.1
Summary:	Cloud Storage Server
Name:		minio
Version:	1.1.0
Release:	0.%{subver}.%{rel}
License:	Apache v2.0
Group:		Development/Building
Source0:	https://github.com/minio/minio/archive/RELEASE.2016-03-21T21-08-51Z.tar.gz
# Source0-md5:	-
URL:		https://www.minio.io/
BuildRequires:	golang >= 1.6
ExclusiveArch:	%{ix86} %{x8664} %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# go stuff
%define _enable_debug_packages 0
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};

%description
Minio is an object storage server written in Golang. Minio server,
client and SDK are API compatible with Amazon S3 cloud storage
service.

%prep
%setup -qc

# https://github.com/minio/minio/blob/master/CONTRIBUTING.md#setup-your-minio-github-repository
GOPATH=$(pwd)/go
mkdir -p $GOPATH/src/github.com/minio
mv minio-* $GOPATH/src/github.com/minio/minio

%build
export GOPATH=$(pwd)/go
export GOROOT=%{_libdir}/golang
cd go/src/github.com/minio/minio
> buildscripts/checkgopath.sh
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.md
