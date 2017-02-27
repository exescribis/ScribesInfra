#!/usr/bin/env bash
SPHINXZONE=../SphinxZone
cp -fR $SPHINXZONE/sphinx* .
cp -fR $SPHINXZONE/sqlrst .
cp -fR $SPHINXZONE/dbcase .
cp -f $SPHINXZONE/*.py .