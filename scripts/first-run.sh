#!/bin/bash

# prompt colors
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

#
# check to see if already ran
#
if [ ! -d ./.first-run ]; then

read -p "Enter name of new service: " service_name

if [[ -z ${service_name} ]]; then
    # error
    echo "${red}Please enter a valid service name.${reset}"
    exit 0
fi

read -p "Enter git repo name: " git_repo_name

if [[ -z ${git_repo_name} ]]; then
    # error
    echo "${red}Please enter a valid git repository name.${reset}"
    exit 0
fi

#
# Originally tried to do find . but got too complex and sed was complaining about non-supported file types.
#
# Code is here if someone wants to figure out all the issues
# - find in all files, /gp prints lines and -n silents everything
# - skipping a few folders
# - find . \( -path ./venv -prune -o -path ./.git -prune -o -path ./scripts -prune \) -type f -print0 | xargs -0 sed -n -e "s/package_server/${name}_server/gp"
# - find . \( -path ./venv -prune -o -path ./.git -prune -o -path ./scripts -prune \) -type f -print0 | xargs -0 sed -n -e "s/package_grpc/${name}_grpc/gp"
#

#
# Create a few lists to scan
# Modify the files and folders first
#
declare -a file_list_root=(
  "./protos/v1/recommendations.proto"
  "./scripts/gen_protos.sh"
  "./pyproject.toml"
  "./pylintrc"
  "./Makefile"
#  "./.vscode/launch.json"
#  "./.vscode/settings.json"
#  "./.pre-commit-config.yaml"
  )

declare -a file_list_servicer=(
  "./servicer/mypy.ini"
  "./servicer/Dockerfile"
  "./servicer/CHANGELOG.md"
  "./servicer/README.md"
  "./servicer/MANIFEST.in"
  "./servicer/pyproject.toml"
  "./servicer/setup.py"
  "./servicer/pylintrc"
  "./servicer/src/package_server/__main__.py"
  "./servicer/src/package_server/recommendations.py"
  "./servicer/src/package_server/server.py"
  "./servicer/tests/test_base.py"
  "./servicer/tests/test_recommendations.py"
  "./servicer/tests/test_server.py"
  "./servicer/tests/test_something.py"
  "./servicer/docs/source/index.rst"
  "./servicer/docs/source/modules.rst"
  "./servicer/docs/source/package_server.rst"
  "./servicer/requirements.txt"
  )

declare -a file_list_grpc=(
  "./servicer_grpc/CHANGELOG.md"
  "./servicer_grpc/MANIFEST.in"
  "./servicer_grpc/pyproject.toml"
  "./servicer_grpc/setup.py"
  "./servicer_grpc/docs/source/index.rst"
  "./servicer_grpc/docs/source/modules.rst"
  "./servicer_grpc/docs/source/package_grpc.rst"
  "./servicer_grpc/src/package_grpc/__init__.py"
  "./servicer_grpc/src/package_grpc/v1/__init__.py"
  "./servicer_grpc/tests/test_something.py"
)
  #
  # fix up these "special files" as not sure why they don't work in the array
  #
  sed -n -e "s/package_server/${service_name}_server/g" "./.vscode/launch.json"
  sed -n -e "s/package_server/${service_name}_server/g" "./.pre-commit-config.yaml"
  sed -n -e "s/package_grpc/${service_name}_grpc/g" "./.pre-commit-config.yaml"

  for file in "${file_list_root[@]}" "${file_list_servicer[@]}" "${file_list_grpc[@]}"; do
    echo "modifying file: ${file}"
    sed -i~ -e "s/package_server/${service_name}_server/g" $file
    sed -i~ -e "s/package_grpc/${service_name}_grpc/g" $file
    sed -i~ -e "s/package-grpc/${service_name}-grpc/g" $file
  done

  #
  # Now modify the requirements.txt
  sed -i~ -e "s/python-services-template.git/${git_repo_name}.git/g" ./servicer/requirements.txt

  #
  # Now modify file names & folder names
  #
  mv ./servicer/docs/source/package_server.rst ./servicer/docs/source/${service_name}_server.rst
  mv ./servicer/src/package_server ./servicer/src/${service_name}_server/

  mv ./servicer_grpc/docs/source/package_grpc.rst ./servicer_grpc/docs/source/${service_name}_grpc.rst
  mv ./servicer_grpc/src/package_grpc ./servicer_grpc/src/${service_name}_grpc/

  #
  # Next reset the version strings
  #
  sed -i~ -e "s/[0-9][\.][0-9][\.][0-9]/0.0.0/g" ./servicer/src/${service_name}_server/__init__.py
  sed -i~ -e "s/[0-9][\.][0-9][\.][0-9]/0.0.0/g" ./servicer_grpc/src/${service_name}_grpc/__init__.py

  #
  # Cleanup the Changelogs
  #
  sed -i~ '4,$d' ./servicer/CHANGELOG.md
  sed -i~ '4,$d' ./servicer_grpc/CHANGELOG.md

  #
  # Cleanup all the modified files
  #
  for file in $(find . -name "*~"); do
    rm -f $file
  done

  #
  # Create Firstrun file
  #
  touch ./.first-run

  #
  # Stage & commit all the changes
  #
  git add .
  make setup-all
  make install-all-dev
  . venv/bin/activate && git commit -m "fix: Fixing up the names for first-run"

else

echo "${red}First run script already ran.${reset}"

fi
