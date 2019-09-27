#!/usr/bin/env bash
if [ -z "$1" ]; then
 echo "usage: $0 <directory>"
 exit 1
fi
set -ex
cd $1
find -type f -name *obj \
 | perl -ne'chomp; print "$ENV{'HOME'}/dev/v-hacd/build/linux/test/testVHACD --input $_";s/obj/vhacd.obj/;print " --output $_ --log /dev/null\n"' \
 | parallel
