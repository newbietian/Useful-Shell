# coding=utf8
import base64
import sys
import os


def f2b(file_path):
    try:
        os.remove(file_path + "__base64")
    except Exception as e:
        pass

    base64_str_file = open(file_path + "__base64", "wb")

    print "Processing..."
    try:
        with open(file_path, "rb") as f:
            while True:
                block = f.read(3 * 1024)
                if not block:
                    break
                base64_data = base64.b64encode(block)
                base64_str_file.write(base64_data)
            f.close()
            base64_str_file.close()
    except Exception as e:
        print "Error:" + e.message
        exit(-1)
    print "Done. >>  %s" % (file_path + "__base64")


def b2f(base64_file_path, target_name):
    try:
        os.remove(target_name)
    except Exception as e:
        pass

    target_file = open(target_name, "wb")

    print "Processing..."
    try:
        with open(base64_file_path, "rb") as f:
            while True:
                block = f.read(4 * 1024)
                if not block:
                    break
                raw_data = base64.b64decode(block)
                target_file.write(raw_data)
            f.close()
            target_file.close()
    except Exception as e:
        print "Error:" + e.message
        exit(-1)
    print "Done. >>  %s" % target_name


def error():
    print "Usage: python File2Base64.py -b <src_file_path>\n" \
          "                              -f <base64_file> <target_file>\n"
    exit(-1)


if __name__ == "__main__":
    if sys.argv[1] == '-b':
        if len(sys.argv) == 3:
            f2b(sys.argv[2])
        else:
            error()
    elif sys.argv[1] == '-f':
        if len(sys.argv) == 4:
            b2f(sys.argv[2], sys.argv[3])
        else:
            error()
    else:
        error()
    exit(0)