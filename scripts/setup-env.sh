#!/bin/bash

#
#  Setup-env.sh
#
#   Script to setup specific environment variables for the repository.  This can't restart the bash shell (yet)
#   so we just warn the user to restart.
#
restart=false
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

# This token needs to be added for use with any services that need to pull from GITHUB
if [[ -z "${PASSPORT_CI_TOKEN}" ]]; then
    export ci_title="\n# PASSPORT_CI needed variables"
    export ci_env_vars="export PASSPORT_CI_TOKEN=\$GITHUB_TOKEN\n"

    echo $ci_title >> ~/.bash_profile
    echo "$ci_env_vars" >> ~/.bash_profile

    restart=true
elif [ "${GITHUB_TOKEN}" != "${PASSPORT_CI_TOKEN}" ]; then
    echo "${red} PASSPORT_CI_TOKEN value doesn't math GITHUB_TOKEN, please update!${reset}"
fi

if $restart; then
    echo "${red}RESTART terminal as environment variables weren't set.${reset}"
fi
