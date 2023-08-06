#!/bin/sh

MAJOR_MINOR="2.10"

pip install --user antsibull
git clone git@github.com:ansible-community/ansible-build-data
mkdir built
if test -e "ansible-build-data/${MAJOR_MINOR}/ansible-${MAJOR_MINOR}.build" ; then
  BUILDFILE="ansible-build-data/${MAJOR_MINOR}/ansible-${MAJOR_MINOR}.build"
else
  BUILDFILE="ansible-build-data/${MAJOR_MINOR}/acd-${MAJOR_MINOR}.build"
fi
antsibull-build rebuild-single "2.10.0a9" --build-file "$BUILDFILE" --dest-dir built

#pip install twine
#twine upload "built/ansible-2.10.0a9.tar.gz"