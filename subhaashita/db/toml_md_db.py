import logging
import os
import shutil
from copy import copy

import editdistance
import regex
from sanskrit_data import collection_helper
from tqdm import tqdm

import chandas
import subhaashita
from curation_utils import file_helper
from doc_curation.md import library
from doc_curation.md.file import MdFile
from indic_transliteration import sanscript


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
        key = regex.sub("\(.+?\)", "", key).strip()
        dict_d.setdefault(key.strip(), []).append(value)

  shutil.rmtree(dest_path, ignore_errors=True)
  for quote_path, quote in quotes_dict.items():
    key = os.path.basename(quote_path).replace(".md", "")

    # The below works for punctuated devanAgarI as well!
    first_letter = regex.search("\w", quote.get_text()).group(0)
    if quote._script is not None and first_letter == sanscript.transliterate("ॐ", sanscript.DEVANAGARI, quote._script):
      first_letter = sanscript.transliterate("ओ", sanscript.DEVANAGARI, quote._script)

    indices.setdefault("first_letter", {}).setdefault(first_letter, []).append(key)

    for attr in ["topics", "sources", "types", "meters", "rasas", "bhaavas", "ornaments", "ratings"]:
      update_dict(dict_d=indices.setdefault(attr, {}), keys=getattr(quote, attr), value=key)
    

  for attr, value_to_quote_keys in indices.items():
    outfile_path_attr = os.path.join(dest_path, attr)
    logging.info("Updating %s", outfile_path_attr)
    attr_summary = []
    os.makedirs(outfile_path_attr, exist_ok=True)
    for attr_value in tqdm(sorted(value_to_quote_keys.keys())):
      attr_value = regex.sub("\(.+?\)", "", attr_value).strip()
      attr_value_optitrans = file_helper.get_storage_name(attr_value)
      quote_keys = sorted(value_to_quote_keys[attr_value])
      quote_count = len(value_to_quote_keys[attr_value])
      if quote_count < 5:
        file_key = file_helper.get_storage_name(attr_value)
      else:
        file_key = ""
        outfile_path = os.path.join(outfile_path_attr, attr_value_optitrans + ".tsv")
        with open(outfile_path, "w") as outfile:
          outfile.write("\n".join(quote_keys))
        quote_keys = []
      attr_summary.append("%s\t%d\t%s\t%s" % (attr_value, quote_count, file_key, ", ".join(quote_keys)))
    if len(attr_summary) > 0:
      outfile_path = os.path.join(outfile_path_attr, "_summary.tsv")
      with open(outfile_path, "w") as attr_stats_file:
        attr_stats_file.write("value\tfile_key\tquote_count\tquote_keys\n")
        attr_stats_file.write("\n".join(attr_summary))


def set_meters(md_file, dry_run=False):
  quote = subhaashita.Quote.from_metadata_md_file(md_file=md_file)
  pattern_lines = chandas.to_pattern_lines(quote.get_text().split("\n"))
  id_result = chandas.svat_identifier.IdentifyFromPatternLines(pattern_lines)
  from sortedcontainers import SortedSet

  if quote.meters is None:
    meters = SortedSet()
  else:
    meters = SortedSet(quote.meters)
  meters = meters.union([sanscript.transliterate(metre.lower(), _from=sanscript.IAST, _to=sanscript.DEVANAGARI) for metre in id_result.get('exact', {}).keys()])
  if len(meters) == 0:
    meters.add("UNKNOWN")
  if len(meters) > 1 and "UNKNOWN" in meters:
      meters.remove("UNKNOWN")
  quote.meters = list(meters)

  (metadata, md) = quote.to_metadata_md()
  md_file.dump_to_file(metadata=metadata, content=md, dry_run=dry_run, silent=True)


def filter(quotes_path, filter_fn):
  quotes_dict = library.apply_function(fn=subhaashita.Quote.from_metadata_md_file, dir_path=quotes_path, file_name_filter=lambda x: not os.path.basename(x).startswith("_"))
  results = {}
  for quote_path, quote in quotes_dict.items():
    if filter_fn(quote):
      results[quote_path] = quote
  return results


def dump_matching(quotes_path, dest_path, meter):
  def filter_fn(x):
    selected = True
    if meter is not None and x.meters is not None:
      selected &= meter in x.meters
    return selected

  quotes_dict = filter(quotes_path=quotes_path, filter_fn=filter_fn)
  content = "\n\n".join([str(x) for x in quotes_dict.values()])
  dest_md = MdFile(file_path=dest_path)
  dest_md.dump_to_file(metadata={"title": f"m:{meter}"}, content=content, dry_run=False)
  pass
