#-*- coding:utf-8 -*-
from collections import defaultdict
import math
import sys
class Cvalue(object):
    def __init__(self, config):
        self.config = config

    def Exec(self, docLen, docLines, graphResult, position_Distribution, candidate_Position):
        self.c_value = defaultdict(float)
        self.result = defaultdict(float)

        if self.config['data']['name'] == 'Inspec':
            interval = int(docLen / 12.5)
        elif self.config['data']['name'] == 'SemEval2010':
            interval = int(docLen / 959)

        for key in graphResult.keys():
            if len(key.split()) >= 1:
                try:
                    self.c_value[key] += graphResult[key] * position_Distribution[int(candidate_Position[key][0]) / interval] * docLines.count(key)
                except:
                    self.c_value[key] += graphResult[key] * (position_Distribution[-1] * docLines.count(key)) 

        self.srScoreXcvalue()
                                                                              
    def isSubToken(self, candidate, key):
        k_ = key.split(' ')
        c_ = candidate.split(' ')
        len_c_ = len(c_)
        range_ = len(k_) - len_c_ + 1
        if range_ > 0:
            for i in xrange(range_):
                if " ".join(k_[i:i+len_c_]) == candidate:
                    return True
            return False
        else:
            return False

    def calCvalue(self, candidate):
        count = 0.0
        f_b = 0.0
        f_a = self.c_value[candidate]
        for key in self.c_value.keys():
            if key != candidate and self.isSubToken(candidate, key) == True:
                count = count + 1.0
                f_b += self.c_value[key]
        if count == 0.0:
            return f_a
        else :
            return (f_a - (f_b/count))
                                                                              
    def srScoreXcvalue(self):
        for candidate in self.c_value.keys():
            if len(candidate.split()) > 0:
                para_ =  (math.log(len(candidate.split()),2))
                if para_ == 0.0:
                    para_ = self.config['beta']
                Cvalue = self.calCvalue(candidate) * para_
                self.result[candidate] = 1.0*Cvalue
