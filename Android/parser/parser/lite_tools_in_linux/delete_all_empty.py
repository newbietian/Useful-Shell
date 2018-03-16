# coding=utf-8

import sys
import os
import re

# 删除指定目录所有指定格式的文件。

def checkDirExists(path):
    return os.path.isdir(path)


def clearBlankLine(file_path):
    file1 = open(file_path, 'r')  # 要去掉空行的文件
    file2 = open(file_path + ".bak", 'w')  # 生成没有空行的文件
    try:
        for line in file1.readlines():
            if not re.match(r"^\d", line):
                continue
            m = re.match(r"^(.*)(\s+)$", line)
            if m:
                print m.group(1)

            file2.write(line)
            return
    finally:
        file1.close()
        file2.close()
        #os.system("rm -f %s" % file_path)
        #os.system("mv %s.bak %s" % (file_path, file_path))



if __name__ == "__main__":

    # f = "/home/pt/Downloads/2018-03-07_10_30_46/2018-03-07_10_30_46/1d46901f/com.android.chrome2018-03-08_20_05_23CRASH.log"
    # os.system("sed '/^\s*$/d' %s > %s.bak" % (f,f))
    # exit()

    args = sys.argv
    if not args or len(args) != 2:
        print "Usage: python delete_all_empty.py [Target_Folder]"
        exit(1)

    scripts, target_folder = args

    if not checkDirExists(target_folder):
        print "Target_Folder {} is not exist!".format(target_folder)

    enter = raw_input('Are you sure to delete all empty lines in {folder}?  Y/N: '.format(folder=target_folder))
    if enter.lower().startswith("y"):
        for root, sub_dirs, files in os.walk(target_folder):
            for file in files:
                file_path = os.path.join(root, file)
                print "Handing %s" % file_path
                os.system("sed '/^\s*$/d' %s > %s.bak" % (file_path, file_path))
                #os.system("cat %s |sed '/^$/d' > %s.bak" % (file_path, file_path))
                os.system("rm -f %s" % file_path)
                os.system("mv %s.bak %s" % (file_path, file_path))
                os.system("dos2unix %s" % file_path)
        print "Done"
    else:
        print "choose no, exit"
