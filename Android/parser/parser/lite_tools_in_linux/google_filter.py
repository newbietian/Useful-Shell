import re
import sys
import os
import time
import threading

# 用来剔除git log记录中包含google|intel|android|arm的 工具，最后会新生成一份commit log

PAT_COMMIT = r"^commit [\da-z]+$"
PAT_AUTHOR = r"^Author: .+<.+@(?:google|intel|android|arm).com>$"
PAT_MERGE = r"^Merge: .+$"

class LineReader(file):
    def __init__(self, name, mode):
        super(LineReader, self).__init__(name, mode)
        self.line_num=0

    def readline(self,size=None):
        if not size:
            line = super(LineReader, self).readline()
        else:
            line = super(LineReader, self).readline(size)
        self.line_num += 1
        return line

    def rollbackline(self, offset):
        try:
            super(LineReader, self).seek(offset, 1)
            self.line_num-=1
        except IOError as ioe:
            print "IOError: " , ioe.strerror

# 0 - 100
PERCENT = 0

def show_progress():
    global PERCENT
    while(PERCENT <= 100):
        bar_length = 20
        hashes = '#' * int(PERCENT / 100.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [%s] %d%%" % (hashes + spaces, PERCENT))
        sys.stdout.flush()
        if PERCENT == 100:
            print
            break
        time.sleep(0.5)

def progress_test():
    global PERCENT
    while(PERCENT <= 100):
        PERCENT+=1
        time.sleep(0.5)


if __name__=="__main__":

    # test pattern
    # commit = "commit 16664fe9698f95463040946b915ef9c4502028b1"
    # m = re.match(PAT_COMMIT, commit)
    # if m:
    #     print "commit success"
    #
    # author = "Author: Shangbing Hu <shangbing.hu@google.com>"
    # m = re.match(PAT_AUTHOR, author)
    # if m:
    #     print "author success"
    #
    # date = "Date:   Tue Aug 15 15:13:13 2017 +0800"
    #m = re.match()
    # merge = "Merge: d9ca7ae 91d19d5"
    # m = re.match(PAT_MERGE, merge)
    # if m:
    #     print "merge success"
    #
    # exit(1)
    if not len(sys.argv) == 3:
        print "Usage: python google_filter.py [src_path] [dest_path]"
        exit(1)

    src_path = sys.argv[1]
    if not src_path or src_path == '' or not os.path.isfile(src_path):
        print "Usage: python google_filter.py [src_path] [dest_path]"
        exit(1)

    dest_path = sys.argv[2]
    if not dest_path or dest_path == '':
        print "Usage: python google_filter.py [src_path] [dest_path]"
        exit(1)

    # make a copy of file
    print "making copy... "
    src_path_copy = src_path+".tgf"
    code = os.system("cp " + '"' + src_path + '" ' + '"' + src_path_copy + '"' )
    # code == 0 is success
    if code != 0:
        print "Error in copy ", src_path
        exit(1)
    else:
        print "making copy done."

    fw = None
    try:
        fw = open(dest_path, 'w')
    except IOError as e:
        print "IOError: create dest_file \"{}\" failed".format(dest_path)

    # start progress thread
    thread1 = threading.Thread(target=show_progress)
    thread1.setDaemon(True)
    thread1.start()

    # read copy
    total_byte = os.path.getsize(src_path_copy)
    unit_byte = total_byte / 100

    fr=LineReader(src_path_copy, 'r')
    line="#"
    while(line):
        line = fr.readline()

        PERCENT = fr.tell() / unit_byte

        m = re.match(PAT_COMMIT, line)
        if m:
            next_line = fr.readline()

            # some paragraph has merge below commit
            if re.match(PAT_MERGE, next_line):
                next_line = fr.readline()

            if re.match(PAT_AUTHOR, next_line):
                continue
            else:
                # line
                fw.write(line)
                # next_line
                fw.write(next_line)

                inner="#"
                while inner:
                    inner = fr.readline()
                    if re.match(PAT_COMMIT, inner):
                        fr.rollbackline(-len(inner))
                        break
                    else:
                        fw.write(inner)

    PERCENT = 100

    fr.close()
    fw.close()

    thread1.join()
    # delete src copy
    print "delete src copy..."
    code = os.system("rm " + '"' + src_path_copy + '"')
    if code != 0:
        print "delete src copy failed"
    else:
        print "delete src copy done."
    print "Done"

