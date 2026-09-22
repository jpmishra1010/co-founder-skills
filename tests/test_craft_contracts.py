from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest
from _load import ROOT,load
validator=load('craft_contract_validator','scripts/validate.py')

class ContractTests(unittest.TestCase):
 def test_every_workflow_has_principles_and_binding(self):
  m=json.loads((ROOT/'manifest.json').read_text())
  for name in m['specialists']:
   s=(ROOT/'skills/co-founder/workflows'/f'{name}.md').read_text()
   self.assertIn('references/project-identity.md',s)
   self.assertIn(f'references/principles/{name}.md',s)
 def test_visual_production_no_universal_default(self):
  s=(ROOT/'skills/co-founder/references/media-production.md').read_text()
  self.assertIn('not a creative default',s);self.assertIn('project-local',s)
 def test_review_covers_all_specialists(self):
  m=json.loads((ROOT/'manifest.json').read_text());c=json.loads((ROOT/'skills/co-founder/references/review-contracts.json').read_text())
  self.assertEqual(set(m['specialists']),set(c['workflows']))
 def test_version_consistency(self):self.assertEqual((ROOT/'VERSION').read_text().strip(),json.loads((ROOT/'manifest.json').read_text())['version'])
 def test_no_external_reference_media_bundled(self):
  c=json.loads((ROOT/'skills/co-founder/references/research-catalog.json').read_text());self.assertFalse(c['source_media_included']);self.assertTrue(all(not x.get('media_redistributed',False) for x in c['sources']))
 @unittest.skipUnless(shutil.which('git'),'git not available')
 def test_only_exact_fictional_context_files_are_unignored(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);shutil.copy2(ROOT/'.gitignore',root/'.gitignore')
   subprocess.run(['git','init','-q',str(root)],check=True)
   cases={'.co-founder/brand.json':True,'examples/connected-brand/northline/.co-founder/project.json':False,'examples/connected-brand/northline/.co-founder/customer-data.json':True,'examples/connected-brand/second-project/.co-founder/brand.json':False,'examples/connected-brand/second-project/.co-founder/tasks/run.json':True}
   for rel,ignored in cases.items():
    p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}')
    result=subprocess.run(['git','-C',str(root),'check-ignore','-q',rel])
    self.assertEqual(result.returncode==0,ignored,rel)
 def test_validator_detects_missing_principles(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)/'pack';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.git'))
   (root/'skills/co-founder/references/principles/sales.md').unlink()
   self.assertIn('Missing workflow principles: sales',validator.validate(root)['errors'])
 def test_validator_detects_private_context(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)/'pack';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.git'))
   p=root/'.co-founder';p.mkdir();(p/'private.json').write_text('{}')
   self.assertTrue(any('Unexpected private-context' in e for e in validator.validate(root)['errors']))

if __name__=='__main__':unittest.main()
