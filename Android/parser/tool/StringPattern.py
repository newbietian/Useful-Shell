# coding=utf-8
class StringPattern(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StringPattern, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.src = ''
        self.p = ''
        self.p_len = len(self.p)
        self.pi = [0 for i in range(self.p_len)]

    def set_pattern(self, p):
        self.p = p
        self.p_len = len(p)
        self.pi = [0 for i in range(self.p_len)]

    def set_source(self, src):
        self.src = src

    '''  Boyer-Moore algorithm  '''
    def __calc_match__(self, num):
        #print num
        k = num
        j = 0
        while k >= 0:
            if self.p[-k] == self.p[j]:
                k = k - 1
                j = j + 1
                if k <= 0:
                    self.pi[num - 1] = num
                    return 0
            else:
                if num == 1:
                    return 0
                self.pi[num - 1] = self.pi[num - 2]
                return 0
        #else:
            #print "__calc_match__ end"

    def __init_good_table(self):
        i=1
        while i <= self.p_len:
            self.__calc_match__(i)
            i = i + 1
        #else:
            #print "__init_good_table end"

        #print (self.pi)
        return 0

    def __check_bad_table__(self, tmp_chr):
        i = 1
        while self.p_len-i >= 0:
            if self.p[-i] == tmp_chr:
                return i
            else:
                i = i+1
        return self.p_len + 1

    def __check_good_table__(self, num):
        if not num:
            return self.p_len
        else:
            return self.pi[num]

    def string_pattern_bm(self):
        self.__init_good_table()
        tmp_len = self.p_len
        i = 1
        while tmp_len <= len(self.src):
            if self.p[-i] == self.src[tmp_len-i]:
                i = i+1
                if i > self.p_len:
                    return tmp_len-self.p_len
            else:
                tmp_bad = self.__check_bad_table__(self.src[tmp_len-i])-i
                tmp_good = self.p_len-self.__check_good_table__(i-1)
                tmp_len = tmp_len+max(tmp_bad, tmp_good)
                #print(tmp_bad, tmp_good, tmp_len)
                i = 1
        return -1
