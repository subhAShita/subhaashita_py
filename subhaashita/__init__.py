import logging
import os
import sys
import textwrap

import chandas
import methodtools
import regex
from bs4 import BeautifulSoup
from curation_utils import file_helper
from doc_curation.utils import text_utils
from indic_transliteration import deduplication, sanscript, detect
from sanskrit_data.schema import common
from sanskrit_data.schema.common import JsonObject


class Commentary(JsonObject):
  
  def __init__(self, name, content):
    self.name = name
    self.content = content

  def to_details_tag(self, attributes=""):
    details_tag_start = ("details %s" % attributes).strip()
    return textwrap.dedent("""
    <%s><summary>%s</summary>
    
    %s
    </details>
    """) % (details_tag_start, self.name, self.content)


HARD_MAX_KEY_LENGTH = 20
MAX_KEY_LENGTH = 10


class CommentaryKey(object):
  TEXT = "Text"
  VARIANT_JOINER = "\n_________\n"
  VISH = "विश्वास-प्रस्तुतिः"
  pass


class Quote(JsonObject):

  def __init__(self, variants, topics=None, sources=None, secondary_sources=None, commentaries=None, types=None, ratings=None, ornaments=None, rasas=None, bhaavas=None, meters=None, pratimaalaa_letters=None):
    self.topics = topics
    self.sources = sources
    self.secondary_sources = secondary_sources
    self._commentaries = commentaries if commentaries is not None else {}
    self.set_variants(variants=variants)
    self.types = types
    self.ratings = ratings
    self.ornaments = ornaments
    self.rasas = rasas
    self.meters = meters
    self.bhaavas = bhaavas
    self.pratimaalaa_letters = pratimaalaa_letters
    self._script = None
  
  def __repr__(self):
    return self._commentaries[CommentaryKey.TEXT]

  @methodtools.lru_cache()
  def get_variants(self):
    VARIANT_JOINER_PATTERN = "\n____+ *\n"
    return regex.split(VARIANT_JOINER_PATTERN, self._commentaries[CommentaryKey.TEXT])

  def get_variant_keys(self):
    return [file_helper.get_storage_name(text=x, max_length=None, source_script=self._script) for x in self.get_variants()]

  def set_variants(self, variants):
    self._commentaries[CommentaryKey.TEXT] = CommentaryKey.VARIANT_JOINER.join(variants)

  def get_text(self):
    return self.get_variants()[0]
  
  def get_key(self, max_length=MAX_KEY_LENGTH):
    return file_helper.get_storage_name(text=self.get_text().toLowerCase(), max_length=max(max_length, HARD_MAX_KEY_LENGTH), source_script=self._script)

  def make_title(self):
    return text_utils.title_from_text(text=self.get_text(), script=self._script)

  def to_metadata_md(self):
    metadata = self.to_json_map()
    metadata["title"] = self.make_title()
    commentaries = self._commentaries
    commentary_order = [CommentaryKey.VISH, CommentaryKey.TEXT, "MT"]
    commentaries_sorted = []
    for name in commentary_order: 
      if name in commentaries:
        commentaries_sorted.append(Commentary(name=name, content=commentaries[name]))
    commentaries_sorted.extend([Commentary(name=name, content=commentary) for name, commentary in commentaries.items() if name not in commentary_order])
    detail_elements = [commentaries_sorted[0].to_details_tag(attributes="open")]
    if len(commentaries_sorted) > 1:
      detail_elements.extend([commentary.to_details_tag(attributes="") for commentary in commentaries_sorted[1:]])
    md = "\n\n".join(detail_elements)
    md = regex.sub("\n\n\n*", "\n\n", md)
    return (metadata, md)

  @classmethod
  def from_metadata_md(cls, metadata, md):
    soup = BeautifulSoup(md, features="lxml")
    commentaries = {}
    for detail in soup.find("body").findChildren("details", recursive=False):
      summary = detail.find("summary")
      summary.extract()
      comment_key = summary.text
      if comment_key == "मूलम्":
        comment_key = CommentaryKey.TEXT
      commentaries[comment_key] = detail.text.strip()
    metadata.pop("title", None)
    obj = common.JsonObject.make_from_dict(input_dict=metadata)
    obj._commentaries = commentaries
    obj._script = detect.detect(commentaries[CommentaryKey.TEXT])
    return obj

  @classmethod
  def from_metadata_md_file(cls, md_file, delete_file=False):
    (metadata, md) = md_file.read()
    try:
      quote = Quote.from_metadata_md(metadata=metadata, md=md)
    except ValueError:
      logging.error("Illegal file contents: %s", md_file.file_path)    
      sys.exit(-1)
    if delete_file:
      os.remove(path=md_file.file_path)
    return quote


class Subhaashita(Quote):
  def __init__(self, variants, topics=None, sources=None, secondary_sources=None, commentaries=None, types=None, ratings=None, ornaments=None, rasas=None, bhaavas=None, meters=None, script=sanscript.DEVANAGARI):
    super(Subhaashita, self).__init__(variants=variants, topics=topics, sources=sources, secondary_sources=secondary_sources, commentaries=commentaries, types=types, ratings=ratings, ornaments=ornaments, rasas=rasas, bhaavas=bhaavas, meters=meters)
    # Note: This constructor is not called when the object is automatically constructed from a dict.
    self._script=script
    self.pratimaalaa_letters = None

  def get_key(self, max_length=MAX_KEY_LENGTH):
    approx_key = deduplication.get_approx_deduplicating_key(text=self.get_text())
    return file_helper.get_storage_name(text=approx_key, max_length=max_length, source_script=self._script)

  def get_variant_keys(self):
    return [deduplication.get_approx_deduplicating_key(text=x) for x in self.get_variants()]

  def set_pratimaalaa_letters(self):
    quote_text = self.get_text()
    consonants = sanscript.SCHEMES[sanscript.DEVANAGARI].get_consonant_letters(quote_text)
    # logging.debug(md_file)
    last_letter = consonants[-1]
    pratimaalaa_letters = [last_letter]
    if last_letter in "ख-घ-छ-झ-ट-ठ-ड-ढ-ण-ङ-ञ-थ-ष":
      pratimaalaa_letters.extend("अआइईउऊऋॠऌॡऎएऐऒओऔ")
  
    last_letter_index = -1
    while last_letter in "मत":
      last_letter_index = last_letter_index - 1
      last_letter = consonants[last_letter_index]
      pratimaalaa_letters.append(last_letter)
    try:
      first_letter_second_half = regex.search("\w", quote_text.split("।")[-1]).group(0)
      pratimaalaa_letters.append(first_letter_second_half)
    except AttributeError:
      logging.error(f"{quote_text}")
    self.pratimaalaa_letters = list(set(pratimaalaa_letters))


  def set_meters(self):
    pattern_lines = chandas.to_pattern_lines(self.get_text().split("\n"))
    id_result = chandas.svat_identifier.IdentifyFromPatternLines(pattern_lines)
    from sortedcontainers import SortedSet
  
    if self.meters is None:
      meters = SortedSet()
    else:
      meters = SortedSet(self.meters)
    meters = meters.union([sanscript.transliterate(metre.lower(), _from=sanscript.IAST, _to=sanscript.DEVANAGARI) for metre in id_result.get('exact', {}).keys()])
    if len(meters) == 0:
      meters.add("UNKNOWN")
    if len(meters) > 1 and "UNKNOWN" in meters:
      meters.remove("UNKNOWN")
    self.meters = list(meters)

# Essential for depickling to work.
common.update_json_class_index(sys.modules[__name__])
logging.debug(common.json_class_index)
