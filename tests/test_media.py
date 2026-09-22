import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from _load import load,ROOT
media=load('media','skills/co-founder/scripts/media.py');audit=load('ui_audit','skills/co-founder/scripts/ui_audit.py')
class MediaTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.c=json.loads((ROOT/'skills/co-founder/assets/studio/sample-post.json').read_text())
 def tearDown(self):self.tmp.cleanup()
 def config(self,data=None):
  p=self.root/'config.json';p.write_text(json.dumps(data if data is not None else self.c));return p
 def test_all_samples_valid(self):
  for p in (ROOT/'skills/co-founder/assets/studio').glob('sample-*.json'):
   with self.subTest(p=p.name):self.assertEqual(media.load_config(p)['version'],1)
 def test_build_offline(self):
  p=self.root/'out.html';media.build(self.config(),p);s=p.read_text();self.assertIn("connect-src 'none'",s);self.assertNotIn('__CONFIG_JSON__',s)
 def test_script_injection_escaped(self):
  self.c['brand']='</script><script>alert(1)</script>';s=media.html_for(media.load_config(self.config()));self.assertNotIn('</script><script>alert',s)
 def test_color_rejected(self):
  self.c['theme']['accent']='url(https://invalid.example)'
  with self.assertRaises(media.MediaError):media.load_config(self.config())
 def test_dimensions_rejected(self):
  self.c['width']=20000
  with self.assertRaises(media.MediaError):media.load_config(self.config())
 def test_boolean_dimension_rejected(self):
  self.c['width']=True
  with self.assertRaises(media.MediaError):media.load_config(self.config())
 def test_long_copy_rejected(self):
  self.c['scenes'][0]['title']='x'*101
  with self.assertRaises(media.MediaError):media.load_config(self.config())
 def test_remote_asset_rejected(self):
  self.c['scenes'][0]['asset']='https://example.invalid/asset.png'
  with self.assertRaises(media.MediaError):media.load_config(self.config())
 def test_asset_escape_rejected(self):
  with self.assertRaises(media.MediaError):media.local_asset(self.root,'../private.png')
 def test_fake_image_rejected(self):
  (self.root/'bad.png').write_text('not a png')
  with self.assertRaises(media.MediaError):media.local_asset(self.root,'bad.png')
 def test_embedded_data_rejected(self):
  self.c['scenes'][0]['assetData']='data:text/html,whatever'
  with self.assertRaises(media.MediaError):media.load_config(self.config())
 def test_symlink_asset_rejected(self):
  (self.root/'file.png').write_bytes(b'\x89PNG\r\n\x1a\n')
  try:(self.root/'link.png').symlink_to(self.root/'file.png')
  except OSError:self.skipTest('symlink unavailable')
  with self.assertRaises(media.MediaError):media.local_asset(self.root,'link.png')
 def test_no_overwrite(self):
  p=self.root/'out.html';p.write_text('user file')
  with self.assertRaises(media.MediaError):media.build(self.config(),p)
 def test_explicit_overwrite(self):
  p=self.root/'out.html';p.write_text('user file');media.build(self.config(),p,True);self.assertIn('<!doctype',p.read_text())
 def test_odd_video_rejected(self):
  c=json.loads((ROOT/'skills/co-founder/assets/studio/sample-video.json').read_text());c['width']=1281
  with self.assertRaises(media.MediaError):media.load_config(self.config(c))
 def test_nan_duration_rejected(self):
  c=json.loads((ROOT/'skills/co-founder/assets/studio/sample-video.json').read_text());c['scenes'][0]['seconds']=float('nan')
  with self.assertRaises(media.MediaError):media.load_config(self.config(c))
 def test_loopback_audit_valid(self):self.assertEqual(audit.validate_target('http://127.0.0.1:8000',['/'])[0],'http://127.0.0.1:8000')
 def test_remote_audit_requires_permission(self):
  with self.assertRaises(audit.AuditError):audit.validate_target('https://example.invalid',['/'])
 def test_remote_explicit(self):self.assertTrue(audit.validate_target('https://example.invalid',['/'],True))
 def test_audit_credentials_rejected(self):
  with self.assertRaises(audit.AuditError):audit.origin('https://u:p@example.invalid')
 def test_audit_path_escape_rejected(self):
  with self.assertRaises(audit.AuditError):audit.validate_target('http://localhost:3000',['//example.invalid/'])
 def test_audit_file_scheme_rejected(self):
  with self.assertRaises(audit.AuditError):audit.validate_target('file:///etc/passwd',['/'])
 def test_viewport_valid(self):self.assertEqual(audit.viewport('390x844')['width'],390)
 def test_viewport_too_small(self):
  with self.assertRaises(audit.AuditError):audit.viewport('100x100')
if __name__=='__main__':unittest.main()
