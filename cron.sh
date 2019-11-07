#!/bin/bash

# Check for an interactive shell
if [ -z "$PS1" ]; then
    INTERACTIVE=0
else
    INTERACTIVE=1
fi

PATH="/usr/local/bin:${PATH}"
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TERMINAL_NOTIFIER=`which terminal-notifier`

if [ ! -e $TERMINAL_NOTIFIER ]; then
    [ "${INTERACTIVE}" -eq "1" ] && echo "terminal-notifier does not exist on the path"
    exit 1
fi


NOTIF_ARGS="-appIcon $BASE_DIR/camping.png"

if [ -z "$VIRTUAL_ENV" ]; then
    [ "${INTERACTIVE}" -eq "1" ] && echo "Not running in a virtualenv, this is not recommended! Set up your virtualenv use it by setting VIRTUAL_ENV"
    result=`$BASE_DIR/camping.py -m ${@:1}`
else
    result=`$VIRTUAL_ENV/bin/python $BASE_DIR/camping.py -m ${@:1}`
fi

# See if there were any hits

if [ -z "$result" ] ; then
    # No sites available
else
    # We've got a site available
    # Send to the Notification Center
    $TERMINAL_NOTIFIER $NOTIF_ARGS \
        -title "Campsites Are Available" \
        -message "$result"
fi
