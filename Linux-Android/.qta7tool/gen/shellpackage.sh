#!/bin/bash -
#===============================================================================
#
# FILE: shell_pack.sh
#
# USAGE: ./shell_pack.sh
#
# DESCRIPTION:
#
# OPTIONS: ---
# REQUIREMENTS: ---
# BUGS: ---
# NOTES: ---
# AUTHOR: lwq (28120), scue@vip.qq.com
# ORGANIZATION:
# CREATED: 04/22/2015 02:38:01 PM CST
# REVISION: ---
#===============================================================================

#=== FUNCTION ================================================================
# NAME: usage
# DESCRIPTION: Display usage information.
#===============================================================================
function usage ()
{
        cat <<- EOT
  Usage : $0 -p package -s script file1 file2 file3 ..
  Options:
  -h|help         Display this message
  -p|package      The output package name
  -s|script       The script will run when unpack package
  Other           The all files what you want to pack
EOT
} # ---------- end of function usage ----------

#-----------------------------------------------------------------------
# Handle command line arguments
#-----------------------------------------------------------------------

while getopts ":hp:s:" opt
do
  case $opt in

    h|help ) usage; exit 0 ;;
    p|package ) package_name=$OPTARG ;;
    s|script ) install_script=$OPTARG ;;
    \? ) echo -e "\n Option does not exist : $OPTARG\n"
          usage; exit 1 ;;

  esac # --- end of case ---
done
shift $(($OPTIND-1))

if [[ -z $package_name ]]; then
    echo "package_name can't not be empty"
    usage
    exit
fi

if [[ -z $package_name ]]; then
    echo "install_script can't not be empty"
    usage
    exit
fi

files=$@

generate_wrapper_script(){
    local install_script=$1
    local wrapper_script=$2
    cat <<-'EOT' >$wrapper_script
#!/bin/sh
echo "begin ..."
#unpackdir=/tmp/$(basename $0)_unpack
#rm -rf $unpackdir 2>/dev/null
#mkdir -p $unpackdir
#unpackdir=./
echo "unpacking ..."
sed '1, /^#__SCRIPTEND__/d' $0 | tar zxf - -C ./
if [ $? -ne 0 ]; then
    echo "unpack package failed."
    exit 1
fi
echo "installing ..."
# cd $unpackdir
EOT
    cat <<-EOR >>$wrapper_script
chmod +x $install_script
./$install_script
EOR
    cat <<-'EOE' >>$wrapper_script
if [ $? -ne 0 ]; then
    echo "install failed."
    exit 2
# elif [[ -d $unpackdir ]]; then
# rm -rf $unpackdir
fi
echo "install ok, enjoy!"
exit 0
#__SCRIPTEND__
EOE
}

tarfile=package_content_$$.tgz
wrapfile=wrap_$$.sh

echo -e "start packing ..\n"
tar zcvf $tarfile $files $install_script
generate_wrapper_script $install_script $wrapfile
cat $wrapfile $tarfile > $package_name
chmod +x $package_name

echo -e "\noutput: $package_name\n"

rm -f $tarfile
rm -f $wrapfile
