#!/usr/bin/env bash
# This is a template so braces are like this {{  }}

# Evaluate a "Use OCL" case.
# --------------------------------------------------------------------
# python manage.py eval-useoclcase CyberResidencesOCl
#
# Compile the .use file
# Compile and validate each soil files listed in "soils.txt" meta file.
# For each file return
# (1) the number of LOC of the input file
# (2) the number of line in output
# (3) the number of line of errors


#--- parameter handling -----------------------------------------------
GROUP="G{key}"
CASE=$1
SOURCE_PATH_PREFIX="/home/jmfavre/DEV/m2gi/m2gi-idm-groups/m2gi-idm-$GROUP/$CASE"


ERROR="-99"
flatfilename() {{  # }} because of template
    echo $1 | sed 's|/|_|g'
}}   # }} because of template

# search use.txt file to check where to get the use file
USEFILE_REF={hq_root_repo_dir}/$CASE/use.txt
if [ -f $USEFILE_REF ] ;
then
    USE=`cat $USEFILE_REF`
else
    USE=$CASE.use
fi
USE_FLAT_NAME=`flatfilename $USE`


# search the soils.txt file
SOILLIST={hq_root_repo_dir}/$CASE/soils.txt
if [ ! -f $SOILLIST ] ;
then
    echo "File not found: $SOILLIST" > /dev/stderr
    exit 2
fi

#--- output -----------------------------------------------------------
OUTDIR={hq_root_repo_dir}/$CASE/.build/$GROUP
SUMMARY=$OUTDIR/summary.csv
# rm -rf $OUTDIR
mkdir -p $OUTDIR

# echo
# echo
# echo "=== {key} ===================================================="
cd "{local_group_repo_dir}"
cd $CASE

printf '"%s",' "G{key}"
FILE_PATH="$SOURCE_PATH_PREFIX/$USE"
FILE_PATH='' # TODO: remove


# echo '----- compilation -----------------------------------'
printf '"%s","%s",' `basename $USE_FLAT_NAME .use` "$FILE_PATH"
if [ -f $USE ] ;
then
    cat $USE >$OUTDIR/$USE_FLAT_NAME
    NB_NCLOC=`cat $USE | egrep -v '^ *(--.*|)$' | wc -l`
    outfile=$OUTDIR/$USE_FLAT_NAME.out
    errfile=$OUTDIR/$USE_FLAT_NAME.err
    use -cp $USE >$outfile  2>$errfile
    NB_ERR=`cat $errfile | wc -l`
    NB_OUT=`cat $outfile | wc -l`
    if [ "$NB_ERR" -eq 0 ];
    then
        NB_ENUM=`cat $outfile | egrep '^enum ' | wc -l`
        NB_CLASS=`cat $outfile | egrep '^class ' | wc -l`
        NB_ASSOC=`cat $outfile | egrep '^(association|associationclass|composition|aggregation) ' | wc -l`
        NB_INV=`cat $outfile | egrep '^context' | wc -l`
    else
        NB_ENUM=$ERROR
        NB_CLASS=$ERROR
        NB_ASSOC=$ERROR
        NB_INV=$ERROR
    fi
    printf "%03s,%03d,%03d,%03d,%03d,%03d,%03d," \
        "$NB_NCLOC" "$NB_ERR" "$NB_OUT" "$NB_ENUM" "$NB_CLASS" "$NB_ASSOC" "$NB_INV"



    for LINE in `cat $SOILLIST | tr ' ' '|'`
    do
        read SOIL_FILENAME SOIL_TITLE <<< $( echo $LINE | tr '|' ' ' )
#        echo
#        echo '--'$SOIL_FILENAME
#        echo '--'$SOIL_TITLE
        # echo -n '"'$SOIL_TITLE'",'
        if [ -f $SOIL_FILENAME ] ;
        then
            FILE_MESSAGE="$SOURCE_PATH_PREFIX/$SOIL_FILENAME"
            FILE_MESSAGE='' # TODO: remove
            # echo "----- $SOIL -----------------------------------------"
            NB_NCLOC=`cat $SOIL_FILENAME | egrep -v '^ *(--.*|)$' | wc -l`
            # IF IN DIR mkdir -p $OUTDIR/`dirname $SOIL`
            infile=$OUTDIR/$SOIL_TITLE.soil
            outfile=$OUTDIR/$SOIL_TITLE.out
            errfile=$OUTDIR/$SOIL_TITLE.err
            cat $SOIL_FILENAME > $infile
            use -qv $USE $SOIL_FILENAME > $outfile  2> $errfile
            NB_ERR=`cat $errfile | wc -l`
            NB_OUT=`cat $outfile | wc -l`
        else
            FILE_MESSAGE="NOT FOUND: $SOURCE_PATH_PREFIX/$SOIL_FILENAME"
            FILE_MESSAGE="NOT FOUND" #TODO: remove
            NB_NCLOC=$ERROR
            NB_ERR=$ERROR
            NB_OUT=$ERROR
        fi
        printf '"%s","%s",%03d,%03d,%03d,' "$SOIL_TITLE" "$FILE_MESSAGE" "$NB_NCLOC" "$NB_ERR" "$NB_OUT"
    done
    echo '"done"'
else
    echo '"NOT FOUND"'
fi
