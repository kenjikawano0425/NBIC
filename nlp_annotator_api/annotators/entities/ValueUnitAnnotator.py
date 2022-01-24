import os
import re
#from types import _T1
from typing import Any, Optional
from .common.utils import resources_dir
from .common.utils import RegValueUnitAnnotator

class ValueUnitAnnotator:
    
    def key(self) -> str:
        return "value+unit"

    def description(self) -> str:
        return "finding value+unit, where 3 options, float_value(500, 0.05), unit(mg, km) and range_bool(and, to, -)."

    def __init__(self):

        # init CDE
        self.parser = RegValueUnitAnnotator

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
                "type":"value+unit",
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