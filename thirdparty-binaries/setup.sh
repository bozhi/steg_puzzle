BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PREBUILT_DIR=$BASEDIR/pre-built
PLATFORM=$($BASEDIR/tools/platform_name.sh)

ln -nsf $PREBUILT_DIR/$PLATFORM $PREBUILT_DIR/current_platform
