#!/bin/bash

cfgName=".qta7tool.cfg"

CFGFILE="$HOME/$cfgName"
if [ ! -f $CFGFILE ];
then
    echo -e "\033[31m Please Run config.sh first! \033[0m"
    exit
fi

# SDK相关环境变量
sdk_env="environment-setup-cortexa7hf-vfp-poky-linux-gnueabi"
export A7SDK=`sed '/^A7SDK=/!d;s/.*=//' $CFGFILE`
A7SDK_ENV="$A7SDK/$sdk_env"
source $A7SDK_ENV
export CXXFLAGS="-isystem$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi/usr/include/c++/4.9.2/arm-linux-gnueabihf -isystem$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi/usr/include/c++/4.9.2 -isystem$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi/usr/include -O2 -pipe -feliminate-unused-debug-types"
export OE_QMAKE_CXXFLAGS="-isystem$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi/usr/include/c++/4.9.2/arm-linux-gnueabihf -isystem$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi/usr/include/c++/4.9.2 -isystem$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi/usr/include -O2 -pipe -g -feliminate-unused-debug-types -I$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi/usr/include/c++/4.9.2/backward"
export SYSROOT_DIR="$A7SDK/sysroots/cortexa7hf-vfp-poky-linux-gnueabi"

# 项目相关环境变量
export PRODIR=`sed '/^PRODIR=/!d;s/.*=//' $CFGFILE`
export BUILD_DIR="$PRODIR/output"

# 启动QtCreator
QTCREATOR=`sed '/^QTCREATOR=/!d;s/.*=//' $CFGFILE`
$QTCREATOR/Tools/QtCreator/bin/qtcreator.sh &
