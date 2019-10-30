# -*- coding: utf-8 -*-
import argparse
from collections import defaultdict
import re
import Graph
import Cvalue
import Pattern

class PPScore(object):
    def __init__(self, config):
        self.config = config
        self.pattern = Pattern.Pattern()
        self.posPattern = re.compile('_[A-Z\.\!\@\#\$\%\^\&\*\?]+')
        self.dot = re.compile('[\.\!\@\#\$\%\^\&\*\?]')
        self.position_Distribution = []
        sum_ = 133530.0
        with open(config['data']['position'], 'r') as f:
            for line in f:
                self.position_Distribution.append(float(line.strip())/sum_)
        self.graph = Graph.Graph(self.config)
        self.cvalue = Cvalue.Cvalue(self.config)
        self.fo = open(config['data']['output'], 'w')


    def load(self, file, window_size):
        with open(file) as doc:
            self.word_Dic = defaultdict(float)
            self.document = []
            self.posTags = []
            self.position = defaultdict(list)
            doc_idx = 0
            self.doc_Lines = doc.read()
            tokens = self.doc_Lines.split()
            self.doc_len = len(tokens)
            for token in tokens:
                word = token.split('_')[0]
                try : pos = token.split('_')[1]
                except : continue

                word = word.strip().lower()
                self.word_Dic[word] += 1. 
                self.document.append(word)
                self.posTags.append(pos)
                        
                flag1 = self.pattern.isGoodPOS(pos)
                flag2 = self.pattern.isSpecialToken(word)
                doc_idx = doc_idx + 1
                if(flag1 == False or flag2 == False):
                    continue
                self.position[word].append(doc_idx)
        self.doc_Lines = self.posPattern.sub('', self.doc_Lines)
        self.doc_Lines = self.dot.sub('',self.doc_Lines)
        self.doc_Lines = self.doc_Lines.lower()

    def Exec(self, file):
        self.load(file, self.config['window'])
        self.graph.Exec(self.document, self.posTags, self.position, self.word_Dic, self.doc_Lines)
        self.cvalue.Exec(self.doc_len, self.doc_Lines, self.graph.result, self.position_Distribution, self.graph.candidate_Position)
        self.write(file)

    def write(self, file):
            self.fo.write(file.split('/')[-1].split('.')[0]+':'+', '.join([x for x, _ in sorted(self.cvalue.result.items(), key=lambda x:x[1], reverse=True)[:15]])+'\n')
