import os

from doc_curation.md import library
from doc_curation.md.file import MdFile

from subhaashita import importer
from subhaashita.db import toml_md_db
from subhaashita.importer import subhaashita_ratna_bhaandaagaara
from indic_transliteration import sanscript

PATH_DB_SA = "/home/vvasuki/sanskrit/raw_etexts/kAvyam/padyam/subhAShitam/db_toml_md__sa__padya"
PATH_SRB = "/home/vvasuki/vishvAsa/kAvyam/content/laxyam/padyam/subhAShitam/subhAShita-ratna-bhANDAgAram/"


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


if __name__ == '__main__':
  # dump_mss()
  dump_srb()
  # prep_srb()
  pass