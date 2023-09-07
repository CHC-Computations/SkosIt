# -*- coding: utf-8 -*-
"""SKOSIT_LITERARY_STUDIES

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kORUuNIj88LCTm-ZqfFtebcw94nes9n8
"""

!pip install rdflib
!pip install unidecode
!pip install tqdm
!pip install SPARQLWrapper

import pandas as pd
import itertools
from rdflib import Graph, Literal, RDF, URIRef, Namespace, SKOS, RDFS #basic RDF handling
from rdflib.namespace import FOAF , XSD, DC #most common namespaces
import urllib.parse #for parsing strings to URI's
import json
import unidecode
from tqdm import tqdm
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import regex as re

with open("/content/drive/MyDrive/bn_all_final.json", "r", encoding="utf-8") as f:
  dict_whole = json.load(f)

with open("/content/forma_gatunek_lit_wiki(1).json", "r", encoding="utf-8") as f:
  gatunki = json.load(f)

literaturoznawczy = {}

for k,v in dict_whole.items():
  if "Literaturoznawstwo" in  v["all_categories"]:
    literaturoznawczy[k]= dict_whole[k]
for key, value in gatunki.items():
    if key not in literaturoznawczy:
        literaturoznawczy[key] = value

for k,v in literaturoznawczy.items():
  literaturoznawczy[k]["subject_category"] = "Literaturoznawstwo"

literaturoznawczy.update(gatunki)

with open('literaturoznawczy.json', 'w', encoding='utf-8') as f:
    json.dump(literaturoznawczy, f, ensure_ascii=False, indent=4)

'''
Name of controlled dictionary
'''

BN_SKOS = "Deskryptory_literackie_BN_w_SKOS"


'''
Namespaces
'''
TERMS = Namespace('https://bn-lit-skos.lab.dariah.pl/scheme/')
ALL = Namespace('https://bn-skos.lab.dariah.pl/scheme/')
WIKIDATA = Namespace("http://www.wikidata.org/entity/")

schema = Namespace('http://schema.org/')
lcsh = Namespace("http://id.loc.gov/authorities/subjects/")
YSO = Namespace("https://finto.fi/yso/en/page/")
EUROVOC = Namespace("")
openalex = Namespace("https://openalex.org/")


'''
Types of relations (with labels) in BN-SKOS
'''
ALT_LABELS = ["450","450a", "455", "label_en", "label_fr", "label_ger", "label_ukr"]
RELATED = ["550a", "555a", "555g", "555h"]
BROADER = ["550g", "555g"]
NARROWER = ["550h", "555h"]
CLOSE_MATCH = ["lcsh", "YSO", "openalex", "eurovoc", "item"]

def prepare_term(term):

  def replacer(text):
    chars = "\\`*{})[]>#+.!$"
    for c in chars:
        if c in text:
            text = text.replace(c, "")
    return text

  final_term = unidecode.unidecode(
      term.replace(" (", "-")
      .replace(" ", "_")
      .replace('"', "")
      .strip()
  )
  return replacer(final_term)


def add_alt_label_node(elem, language):
  if not isinstance(elem, float):
    for item in elem:
      item = item.strip()
      graph.add((URIRef(TERMS + pref_label), SKOS.altLabel, Literal(item, lang = language)))
      graph.add((URIRef(TERMS + pref_label), SKOS.broader, URIRef(TERMS+BN_SKOS)))

def add_single_alt_label_node(item, language):
  if not isinstance(item, float):
    item = item.strip()
    graph.add((URIRef(TERMS + pref_label), SKOS.altLabel, Literal(item, lang = language)))
    graph.add((URIRef(TERMS + pref_label), SKOS.broader, URIRef(TERMS+BN_SKOS)))

PREF_LABELS = []
for k,v in literaturoznawczy.items():
  PREF_LABELS.append(prepare_term(k))

graph = Graph()

#Create top concept of graph, altLables, prefLabel and basic info about the graph

graph.add((URIRef(TERMS), RDF.type, SKOS.ConceptScheme))
graph.add((URIRef(TERMS), RDFS.label, Literal("Deskryptory literackie BN w SKOS")))
graph.add((URIRef(TERMS + "/" + BN_SKOS), RDF['type'], SKOS.Concept))
graph.add((URIRef(TERMS + "/" + BN_SKOS), SKOS.inScheme, URIRef(TERMS)))
graph.add((URIRef(TERMS + "/" + BN_SKOS), SKOS.topConceptOf, URIRef(TERMS)))
graph.add((URIRef(TERMS),SKOS.topConceptOf, URIRef(TERMS + "/" + BN_SKOS)))
graph.add((URIRef(TERMS), RDFS.label, Literal("Deskryptory literackie BN w SKOS", lang = "en") ))
graph.add((URIRef(TERMS + "/" + BN_SKOS), SKOS.altLabel, Literal("BN_LIT_SKOS", lang = "en") ))
graph.add((URIRef(TERMS + "/" + BN_SKOS), SKOS.prefLabel, Literal("Deskryptory literackie BN w SKOS", lang = "pl") ))
graph.add((URIRef(TERMS + "/" + BN_SKOS), RDFS.label, Literal("Deskryptory literackie BN w SKOS", lang = "pl") ))


for single_dict in tqdm(literaturoznawczy.values()):
  for k, v in single_dict.items():
    if k == "150" or k =="155":
      pref_label = prepare_term(v)
      print(pref_label)
      graph.add((URIRef(TERMS + "/" + pref_label), RDF['type'], SKOS.Concept))
      graph.add((URIRef(TERMS + "/" + pref_label), SKOS.prefLabel, Literal(v.strip(), lang= 'pl') ))
      graph.add((URIRef(TERMS + "/" + pref_label), SKOS.inScheme, URIRef(TERMS)))
    elif k == "subject_category":
      v_term = prepare_term(v).capitalize()
      graph.add((URIRef(TERMS + "/" + pref_label), SKOS.broader, URIRef(TERMS + "/"+ v_term)))

    elif k == "450a":

      add_alt_label_node(v, "pl")

    elif k == "enLabel":
      add_single_alt_label_node(v, "en")

    elif k == "frLabel":
      add_single_alt_label_node(v, "fr")

    elif k == "deLabel":
      add_single_alt_label_node(v, "de")

    elif k == "ukLabel":
      add_single_alt_label_node(v, "uk")

    elif k in RELATED and not isinstance(v, float):
        for elem in v:
          if elem in PREF_LABELS:
            related_term = prepare_term(elem)
            graph.add((URIRef(TERMS + "/" + pref_label), SKOS.related, URIRef(TERMS + "/" + unidecode.unidecode(related_term))))
          else:
            related_term = prepare_term(elem)
            graph.add((URIRef(TERMS + "/" + pref_label), SKOS.related, URIRef(ALL + "/" + unidecode.unidecode(related_term))))
    elif k in BROADER and not isinstance(v, float):
      for elem in v:
        if elem in PREF_LABELS:
          broader_term = prepare_term(elem)
          graph.add((URIRef(TERMS + "/" + pref_label), SKOS.broader, URIRef(TERMS + "/" + unidecode.unidecode(broader_term))))
        else:
          broader_term = prepare_term(elem)
          graph.add((URIRef(TERMS + "/" + pref_label), SKOS.broader, URIRef(ALL + "/" + unidecode.unidecode(broader_term))))
    elif k in NARROWER and not isinstance(v, float):
      for elem in v:
        if elem in PREF_LABELS:
          narrower_term = prepare_term(elem)
          graph.add((URIRef(TERMS + "/" + pref_label), SKOS.narrower, URIRef(TERMS + "/" + unidecode.unidecode(narrower_term))))
        else:
          narrower_term = prepare_term(elem)
          graph.add((URIRef(TERMS + "/" + pref_label), SKOS.narrower, URIRef(ALL + "/" + unidecode.unidecode(narrower_term)))),
    elif k == "lcsh":
        close_term = prepare_term(v)
        graph.add((URIRef(TERMS + "/" + pref_label), SKOS.closeMatch, URIRef(lcsh + unidecode.unidecode(close_term))))
    elif k == "yso":
          close_term = prepare_term(v)
          graph.add((URIRef(TERMS + "/" + pref_label), SKOS.closeMatch, URIRef(YSO + unidecode.unidecode(close_term))))

    elif k == "openalex":
          close_term = prepare_term(v)
          graph.add((URIRef(TERMS + "/" + pref_label), SKOS.closeMatch, URIRef(openalex + unidecode.unidecode(close_term))))

    elif k == "item":
          graph.add((URIRef(TERMS + "/" + pref_label), SKOS.closeMatch, URIRef(v)))

try:
  graph.serialize("lit_bn_skos_27_04_23.ttl", format = "turtle")
except:
  print(pref_label)