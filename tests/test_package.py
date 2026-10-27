from pathlib import Path
import json
import unittest
from _load import load,ROOT
validator=load('validator','scripts/validate.py')
class PackageTests(unittest.TestCase):
 def test_structure(self):self.assertEqual(validator.validate()['errors'],[])
 def test_fourteen_entries(self):self.assertEqual(validator.validate()['skill_count'],14)
 def test_thirteen_workflows(self):self.assertEqual(validator.validate()['workflow_count'],13)
 def test_reference_limits_explicit(self):
  r=json.loads((ROOT/'skills/co-founder/references/research-catalog.json').read_text());self.assertTrue(r['no_full_external_video_playback']);self.assertFalse(r['source_media_included'])
 def test_evaluations_not_claimed(self):
  r=json.loads((ROOT/'evals/cases.json').read_text());self.assertFalse(r['results_claimed']);self.assertTrue(all(c['execution_status']=='not-run' for c in r['cases']))
 def test_no_hidden_model_requirement(self):self.assertFalse(json.loads((ROOT/'manifest.json').read_text())['model_api_required'])
 def test_templates_private_placeholders(self):self.assertIn('UNSET',(ROOT/'skills/co-founder/assets/templates/company.md').read_text())
 def test_core_has_no_permission_grants(self):
  s=(ROOT/'skills/co-founder/SKILL.md').read_text().split('---',2)[1];self.assertNotIn('allowed-tools:',s);self.assertNotIn('context: fork',s)
 def test_category_coverage(self):self.assertEqual(len(list((ROOT/'skills/co-founder/references/categories').glob('*.md'))),17)
 def test_no_font_files(self):
  self.assertFalse([p for p in ROOT.rglob('*') if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'}])
if __name__=='__main__':unittest.main()
