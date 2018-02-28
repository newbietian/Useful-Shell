# coding=utf-8

import sys
import os
import re

# 目的： 去除.java.xml文件的patch

# 针对.java、.xml文件， 按行扫描， 如果开头第一个字符是+号， 则去除

def checkFileExists(path):
    return os.path.isfile(path)

def checkDirExists(path):
    return os.path.isdir(path)

def readfile(path):
    fp = open(path, "w")


if __name__ == "__main__":

    args = sys.argv
    if not args or len(args) != 2:
        print "Usage: python replacelineheader.py [Target_Folder]"
        exit(1)

    scripts, target_folder = args

    if not checkDirExists(target_folder) and not checkFileExists(target_folder):
        print "Target_Folder {} is not exist!".format(target_folder)
        exit(1)

    filelist = []

    print "Searching .java and .xml ..."
    if checkDirExists(target_folder):
        for root, sub_dirs, files in os.walk(target_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(".java") or file_path.endswith(".xml"):
                    filelist.append(file_path)
    elif target_folder.endswith(".java") or target_folder.endswith(".xml"):
        filelist.append(target_folder)
    else:
        print "searching done, no fit files"


    print "searching done."

    print "parsing..."

    for file in filelist:
        # open src and read
        print "handling %s ..." % file,
        fr = open(file, "r")

        file_tmp = file + ".tmp"
        fw = open(file_tmp, "w")
        line = "#"
        while (line):
            line = fr.readline()
            if not line or line == '':
                break

            #m = re.match(r'^\+(.*)?$', line)
            if line.startswith("+"):
                sub_line =  line[1:]
                fw.write(sub_line)
            else:
                fw.write(line)

        fr.close()
        fw.close()

        os.system("rm -f " + '"' + file + '"')
        os.system("mv " + '"' + file_tmp + '"' + " " + '"' + file + '"')
        print " done"

    print "All done"




