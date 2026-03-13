%define		tag	RELEASE.2025-10-15T17-29-55Z
%define		subver	%(echo %{tag} | sed -e 's/[^0-9]//g')
%define		commitid	9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a
%define		vendor_version	20251015
Summary:	Object Storage Server
Name:		minio
Version:	0.0.%{subver}
Release:	1
License:	Apache v2.0
Group:		Development/Building
Source0:	https://github.com/minio/minio/archive/%{tag}.tar.gz
# Source0-md5:	e86a4ebe9720a4bba2640caf8f47504f
# cd minio-%%{tag}
# go mod vendor
# cd ..
# tar cJf minio-vendor-%%{vendor_version}.tar.xz minio-%%{tag}/vendor
Source1:	%{name}-vendor-%{vendor_version}.tar.xz
# Source1-md5:	fe00b43632fbd0fa1edcc51be77bffce
URL:		https://min.io/
BuildRequires:	golang >= 1.24.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%define		import_path	github.com/minio/minio

%description
MinIO is a high-performance, S3 compatible object store. It is built
for large scale AI/ML, data lake and database workloads.

%prep
%setup -qc -a1

mv %{name}-*/*.md .
mv %{name}-*/vendor .
mv %{name}-*/* .

%{__mkdir_p} .go-cache

%build
# setup flags like 'go run buildscripts/gen-ldflags.go' would do
tag=%{tag}
version=${tag#RELEASE.}
commitid=%{commitid}
scommitid=$(echo $commitid | cut -c1-12)
prefix=%{import_path}/cmd

%__go build -v -mod=vendor \
	-ldflags " \
	-X $prefix.Version=$version \
	-X $prefix.ReleaseTag=$tag \
	-X $prefix.CommitID=$commitid \
	-X $prefix.ShortCommitID=$scommitid \
	-X $prefix.CopyrightYear=2025 \
	-X $prefix.GOPATH=%{_libdir}/golang \
	-X $prefix.GOROOT=%{_libdir}/golang" \
	-o %{name}

# check that version set properly
# output: minio version RELEASE.xxx (commit-id=xxx)
./%{name} --version | tee v
grep -q "$tag" v
grep -q "$scommitid" v

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
