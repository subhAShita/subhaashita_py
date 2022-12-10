import os

from doc_curation.md import library
from doc_curation.md.file import MdFile

from subhaashita import importer, Quote
from subhaashita.db import toml_md_db
from subhaashita.importer import subhaashita_ratna_bhaandaagaara, google_sheet
from indic_transliteration import sanscript

PATH_DB_SA = "/home/vvasuki/gitland/sanskrit/raw_etexts/kAvyam/padyam/subhAShitam/db_toml_md__sa__padya/main"
PATH_SRB = "/home/vvasuki/gitland/vishvAsa/kAvyam/content/laxyam/padyam/subhAShitam/subhAShita-ratna-bhANDAgAram/"
IMPORT_DIR = os.path.join(os.path.dirname(PATH_DB_SA), "to_import")


def dump_mss():
  quotes = importer.import_from_mss_tsv(tsv_path="/home/vvasuki/sanskrit/raw_etexts/mixed/gretil_devanAgarI/5_poetry/5_subhas/mahA-subhAShita-sangraha_1_per_line_dev.tsv")
  toml_md_db.add(quotes, base_path=PATH_DB_SA)


def prep_srb():
  # library.apply_function(fn=MdFile.split_to_bits, dir_path="/home/vvasuki/vishvAsa/kAvyam/content/laxyam/padyam/subhAShitam/subhAShita-ratna-bhANDAgAram/04_chitraprakaraNam/", frontmatter_type=MdFile.TOML, dry_run=False, source_script=sanscript.DEVANAGARI)
  # library.apply_function(fn=MdFile.split_to_bits, dir_path="/home/vvasuki/vishvAsa/kAvyam/content/laxyam/padyam/subhAShitam/subhAShita-ratna-bhANDAgAram/02_sAmAnyaprakaraNam_p1/", frontmatter_type=MdFile.TOML, dry_run=False, source_script=sanscript.DEVANAGARI)
  # library.apply_function(fn=MdFile.split_to_bits, dir_path="/home/vvasuki/vishvAsa/kAvyam/content/laxyam/padyam/subhAShitam/subhAShita-ratna-bhANDAgAram/03_rAjaprakaraNam/", frontmatter_type=MdFile.TOML, dry_run=False, source_script=sanscript.DEVANAGARI)
  library.apply_function(fn=MdFile.split_to_bits, dir_path="/home/vvasuki/vishvAsa/kAvyam/content/laxyam/padyam/subhAShitam/subhAShita-ratna-bhANDAgAram/06_navarasaprakaraNam/", frontmatter_type=MdFile.TOML, dry_run=False, source_script=sanscript.DEVANAGARI)

  pass

def dump_srb():
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "01_mangalAcharaNaprakaraNam"), deduce_from_title="topics")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "04_chitraprakaraNam/12_jAtivarNanam"), deduce_from_title="topics")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "04_chitraprakaraNam/"), deduce_from_title="types")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "02_sAmAnyaprakaraNam_p1"), deduce_from_title="topics")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "05_anyoktiprakaraNam"), deduce_from_title="types")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "03_rAjaprakaraNam"), deduce_from_title="topics")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "06_navarasaprakaraNam"), deduce_from_title="topics")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "06_navarasaprakaraNam/"), deduce_from_title="rasas", file_pattern="*.md")
  # quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "06_navarasaprakaraNam/09_shAntarasanirdeshaH"), deduce_from_title="topics", file_pattern="*.md")
  quotes = subhaashita_ratna_bhaandaagaara.from_dir(base_path=os.path.join(PATH_SRB, "06_navarasaprakaraNam/01_shRngArarasanirdeshaH"), deduce_from_title="topics", )
  toml_md_db.add(quotes, base_path=PATH_DB_SA)
  pass


def dump_dir():
  quotes_dict = library.apply_function(fn=Quote.from_metadata_md_file, dir_path=IMPORT_DIR, file_name_filter=lambda x: not os.path.basename(x).startswith("_"))
  toml_md_db.add(quotes_dict.values(), base_path=PATH_DB_SA)
  importer.empty_import_dir(IMPORT_DIR)


def standardize_all():
  # library.apply_function(fn=toml_md_db.standardize_file, dir_path=PATH_DB_SA, file_name_filter=lambda x: not os.path.basename(x).startswith("_"))
  library.apply_function(fn=toml_md_db.set_meters, dir_path=PATH_DB_SA, file_name_filter=lambda x: not os.path.basename(x).startswith("_"), dry_run=False)


def dump_sheets():
  quotes = google_sheet.import_all(worksheet_name="सं-पद्यानि")
  toml_md_db.add(quotes, base_path=PATH_DB_SA)


def dump_by_meter():
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="शार्दूलविक्रीडितम्", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/shArdUlavikrIDita/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="शिखरिणी", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/shikhariNI/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="स्रग्धरा", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/sragdharA/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="स्वागता", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/svAgatA/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="वियोगिनी", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/viyoginI/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="वसन्ततिलका", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/vasantatilakA/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="रथोद्धता", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/rathoddhatA/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="मालिनी", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/mAlinI/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="मन्दाक्रान्ता", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/mandAkrAntA/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="पुष्पिताग्रा", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/puShpitAgrA/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="द्रुतविलम्बितम्", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/drutavilambitam/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="गीति", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/gIti/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="उपेन्द्रवज्रा", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/indravajropajAti/kAvyam/upendravajra-subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="उपजाति", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/indravajropajAti/kAvyam/upajAti-subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="इन्द्रवज्रा", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/indravajropajAti/kAvyam/indravajra-subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="आर्या", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/AryA/kAvyam/subhAShita-db.md")
  toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="अनुष्टुप् (श्लोक)", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/anuShTup-shlokaH/kAvyam/subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="वंशस्थ", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/vaMshasthopajAtiH/kAvyam/vaMshastha-subhAShita-db.md")
  # toml_md_db.dump_matching(quotes_path=PATH_DB_SA, meter="हरिणी", dest_path="/home/vvasuki/gitland/sanskrit/tts-corpus/padyam/hariNI/kAvyam/subhAShita-db.md")
  pass


if __name__ == '__main__':
  # dump_mss()
  # dump_srb()
  # prep_srb()
  # standardize_all()
  # toml_md_db.update_indices(quotes_path=PATH_DB_SA, dest_path=os.path.join(os.path.dirname(PATH_DB_SA), "index"))
  # dump_dir()
  # dump_sheets()
  dump_by_meter()
  pass