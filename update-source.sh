#!/bin/sh
set -e

repo_url="https://github.com/minio/minio.git"
specfile=minio.spec

# Work in package dir
dir=$(dirname "$0")
cd "$dir"

if [ "$1" ]; then
	version=$1
else
	# fetch version from pldnotifdy
	version=$(pldnotify.py $specfile | awk '/Found an update/{print $NF}')
fi

tag=RELEASE.${version#RELEASE.}

# grab git hash
git fetch "$repo_url" refs/tags/$tag
# save this under some local ref, so repeated calls don't have to fetch everything
git update-ref refs/keep-around/FETCH_HEAD FETCH_HEAD

commitid=$(git rev-list -n 1 FETCH_HEAD)

echo "Updating $specfile: tag: $tag; commitid: $commitid"
sed -i -re "
	s/^[#%](define[ \t]+tag[ \t]+)[0-9]+\$/%\1$tag/
	s/^[#%](define[ \t]+commitid[ \t]+)[0-9a-fg]+\$/%\1$commitid/
" $specfile
../builder -ncs -5 $specfile
