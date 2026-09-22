import json
import os
from pathlib import Path
import tempfile
import unittest
from _load import load,ROOT
ins=load('installer','scripts/install.py')
class InstallerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.src=self.root/'source';self.src.mkdir();(self.src/'SKILL.md').write_text('fixture');self.target=self.root/'skills/co-founder';self.back=self.root/'backups'
 def tearDown(self):self.tmp.cleanup()
 def install(self,**kw):return ins.install_one(self.src,self.target,self.back,**kw)
 def test_install(self):self.install();self.assertTrue((self.target/'SKILL.md').exists())
 def test_idempotent(self):self.install();self.assertIn('unchanged',self.install())
 def test_dry_no_write(self):self.install(dry_run=True);self.assertFalse(self.target.exists())
 def test_collision(self):
  self.target.mkdir(parents=True)
  with self.assertRaises(ins.InstallError):self.install()
 def test_modified_refused(self):
  self.install();(self.target/'SKILL.md').write_text('custom')
  with self.assertRaises(ins.InstallError):self.install(update=True)
 def test_update_requires_flag(self):
  self.install();(self.src/'SKILL.md').write_text('new')
  with self.assertRaises(ins.InstallError):self.install()
 def test_update_backup(self):
  self.install();(self.src/'SKILL.md').write_text('new');self.install(update=True);self.assertEqual((self.target/'SKILL.md').read_text(),'new');self.assertEqual(len(list(self.back.iterdir())),1)
 def test_modified_explicit_backup(self):
  self.install();(self.target/'SKILL.md').write_text('custom');self.install(update=True,replace_modified=True);self.assertEqual(next(self.back.iterdir()).joinpath('SKILL.md').read_text(),'custom')
 def test_uninstall_backup(self):self.install();ins.uninstall_one(self.target,self.back);self.assertFalse(self.target.exists());self.assertTrue(self.back.is_dir())
 def test_uninstall_modified_refused(self):
  self.install();(self.target/'extra.md').write_text('x')
  with self.assertRaises(ins.InstallError):ins.uninstall_one(self.target,self.back)
 def test_uninstall_force_managed(self):
  self.install();(self.target/'extra.md').write_text('x');ins.uninstall_one(self.target,self.back,force=True);self.assertFalse(self.target.exists())
 def test_uninstall_cannot_force_unmanaged(self):
  self.target.mkdir(parents=True)
  with self.assertRaises(ins.InstallError):ins.uninstall_one(self.target,self.back,force=True)
 def test_symlink_rejected(self):
  self.target.parent.mkdir()
  try:self.target.symlink_to(self.src,target_is_directory=True)
  except OSError:self.skipTest('symlink unavailable')
  with self.assertRaises(ins.InstallError):self.install()
 def test_source_symlink_rejected(self):
  try:(self.src/'bad').symlink_to(self.src/'SKILL.md')
  except OSError:self.skipTest('symlink unavailable')
  with self.assertRaises(ins.InstallError):self.install()
 def test_locations_user(self):
  loc=list(ins.locations('both','user',None,str(self.root)));self.assertEqual(len(loc),2);self.assertEqual(loc[0][1],self.root/'.agents/skills')
 def test_project_requires_path(self):
  with self.assertRaises(ins.InstallError):list(ins.locations('codex','project',None,str(self.root)))
 def test_full_package_has_valid_sources(self):
  for path in (ROOT/'skills').iterdir():self.assertTrue(ins.hashes(path))
if __name__=='__main__':unittest.main()
