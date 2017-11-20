#!/bin/bash

#Function define
function CreatePkg()
{
    cfgName=".qta7tool.cfg"

    CFGFILE="$HOME/$cfgName"
    A7SDK=`sed '/^A7SDK=/!d;s/.*=//' $CFGFILE`
    PRODIR=`sed '/^PRODIR=/!d;s/.*=//' $CFGFILE`
    BUILD_DIR="$PRODIR/output"

    $A7SDK/sysroots/x86_64-pokysdk-linux/usr/bin/arm-linux-gnueabihf-strip --strip-unneeded $BUILD_DIR/arm/*
    
    echo "开始创建升级包..."
    
    # 进入output目录
    cd $BUILD_DIR

    OUTPUT_PATH="$BUILD_DIR/arm"
    HMI_UPDATE="hmi-update.tar"

    if [ ! -d $OUTPUT_PATH ]; then
        echo "Error: 请先进行代码编译"
        if [ -n "`which zenity`" ]; then
            zenity --error --title="Error" --text="Error: 请先进行代码编译"
        fi
        exit 1
    fi

    if [ -d "./bin" ]; then
        rm -r ./bin
    fi

    if [ -d "./lib" ]; then
        rm -r ./lib
    fi

    if [ -d "./$HMI_UPDATE" ]; then
        rm  ./$HMI_UPDATE
    fi

    mkdir ./bin
    mv $OUTPUT_PATH/HMI $OUTPUT_PATH/APPUPDATE $OUTPUT_PATH/UpdateBTAddress ./bin/.

    mv $OUTPUT_PATH lib
    tar cvf $HMI_UPDATE bin lib 

    mv lib $OUTPUT_PATH
    mv bin/HMI bin/APPUPDATE bin/UpdateBTAddress $OUTPUT_PATH

    rm -r bin
    echo "升级包创建完成..."
    
    if [ -n "`which notify-send`" ]; then
        notify-send "升级包创建完成"
    fi
}

CreatePkg
exit 0
