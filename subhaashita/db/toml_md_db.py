import logging
import os
import sys
from copy import copy

import subhaashita
from doc_curation.md.file import MdFile
from sanskrit_data import collection_helper

import editdistance


def add(quotes, base_path, dry_run=False):
  for quote in quotes:
    key = quote.get_key()
    dir_path = base_path
    for letter in key[:5]:
      dir_path = os.path.join(dir_path, letter)
    (metadata, md) = quote.to_metadata_md()
    file_path = os.path.join(dir_path, key + ".md")
    while os.path.exists(file_path):
      quote_old = subhaashita.Quote.from_metadata_md_file(MdFile(file_path=file_path))
      quote_keys = quote.get_variant_keys()
      quote_old_keys = quote_old.get_variant_keys()
      distance = min([editdistance.eval(quote_keys[0], quote_old_key) / float(max(len(quote_keys[0]), len(quote_old_key))) for quote_old_key in quote_old_keys]) 
      if distance > 0.1:
        logging.warning("Quote key clash %0.2f detected: (%s vs %s)\n(%s vs %s)", distance, quote_keys[0], quote_old_keys[0], quote.get_text(), quote_old.get_text())
        key = quote.get_key(max_length=len(key) + 5)
        if len(key) >= subhaashita.HARD_MAX_KEY_LENGTH:
          key_parts = key.split("_")
          index = 1 if len(key_parts) == 1 else int(key_parts[1]) + 1
          key = "%s_%d" % (key, index)
          logging.warning("Quote key clash - forced to enumerate: %s (%s vs %s)", key, quote.get_text(), quote_old.get_text())
          # sys.exit()
        file_path = os.path.join(dir_path, key + ".md")
        continue
      else:
        metadata_old = quote_old.to_json_map()
        metadata = collection_helper.update_with_lists_as_sets(metadata_old, metadata)
        quote_text = quote.get_text()
        commentaries = quote._commentaries
        quote._commentaries = copy(quote_old._commentaries)
        quote._commentaries.update(commentaries)
        old_variants = quote_old.get_variants()
        quote.set_variants(old_variants)
        if quote_keys[0] not in quote_old_keys:
          old_variants.append(quote_text)
        (_, md) = quote.to_metadata_md()
        break
    md_file = MdFile(file_path=file_path)
    md_file.dump_to_file(metadata=metadata, content=md, dry_run=dry_run)
    

def standardize_file(md_file, dry_run=False):
  quote = subhaashita.Quote.from_metadata_md_file(md_file=md_file)
  (metadata, md) = quote.to_metadata_md()
  md_file.dump_to_file(metadata=metadata, content=md, dry_run=dry_run, silent=True)


def update_indices(quotes_path, dest_path):
  quotes_dict = library.apply_function(fn=subhaashita.Quote.from_metadata_md_file, dir_path=quotes_path, file_name_filter=lambda x: not os.path.basename(x).startswith("_"))
  
  indices = {}

  def update_dict(dict_d, keys, value):
    if keys:
      for key in keys:
        dict_d.setdefault(key, []).append(value)

  for quote_path, quote in quotes_dict.items():
    key = os.path.basename(quote_path).replace(".md", "")

    first_letter = quote.get_text()[0]
    indices.setdefault("first_letter", {}).setdefault(first_letter, []).append(key)

    for attr in ["topics", "sources", "types", "meters", "rasas", "bhaavas", "ornaments"]:
      update_dict(dict_d=indices.setdefault(attr, {}), keys=getattr(quote, attr), value=key)
    

  for attr, value_to_quote_keys in indices.items():
    outfile_path_attr = os.path.join(dest_path, attr)
    for value, quote_keys in value_to_quote_keys.items():
      outfile_path = os.path.join(outfile_path_attr, value + ".tsv")
      with open(outfile_path, "w") as outfile:
        outfile.write("\n".join(sorted(quote_keys)))
    outfile_path = os.path.join(outfile_path_attr, "items.tsv")
    with open(outfile_path, "w") as outfile:
      outfile.write("\n".join(sorted(value_to_quote_keys.keys())))

