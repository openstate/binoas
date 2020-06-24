#!/bin/bash
FQPATH=`readlink -f $0`
BINDIR=`dirname $FQPATH`
APP_TEMPLATE_DIR=
for t in $BINDIR/../templates/applications/*$1*.mjml;
do
  ft=`readlink -f $t`
  bt=`basename $ft .mjml`
  echo "$ft => $bt.html"
  $BINDIR/make_template.sh $ft >"$BINDIR/../templates/applications/$bt.html"
done
