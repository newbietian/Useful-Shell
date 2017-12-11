# coding=utf-8
import json

from parser.tool.StringPattern import *


class Parser(object):
    def __init__(self, cfg_path, log_path, modules):
        self.cfg_path = cfg_path
        self.log_path = log_path
        self.modules = modules
        self.searcher=StringPattern()

    def set_config_path(self, path):
        self.cfg_path = path

    def set_log_path(self, path):
        self.log_path = path

    def __load_config__(self):
        with open(self.cfg_path, 'r') as json_file:
            data = json.load(json_file)
            return data

    def __index_of__(self, child, parent):
        self.searcher.set_pattern(child)
        self.searcher.set_source(parent)
        return self.searcher.string_pattern_bm()

    def __parse_crash__(self, logfp, rule):
        if rule == 'reason':
            location = logfp.readline().decode("utf-8").replace("\n", " ")
            # 恢复/返回上一行
            logfp.seek(-len(location), 1)

            location = self._cut_line_left(": ", location)

            # 解析后一行，此行对于Crash来说是抛出行
            s = location.find("(") + 1
            e = location.find(")")
            if s > 0 and e > 0:
                pointer = location[s:e].split(":")
                if len(pointer) == 2:
                    return {"filename": pointer[0], "line": pointer[1], "full": location}

    def _cut_line_left(self, flag, l):
        try:
            first_colon_index = l.index(flag)
            # print "first_colon_index = %d" % first_colon_index

            if first_colon_index < 0:
                # 去除每行左侧的空格
                l = l.lstrip()
            else:
                l = l[first_colon_index + 1:]
                l = l.lstrip()
            return l
        except Exception as e:
            # print "Exception = ", e.message
            return l.lstrip()

    def _check_is_repeat(self, src, key1, key2, s):
        try:
            for r in src:
                if not r.has_key(key1):
                    # print "countcountcountcouont == = = some result don't has key1"
                    continue
                for v in r[key1]:
                    if v == key2 and r[key1][v] == s:
                        try:
                            r[key1]["count"] = r[key1]["count"] + 1
                            # print "countcountcountcouont == = =", r[key1]["count"]
                        except Exception as e:
                            # print "countcountcountcouont == = =", e.message
                            r[key1]["count"] = 2
                        return True
        except Exception as e:
            pass # print "countcountcountcouont == = =", e.message, e.args
        return False

    def _check_is_repeat_without_location(self, src, key, total):
        try:
            for r in src:
                if not r.has_key(key):
                    # print "_check_is_repeat_without_location == = = some result don't has key1"
                    continue
                # print "total = ", total, "\nr[key] = ",r[key]
                if self.__index_of__(total, r[key]) > 0\
                        or self.__index_of__(r[key], total) > 0:
                    if r.has_key("count"):
                        r["count"] = r["count"] + 1
                    else:
                        r["count"] = 2
                    return True
        except Exception as e:
            pass
            # print "_check_is_repeat_without_location", e.message
        return False

    def _check_is_same_total(self, src, key, total):
        try:
            for r in src:
                if key not in r:
                    # print "_check_is_repeat_without_location == = = some result don't has key1"
                    continue

                tmp1 = ''.join(total[1:])
                tmp2 = ''.join(r[key])

                # print tmp1, tmp2

                if self.__index_of__(tmp1, tmp2) > 0\
                        or self.__index_of__(tmp2, tmp1) > 0:
                    if r.has_key("count"):
                        r["count"] = r["count"] + 1
                    else:
                        r["count"] = 2
                    return True
        except Exception as e:
            pass # print "_check_is_repeat_without_location", e.message
        return False

    def _check_is_entry(self, entry, l):
        try:
            if self.__index_of__(entry, l) > 0:
                return True
        except Exception as e:
            return False
        return False

    def parse(self):
        # 读取配置文件, 找出要解析的module
        config_data = self.__load_config__()
        # print "ptt heh"

        # 获取所有模块数组
        module_list=[]
        for mstr in self.modules:
            for i in config_data['module']:
                # print i['name'], mstr
                if i["name"] == mstr:
                    module_list.append(i)
        # print "haha"
        # print module_list

        # 打开log文件
        logfp = open(self.log_path, 'r')

        # 所有模块的结果
        all_module_results={}

        # 根据模块搜索, 可能有多个模块
        for mdict in module_list:
            # 将文件指针移到文件开头
            logfp.seek(0)

            # 通用属性
            ENTRY=mdict['entry']
            RULES = mdict["rules"]
            NOT_MATCHED_LINE = mdict['not_matched']

            # 单模块结果
            module_result=[]

            line='#'
            # 单模块中的异常个数
            count = 0

            while line:
                # 按行扫描，是否存在异常入口
                line = logfp.readline().decode("utf-8").replace("\n", " ")
                val = self.__index_of__(ENTRY, line)

                # 定义一个module中中一次异常的扫描结果
                one_result = {}

                # 发现匹配项入口
                if val >= 0:
                    # 获取一次异常 begin
                    not_matched = 0
                    is_repeat = False
                    l = "#"
                    tmp_total_list = [line]
                    # 进行此次异常信息匹配
                    while l:
                        l = logfp.readline().decode("utf-8").replace("\n", " ")
                        l_bak = l

                        is_entry = self._check_is_entry(ENTRY, l)
                        if is_entry:
                            # 返回上一行
                            logfp.seek(-len(l_bak), 1)
                            break

                        # 去除每行左侧的时间戳和TAG
                        # print "real line %s" % l
                        l = self._cut_line_left(flag=": ", l=l)
                        # print l

                        # 如果以RULES中的任意关键字开头，则匹配，允许中间有NOT_MATCHED_LINE行的容错
                        for rule in RULES:
                            if l.startswith(RULES[rule], 0, len(RULES[rule])):
                                # 以*开头的key需要记录所有匹配值
                                # l = l.replace("\n", "")
                                tmp_total_list.append(l)
                                if not rule.startswith("*", 0, 1):
                                    if "Crash" == mdict["name"]:
                                        # Crash的特性处理， 在reason的下一行就是抛出行
                                        if rule == 'reason':
                                            one_result["location"] = self.__parse_crash__(logfp, rule)
                                            if not one_result["location"].has_key("count"):
                                                one_result["location"]["count"] = 1
                                            # print one_result["location"]

                                            # 去除重复第1步
                                            is_repeat = self._check_is_repeat(
                                                module_result, "location", "full", one_result["location"]["full"])
                                            # print is_repeat
                                            if is_repeat:
                                                # print "@@@@@@@@@@@@ Repeat"
                                                is_repeat=True
                                                break
                                            # print l
                                    elif "ANR" == mdict["name"]:
                                        print "ANR"
                                    else:
                                        print "else"

                                    one_result[rule] = l
                                not_matched = 0
                                break
                        else:
                            not_matched += 1
                            tmp_total_list.append(l)
                        # 重复， 退出此次entry
                        if is_repeat:
                            # print "1 is_repeat"
                            break

                        # 下面是无效行
                        if not_matched > NOT_MATCHED_LINE:
                            # 返回上一行
                            logfp.seek(-len(l_bak), 1)
                            break
                    # 重复结果，不添加
                    if is_repeat:
                        # print "2 is_repeat"
                        continue
                    # 获取一次异常 END

                    # 形成一次结果
                    # total = ''.join(tmp_total_list)
                    total = tmp_total_list
                    one_result['total'] = total

                    if "Crash" == mdict["name"]:
                        # 去除重复第二步
                        if not one_result.has_key("location"):
                            # 去除entry，因为包含时间不同，对比会失败
                            # tmp_total_list.pop(0)
                            # total_no_entry = ''.join(tmp_total_list)
                            # has_total=self._check_is_repeat_without_location(module_result, "total", total_no_entry)
                            has_total = self._check_is_same_total(module_result, "total", total)
                            if has_total: continue

                    module_result.append(one_result)
            all_module_results[mdict["name"]]=module_result
        logfp.close()
        # print all_module_results
        return all_module_results

#test
'''
if __name__ == "__main__":
    p = Parser('config.json','/home/qinsw/Downloads/null.log', "Crash")
    data = p.parse()
'''
'''
    for i in data["module"]:
        print i["name"]
        for j in i["rules"]:
            print i["rules"][j]
            # print j
        break


start=datetime.datetime.now()
f=open("/home/qinsw/Downloads/null.log")
line=f.readline()
patterner = StringPattern.StringPattern()
i=1
while line:
    i += 1
    line = f.readline()
    patterner.set_pattern("E/AndroidRuntime: FATAL EXCEPTION:")
    patterner.set_source(line)
    value = patterner.string_pattern_bm()
    if value != 0:
        print value
        print i

f.close()

print (datetime.datetime.now()-start).microseconds
'''