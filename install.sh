#!/usr/bin/env bash
VENV=$PWD/venv/
mkdir -p $VENV
for reqfile in `ls requirements-*.txt`
do
    echo "======= Installing   $reqfile  ======================================"
    pip install --upgrade --target=$VENV --install-option="--install-scripts=$VENV/bin" -r ${reqfile?}
done

for file in `ls bin`
do
    echo +x bin/$file
    chmod +x bin/$file
done
