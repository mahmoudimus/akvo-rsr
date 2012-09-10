#!/bin/bash

THIS_SCRIPT=$0

SHARED_SCRIPTS_HOME="$(cd `dirname $THIS_SCRIPT` && pwd)"
CONFIG_DIR="$(cd $SHARED_SCRIPTS_HOME/../config && pwd)"

DEPLOYMENT_SCRIPTS_DIR="$(cd "$SHARED_SCRIPTS_HOME/../.." && pwd)"
PIP_REQUIREMENTS_DIR="$DEPLOYMENT_SCRIPTS_DIR/pip/requirements"
VERIFIERS_DIR="$DEPLOYMENT_SCRIPTS_DIR/verifiers"

"$VERIFIERS_DIR/verify_system_packages.py"

# exit if any errors occurred while verifying the system packages
if [ $? -ne 0 ]; then
    printf "\n>> Unable to build virtualenv packages until system package dependencies have been resolved\n"
    exit -1
fi

DEV_EXECUTION_MODE='dev'

source "$CONFIG_DIR/load_config.sh" "rsr_env.config" $DEV_EXECUTION_MODE

function ensure_virtualenvs_home_exists
{
    CURRENT_USER=`whoami`
    USER_GROUP=`id -ng $CURRENT_USER`

    if [ ! -d "$VIRTUALENVS_HOME" ]; then
        sudo mkdir -p "$VIRTUALENVS_HOME"
        sudo chown $CURRENT_USER:$USER_GROUP "$VIRTUALENVS_HOME"
    fi
}

function ensure_rsr_virtualenv_exists
{
    ensure_virtualenvs_home_exists

    if [ ! -d "$RSR_VIRTUALENV_PATH" ]; then
        printf "\n>> Creating RSR virtualenv at $RSR_VIRTUALENV_PATH\n"
        virtualenv --distribute "$RSR_VIRTUALENV_PATH"
    else
        printf "\n>> Updating existing RSR virtualenv at $RSR_VIRTUALENV_PATH\n"
    fi
}

function exit_if_pip_not_installed
{
    PIP_PATH=`which pip`

    # check if pip is installed
    if [ -z "$PIP_PATH" ]; then
        printf "\n>> pip not installed or not on the PATH\n"
        printf "\n>> Current path: $PATH\n\n"
        exit -1
    fi
}

function install_packages_with_pip
{
    # function parameters:
    REQUIREMENTS_FILE_NAME=$1
    PACKAGE_SET_NAME=$2

    cd "$PACKAGE_DOWNLOAD_DIR"
    printf "\n>> Installing/upgrading $PACKAGE_SET_NAME packages:\n"
    pip install -M -r "$PIP_REQUIREMENTS_DIR/$REQUIREMENTS_FILE_NAME"

    if [ $? -ne 0 ]; then
        printf "\n## Package installation failed as above\n"
        exit -1
    fi
}

function install_rsr_and_infrastructure_packages
{
    printf "\n>> Fresh virtualenv should only contain the distribute and wsgiref packages:\n"
    pip freeze

    install_packages_with_pip "1_deployment.txt" "deployment"
    install_packages_with_pip "2_rsr.txt" "RSR"
    install_packages_with_pip "3_testing.txt" "testing"

    printf "\n>> Packages installed in the $VIRTUALENV_NAME virtualenv:\n"
    pip freeze
}

function install_rsr_packages_within_virtualenv
{
    ensure_rsr_virtualenv_exists

    printf "\n>> Working on virtualenv: $VIRTUALENV_NAME\n"
    source "$RSR_VIRTUALENV_PATH/bin/activate"

    # proceed if no errors occur when switching to the named virtualenv
    if [ $? -eq 0 ]; then
        install_rsr_and_infrastructure_packages
        printf "\n>> Deactivating virtualenv: $VIRTUALENV_NAME\n"
        deactivate
    else
        printf "\n>> Could not switch to $VIRTUALENV_NAME -- has this virtualenv been created?\n"
        exit -1
    fi
}


exit_if_pip_not_installed
install_rsr_packages_within_virtualenv
