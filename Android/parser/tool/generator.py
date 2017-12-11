import os
import subprocess


def get_all_result_file(path):
    '''
    get readable file number in this path
    :param path: the path to be scanned
    :return: number
    '''
    list=[]
    try:
        source_dir = path
        for root, sub_dirs, files in os.walk(source_dir):
            for special_file in files:
                special_file_dir = os.path.join(root, special_file)
                try:
                    if special_file_dir.endswith(".re.json"):
                        list.append(special_file_dir)
                except Exception as x:
                    print "special_file_dir.endswith(.hex)", x.message
    except Exception as e:
        pass
    return list

def generate_list(list, target=''):
    target = target + '/FINAL.gen.list'
    final_list = open(target, "a+")
    for i in list:
        final_list.write(i+"\n")
    final_list.close()


def generate(list, target=''):
    generate_list(list, target)
    target = target + '/FINAL.gen.json'
    final_file = open(target, "a+")
    for i in list:
        ifp = open(i, "r")
        iall = ifp.read()
        final_file.write(iall+"\n")
        ifp.close()
    final_file.close()

if __name__ == '__main__':

    path = "/home/qinsw/pengtian/tmp/cmcc_monkey"

    list = get_all_result_file(path)

    generate(list, target = path)

