#!/bin/bash

error()
{   local error=$1
    if [ -n "`which zenity`" ]; then
        zenity --error --title="Error" --text="QtA7\n$error"
    fi
}

success()
{
    local info=$1
    if [ -n "`which zenity`" ]; then
        zenity --info --title="Info" --text="QtA7\n$info"
    fi
}

USB="/media/PT"

cfgName=".qta7tool.cfg"
CFGFILE="$HOME/$cfgName"
PRODIR=`sed '/^PRODIR=/!d;s/.*=//' $CFGFILE`
BUILD_DIR="$PRODIR/output"
HMI_UPDATE="hmi-update.tar"

if [ ! -d "$USB" ];then
    error "cp失败"
    exit 1
fi

rm -rf "$USB/$HMI_UPDATE"

`cp $BUILD_DIR/$HMI_UPDATE $USB`
if [ $? -ne 0 ];then
    error "cp失败"
    exit 1
fi
success "升级包copy完成"
exit 0
