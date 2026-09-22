from pathlib import Path
import copy
import json
import shutil
import tempfile
import unittest
from _load import ROOT, load
studio=load('connected_studio_test','skills/co-founder/scripts/connected_studio.py')

class ConnectedStudioTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name).resolve()/ 'project'
  shutil.copytree(ROOT/'examples/connected-brand/northline',self.root)
 def tearDown(self):self.temp.cleanup()
 def svg(self,source):
  p=self.root/'assets/test.svg';p.write_text(source);return p
 def test_approved_logo_embedded_exactly(self):
  html,b,sha=studio.compose(self.root,'post.html','post')
  self.assertNotIn('__BRAND_JSON__',html);self.assertIn(studio.asset_data(self.root/'assets/logo.svg'),html)
  self.assertEqual(b['project_id'],'northline-demo');self.assertEqual(len(sha),64)
 def test_private_root_not_embedded(self):
  html,_,_=studio.compose(self.root,'post.html','post');self.assertNotIn(str(self.root),html)
 def test_surface_uses_own_palette(self):
  _,post,_=studio.compose(self.root,'post.html','post');_,ui,_=studio.compose(self.root,'ui.html','product-ui');self.assertNotEqual(post['tokens']['background'],ui['tokens']['background'])
 def test_unknown_brand_rejected(self):
  with self.assertRaises(ValueError):studio.compose(self.root,'post.html','post','unknown')
 def test_other_project_template_not_read(self):
  with self.assertRaises(ValueError):studio.compose(self.root,'../other/post.html','post')
 def test_no_slot_rejected(self):
  (self.root/'test.html').write_text('<html>no binding</html>')
  with self.assertRaises(ValueError):studio.compose(self.root,'test.html','post')
 def test_multiple_slots_rejected(self):
  (self.root/'test.html').write_text('__BRAND_JSON__ __BRAND_JSON__')
  with self.assertRaises(ValueError):studio.compose(self.root,'test.html','post')
 def test_template_extension(self):
  (self.root/'test.txt').write_text('__BRAND_JSON__')
  with self.assertRaises(ValueError):studio.compose(self.root,'test.txt','post')
 def test_oversized_template(self):
  (self.root/'test.html').write_text('__BRAND_JSON__'+' '*1_000_001)
  with self.assertRaises(ValueError):studio.compose(self.root,'test.html','post')
 def test_json_cannot_terminate_script(self):
  p=self.root/'.co-founder/project.json';j=json.loads(p.read_text());j['display_name']='</script><script>bad()</script>';p.write_text(json.dumps(j))
  html,_,_=studio.compose(self.root,'post.html','post');self.assertNotIn('</script><script>bad()',html);self.assertIn('\\u003c/script',html)
 def test_build_is_not_render(self):
  out=Path(self.temp.name)/'post.html';r=studio.build(self.root,'post.html','post',out);self.assertTrue(out.is_file());self.assertFalse(r['rendered']);self.assertFalse(r['human_accepted'])
 def test_output_not_overwritten(self):
  out=Path(self.temp.name)/'post.html';out.write_text('existing')
  with self.assertRaises(ValueError):studio.build(self.root,'post.html','post',out)
  self.assertEqual(out.read_text(),'existing')
 def test_explicit_overwrite(self):
  out=Path(self.temp.name)/'post.html';out.write_text('existing');studio.build(self.root,'post.html','post',out,overwrite=True);self.assertNotEqual(out.read_text(),'existing')
 def test_no_font_embedding(self):
  f=self.root/'assets/font.woff2';f.write_bytes(b'font')
  with self.assertRaises(ValueError):studio.asset_data(f)
 def test_png_signature(self):
  f=self.root/'assets/image.png';f.write_bytes(b'not png')
  with self.assertRaises(ValueError):studio.asset_data(f)
 def test_webp_signature(self):
  f=self.root/'assets/image.webp';f.write_bytes(b'not webp')
  with self.assertRaises(ValueError):studio.asset_data(f)
 def test_safe_svg(self):self.assertTrue(studio.asset_data(self.svg('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>')).startswith('data:image/svg+xml;base64,'))
 def test_svg_script(self):
  with self.assertRaises(ValueError):studio.asset_data(self.svg('<svg><script>bad()</script></svg>'))
 def test_svg_handler(self):
  with self.assertRaises(ValueError):studio.asset_data(self.svg('<svg onload="bad()"/>'))
 def test_svg_entity(self):
  with self.assertRaises(ValueError):studio.asset_data(self.svg('<!DOCTYPE svg [<!ENTITY x SYSTEM "file:///private">]><svg>&x;</svg>'))
 def test_svg_external_image(self):
  with self.assertRaises(ValueError):studio.asset_data(self.svg('<svg><image href="https://example.invalid/a"/></svg>'))
 def test_svg_foreign_object(self):
  with self.assertRaises(ValueError):studio.asset_data(self.svg('<svg><foreignObject/></svg>'))
 def test_svg_css_external(self):
  with self.assertRaises(ValueError):studio.asset_data(self.svg('<svg fill="url(https://example.invalid/a)"/>'))
 def test_svg_animation_rejected(self):
  with self.assertRaises(ValueError):studio.asset_data(self.svg('<svg><animate attributeName="href" values="bad"/></svg>'))
 def test_asset_symlink(self):
  p=self.root/'assets/linked.svg';p.symlink_to(self.root/'assets/logo.svg')
  with self.assertRaises(ValueError):studio.asset_data(p)
 def test_export_bad_dimensions(self):
  with self.assertRaises(ValueError):studio.export(self.root,'post.html','post',Path(self.temp.name)/'post.png',width=True)
 def test_export_wrong_extension(self):
  with self.assertRaises(ValueError):studio.export(self.root,'post.html','post',Path(self.temp.name)/'post.mp4')
 def test_second_brand_is_distinct(self):
  _,a,_=studio.compose(self.root,'brand-proof.html','post')
  html,b,_=studio.compose(ROOT/'examples/connected-brand/second-project','brand-proof.html','post')
  self.assertNotEqual(a['project_id'],b['project_id']);self.assertNotEqual(a['tokens']['accent'],b['tokens']['accent']);self.assertNotEqual(a['typography']['heading'],b['typography']['heading']);self.assertNotIn('northline',html.lower())
 def test_missing_asset_does_not_fallback(self):
  (self.root/'assets/logo.svg').unlink()
  with self.assertRaises((ValueError,OSError)):studio.compose(self.root,'post.html','post')

if __name__=='__main__':unittest.main()
