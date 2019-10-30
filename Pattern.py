#-*-coding:utf-8 -*-
import re
from collections import defaultdict
class Pattern(object):
    def __init__(self):
        self.stopList = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each","effort", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill","mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere",  "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"]
        self.goodPOS = ["NN", "NNS", "NNP", "NNPS", "JJ", "JJR", "JJS", "FW", "VBN"]
    def isStopWord(self, word):
        if word in self.stopList:
            return False
        return True

    def isGoodPOS(self, pos):
        if pos in self.goodPOS:
            return True
        else:
            return False

    def isSpecialToken(self, word):
        p = re.compile('[#]+')
        m = p.match(word)
        if word == '%' or m != None or word == '=' or len(word) == 1:
            return False
        else:
            return True       

    def extract(self, document, posTags):
        candidate_Clause = {}
        pattern = []
        patternPos = []
        idx = 0
        for pos in posTags:
            if (self.isGoodPOS(pos) == True and self.isSpecialToken(document[idx]) and self.isStopWord(document[idx])):
                pattern.append(document[idx])
                patternPos.append(posTags[idx])       
            elif len(pattern) > 4:
                pattern = []
                patternPos = []
            elif len(pattern) != 0 and (self.isGoodPOS(pos) == False or self.isStopWord(document[idx]) == False or self.isSpecialToken(document[idx]) == False):

                s = " ".join(pattern).strip()
            
                if patternPos[-1] != 'JJ'and patternPos[-1] != 'JJS'and patternPos[-1] != 'JJR'and patternPos[-1] != "FW"and patternPos[-1] != "VBN" and patternPos[-1] != "CC" and patternPos[-1] != "IN" and patternPos[0] != "CC" and patternPos[0] != "IN":
                    if s != "and":
                        candidate_Clause[s] = candidate_Clause.get(s,0) + 1
                pattern = []
                patternPos = []
            
            idx = idx + 1
        if len(pattern) != 0 :
            s = " ".join(pattern).strip()
            if len(pattern) > 4:
                pattern = []
                patternPos = []

            elif patternPos[-1] != 'JJ'and patternPos[-1] != 'JJS'and patternPos[-1] != 'JJR'and patternPos[-1] != "FW"and patternPos[-1] != "VBN" and patternPos[-1] != "CC" and patternPos[-1] != "IN":
                candidate_Clause[s] = candidate_Clause.get(s,0) + 1

            pattern = []
            patternPos = []
    
        return candidate_Clause

    def extractPosition(self, candidate_Clause, doc_Lines):
        ans_pos = defaultdict(list)
        document = doc_Lines
        document = re.sub("[\r]", '', document)
        document = re.sub("[\t]", '', document)
        document = re.sub("[\n]", '', document)
        document = re.sub("[ ]+", ' ',document)
        doc = document.split(' ')
        for candidate in candidate_Clause.keys():
            cand = candidate.split(' ')
            len_cand = len(cand)
            len_doc  = len(doc) - len_cand + 1
            if len_doc > 0:
                for i in xrange(len_doc):
                    if " ".join(doc[i:i+len_cand]) == candidate:
                        ans_pos[candidate].append(i)
        return ans_pos
