import os

import subhaashita
from doc_curation.md.file import MdFile
from subhaashita import Subhaashita
from subhaashita.db import toml_md_db

PATH_DB_SA = os.path.join(os.path.dirname(__file__), "data", "corpus")


def test_get_text():
  content = """<details><summary>Text</summary>

अभिनवनवनीतप्रीतमाताम्रनेत्रं विकचनलिनलक्ष्मीस्पर्धि सानन्दवक्त्रम्।  
हृदयभवनमध्ये योगिभिर्ध्यानगम्यं नवगगनतमालश्यामलं कंचिदीडे॥
_________
अभिनवनवनीतप्रीतमाताम्रवेत्रं विकचनलिनलक्ष्मीस्पर्धि सानन्दवक्त्रम्।  
हृदयभवनमध्ये योगिभिर्ध्यानगम्यं नवगगनतमालश्यामलं कंचिदीडे॥
</details>"""
  metadata = {"jsonClass" : "Subhaashita"}
  quote = subhaashita.Quote.from_metadata_md(metadata=metadata, md=content)
  expected_text = """अभिनवनवनीतप्रीतमाताम्रनेत्रं विकचनलिनलक्ष्मीस्पर्धि सानन्दवक्त्रम्।  
हृदयभवनमध्ये योगिभिर्ध्यानगम्यं नवगगनतमालश्यामलं कंचिदीडे॥"""
  assert quote.get_text() == expected_text
  pass


def test_add():
  text = """एक एव खगो मानी चिरं जीवतु चातकः।  
    म्रियते वा पिपासायां याचते वा पुरन्दरम्॥"""
  quotes = [Subhaashita(variants=[text])]
  toml_md_db.add(quotes, base_path=PATH_DB_SA)
  assert not os.path.exists(os.path.join(PATH_DB_SA, "e/k/a/e/v/ekaevakhagomAmI.md"))




def test_standardize():
  md_file = MdFile(file_path=os.path.join(PATH_DB_SA, "k/A/v/e/r/kAverIvAri.md"))
  (metadata_old, md_old) = md_file.read()
  toml_md_db.standardize_file(md_file=md_file)
  (metadata, md) = md_file.read()
  assert md_old == md
  assert metadata_old == metadata