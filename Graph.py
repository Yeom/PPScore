#-*-coding:utf-8 -*-
from collections import defaultdict
import Pattern
import copy
import math

class Graph(object):
    def __init__(self, config):
        self.window = config['window']
        self.dataset = config['data']['name']
        self.alpha = config['alpha']
        self.pattern = Pattern.Pattern()

    def Exec(self, document, pos, position, wordDic, docLines):
        self.result = defaultdict(float)
        srGraph = self.build(document, pos, position)#Time Consume 2nd
        srGraph = self.weight(wordDic, srGraph)
        srScore = self.rank(srGraph, position)#Time Consume 3rd
        candidate_Clause = self.pattern.extract(document, pos)
        self.candidate_Position = self.pattern.extractPosition(candidate_Clause, docLines)#Time Consume 1st
        self.scoring(srScore, candidate_Clause, self.alpha)


    def sum_two_dics(self, dic1,dic2):
        dic = dic1
        key_list = dic2.keys()
        for key in key_list:
            if key in dic:
                temp = dic[key]
                dic[key] = temp + dic2[key]
            else:
                dic[key] = dic2[key]
        return dic

    def build(self, document, pos, position):
        srGraph = {}
        idx = 0
        for word in document:
            if word in position.keys() :
                adjacency_vertex = {}
                index = idx - 1
                count = self.window
                while index >= 0 and count > 0:
                    neighbor = document[index]
                    if neighbor in position.keys():
                        adjacency_vertex[neighbor] = adjacency_vertex.get(neighbor,0.0) + 1.0
                    index = index - 1
                    count = count - 1
            
                index = idx +1
                count = self.window
            
                while index < len(document) and count > 0:
                    neighbor = document[index]
                
                    if neighbor in position.keys() :
                        adjacency_vertex[neighbor] = adjacency_vertex.get(neighbor,0) + 1.0
# 
                    index = index + 1
                    count = count - 1
            
                if word in srGraph:
                    Dic1 = srGraph[word]
                    Dic2 = adjacency_vertex
                    Dic = self.sum_two_dics(Dic1, Dic2)
                    srGraph[word] = Dic
                else:
                    srGraph[word] = adjacency_vertex
            idx = idx + 1
        return srGraph

    def normalize(self, srGraph):
        new_srGraph = copy.deepcopy(srGraph)
        vtx_list = srGraph.keys()
        for vtx in vtx_list:
            sum_ = 0.0
            adjacency_vtx_list = srGraph[vtx].keys()
            for adjacency_vtx in adjacency_vtx_list:
                sum_ = sum_ + srGraph[vtx][adjacency_vtx]
            for adjacency_vtx in adjacency_vtx_list:
                if sum_ != 0.0:#1.0-?
                    new_srGraph[vtx][adjacency_vtx] = srGraph[vtx][adjacency_vtx]/sum_
                else:
                    new_srGraph[vtx][adjacency_vtx] = 0.0
        return new_srGraph

    def weight(self, wordDic, srGraph):
        weight_sum = 0.0
        weight_count = 0.0
        for vtx in srGraph.keys():
            adjacency_vtx_list = srGraph[vtx].keys()
            for adjacency_vtx in adjacency_vtx_list:
                attr = ((srGraph[vtx][adjacency_vtx]) / (wordDic[vtx] * wordDic[adjacency_vtx]))
#Adjust Weight
                srGraph[vtx][adjacency_vtx] = attr
                weight_sum += attr
                weight_count += 1

        if weight_count > 0:
            weight_avg = weight_sum / weight_count
        else :
            weight_avg = weight_sum / 1.0

        biased_weight = 0.0
        for vtx in srGraph.keys():
            adjacency_vtx_list = srGraph[vtx].keys()
            for adjacency_vtx in adjacency_vtx_list:
                biased_weight = 1 + (srGraph[vtx][adjacency_vtx]-weight_avg)
                srGraph[vtx][adjacency_vtx] = biased_weight
        return self.normalize(srGraph)

    def nodeCalculate(self, srGraph):
        nodeCount = 0
        vtx_list = srGraph.keys()
        for vtx in vtx_list:
            adj_vtx_list = srGraph[vtx].keys()
            for adj_vtx in adj_vtx_list:
                if srGraph[vtx][adj_vtx] != 0:
                    nodeCount += 1
        return nodeCount / 2

    def rank(self, srGraph, position):
        srScore = {}
        vtx_list = srGraph.keys()
        nodeCount = self.nodeCalculate(srGraph)
        #Initialize Score
        for vtx in vtx_list:
            if vtx in position.keys():
                srScore[vtx] = 1.0
        #iteration
        breakFlag = False

        for i in range(20):
            srScoreDiff = srScore
            srScoreTemp = {}
            #vertices in Graph
            for vtx in vtx_list:
                score = 0.0
                adjacency_vtx_list = srGraph[vtx].keys()
                #adjacency vertex
                for adjacency_vtx in adjacency_vtx_list:
                    score = score + srGraph[adjacency_vtx][vtx] * srScore[adjacency_vtx]
                score = score * (1.0 - 0.15)
                score = score + (0.15/(1.0 * nodeCount))
                srScoreTemp[vtx] = score
                if abs(srScoreTemp[vtx] - srScoreDiff[vtx]) < 0.0001:
                    breakFlag = True        
            srScore = srScoreTemp
            if breakFlag == True:
                break
        
        srScore['of'] = 0.0
        srScore['and'] = 0.0
        return srScore

    def harmonicMean(self, srScore, candidate):
        d = 0.0
        token_list = candidate.split()
        for token in token_list:
            try : d = d + 1 / srScore[token]
            except : pass 
        len_ = len(token_list)
        try : score = 1 / (d / len_)
        except : score = 0.0
        return score

    def scoring(self, srScore, candidate_Clause, alpha):
        cand_list = candidate_Clause.keys()
        for candidate in cand_list:
            if candidate_Clause[candidate] != None:
                len_ = len(candidate.split())
                para_ =  (math.log(len(candidate.split()),2))
                if para_ == 0.0:
                    para_ = alpha# /10?
                self.result[candidate] = self.harmonicMean(srScore,candidate) * para_
