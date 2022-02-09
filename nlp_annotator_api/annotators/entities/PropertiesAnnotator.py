import os
from typing import Any, Optional
from .common.utils import resources_dir
from .common.DictionaryTextEntityAnnotator import DictionaryTextEntityAnnotator, Config


class PropertiesAnnotator(DictionaryTextEntityAnnotator):
    
    def key(self) -> str:
        return "properties"

    def description(self) -> str:
        return "Names of properties"

    def __init__(self):
        super().__init__(
            Config(
                dictionary_filename=os.path.join(resources_dir, "properties.json")
            )
        )

