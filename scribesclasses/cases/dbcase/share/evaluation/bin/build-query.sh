#!/usr/bin/env bash

# This file is not intended to be called from command line.
# It is called from build.py
#
# Evaluate one or more query for one or more groups for a given case study.
#
# For the usage see the function usage to type "build-query.sh"
#
# FIXME: For anonymous query (e.g. SELECT 2*3) the header in the result is the query itself
#        This leads to issue when the query is multiline as the header is no
#        longer on the first line. Since there is no separator beetween the
#        header and content, the best solution is to evaluate the request twice.
#        One with header mode of, for the content and once for the header.
#        In practice this case should never happened as thee results of the
#        query are always named and specified.
#
# FIXME: the csv generated by sqlite3 interpreter is not the same as sqlalchemy
#        This breaks comparison because some " are not always in the same places.
#        Workaround is suppressing quotes but this is not really safe.
#
# FIXME: null values are not represented as "null" using sqlalchemy
#        The null value is an option in sqlite3 interpreter
#        Using both ways breaks comparison
#
# TODO: improve verbose display for failure
#       display the error (and the actual query).qu
#


#echo "==============================================="
#echo PY_PATH=$PY_PATH
#echo PY_BIN=$PY_BIN
#echo "==============================================="

if [ "$PY_PATH" == "" ]
then
    echo 'env variables $PY_PATH and $PY_BIN must be set' >/dev/stderr
    exit 2
fi

OUTEXTENSION=csv


function usage {
    echo "NOT TO BE CALLED DIRECTLY:"
    echo "    build-query.sh <case> <group> <query> [-v]"
    echo
    echo "where"
    echo
    echo "    <case>    name of case (e.g. CyberFrais)"
    echo
    echo "    <group>   the specification of group(s) to apply on"
    echo "        .     for local usage in student group"
    echo "        05    for group key 05 from hq"
    echo
    echo "    <query>   the specification of the query to evaluate"
    echo "        010   for evaluating the query prefixed by 010"
    echo "        all   for evaluating all queries"
    echo "        -     no query is evaluated, sqlite3 is launched"
    echo
    echo "Examples"
    echo "--------"
    echo "    build-query.sh CyberCDs 03 all    # for headquarter usage"
    echo "    build-query.sh CyberCDs 03 010 -v  # for group usage"
    echo "    build-query.sh CyberCDs . 010      # for group usage"
    echo
    echo "Evaluation symbols"
    echo "------------------"
    echo "  O  OK"
    echo "  ^  wrong signature, content OK"
    echo "  x  shape OK, wrong content"
    echo "  |  wrong height, width OK"
    echo "  -  wrong width, height OK"
    echo "  #  wrong width, wrong height"
    echo "  $  failure"
    echo "  .  not implemented"
    echo "  ?  result is unavailable (in summary matrix)"
}


function isEmptySQL {
    # isEmptySQL <sqlfile>
    # ignore -- at begining of lines and blank lines
    egrep -v '^--|^[[:space:]]*$' ${1?} >/dev/null
}

function nbOfColumns {
    # nbOfColumns <csvfile>
    # Count the number of columns in the given csv file
    # The result is in $RESULT
    # Return 0 if the file is empty
    if [ -s "$1" ]
    then
        RESULT=$( \
            cat ${1?} \
            | awk -F, '{print NF}' \
            | sort -nu \
            | tail -n 1 \
        )
        # echo "//////$RESULT//"
    else
        # empty file
        RESULT=0
    fi
}


function buildQueryRSTFile {

    # TODO improve this function using MESSAGE and more

    mkdir -p ${RST_DIR?}

    # build the query file
    QUERY_RST_FILE=${RST_DIR?}/$QUERY_NAME.generated.rst
    PYTHONPATH=${PY_PATH?} ${PY_BIN?} -m sqlrst ${SQL_QUERY_FILE} $QUERY_RST_FILE

    # echo "--------------- ${SQL_ERRORS_FILE?}"
    if [ -s ${SQL_ERRORS_FILE?} ]
    then
        printf " \n\n" >> $QUERY_RST_FILE
        echo "Errors" >> $QUERY_RST_FILE
        printf "......\n\n" >> $QUERY_RST_FILE
        echo ".. literalinclude:: ../${SQL_ERRORS_FILE?}" >> $QUERY_RST_FILE
        echo " " >> $QUERY_RST_FILE
    fi

    printf " \n\n" >> $QUERY_RST_FILE
    echo "Resultat" >> $QUERY_RST_FILE
    echo "........" >> $QUERY_RST_FILE
    echo " " >> $QUERY_RST_FILE
    if [ -f ${ACTUAL_RESULT_FILE?} ]
    then
        if  [[ $(wc -l <${ACTUAL_RESULT_FILE?}) -ge 1 ]]
        then
            echo "..  csv-table::" >> $QUERY_RST_FILE
            echo "    :header-rows: 1" >> $QUERY_RST_FILE
            echo "    :file: ../../${ACTUAL_RESULT_FILE?}" >> $QUERY_RST_FILE

            echo " " >> $QUERY_RST_FILE
            if [ "$VERBOSE" == "1" ]
            then
                echo "ACTUAL RESULT FOR $GROUP_KEY $QUERY_NAME"
                echo "------------------------------------------------"
                cat ${ACTUAL_RESULT_FILE?}
            fi
        else
            echo "Empty result" >> $QUERY_RST_FILE
            if [ "$VERBOSE" == "1" ]
            then
                echo "ACTUAL RESULT FOR $GROUP_KEY $QUERY_NAME"
                echo "------------------------------------------------"
                echo "Empty result"
            fi
        fi
    else
        echo "No result" >> $QUERY_RST_FILE
        echo "Empty result" >> $QUERY_RST_FILE
        if [ "$VERBOSE" == "1" ]
        then
            echo "ACTUAL RESULT FOR $GROUP_KEY $QUERY_NAME"
            echo "------------------------------------------------"
            echo "No result"
        fi
    fi

    if [ -s ${DIFF_RESULT_FILE} ]
    then
        printf " \n\n" >> $QUERY_RST_FILE
        echo "Resultat attendu" >> $QUERY_RST_FILE
        echo "................" >> $QUERY_RST_FILE
        echo " " >> $QUERY_RST_FILE

        if  [[ $(wc -l <${EXPECTED_RESULT_FILE?}) -ge 0 ]]
        then
            echo "..  csv-table::" >> $QUERY_RST_FILE
            echo "    :header-rows: 1" >> $QUERY_RST_FILE
            echo "    :file: ../../${EXPECTED_RESULT_FILE?}" >> $QUERY_RST_FILE
            if [ "$VERBOSE" == "1" ]
            then
                echo
                echo "EXPECTED RESULT FOR $GROUP_KEY $QUERY_NAME"
                echo "------------------------------------------------"
                cat ${EXPECTED_RESULT_FILE?}
            fi
        else
            echo "Empty result" >> $QUERY_RST_FILE
            if [ "$VERBOSE" == "1" ]
            then
                echo
                echo "EXPECTED RESULT FOR $GROUP_KEY $QUERY_NAME"
                echo "------------------------------------------------"
                echo "Empty result"
            fi
        fi


        printf " \n\n" >> $QUERY_RST_FILE
        echo "Differences" >> $QUERY_RST_FILE
        echo "..........." >> $QUERY_RST_FILE
        echo " " >> $QUERY_RST_FILE

        echo ".. literalinclude:: ../${DIFF_RESULT_FILE?}" >> $QUERY_RST_FILE
        echo " " >> $QUERY_RST_FILE


        if [ "$VERBOSE" == "1" ]
        then
            echo
            echo "DIFFERENCES FOR $GROUP_KEY $QUERY_NAME"
            echo "------------------------------------------------"
            cat ${DIFF_RESULT_FILE}
        fi
    fi
}


function createTempDB {
    TEMP_DB=/tmp/db.sqlite3
    cp ${DB?} ${TEMP_DB?}
}

function evaluateQuery {
    #
    # This line generate |-separated result
    #   sqlite3 -header $3 -nullvalue null -list ${DB?} \
    createTempDB
    sqlite3 -header -nullvalue null -csv ${TEMP_DB?} \
        < ${SQL_QUERY_FILE?} \
        > ${ACTUAL_RESULT_FILE?} \
        2> ${SQL_ERRORS_FILE?}
    # Here we suppress \n and " in the comparison
    sed -i -e 's|\r||g' -e's|"||g' ${ACTUAL_RESULT_FILE?}
    # TODO: check why the dbcase system generate sometimes " and sometimes not
    # it seems that this is due to the fact that sqlalchemy has a different
    # behavior that sqlite3 command liine.
}


function compareSignature {
    ACTUAL_SIGNATURE=`head -1 ${ACTUAL_RESULT_FILE?}`
    EXPECTED_SIGNATURE=`head -1 ${EXPECTED_RESULT_FILE?}`

    if [ "$ACTUAL_SIGNATURE" != "$EXPECTED_SIGNATURE" ]
    then
        QUERY_WRONG_SIGNATURE=1
        echo $ACTUAL_SIGNATURE > ${DIFF_SIGNATURE_FILE?}
        echo $EXPECTED_SIGNATURE >> ${DIFF_SIGNATURE_FILE?}
    else
        QUERY_WRONG_SIGNATURE=0
    fi
}

function compareRowNumber {
    ACTUAL_ROW_NB=`tail -n +2 ${ACTUAL_RESULT_FILE?} | wc -l`
    EXPECTED_ROW_NB=`tail -n +2 ${EXPECTED_RESULT_FILE?} | wc -l`
    DIFF_ROW_NB=`expr $ACTUAL_ROW_NB - $EXPECTED_ROW_NB`
    if [ "$DIFF_ROW_NB" -ne 0 ]
    then
        QUERY_WRONG_HEIGHT=1
    else
        QUERY_WRONG_HEIGHT=0
    fi
    # echo "Rows: $ACTUAL_ROW_NB vs $EXPECTED_ROW_NB"
}

function compareColumnNumber {
    nbOfColumns ${ACTUAL_RESULT_FILE?}
    ACTUAL_COLUMN_NB="$RESULT"
    nbOfColumns ${EXPECTED_RESULT_FILE?}
    EXPECTED_COLUMN_NB="$RESULT"
    DIFF_COLUMN_NB=`expr $ACTUAL_COLUMN_NB - $EXPECTED_COLUMN_NB`

    if [  "$DIFF_COLUMN_NB" == "0" ]
    then
        QUERY_WRONG_WIDTH=0
    else
        QUERY_WRONG_WIDTH=1
    fi
#    echo "******** ACTUAL_RESULT_FILE = $ACTUAL_RESULT_FILE"
#    echo "******** EXPECTED_RESULT_FILE = $EXPECTED_RESULT_FILE"
#    echo "******** ACTUAL_COLUMN_NB = $ACTUAL_COLUMN_NB"
#    echo "******** EXPECTED_COLUMN_NB = $EXPECTED_COLUMN_NB"
#    echo "******** DIFF_COLUMN_NB = $DIFF_COLUMN_NB"
#    echo "******** QUERY_WRONG_WIDTH = $QUERY_WRONG_WIDTH"

#    echo "******** QUERY_WRONG_WIDTH = $QUERY_WRONG_WIDTH"

}


function compareContent {
    # remove the header and compare the lines
    # sort the content to avoid difference due to result order
    # This could be too much for ORDER BY query, but not so much frequent
    diff \
        <(tail -n +2 ${EXPECTED_RESULT_FILE?} | sort) \
        <(tail -n +2 ${ACTUAL_RESULT_FILE?} | sort)   \
        -y --suppress-common-lines > ${DIFF_RESULT_FILE}

    if [ -s ${DIFF_RESULT_FILE} ]
    then
        QUERY_WRONG_CONTENT=1
    else
        QUERY_WRONG_CONTENT=0
    fi
}

function processQuery {
       # processQuery <query>
       # execute a query
    QUERY=${1?}
    SQL_QUERY_FILE=${SOURCE_SQL_QUERY_DIR?}/${QUERY?}*.sql
    # TODO: add a test to check that there is one and only one .sql file

    if [ ! -f ${SQL_QUERY_FILE?} ]; then
        echo "********* Query $QUERY file does not exist. Not found: $SQL_QUERY_FILE" > /dev/stderr
        echo "          Query $QUERY ignored"
        return
    fi


    mkdir -p ${ACTUAL_STATE_DIR?}

    QUERY_NAME=`basename ${SQL_QUERY_FILE?} .sql`
    ACTUAL_RESULT_FILE=${ACTUAL_STATE_DIR?}/${QUERY_NAME?}.${OUTEXTENSION?}
    EXPECTED_RESULT_FILE=${EXPECTED_STATE_DIR?}/${QUERY_NAME?}.${OUTEXTENSION?}
    DIFF_RESULT_FILE=${ACTUAL_STATE_DIR?}/${QUERY_NAME?}.data.diff
    DIFF_SIGNATURE_FILE=${ACTUAL_STATE_DIR?}/${QUERY_NAME?}.sig.diff
    SQL_ERRORS_FILE=${ACTUAL_STATE_DIR?}/${QUERY_NAME?}.err
    QUERY_SUMMARY_FILE=${ACTUAL_STATE_DIR?}/${QUERY_NAME?}.summary.txt
    ACTUAL_QUERY_FILE=${ACTUAL_STATE_DIR?}/${QUERY_NAME?}.sql

    cp ${SQL_QUERY_FILE?} ${ACTUAL_QUERY_FILE?}


    QUERY_NOT_IMPLEMENTED=0
    QUERY_FAILURE=0
    QUERY_WRONG_WIDTH=0
    QUERY_WRONG_HEIGHT=0
    QUERY_WRONG_CONTENT=0
    QUERY_WRONG_SIGNATURE=0


    if ! isEmptySQL $SQL_QUERY_FILE
    then
        QUERY_NOT_IMPLEMENTED=1
        QUERY_STATUS="."
        QUERY_MESSAGE="not implemented"
    else
        QUERY_NOT_IMPLEMENTED=0

        evaluateQuery
#        echo "///////////////////////////////////////////"
#        cat ${SQL_ERRORS_FILE}
#        wc ${SQL_ERRORS_FILE}
#        echo "///////////////////////////////////////////"
        if [ -s "${SQL_ERRORS_FILE?}" ]
        then
#            echo "ERROR"
            QUERY_FAILURE=1
            QUERY_STATUS="$"
            QUERY_MESSAGE="execution failure"

        else
#            echo "NO ERROR"
            QUERY_FAILURE=0

            compareColumnNumber
            compareRowNumber
            compareContent


            if [ "${QUERY_WRONG_WIDTH?}" -ne 0 ] && [ "${QUERY_WRONG_HEIGHT?}" -ne 0 ]
            then
                QUERY_WRONG_SHAPE=1
                QUERY_STATUS='#'
                QUERY_MESSAGE="wrong width ($ACTUAL_COLUMN_NB vs $EXPECTED_COLUMN_NB) and wrong height ($ACTUAL_ROW_NB vs $EXPECTED_ROW_NB)"
            elif [ "${QUERY_WRONG_WIDTH?}" -ne 0 ] && [ "${QUERY_WRONG_HEIGHT?}" -eq 0 ]
            then
#                echo "WW ${QUERY_WRONG_WIDTH?} $ACTUAL_COLUMN_NB instead of $EXPECTED_COLUMN_NB"
#                echo "WH ${QUERY_WRONG_HEIGHT?}"
#                echo "DIFF_COLUMN_NB $DIFF_COLUMN_NB"
                QUERY_WRONG_SHAPE=1
                QUERY_STATUS='-'
                QUERY_MESSAGE="wrong width ($ACTUAL_COLUMN_NB vs $EXPECTED_COLUMN_NB)"
#                echo [ "${QUERY_WRONG_WIDTH?}" -ne 0 ]
            elif [ "${QUERY_WRONG_WIDTH?}" -eq 0 ] && [ "${QUERY_WRONG_HEIGHT?}" -ne 0 ]
            then
                QUERY_WRONG_SHAPE=1
                QUERY_STATUS='|'
                QUERY_MESSAGE="wrong height ($ACTUAL_ROW_NB vs $EXPECTED_ROW_NB)"
            elif [ "${QUERY_WRONG_WIDTH?}" -eq 0 ] && [ "${QUERY_WRONG_HEIGHT?}" -eq 0 ]
            then
                QUERY_WRONG_SHAPE=0
                if [ ${QUERY_WRONG_CONTENT?} -ne 0 ]
                then
                    QUERY_STATUS='x'
                    QUERY_MESSAGE="same sizes but wrong content"
                else
                    compareSignature    # set QUERY_WRONG_SIGNATURE
                    if [ $QUERY_WRONG_SIGNATURE -ne 0 ]
                    then
                        QUERY_STATUS="^"
                        QUERY_MESSAGE="same content but wrong signature"
                    else
                        QUERY_STATUS="O"
                        QUERY_MESSAGE="OK"
                    fi
                fi
            fi

        fi
    fi

    echo "$GROUP_KEY ${QUERY_STATUS?} ${QUERY_NAME?} -> ${QUERY_STATUS?}: ${QUERY_MESSAGE} "
    # save it to file for matrix later matrix building
    echo "${QUERY_STATUS?}" >${QUERY_SUMMARY_FILE?}
#    if [ "$VERBOSE" == "1" ]
#    then
#        echo $QUERY_MESSAGE
#    fi

    buildQueryRSTFile

    find ${CASE?} -wholename ${SQL_ERRORS_FILE} -size 0 -delete
    find ${CASE?} -wholename ${DIFF_RESULT_FILE} -size 0 -delete

}

#function displayMatrix {
#    _build-query-summary.py ${CASE?}
#}

function configure {
    if [ ${GROUP_PARAM} == "." ]
    then
        GROUP_KEY='.'    # not used unless for printing
        GROUP_DIR='.'    # not used

        # for Sandbox_             DB=${CASE?}/.build/states/default/${CASE?}_default.sqlite3
        DB=${CASE?}/${CASE?}_default.sqlite3
        SOURCE_SQL_QUERY_DIR=${CASE?}
        # for sandbox               ACTUAL_STATE_DIR=${CASE?}/.build
        ACTUAL_STATE_DIR=${CASE?}/.build/ActualStates
        EXPECTED_STATE_DIR=${CASE?}/ExpectedStates
        RST_DIR=${CASE?}/.build
    else
        GROUP_KEY=${1?}
        GROUP_DIR=../*-groups/*${GROUP_KEY}

        DB=${CASE?}/${CASE?}_default.sqlite3
        SOURCE_SQL_QUERY_DIR=${GROUP_DIR?}/${CASE?}
        ACTUAL_STATE_DIR=${CASE?}/.build/${GROUP_KEY}
        EXPECTED_STATE_DIR=${CASE?}/ExpectedStates
        RST_DIR=${CASE?}/.build/${GROUP_KEY}
    fi

}

function displayDirectories {
    echo "GROUP_KEY                 = $GROUP_KEY"
    echo "GROUP_DIR                 = $GROUP_DIR"
    echo "DB                        = $DB"
    echo "SOURCE_SQL_QUERY_DIR      = $SOURCE_SQL_QUERY_DIR"
    echo "ACTUAL_STATE_DIR          = $ACTUAL_STATE_DIR"
    echo "EXPECTED_STATE_DIR        = $EXPECTED_STATE_DIR"
    echo "RST_DIR                   = $RST_DIR"
}

function launchSqlite3 {
    createTempDB
    echo "NOTE: A temporary DB has been created from $DB"
    echo "      Database changes will not be saved"
    sqlite3 -header -nullvalue null -init sqlite3ini.txt ${TEMP_DB?}
}



function processAllQuery {
    # This is for all queries in the "group" directory
    # for _ITEM in `ls ${SOURCE_SQL_QUERY_DIR?}/*.sql`
    csv_files=`ls ${EXPECTED_STATE_DIR?}/*_*.csv 2>/dev/null`
    if [ $? -ne 0 ]
    then
        echo "******* Can't find csv file with ${EXPECTED_STATE_DIR?}/*_*.csv"  >/dev/stderr
        echo "        Check the spelling of $CASE}. Check also the content of directory"
        exit 1
    fi
    for _ITEM in ${csv_files?}
    do
        _Q=`basename ${_ITEM?} .csv`
        processQuery ${_Q?}
    done
}







function process {

    configure ${GROUP_PARAM}
    # displayDirectories


    if [ "$QUERY_PARAM" == "-" ]
    then
        # one parameter: launch the interpreter for the case
        launchSqlite3
    else
        if [ "$QUERY_PARAM" == "all" ]
        then
            processAllQuery
        else
            processQuery "$QUERY_PARAM"
        fi
    fi

}


if [ $# -ne 3 ] && [ $# -ne 4 ]
then
    echo "Illegal number of parameters"
    usage
    exit 1
fi


CASE=${1?}
GROUP_PARAM=${2?}
QUERY_PARAM=${3?}
if [ "$4" == "" ]
then
    VERBOSE=0
else
    VERBOSE=1
fi

process
