# coding=utf-8

import sys
import os



def checkDirExists(path):
    return os.path.isdir(path)

if __name__ == "__main__":

    args = sys.argv
    if not args or len(args) != 3:
        print "Usage: python deleteall.py [Target_Folder] [Target_end]"
        exit(1)

    scripts, target_folder, target_end = args

    if not checkDirExists(target_folder):
        print "Target_Folder {} is not exist!".format(target_folder)

    enter = raw_input('Are you sure to delete all "{0}" files in {1}?  Y/N: '.format(target_end, target_folder))
    if enter.lower().startswith("y"):
        for root, sub_dirs, files in os.walk(target_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(target_end):
                    code = os.system("rm -f " + '"' + file_path + '"')
                    if code != 0:
                        print " >>> Error in remove %s " % file_path
                    else:
                        print "remove %s done" % file_path
    else:
        print "choose no, exit"



