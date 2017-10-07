#!/usr/bin/env bash
if [ -z "$1" ]; then
 echo "usage: $0 <directory>"
 exit 1
fi  
set -ex
cd $1
export BULLET=$HOME/dev/bullet3
find -type f -name *obj \
 | perl -ne'chomp; print "$ENV{'BULLET'}/bin/test_vhacd_gmake_x64_release --input $_";s/obj/vhacd.obj/;print " --output $_ --log /dev/null\n"' \
 | parallel
