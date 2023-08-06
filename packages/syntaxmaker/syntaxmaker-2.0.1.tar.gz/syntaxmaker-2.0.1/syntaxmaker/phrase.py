#encoding: utf-8
__author__ = 'Mika Hämäläinen'
from .head import Head
import copy
import re, sys

unicode = str

class Phrase:
    def __init__(self, head, structure, morphology={}):
        self.new_python = True
        self.parent = None
        self.head = Head(head, structure["head"])
        self.components = copy.deepcopy(structure["components"])
        if self.components is None:
            self.components = {}
            self.order = ["head"]
        else:
            self.order = copy.deepcopy(structure["order"])
        if "agreement" in structure:
            self.agreement = copy.deepcopy(structure["agreement"])
        else:
            self.agreement = {}
        if "governance" in structure:
            self.governance = copy.deepcopy(structure["governance"])
        else:
            self.governance = {}
        self.morphology = copy.deepcopy(morphology)

    def resolve_agreement(self):
        forms = {}
        for key in self.agreement:
            if key == "parent" and self.parent is not None:
                morphology = self.parent.morphology
            elif key.startswith("parent->")and self.parent is not None:
                key_p = key[8:]
                morphology = self.parent.components[key_p].morphology
            elif key in self.components:
                morphology = self.components[key].morphology
            else:
                r = {"CASE": "Nom", "NUM": "SG", "PERS": "3"}
                r.update(self.morphology)
                return r
            for agreement_type in self.agreement[key]:
                forms[agreement_type] = morphology[agreement_type]
        return forms

    def to_string(self, received_governance = {}):
        self.morphology.update(received_governance)
        string_representation = ""
        if "dir_object" in self.components:
            if type(self.components["dir_object"]) is not str:
                if "NUM" in self.components["dir_object"].morphology and self.components["dir_object"].morphology["NUM"] == "PL":
                    if "dir_object" in self.governance:
                        if self.governance["dir_object"]["CASE"] == "Gen":
                            self.governance["dir_object"]["CASE"] = "Par"
        for item in self.order:
            if item == "head":
                head_word = self.head.get_form(self.morphology, self.resolve_agreement())
                string_representation = string_representation + " " + head_word
            else:
                phrase = self.components[item]
                if type(phrase) is str or (not self.new_python and type(phrase) is unicode):
                    #Data not set
                    pass
                else:
                    phrase.parent = self
                    governance = {}
                    if item in self.governance:
                        governance = self.governance[item]
                    if "PREDICATIVE" in governance and governance["PREDICATIVE"]:
                        if governance["NUM"] is None:
                            governance["NUM"] = self.components["subject"].morphology["NUM"]
                        if governance["CASE"] is None:
                            if governance["NUM"] == "SG":
                                governance["CASE"] = "Nom"
                            else:
                                governance["CASE"] = "Par"
                    string_representation = string_representation + " " + phrase.to_string(governance)
        return string_representation.strip()

    def __str__(self):
        text = self.to_string()
        #remove multiple spaces
        text = re.sub("\s\s+", " ", text)
        #remove spaces before punctuation
        text = self.__remove_spaces_punct__(text)
        return text.strip()

    def __remove_spaces_punct__(self, text):
        puncts = ".,;:?!"
        for punct in puncts:
            if " "+punct in text:
                text = text.replace(" " + punct, punct)
        return text
