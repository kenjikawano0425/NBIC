import os
import re
#from types import _T1
from typing import Any, Optional
from .common.utils import resources_dir
from .common.utils import RegValueAnnotator

class ValueAnnotator:
    
    def key(self) -> str:
        return "values"

    def description(self) -> str:
        return "finding values, where 2 options, float_value(500, 0.05), range_bool(and, to, -)."

    def __init__(self):

        # init CDE
        self.parser = RegValueAnnotator

    def annotate_entities_text(self, text:str):


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
                "type":"values",
                "unit":cem[4],
                "range_bool":cem[5],
                "float_value":cem[6]
            }
            ents.append(ent)

        #print(ents)

        return ents
    

#                "value" : 1,
#                "unit" : "degree Celusius",
#               "sentence" : " Li has conductivtiy 2e-4 mS at 1℃",