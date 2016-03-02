#!/usr/bin/env bash
SCRIBESINFRA=../..
SPHINXZONE=$SCRIBESINFRA/../SphinxZone
DIRS="sphinxdata sphinxgantt sphinxgithub sphinxgspread sphinxproblems sphinxse sphinxxrefs libs"
FILES="`ls ${SPHINXZONE?}/*.py`"

for dir in $DIRS
do
    echo "  updating $dir"
    rm -rf ${SCRIBESINFRA?}/$dir
    cp -r ${SPHINXZONE?}/$dir ${SCRIBESINFRA?}/$dir
done

for file in $FILES
do
    name=`basename $file`
    echo "  updating $name"
    cp ${SPHINXZONE?}/$name ${SCRIBESINFRA?}/$name
done