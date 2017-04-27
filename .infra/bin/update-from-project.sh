#!/usr/bin/env bash
SCRIBESINFRA=~/DEV/ScribesZone/ScribesInfra/

function updateItem {
    # update a directory or file in ScribesInfra
    # from a directory or a file
    #
    # updateItem <project> <item>
    #
    # e.g.
    #
    #   updateItem SphinxZone sphinxdata
    #   updateItem SphinxZone sphinxdata
    #

    project=${1?}
    item=${2?}
    sourceitem=$SCRIBESINFRA/../${project?}/${item?}
    targetitem=${SCRIBESINFRA?}/${item?}
    if [ -d "${sourceitem?}" ]
    then
        echo "    updating directory ${item?}/ from ${project?}"
#        rm -rf ${targetitem?}
#        cp -r ${sourceitem?} ${targetitem?}
    elif [ -f "${sourceitem?}" ]
    then
        echo "    updating file ${item?} from ${project?}"
        # cp ${sourceitem?} ${targetitem?}
    else
        echo "**ERROR** ${sourceitem?} does not exist!" > /dev/stderr
    fi

    #
}

function updateProjectItems {
    # updateProjectItems <project>
    project=${1?}
    echo "updating ${project?}"
    projectdir=$SCRIBESINFRA/../${project?}
    projectfilespec=${projectdir?}/.scribesinfra
    for item in `cat ${projectfilespec}`
    do
        updateItem ${project?} ${item?}
    done
}

function publish {
    # publish <project>
    project=${1?}
    echo "publishing ${project?}"
    git -C ${SCRIBESINFRA?} add .
    git -C ${SCRIBESINFRA?} commit -am 'update ${project?}'
    git -C ${SCRIBESINFRA?} push origin master
}

function updateAndPublish {
    # updateAndPublish <project>
    project=${1?}
    updateProjectItems ${project?}
    publish ${project?}
}



if [ "$1" == "" ]
then
    PROJECTSFILE=${SCRIBESINFRA?}/.infra/projects.txt
    for project in `cat ${PROJECTSFILE?}`
    do
        updateAndPublish ${project?}
    done
else
    updateAndPublish ${1?}
fi