#!/bin/sh
curl -s "https://0xacab.org/jvoisin/mat2/-/tags" |grep "tags/" |sed -e 's,.*tags/,,;s,\".*,,;' |grep -E '^[0-9.]+$' |grep -v '[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]' |sort -V |tail -n1

