import os
import sys

import pandas
import regex

from subhaashita import Subhaashita
from indic_transliteration import sanscript



def import_from_dir(dir_path):
  pass


def import_from_mss_tsv(tsv_path):
  quote_df = pandas.read_csv(tsv_path, sep="\t", keep_default_na=False)
  quote_df = quote_df.set_index("ID")
  quotes = []
  for mss_id in quote_df.index:
    text = str(quote_df.loc[mss_id].quote)
    text = regex.sub(r"। *", "।  \n", text)
    text = sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara(text, omit_sam=True, omit_yrl=True, ignore_padaanta=True)
    quote = Subhaashita(variants=[text], secondary_sources=[mss_id], script=sanscript.DEVANAGARI)
    quotes.append(quote)
  return quotes

