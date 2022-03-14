import os
import re
#from types import _T1
from typing import Any, Optional
from .common.utils import resources_dir
from .common.utils import RegPropertiesAnnotator

class PropertiesAnnotator:
    
    def key(self) -> str:
        return "properties"

    def description(self) -> str:
        return "Names of properties"

    def __init__(self):

        # init CDE
        self.parser = RegPropertiesAnnotator

    def annotate_entities_text(self, text:str):

        #print(text)

        ents=[]

        #implement CDE
        doc = self.parser(text)
        #print(doc)

        for cem in doc:

            name = cem[2]

            t0 = cem[0]
            t1 = cem[1]

            typename = cem[3]
            print(typename)


            ent = {
                "match": name,
                "range": [t0,t1],
                "original": text[t0:t1],
                "type": typename
            }
            ents.append(ent)

        #print(ents)

        return ents
    

#                "value" : 1,
#                "unit" : "degree Celusius",
#               "sentence" : " Li has conductivtiy 2e-4 mS at 1℃",