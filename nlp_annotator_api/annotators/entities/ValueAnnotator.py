import os
import re
#from types import _T1
from typing import Any, Optional
from .common.utils import resources_dir
from .common.utils import RegValueAnnotator

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
    

#                "value" : 1,
#                "unit" : "degree Celusius",
#               "sentence" : " Li has conductivtiy 2e-4 mS at 1℃",