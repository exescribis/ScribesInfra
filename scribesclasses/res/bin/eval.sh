#!/usr/bin/env bash
#
# usage:  bin/eval.sh
#
# Evaluate all cases for all groups
#

HQ_ROOT_DIR=$1
cd $HQ_ROOT_DIR
echo "Working directory: $HQ_ROOT_DIR"

shift

if [ $# -eq 0 ];
then
    CASES=`ls -d */ | grep -v bin`
else
    CASES="$@"
fi



# python manage.py commands > /dev/null
for CASE in $CASES
do
    if [ -f $HQ_ROOT_DIR/$CASE/eval.sh ];
    then
        echo "------ Evaluating $CASE -------------------------------------"
        $HQ_ROOT_DIR/$CASE/eval.sh
        echo
        echo
    else
        echo "...... Ignoring $CASE (no eval script) ......................"
    fi
    echo
done
