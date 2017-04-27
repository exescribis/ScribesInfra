#!/usr/bin/env bash
# This is a template so braces are like this {{  }}


#--- parameter handling -----------------------------------------------

CASE=$1

flatfilename() {{  # }} because of template
    echo $1 | sed 's|/|_|g'
}}   # }} because of template

# search the soils.txt file
FILELIST={hq_root_repo_dir}/$CASE/files.txt
if [ ! -f $FILELIST ] ;
then
    echo "File not found: $FILELIST" > /dev/stderr
    exit 2
fi

#--- output -----------------------------------------------------------
OUTDIR={hq_root_repo_dir}/$CASE/.build/{key}
SUMMARY=$OUTDIR/summary.csv
rm -rf $OUTDIR
mkdir -p $OUTDIR

# echo
# echo
# echo "=== {key} ===================================================="
cd "{local_group_repo_dir}"
cd $CASE
echo -n '"G{key}",'

for LINE in `cat $FILELIST | tr ' ' '|'`
do
    read FILENAME TITLE <<< $( echo $LINE | tr '|' ' ' )
    echo -n '"'$TITLE'",'
    if [ -f $FILENAME ] ;
    then
        infile=$OUTDIR/$TITLE.py
        outfile=$OUTDIR/$TITLE.out
        errfile=$OUTDIR/$TITLE.err
        cat $FILENAME > $infile
        echo -n `cat $infile | wc -l`',"NCLOC",'
    else
        echo -n '"NOT FOUND",-999,-999,'
    fi
    echo '"."'
done

