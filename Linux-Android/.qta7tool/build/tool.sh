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
        exit 0
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
    tar cvf P11-update.tar bin lib 

    mv lib $OUTPUT_PATH
    mv bin/HMI bin/APPUPDATE bin/UpdateBTAddress $OUTPUT_PATH

    rm -r bin
    echo "升级包创建完成..."
    
    if [ -n "`which notify-send`" ]; then
        notify-send "升级包创建完成"
    fi
}

function Update()
{
    echo "update start..."
    HMI_UPDATE="hmi-update.tar"

    if [ ! -f "./$HMI_UPDATE" ]; then
        echo "Error:"
        echo "无升级包或升级包和升级脚本不在同一目录"
        exit 0
    fi

    if [ ! -d "/usr/local/app" ]; then
        echo "Error:"
        echo "请在车机执行升级脚本！"
        exit 0
    fi

    mount -o remount rw /
    systemctl stop hmi
    #cp ./P11-update.tar /usr/local/app/.
    #cd /usr/local/app/.
    tar xvf $HMI_UPDATE -C /usr/local/app/.
    #rm ./P11-update.tar
    systemctl restart hmi

    echo "update finished..."
}

ISARGSOK=1

if [ "$#" -eq 0 ] ; then
    echo "Error:"
    echo "无参数！"
    exit 0
fi

if [ "$#" != 1 ] ; then
    echo "Error:"
    echo "参数过多！"
    exit 0
fi

declare -a arr=("-c" "--create" "-u" "--update")

######################################################################
#checkout argument for each
######################################################################
ISARGSOK=0
for i in "$@"
do
    if [ $1 == $i ] ; then
        ISARGSOK=1
        break
    fi
done

if [ $ISARGSOK -eq 0 ]; then
    echo "Error:"
    echo "Unknow argument: " $i
    exit 0
fi

case $1 in
    "-c")
        CreatePkg
        ;;
    "--create")
        echo "11111"
        CreatePkg
        ;;
    "-u")
        Update
        ;;
    "--update")
        Update
        ;;
esac
