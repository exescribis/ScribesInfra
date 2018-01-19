#SCRIBES_HOME=/ext/INF/BDSI/Scribes
SCRIBES_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#-----------------------------------

VENV=${SCRIBES_HOME?}/venv
INFRA=${SCRIBES_HOME?}

PATH=${INFRA?}/bin:${VENV?}/bin:${PATH}
PYTHONPATH=${INFRA?}:${VENV?}:${PYTHONPATH}

export PATH
export PYTHONPATH
export SCRIBES_HOME

