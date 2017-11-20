#!/bin/bash

function printSuccess()
{
    local str=$1
    echo -e "\033[32m$str\033[0m"
}

function printFailed()
{
    local str=$1
    echo -e "\033[31m$str\033[0m"
}

configPath()
{
    local CFG=""
    if [ -n "`which zenity`" ]; then
        CFG=`zenity --forms \
          --title="QtA7 Config" \
          --width=200 \
          --height=100 \
          --add-entry="项目根目录" \
          --add-entry="Qt根目录" \
          --add-entry="SDK根目录"`
        echo $CFG
    else
        echo -1
    fi
}

checkWritePermission()
{
    local path=$1
	if [ ! -d "$path" ];
	then
	    printFailed "NO $path FOUND"
	    exit 1
	fi
    if [ ! -w $path ];then
        printFailed "No Write Permission, Please use 'sudo'"
        exit 1
    fi
}

##################
# DEFINE START
##################
cfgName=".qta7tool.cfg"
cfgDir=".qta7tool"

VERSION="version 1.2"
NAME="QtA7"

# DON'T MODIFY
DESKTOP="/usr/share/applications"
CONFIG_FILE="$DESKTOP/QtA7.desktop"

EXEC="$HOME/$cfgDir/start/qt-start.sh"
ICON="$HOME/$cfgDir/start/res/fake_qt.png"

Exec_Package="$HOME/$cfgDir/build/package.sh"
Exec_Cp2UDisk="$HOME/$cfgDir/usb/cp2udisk.sh"

#TODO Add Desktop Action

##################
# DEFINE END
##################

# check whether run in sudo
checkWritePermission $DESKTOP

# read -p "项目根目录 (e.g /home/xx/work/Project):" PRODIR
# if [ -z $PRODIR ] || [ $PRODIR != $PWD ]; then
#     printFailed "please run script in your project root dir"
#     exit 1
# fi

# get the configpath return
usrInput=`configPath`
# Array separator 
IFS="|"
# convert to array
usrInput=($usrInput)
# 项目根目录，去除结尾“/”
PRODIR=${usrInput[0]}
PRODIR=${PRODIR%"/"}
# Qt安装目录，去除结尾“/”
QTCREATOR=${usrInput[1]}
QTCREATOR=${QTCREATOR%"/"}
# A7SDK目录，去除结尾“/”
A7SDK=${usrInput[2]}
A7SDK=${A7SDK%"/"}

echo $PRODIR $QTCREATOR $A7SDK

##################
# create config
##################
echo "# Qt A7 tool configuration
VERSION=$VERSION
NAME=$NAME
PRODIR=$PRODIR
QTCREATOR=$QTCREATOR
A7SDK=$A7SDK
" > "$HOME/$cfgName"

# mv .qta7tool directoty to $HOME
if [ -d "$HOME/$cfgDir" ]; then
    rm -rf $HOME/$cfgDir
fi
mv $cfgDir $HOME
if [ ! -d "$HOME/$cfgDir" ]; then
    printFailed "Failed to find tools directory! install failed!"
    exit 1
fi

##################
# create Desktop App
##################
touch "$CONFIG_FILE"
echo "
[Desktop Entry]
Version=$VERSION
Name=$NAME
Exec=$EXEC
Terminal=false
Icon=$ICON
Type=Application
Actions=Package;Cp2UDisk;
Categories=Development

[Desktop Action Package]
Name=Package output
Exec=$Exec_Package
OnlyShowIn=Unity;

[Desktop Action Cp2UDisk]
Name=Copy package to udisk
Exec=$Exec_Cp2UDisk
OnlyShowIn=Unity;
" > $CONFIG_FILE

printSuccess "创建app成功
>>> 请在Dash中查找$NAME
>>> 拖至启动器中
>>> 即可一键启动"
exit 0
