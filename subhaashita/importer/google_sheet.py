import pandas
import regex
from curation_utils.google import sheets
from sanskrit_data import collection_helper

from subhaashita import Subhaashita
from subhaashita.importer import clean_devanaagarii


def import_all(worksheet_name, spreadhsheet_id="18HwdEp49UdRe1l4Lk2pM73xIs9ulBKyDE3BW32vMKyc", google_key='/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', text_column="सुभाषितम्", comment_column="विवरणम्", metadata_map={"विषयः": "topics", "छन्दः": "meters"}, metadata_in={"ratings": ["vvasuki:5"]}, cls=Subhaashita):
  sheet = sheets.get_sheet(spreadhsheet_id=spreadhsheet_id, worksheet_name=worksheet_name, google_key = google_key)

  rows = sheet.get_all_values()
  df = pandas.DataFrame(rows[1:], columns=rows.pop(0))
  quotes = []
  for index in range(0, len(df)):
    text = clean_devanaagarii(df.iloc[index][text_column].strip())
    text = regex.sub("। *\n?", "।\n", text)
    text = text.replace("\n", "  \n")
    if text == "":
      continue
    metadata = metadata_in
    for key_1, key_2 in metadata_map.items():
      metadata[key_2] = [x.strip() for x in df.iloc[index][key_1].split(",") if x.strip() != ""]
      if len(metadata[key_2]) == 0:
        metadata.pop(key_2)
    source = " - ".join(list(filter(lambda x: x != "", [df.iloc[index]["वक्ता"].strip(), df.iloc[index]["स्रोतः"].strip()])))
    if source != "":
      if source == "राजारामज-शङ्करः": source += " - मुक्तकम्"
      sources = [source]
    else:
      sources = None
    comment = df.iloc[index][comment_column].strip()
    if comment != "":
      commentaries = {"अज्ञात-विवरणम्": comment.replace("\n", "  \n")}
    else:
      commentaries = None
    quote = cls(variants=[text], commentaries=commentaries, sources=sources, **metadata)
    quotes.append(quote)
  return quotes

