import os
import re
#from types import _T1
from typing import Any, Optional
from .common.utils import resources_dir


class ValueAnnotator:
    
    def key(self) -> str:
        return "value"

    def description(self) -> str:
        return "finding value"

    def __init__(self):

        # init CDE
        self.parser = RegValueAnnotator

    def annotate_entities_text(self, text:str):

        #print(text)

        ents=[]

        #implement CDE
        doc = self.parser(text)

        for cem in doc:

            name = cem[2]

            t0 = cem[0]
            t1 = cem[1]

            ent = {
                "match": name,
                "range": [t0,t1],
                "original": text[t0:t1],
                "type":"value"
            }
            ents.append(ent)

        #print(ents)

        return ents
    
    def RegValueAnnotator(self, paragraph):
        exlist = []
        ex_in_list = []
        paragraph = list_para[num]
        pattern = '([+\-]?)\s*(((10)(\s+|(\$?\^))\s*(\$\^)?\{?\s*([+\-])\s*(\$\^)?\{?\s*(\d+)\}?\$?)|(((\d+\.?\d*)|(\.\d+))(\s*(E|e|((\s|X|x|((\$_{)?(GLYPH<[A-Z]+\d+>(}\$)?)))\s*10))\s*\^?\s*(\$\^)?\{?\s*([+\-]?)\s*(\$\^)?\{?\s*(\d+)\}?\$?)?))'
        pattern_re = re.compile(pattern)
        parser = pattern_re
        regex = parser.finditer(paragraph)
        for reg in regex:
            exlist.append([reg.start(), reg.end(), reg.group(), 1])

        exlist = list(map(list, set(map(tuple, exlist))))
        exlist = sorted(exlist)

        def is_overlap(start1, end1, start2, end2):
            return start1 <= end2 and end1 >= start2

        tmplist = []
        newlist = []
        for i in range(0, len(exlist)):
            if not i == len(exlist)-1:
                if tmplist == []:
                    lista = exlist[i]
                    listb = exlist[i+1]
                    if is_overlap(lista[0],lista[1], listb[0], listb[1]):
                        if lista[1]-lista[0] > listb[1]-listb[0]:
                            max = lista
                            min = listb
                        else:
                            max = listb
                            min = lista

                        if min[0] < max[0]:
                            gap = max[0] - min[0]
                            newword = min[2][0:gap] + max[2]
                            tmplist = [min[0], max[1], newword, max[3]]
                        elif min[0] >= max[0] and min[1] <= max[1]:
                            tmplist = [max[0], max[1], max[2], max[3]]
                        elif min[1] > max[1]:
                            gap = min[1] - max[1]
                            newword = max[2] + min[2][gap-1:len(min[2])]
                            tmplist = [max[0], min[1], newword, max[3]]
                    else:
                        if exlist[i][3] == 1:
                            newlist.append(exlist[i])
                else:
                    lista = tmplist
                    listb = exlist[i+1]
                    if is_overlap(lista[0],lista[1], listb[0], listb[1]):
                        if lista[1]-lista[0] > listb[1]-listb[0]:
                            max = lista
                            min = listb
                        else:
                            max = listb
                            min = lista

                        if min[0] < max[0]:
                            gap = max[0] - min[0]
                            newword = min[2][0:gap] + max[2]
                            tmplist = [min[0], max[1], newword, max[3]]
                        elif min[0] >= max[0] and min[1] <= max[1]:
                            tmplist = [max[0], max[1], max[2], max[3]]
                        elif min[1] > max[1]:
                            gap = min[1] - max[1]
                            newword = max[2] + min[2][gap-1:len(min[2])]
                            tmplist = [max[0], min[1], newword, max[3]]
                    else:
                        if tmplist[3] == 1:
                            newlist.append(tmplist)
                        tmplist = []
            else:
                newlist.append(exlist[i])


        pattern_inverse = '((?<=\$[_^]{)\d+?(?=}\$))|((?<=\[)(\-*\d+)+?(?=\]))|((?<=figure)|((?<=Figure)|(?<=fig)|(?<=Fig)|(?<=figure\.)|(?<=Figure\.)|(?<=fig\.)|(?<=Fig\.)|(?<=table)|(?<=Table)|(?<=table\.)|(?<=Table\.))( \d+|\d+)(\.|))'
        pattern_re = re.compile(pattern_inverse)
        parser = pattern_re
        regex = parser.finditer(paragraph)
        for reg in regex:
            newlist.append([reg.start(), reg.end(), reg.group(), 1])

        finallist = []
        for new in newlist:
            if newlist.count(new) == 1:
                finallist.append(new)
        
        return finallist
#                "value" : 1,
#                "unit" : "degree Celusius",
#               "sentence" : " Li has conductivtiy 2e-4 mS at 1℃",