##!/usr/bin/env bash
#THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#CASEDIR=$1   #THISDIR
#
#
#
#
#CASE=`basename ${CASEDIR?}`
#
#TMPDIR=$(mktemp -dt "$(basename $0).XXXXXXX")
#SCRIPT="${TMPDIR?}/script"
#
##*** Ensure .build directory
#mkdir -p ${CASEDIR}/.build
#
##--- Create database with .csv files
#DB=${CASEDIR}/.build/${CASE}.db
#rm -f $DB
#
#
#SCHEMAFILE="${CASEDIR?}/${CASE}.schema.sql"
#if [ -f ${SCHEMAFILE?} ]
#then
#    echo "----------------------------------------------------"
#    echo "     ${CASE}:      Creating the database schema"
#    echo "----------------------------------------------------"
#    sqlite3 $DB < ${SCHEMAFILE?}
#fi
#
#echo "----------------------------------------------------"
#echo "   ${CASE}:        Creating the database content"
#echo "----------------------------------------------------"
#
#CSVINPUT=${TMPDIR}/input.csv
#
#for CSVFILE in `ls ${CASEDIR?}/*.in.csv`
#do
#    RELATION=`basename ${CSVFILE} .in.csv`
#    # prepare csv input. If the schema has already been
#    # given, headers have to be removed for sqlite
#    echo -n "    importing ${RELATION} ... "
#    if [ -f ${SCHEMAFILE?} ]
#    then
#        # remove the header since a schema is given
#        tail -n +2 ${CSVFILE} > ${CSVINPUT?}
#    else
#        cat ${CSVFILE} > ${CSVINPUT?}
#    fi
#    echo ".mode csv" >${SCRIPT?}
#    echo ".import ${CSVINPUT} ${RELATION}" >>${SCRIPT?}
#    echo ".quit" >> ${SCRIPT?}
#    sqlite3 $DB <${SCRIPT?}
#    echo " done"
#done
#
#NULLABLEFILE="${CASEDIR?}/${CASE}.nullable.txt"
#if [ -f ${NULLABLEFILE?} ]
#then
#    echo "----- ${CASE}:   SQLite NULL conversion "
#    cat ${NULLABLEFILE?} \
#        | awk -F. \
#            '{print "UPDATE " $1 " SET " $2 " = NULL WHERE " $2 "=\"NULL\" ;"} ' \
#        | sqlite3 $DB
#fi
#
#
#
#echo "----------------------------------------------------"
#echo "   ${CASE}:         Executing queries"
#echo "----------------------------------------------------"
#
#
##--- Execute queries from .sql files
#
#QUERYINDEX=${CASEDIR}/index.queries.txt
#if [ -f ${QUERYINDEX?} ]
#then
#    QUERYFILES=`cat ${QUERYINDEX?}`
#else
#    QUERYFILES=`ls ${CASEDIR?}/*.queries.sql`
#fi
#
#
#for SQLFILE in ${QUERYFILES?}
#do
#    QUERYNAME=`basename ${SQLFILE} .sql`
#    echo "............. Query ${CASE}.$QUERYNAME ..................."
#    QUERYFILE=${CASEDIR?}/${QUERYNAME?}.sql
#    echo ".mode csv" > ${SCRIPT?}
#    echo ".headers on" >> ${SCRIPT?}
#    cat  ${QUERYFILE} >> ${SCRIPT?}
#    OUTFILE=${CASEDIR?}/.build/${QUERYNAME}.csv
#    cat ${SCRIPT?}
#    echo
#    echo "..... execution: $QUERYNAME ........."
#    sqlite3 $DB <${SCRIPT?} >${OUTFILE?}
#    cat ${OUTFILE?}
#    echo
#done
#
#
#
#
#rm ${SCRIPT?}
#rm ${CSVINPUT?}
#rmdir ${TMPDIR?}
