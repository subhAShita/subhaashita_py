import os

import doc_curation.utils.sanskrit_helper
import pandas
import regex

from subhaashita import Subhaashita
from indic_transliteration import sanscript


def clean_devanaagarii(text):
  text = text.replace(":", "ः").replace("|", "।").replace("।।", "॥")
  text = regex.sub("॥ *[०-९- ]+ *॥", "॥", text)
  return text


def is_non_template_file(x):
  return not os.path.basename(x).startswith("_")


def empty_import_dir(dir_path):
  from pathlib import Path
  # logging.debug(list(Path(dir_path).glob(file_pattern)))
  md_file_paths = sorted(filter(is_non_template_file, Path(dir_path).glob("**/*.md")))
  for file_path in md_file_paths:
    os.remove(file_path)


def import_from_mss_tsv(tsv_path):
  quote_df = pandas.read_csv(tsv_path, sep="\t", keep_default_na=False)
  quote_df = quote_df.set_index("ID")
  quotes = []
  for mss_id in quote_df.index:
    text = str(quote_df.loc[mss_id].quote)
    text = regex.sub(r"। *", "।  \n", text)
    text = doc_curation.utils.sanskrit_helper.fix_lazy_anusvaara(text, omit_sam=True, omit_yrl=True, ignore_padaanta=True)
    quote = Subhaashita(variants=[text], secondary_sources=[mss_id], script=sanscript.DEVANAGARI)
    quotes.append(quote)
  return quotes

