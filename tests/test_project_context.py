import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from _load import load,ROOT
pc=load('project_context_test','skills/co-founder/scripts/project_context.py')
qg=load('quality_gate_test','skills/co-founder/scripts/quality_gate.py')

class ProjectTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.make(self.root,'alpha')
 def tearDown(self):self.tmp.cleanup()
 def write(self,path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj))
 def read(self,name):return json.loads((self.root/'.co-founder'/name).read_text())
 def update(self,name,obj):self.write(self.root/'.co-founder'/name,obj)
 def make(self,root,pid):
  ctx=root/'.co-founder';ctx.mkdir(parents=True);(root/'assets').mkdir();(root/'assets/logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
  self.write(ctx/'project.json',{'schema_version':1,'project_id':pid,'display_name':pid,'confirmed':True,'default_brand':'product','brands':{'product':{'profile':'brand.json','assets':'assets.json'}}})
  self.write(ctx/'brand.json',{'schema_version':2,'project_id':pid,'brand_id':'product','status':'approved','approved_by':'fixture','approval_source':'synthetic test declaration','tokens':{'background':'#FFFFFF','foreground':'#121212','accent':'#234567'},'typography':{'heading':'Arial','body':'Arial'},'surfaces':{k:{'status':'approved','direction':'fixture','required_asset_ids':['logo'],'tokens':{},'logo_policy':'required'} for k in ['product-ui','website','post','video']}})
  self.write(ctx/'assets.json',{'schema_version':1,'project_id':pid,'assets':[{'id':'logo','project_id':pid,'path':'assets/logo.svg','sha256':pc.digest(root/'assets/logo.svg'),'role':'logo','status':'approved','source':'original fixture','rights':'MIT','surfaces':['product-ui','website','post','video']}]})
 def test_resolve_exact(self):self.assertEqual(pc.resolve(self.root)['project_id'],'alpha')
 def test_resolve_nested(self):
  p=self.root/'src/components';p.mkdir(parents=True);self.assertEqual(pc.resolve(p)['root'],str(self.root))
 def test_wrong_requested_id(self):
  with self.assertRaises(pc.ProjectError):pc.resolve(self.root,'other')
 def test_no_guess_from_folder(self):
  p=self.root/'other';p.mkdir();(p/'.git').mkdir()
  with self.assertRaises(pc.ProjectError):pc.resolve(p)
 def test_missing_project(self):
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(pc.ProjectError):pc.resolve(Path(td).resolve())
 def test_general_does_not_load_brand(self):
  (self.root/'.co-founder/brand.json').unlink();self.assertEqual(pc.bundle(self.root)['assets'],[])
 def test_general_rejects_asset(self):
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,asset_ids=['logo'])
 def test_bundle(self):
  b=pc.bundle(self.root,'post');self.assertEqual(b['project_id'],'alpha');self.assertEqual(b['assets'][0]['id'],'logo');self.assertEqual(len(b['fingerprint']),64)
 def test_ui_alias(self):self.assertEqual(pc.bundle(self.root,'ui')['surface'],'product-ui')
 def test_stable_bundle(self):self.assertEqual(pc.bundle(self.root,'post')['fingerprint'],pc.bundle(self.root,'post')['fingerprint'])
 def test_unconfirmed(self):
  p=self.read('project.json');p['confirmed']=False;self.update('project.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_v1_requires_migration(self):
  p=self.read('brand.json');p['schema_version']=1;self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_unapproved_brand(self):
  p=self.read('brand.json');p['status']='unapproved';self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_missing_approval_source(self):
  p=self.read('brand.json');p['approval_source']=None;self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_cross_brand(self):
  p=self.read('brand.json');p['brand_id']='personal';self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_unknown_brand(self):
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post','personal')
 def test_cross_project_profile(self):
  p=self.read('brand.json');p['project_id']='beta';self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_cross_project_asset(self):
  p=self.read('assets.json');p['assets'][0]['project_id']='beta';self.update('assets.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_cross_project_registry(self):
  p=self.read('assets.json');p['project_id']='beta';self.update('assets.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_surface_approval(self):
  p=self.read('brand.json');p['surfaces']['video']['status']='unapproved';self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'video')
 def test_surface_specific_tokens(self):
  p=self.read('brand.json');p['surfaces']['post']['tokens']={'background':'#FAFAFA'};self.update('brand.json',p)
  self.assertEqual(pc.bundle(self.root,'post')['tokens']['background'],'#FAFAFA');self.assertEqual(pc.bundle(self.root,'ui')['tokens']['background'],'#FFFFFF')
 def test_missing_color_role(self):
  p=self.read('brand.json');del p['tokens']['accent'];self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_bad_color(self):
  p=self.read('brand.json');p['tokens']['accent']='blue;url(https://bad.invalid)';self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_changed_asset(self):
  (self.root/'assets/logo.svg').write_text('changed')
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_unapproved_asset(self):
  p=self.read('assets.json');p['assets'][0]['status']='candidate';self.update('assets.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_wrong_surface_asset(self):
  p=self.read('assets.json');p['assets'][0]['surfaces']=['video'];self.update('assets.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_asset_traversal(self):
  p=self.read('assets.json');p['assets'][0]['path']='../outside.svg';self.update('assets.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_asset_secret(self):
  p=self.read('assets.json');p['assets'][0]['path']='.env';self.update('assets.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_duplicate_asset(self):
  p=self.read('assets.json');p['assets'].append(copy.deepcopy(p['assets'][0]));self.update('assets.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_missing_asset(self):
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post',asset_ids=['unknown'])
 def test_logo_omission(self):
  p=self.read('brand.json');p['surfaces']['post'].update(required_asset_ids=[],logo_policy='omit');self.update('brand.json',p)
  self.assertEqual(pc.bundle(self.root,'post')['assets'],[])
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post',asset_ids=['logo'])
 def test_logo_required(self):
  p=self.read('brand.json');p['surfaces']['post']['required_asset_ids']=[];self.update('brand.json',p)
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'post')
 def test_lock_current(self):
  b=pc.bundle(self.root,'post');p=pc.write_lock(b,'demo');self.assertEqual(pc.check(self.root,p)['status'],'current')
 def test_lock_not_overwritten(self):
  b=pc.bundle(self.root,'post');pc.write_lock(b,'demo')
  with self.assertRaises(pc.ProjectError):pc.write_lock(b,'demo')
 def test_lock_wrong_project(self):
  b=pc.bundle(self.root,'post');p=pc.write_lock(b,'demo');other=self.root/'other';self.make(other,'beta')
  with self.assertRaises(pc.ProjectError):pc.check(other,p)
 def test_lock_stale(self):
  b=pc.bundle(self.root,'post');p=pc.write_lock(b,'demo');d=self.read('brand.json');d['voice']=['new approved voice'];self.update('brand.json',d)
  with self.assertRaises(pc.ProjectError):pc.check(self.root,p)
 def test_task_traversal(self):
  with self.assertRaises(pc.ProjectError):pc.write_lock(pc.bundle(self.root),'../bad')
 def test_inventory_candidates_only(self):
  d=pc.inventory(self.root,['assets']);self.assertFalse(d['contents_read']);self.assertFalse(d['approval_changed']);self.assertEqual(len(d['candidates']),1)
 def test_inventory_bounded(self):
  (self.root/'assets/x.svg').write_text('<svg/>');self.assertTrue(pc.inventory(self.root,['assets'],1)['truncated'])
 def test_symlink_rejected(self):
  q=self.root/'linked';q.symlink_to(self.root/'assets',target_is_directory=True)
  with self.assertRaises(pc.ProjectError):pc.inventory(self.root,['linked'])
 def test_workspace_selection(self):
  (self.root/'.co-founder/project.json').unlink();self.make(self.root/'a','a');self.make(self.root/'b','b')
  self.update('workspace.json',{'schema_version':1,'projects':[{'id':'a','root':'a'},{'id':'b','root':'b'}]})
  with self.assertRaises(pc.ProjectError):pc.resolve(self.root)
  self.assertEqual(pc.resolve(self.root,'b')['project_id'],'b')
  self.assertEqual(pc.resolve(self.root/'a')['project_id'],'a')
 def test_workspace_mismatch(self):
  (self.root/'.co-founder/project.json').unlink();self.make(self.root/'b','wrong')
  self.update('workspace.json',{'schema_version':1,'projects':[{'id':'b','root':'b'}]})
  with self.assertRaises(pc.ProjectError):pc.resolve(self.root,'b')
 def test_invalid_surface(self):
  with self.assertRaises(pc.ProjectError):pc.bundle(self.root,'whatever')

class QualityTests(unittest.TestCase):
 def base(self,workflow='decide'):
  c=json.loads((ROOT/'skills/co-founder/references/review-contracts.json').read_text())
  return {'schema_version':1,'project_id':'alpha','bundle_fingerprint':'a'*64,'workflow':workflow,'surface':'general','checks':[{'id':r['id'],'status':'pass','evidence':['fixture/evidence.json']} for r in c['common']+c['workflows'][workflow]]}
 def visual(self,surface='post'):
  r=self.base('content-studio');r.update(surface=surface,artifact_sha256='b'*64,artifact_path='draft.png',visual_observations=[{'location':'headline','observation':'Fits at actual feed size','evidence':'draft.png'}],reference_observations=[{'access':'approved-project-reference','observation':'Uses approved hierarchy','source':'approved.png'}],revisions=[{'issue':'too dense','change':'shortened supporting line'}]);return r
 def test_general_ready_is_not_acceptance(self):
  r=qg.evaluate(self.base());self.assertEqual(r['status'],'ready-for-human-review');self.assertIsNone(r['human_acceptance'])
 def test_every_workflow_contract(self):
  for w in json.loads((ROOT/'manifest.json').read_text())['specialists']:
   if w not in {'ui-polish','content-studio'}:self.assertEqual(qg.evaluate(self.base(w))['status'],'ready-for-human-review')
 def test_missing_check(self):
  r=self.base();r['checks'].pop();self.assertEqual(qg.evaluate(r)['status'],'inconclusive')
 def test_revise_blocks(self):
  r=self.base();r['checks'][0]['status']='revise';self.assertEqual(qg.evaluate(r)['status'],'blocked')
 def test_not_checked(self):
  r=self.base();r['checks'][1]['status']='not-checked';self.assertEqual(qg.evaluate(r)['status'],'inconclusive')
 def test_cannot_waive_project(self):
  r=self.base();r['checks'][0].update(status='not-applicable',reason='not relevant according to reviewer');self.assertEqual(qg.evaluate(r)['status'],'blocked')
 def test_no_evidence(self):
  r=self.base();r['checks'][2]['evidence']=[];self.assertEqual(qg.evaluate(r)['status'],'inconclusive')
 def test_duplicate(self):
  r=self.base();r['checks'].append(r['checks'][0])
  with self.assertRaises(qg.ReviewError):qg.evaluate(r)
 def test_wrong_workflow(self):
  r=self.base();r['workflow']='unknown'
  with self.assertRaises(qg.ReviewError):qg.evaluate(r)
 def test_unbound(self):
  r=self.base();r['bundle_fingerprint']=''
  with self.assertRaises(qg.ReviewError):qg.evaluate(r)
 def test_visual_needs_inspection(self):
  r=self.visual();r['visual_observations']=[];self.assertIn('actual-visual-observations',qg.evaluate(r)['missing_or_unverified'])
 def test_visual_ready_is_not_quality_certification(self):self.assertEqual(qg.evaluate(self.visual())['status'],'ready-for-human-review')
 def test_text_reference_not_visual(self):
  r=self.visual();r['reference_observations'][0]['access']='text-only';self.assertEqual(qg.evaluate(r)['status'],'inconclusive')
 def test_motion_sampling_not_playback(self):
  r=self.visual('video');r.update(full_playback='frames-sampled',audio_review='intentionally-silent');self.assertIn('full-playback',qg.evaluate(r)['missing_or_unverified'])
 def test_motion_audio_required(self):
  r=self.visual('video');r.update(full_playback='pass',audio_review='not-checked');self.assertIn('audio-review',qg.evaluate(r)['missing_or_unverified'])
 def test_motion_silent_valid(self):
  r=self.visual('video');r.update(full_playback='pass',audio_review='intentionally-silent');self.assertEqual(qg.evaluate(r)['status'],'ready-for-human-review')
 def test_revision_required(self):
  r=self.visual();r['revisions']=[];self.assertEqual(qg.evaluate(r)['status'],'inconclusive')
 def test_unapproved_template_fails(self):
  t=json.loads((ROOT/'skills/co-founder/assets/templates/quality-review.json').read_text())
  with self.assertRaises(qg.ReviewError):qg.evaluate(t)
if __name__=='__main__':unittest.main()
