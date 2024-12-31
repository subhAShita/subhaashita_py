import doc_curation.utils.sanskrit_helper
import doc_curation.md.content_processor.stripper
import regex
from doc_curation.md import library, content_processor
from doc_curation.md.content_processor import ocr_helper, details_helper
from doc_curation.md.file import MdFile
from doc_curation.utils import patterns, sanskrit_helper

from subhaashita import Subhaashita

SUB = "/home/vvasuki/gitland/vishvAsa/kAvyam/content/laxyam/padyam/subhAShitam/subrahmaNya-sangrahaH.md"

def prep_file(dir_path=SUB):  
  library.apply_function(fn=MdFile.transform, dir_path=dir_path, content_transformer=lambda x, y: ocr_helper.misc_sanskrit_typos(x))
  library.apply_function(fn=MdFile.transform, dir_path=dir_path, content_transformer=lambda x, y: sanskrit_helper.fix_lazy_anusvaara(x), dry_run=False, silent_iteration=False)
  library.apply_function(fn=MdFile.transform, dir_path=dir_path, content_transformer=lambda x, y: sanskrit_helper.fix_bad_visargas(x), dry_run=False, silent_iteration=False)
  library.apply_function(fn=MdFile.transform, dir_path=dir_path, content_transformer=lambda x, y: sanskrit_helper.fix_bad_anunaasikas(x), dry_run=False, silent_iteration=False)
  if dir_path == SUB:
    library.apply_function(fn=content_processor.replace_texts, dir_path=dir_path, patterns=[r"(?<=\n)\*\*(.+)\*\*(?= *\n)"], replacement=r"\1")
  


def import_vimuula(md_file, sources=None, secondary_sources=None):
  quotes = []
  bunches = details_helper.get_detail_bunches(md_file=md_file)
  for bunch in bunches:
    ratings = []
    topics = None
    commentaries = {}
    variants = []
    for detail in bunch:
      sources_quote = sources
      if detail.title.startswith("विश्वास-प्रस्तुतिः"):
        detail_ratings = regex.findall(r"(?<=\+\+\+\()([\d०-९])", detail.content)
        rating = None
        for r in detail_ratings:
          r = int(r)
          if rating is None or rating < r:
            rating = r
        if rating is not None:
          ratings.append(f"vvasuki:{rating}")
        commentaries["विश्वास-प्रस्तुतिः"] = detail.content
      elif detail.title.startswith("विषयः"):
        topics = [x.strip() for x in detail.content.split(",")]
      elif detail.title.startswith("स्रोतः"):
        sources_quote = [x.strip() for x in detail.content.split(",")]
      elif detail.title.startswith("मूलम्"):
        variants.append(detail.content.strip())
      else:
        commentaries[detail.title.strip()] = detail.content.strip()
    if ratings == []:
      ratings = None
    quote = Subhaashita(variants=variants, commentaries=commentaries, ratings=ratings, sources=sources_quote, secondary_sources=secondary_sources, topics=topics)
    quote.set_meters()
    quote.set_pratimaalaa_letters()
    quotes.append(quote)
  return quotes


if __name__ == '__main__':
  prep_file()
  pass