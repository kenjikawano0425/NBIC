import os
#from types import _T1
from typing import Any, Optional
from .common.utils import resources_dir

from chemdataextractor import Document

class MaterialAnnotator:
    
    def key(self) -> str:
        return "material"

    def description(self) -> str:
        return "finding materials with ChemDataExtractor"

    def __init__(self):

        # init CDE
        self.parser = Document

    def annotate_entities_text(self, text:str):

        #print(text)

        ents=[]

        #implement CDE
        doc = self.parser(text)

        for cem in doc.cems:

            name = cem.text

            t0 = cem.start
            t1 = cem.end

            ent = {
                "match": name,
                "range": [t0,t1],
                "original": text[t0:t1],
                "type":"material"
            }
            ents.append(ent)

        #print(ents)

        return ents

#                "value" : 1,
#                "unit" : "degree Celusius",
#               "sentence" : " Li has conductivtiy 2e-4 mS at 1℃",