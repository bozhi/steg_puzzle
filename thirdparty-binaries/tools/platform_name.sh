#!/bin/bash

set -e

OS=`uname -s`
MACHINE=`uname -m`

DISTRO="(unknown)"

if [ "$OS" == "Darwin" ]
then
  DISTRO="osx"
elif [ "$OS" == "Linux" ]
then
  if grep -iq "Debian" /etc/os-release 2>/dev/null
  then
    DISTRO="debian"
  elif grep -iq "b2qt" /etc/os-release 2>/dev/null
  then
    DISTRO="poky"
  elif grep -iq "Amazon Linux" /etc/os-release 2>/dev/null
  then
    DISTRO="amazonlinux"
  else
    echo "error: unrecognized Linux distribution!" >&2
    exit 1
  fi
else
  echo "error: unrecognized platform $OS:$MACHINE" >&2
  exit 1
fi

echo "${DISTRO}_${MACHINE}"
