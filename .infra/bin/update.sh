#!/usr/bin/env bash
SCRIBESINFRA=.
SPHINXZONE=$SCRIBESINFRA/../SphinxZone
DIRS="dbcase pyschemaspy sphinxdata sphinxgantt sphinxgithub sphinxgspread sphinxproblems sphinxuseocl sphinxse sphinxxrefs sqlrst"
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

git add ${SCRIBESINFRA?}
git commit -am 'update'
git push origin master