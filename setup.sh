#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLATFORM=`$BASEDIR/thirdparty-binaries/tools/platform_name.sh`

`$BASEDIR/thirdparty-binaries/setup.sh`

VERSIONED_PYTHON="python3.5"
PREBUILT_PYTHON="$BASEDIR/thirdparty-binaries/pre-built/current_platform/python/bin/${VERSIONED_PYTHON}"
SYSTEM_PYTHON=$(which python3.5 || which python)
SYSTEM_VERSIONED_PYTHON=$(which "$VERSIONED_PYTHON")
VENV="$BASEDIR/env/bin"
VENV_PYTHON="$VENV/python"

if [ -x "$SYSTEM_VERSIONED_PYTHON" ]
then
  PYTHON_TO_INSTALL="$SYSTEM_VERSIONED_PYTHON"
elif [ -x "$PREBUILT_PYTHON"  ]
then
  PYTHON_TO_INSTALL="$PREBUILT_PYTHON"
else
  echo "No $VERSIONED_PYTHON available on the system!" >&2
  exit 1
fi

"$PYTHON_TO_INSTALL" -m venv "$BASEDIR/env"
ln -nsf "$BASEDIR/env/lib/${VERSIONED_PYTHON}/site-packages" "$BASEDIR/site-packages"

PACKAGES="$BASEDIR/thirdparty/python/dev_requirements.txt"

"$VENV_PYTHON" -m pip install \
    --no-cache-dir \
    --no-index \
    --find-links "$BASEDIR/thirdparty-binaries/python/wheels" \
    -r "$PACKAGES"
