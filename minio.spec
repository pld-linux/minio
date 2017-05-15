%define		tag	RELEASE.2017-05-05T01-14-51Z
%define		subver	%(echo %{tag} | sed -e 's/[^0-9]//g')
# git fetch https://github.com/minio/minio.git refs/tags/RELEASE.2017-05-05T01-14-51Z
# git rev-list -n 1 FETCH_HEAD
%define		commitid	4f61bd025deeb1d0136d7a367f56e85877266e0e
Summary:	Object Storage Server
Name:		minio
Version:	0.0.%{subver}
Release:	1
License:	Apache v2.0
Group:		Development/Building
Source0:	https://github.com/minio/minio/archive/%{tag}.tar.gz
# Source0-md5:	353ed77947b86534d374d57054659efd
URL:		https://www.minio.io/
BuildRequires:	golang >= 1.7
ExclusiveArch:	%{ix86} %{x8664} %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# go stuff
%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/minio/minio

%description
Minio is an object storage server released under Apache License v2.0.
It API compatible with Amazon S3 cloud storage service.

%prep
%setup -qc
mv %{name}-*/* .

install -d src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}

%build
export GOPATH=$(pwd)
export GOROOT=%{_libdir}/golang

# setup flags like 'go run buildscripts/gen-ldflags.go' would do
tag=%{tag}
version=${tag#RELEASE.}
commitid=%{commitid}
scommitid=$(echo $commitid | cut -c1-12)
prefix=%{import_path}/cmd

LDFLAGS="
-X $prefix.Version=$version
-X $prefix.ReleaseTag=$tag
-X $prefix.CommitID=$commitid
-X $prefix.ShortCommitID=$scommitid
"

%gobuild -o %{name}

# check that version set properly
./%{name} version | tee v

#Version: 2016-09-11T17-42-18Z
#Release-Tag: RELEASE.2016-09-11T17-42-18Z
#Commit-ID: 85e2d886bcb005d49f3876d6849a2b5a55e03cd3
v=$(awk '/Version:/{print $2}' v)
test "$v" = $version
v=$(awk '/Release-Tag:/{print $2}' v)
test "$v" = $tag
v=$(awk '/Commit-ID:/{print $2}' v)
test "$v" = $commitid

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
