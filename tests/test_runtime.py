import copy
from datetime import date
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from _load import load,ROOT
cf=load('cf','skills/co-founder/scripts/cf.py')

class RuntimeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();cf.init_project(str(self.root))
 def tearDown(self):self.tmp.cleanup()
 def test_init_private(self):
  self.assertTrue((self.root/'.co-founder/company.md').is_file());self.assertIn('/.co-founder/',(self.root/'.gitignore').read_text())
 def test_init_preserves(self):
  p=self.root/'.co-founder/company.md';p.write_text('approved');r=cf.init_project(self.root);self.assertEqual(p.read_text(),'approved');self.assertFalse(r['created'])
 def test_ignore_not_duplicated(self):
  cf.init_project(self.root);self.assertEqual((self.root/'.gitignore').read_text().count('/.co-founder/'),1)
 def test_preserve_existing_ignore(self):
  p=self.root/'.gitignore';p.write_text('hello');cf.init_project(self.root);self.assertTrue(p.read_text().startswith('hello\n'))
 def test_init_permissions(self):
  if os.name!='nt':self.assertEqual((self.root/'.co-founder/company.md').stat().st_mode&0o777,0o600)
 def test_context_alias(self):self.assertEqual(cf.context_plan(self.root,'fix',1000)['task'],'build-fix')
 def test_context_no_contents(self):self.assertNotIn('UNSET',json.dumps(cf.context_plan(self.root,'decide',12000)))
 def test_context_bounds(self):
  with self.assertRaises(cf.CFError):cf.context_plan(self.root,'decide',0)
 def test_context_invalid_task(self):
  with self.assertRaises(cf.CFError):cf.context_plan(self.root,'unknown',1000)
 def test_context_budget(self):self.assertIn('read-scoped-excerpt',[x['suggestion'] for x in cf.context_plan(self.root,'decide',1)['files']])
 def test_doctor_does_not_print_secret(self):
  with patch.dict(os.environ,{'OPENAI_API_KEY':'not-a-real-key-test-value'}):
   r=cf.doctor(self.root);self.assertIn('OPENAI_API_KEY',r['billing_related_environment_variable_names']);self.assertNotIn('not-a-real-key-test-value',json.dumps(r))
 def test_symlink_context_rejected(self):
  if not hasattr(os,'symlink'):self.skipTest('symlinks unavailable')
  p=self.root/'.co-founder/state.json';p.unlink()
  try:p.symlink_to(self.root/'.co-founder/claims.json')
  except OSError:self.skipTest('symlink permission unavailable')
  with self.assertRaises(cf.CFError):cf.context_plan(self.root,'today',1000)
 def test_json_size_limit(self):
  p=self.root/'big.json';p.write_text('{}')
  with self.assertRaises(cf.CFError):cf.read_json(p,1)
 def test_empty_brief(self):self.assertEqual(cf.brief(self.root,'2026-09-23')['priorities'],[])
 def test_brief_priority(self):
  s={'updated_at':'2026-09-23','issues':[{'id':'2','title':'Urgent','priority':'urgent','status':'reported'}],'tasks':[{'id':'1','title':'Small','priority':'normal','status':'open'}]};(self.root/'.co-founder/state.json').write_text(json.dumps(s));self.assertEqual(cf.brief(self.root,'2026-09-23')['priorities'][0]['id'],'2')
 def test_brief_closed_excluded(self):
  (self.root/'.co-founder/state.json').write_text(json.dumps({'issues':[{'id':'1','title':'Done','status':'customer-confirmed'}]}));self.assertEqual(cf.brief(self.root)['priorities'],[])
 def test_brief_bad_date(self):
  with self.assertRaises(cf.CFError):cf.brief(self.root,'tomorrow')
 def test_brief_bad_item(self):
  (self.root/'.co-founder/state.json').write_text('{"issues":[{}]}')
  with self.assertRaises(cf.CFError):cf.brief(self.root)
 def commit(self,*items):(self.root/'.co-founder/commitments.json').write_text(json.dumps({'commitments':list(items)}))
 def test_init_creates_finance_records(self):
  for n in ['metrics.json','commitments.json']:self.assertTrue((self.root/'.co-founder'/n).is_file())
 def test_init_adds_finance_records_to_existing_project(self):
  (self.root/'.co-founder/metrics.json').unlink();r=cf.init_project(self.root);self.assertEqual(r['created'],['metrics.json'])
 def test_context_money_alias(self):self.assertEqual(cf.context_plan(self.root,'money',12000)['task'],'finance')
 def test_brief_overdue_commitment_first(self):
  (self.root/'.co-founder/state.json').write_text(json.dumps({'updated_at':'2026-09-23','tasks':[{'id':'t','title':'New work','priority':'high','status':'open'}]}))
  self.commit({'id':'c1','to':'customer:a','promise':'Send fix update','due_date':'2026-09-22','status':'open'})
  r=cf.brief(self.root,'2026-09-23');self.assertEqual(r['priorities'][0]['id'],'c1');self.assertEqual(r['priorities'][0]['title'],'Send fix update')
 def test_brief_missed_commitment_kept_closed_excluded(self):
  self.commit({'id':'m','promise':'Refund','status':'missed'},{'id':'k','promise':'Call','status':'kept'})
  r=cf.brief(self.root,'2026-09-23');self.assertEqual([x['id'] for x in r['priorities']],['m']);self.assertTrue(r['priorities'][0]['due_or_overdue'])
 def test_brief_bad_commitment_status(self):
  self.commit({'id':'x','promise':'Something','status':'done'})
  with self.assertRaises(cf.CFError):cf.brief(self.root)
 def test_brief_missing_commitments_warns(self):
  (self.root/'.co-founder/commitments.json').unlink();self.assertTrue(any('commitments.json' in w for w in cf.brief(self.root,'2026-09-23')['warnings']))
 def metrics(self,snapshots,north='mrr',direction='up'):
  (self.root/'.co-founder/metrics.json').write_text(json.dumps({'currency':'USD','north_star':north,'metrics':[{'id':'mrr','name':'MRR','unit':'currency','direction':direction,'definition':'Active subscription value','source':'synthetic'}],'snapshots':snapshots}))
 def test_metrics_empty_template(self):
  r=cf.metrics_summary(self.root,'2026-09-23');self.assertEqual(r['metrics'],[]);self.assertIn('No north_star metric chosen.',r['warnings'])
 def test_metrics_trend_and_staleness(self):
  self.metrics([{'metric_id':'mrr','period_end':'2026-08-31','value':1000,'source':'export-aug'},{'metric_id':'mrr','period_end':'2026-07-31','value':800,'source':'export-jul'}])
  m=cf.metrics_summary(self.root,'2026-09-23')['metrics'][0];self.assertEqual((m['change'],m['change_percent'],m['trend'],m['stale']),(200,25.0,'improving',False))
  self.assertTrue(cf.metrics_summary(self.root,'2026-11-30')['metrics'][0]['stale'])
 def test_metrics_direction_down_is_worsening_when_rising(self):
  self.metrics([{'metric_id':'mrr','period_end':'2026-08-31','value':5,'source':'a'},{'metric_id':'mrr','period_end':'2026-09-15','value':6,'source':'b'}],direction='down')
  self.assertEqual(cf.metrics_summary(self.root,'2026-09-23')['metrics'][0]['trend'],'worsening')
 def test_metrics_no_snapshots_reported(self):
  self.metrics([]);r=cf.metrics_summary(self.root,'2026-09-23');self.assertIsNone(r['metrics'][0]['latest']);self.assertIn('No snapshots recorded: mrr',r['warnings'])
 def test_metrics_rejects_unsourced_or_unknown(self):
  for snaps in [[{'metric_id':'mrr','period_end':'2026-08-31','value':1,'source':''}],[{'metric_id':'arr','period_end':'2026-08-31','value':1,'source':'a'}],
                [{'metric_id':'mrr','period_end':'2026-08-31','value':True,'source':'a'}],[{'metric_id':'mrr','period_end':'Aug','value':1,'source':'a'}],
                [{'metric_id':'mrr','period_end':'2026-08-31','value':1,'source':'a'}]*2]:
   self.metrics(snaps)
   with self.assertRaises(cf.CFError):cf.metrics_summary(self.root,'2026-09-23')
 def test_metrics_unknown_north_star_warns(self):
  self.metrics([],north='arr');self.assertIn('north_star is not a defined metric: arr',cf.metrics_summary(self.root,'2026-09-23')['warnings'])
 def test_usage_measured(self):
  cf.usage_add(self.root,'manual-host-record',100,30,40,10);r=cf.usage_summary(self.root);self.assertEqual(r['total_tokens'],130)
 def test_usage_partial_unknown(self):
  cf.usage_add(self.root,'record',input_tokens=100);self.assertIsNone(cf.usage_summary(self.root)['total_tokens'])
 def test_usage_empty_unknown(self):self.assertIsNone(cf.usage_summary(self.root)['total_tokens'])
 def test_usage_negative_rejected(self):
  with self.assertRaises(cf.CFError):cf.usage_add(self.root,'record',-1,20)
 def test_usage_bool_rejected(self):
  with self.assertRaises(cf.CFError):cf.usage_add(self.root,'record',True,20)
 def test_usage_cached_subset(self):
  with self.assertRaises(cf.CFError):cf.usage_add(self.root,'record',10,20,11)
 def test_usage_reasoning_subset(self):
  with self.assertRaises(cf.CFError):cf.usage_add(self.root,'record',10,20,1,21)
 def test_usage_no_invented_estimates(self):
  with self.assertRaises(cf.CFError):cf.usage_add(self.root,'record')
 def test_usage_lock(self):
  (self.root/'.co-founder/.usage.lock').write_text('')
  with self.assertRaises(cf.CFError):cf.usage_add(self.root,'record',10,20)
 def test_run_check_dry(self):
  r,c=cf.run_check(self.root,'check',[sys.executable,'-c','raise RuntimeError()']);self.assertEqual(c,0);self.assertEqual(r['status'],'not-run');self.assertEqual(list((self.root/'.co-founder/evidence').iterdir()),[])
 def test_run_check_pass(self):
  r,c=cf.run_check(self.root,'check',[sys.executable,'-c','print("fixture")'],True);self.assertEqual(c,0);self.assertEqual(r['status'],'passed');self.assertTrue(Path(r['report_path']).is_file())
 def test_run_check_fail(self):
  r,c=cf.run_check(self.root,'check',[sys.executable,'-c','raise SystemExit(3)'],True);self.assertEqual(c,1);self.assertEqual(r['exit_code'],3)
 def test_run_check_missing(self):
  r,c=cf.run_check(self.root,'check',['co-founder-no-such-program-fixture'],True);self.assertEqual(r['exit_code'],127)
 def test_run_check_timeout(self):
  r,c=cf.run_check(self.root,'check',[sys.executable,'-c','import time;time.sleep(5)'],True,1);self.assertEqual(r['status'],'inconclusive');self.assertTrue(r['timed_out'])
 def test_run_check_no_shell(self):
  dest=self.root/'not-created';cf.run_check(self.root,'check',[sys.executable,'-c','import sys;print(sys.argv[1])',f'; touch {dest}'],True);self.assertFalse(dest.exists())
 def test_run_check_invalid_name(self):
  with self.assertRaises(cf.CFError):cf.run_check(self.root,'../escape',['echo'],True)
 def test_run_check_limits(self):
  with self.assertRaises(cf.CFError):cf.run_check(self.root,'check',['echo'],True,0)
 def test_map_unknown_relationship(self):
  with self.assertRaises(cf.CFError):cf.validate_map({'modules':[],'relationships':[{'from':'a','to':'b'}]})
 def test_map_duplicate_ids(self):
  with self.assertRaises(cf.CFError):cf.validate_map({'modules':[{'id':'a','paths':['a/**']},{'id':'a','paths':['b/**']}]})
 def test_sensitive_paths(self):
  for p in ['.env','private/client.csv','.co-founder/state.json','src/secret.key']:
   with self.subTest(p=p):self.assertTrue(cf.path_sensitive(p))
 def test_source_path_allowed(self):self.assertFalse(cf.path_sensitive('src/repair/handler.ts'))

class GateTests(unittest.TestCase):
 def base(self):return {'schema_version':1,'candidate_revision':'abc123','environment':'fixture','required_checks':['a'],'checks':[{'id':'a','status':'passed','candidate_revision':'abc123','evidence':['evidence/a.txt']}],'acceptance_changes':[],'blocking_findings':[]}
 def test_ready(self):self.assertEqual(cf.evaluate_gate(self.base())['status'],'ready-for-review')
 def test_empty_required(self):
  r=self.base();r['required_checks']=[]
  with self.assertRaises(cf.CFError):cf.evaluate_gate(r)
 def test_duplicate_required(self):
  r=self.base();r['required_checks']=['a','a']
  with self.assertRaises(cf.CFError):cf.evaluate_gate(r)
 def test_missing_check(self):
  r=self.base();r['checks']=[];self.assertEqual(cf.evaluate_gate(r)['status'],'inconclusive')
 def test_fail_blocks(self):
  r=self.base();r['checks'][0]['status']='failed';self.assertEqual(cf.evaluate_gate(r)['status'],'blocked')
 def test_skip_inconclusive(self):
  r=self.base();r['checks'][0]['status']='skipped';self.assertEqual(cf.evaluate_gate(r)['status'],'inconclusive')
 def test_no_evidence(self):
  r=self.base();r['checks'][0]['evidence']=[];self.assertEqual(cf.evaluate_gate(r)['status'],'inconclusive')
 def test_bad_status(self):
  r=self.base();r['checks'][0]['status']='probably-fine'
  with self.assertRaises(cf.CFError):cf.evaluate_gate(r)
 def test_wrong_revision(self):
  r=self.base();r['checks'][0]['candidate_revision']='other';self.assertEqual(cf.evaluate_gate(r)['status'],'inconclusive')
 def test_duplicate_check(self):
  r=self.base();r['checks'].append(copy.deepcopy(r['checks'][0]))
  with self.assertRaises(cf.CFError):cf.evaluate_gate(r)
 def test_unapproved_change(self):
  r=self.base();r['acceptance_changes']=[{'description':'skip old check','approved':False}];self.assertEqual(cf.evaluate_gate(r)['status'],'blocked')
 def test_approved_change(self):
  r=self.base();r['acceptance_changes']=[{'description':'new agreed behavior','approved':True,'approved_by':'reviewer','reason':'requirement revised'}];self.assertEqual(cf.evaluate_gate(r)['status'],'ready-for-review')
 def test_open_finding(self):
  r=self.base();r['blocking_findings']=[{'id':'security-1','status':'open'}];self.assertEqual(cf.evaluate_gate(r)['status'],'blocked')
 def test_resolved_without_evidence(self):
  r=self.base();r['blocking_findings']=[{'id':'security-1','status':'resolved'}];self.assertEqual(cf.evaluate_gate(r)['status'],'inconclusive')
 def test_extra_failed_check_not_hidden(self):
  r=self.base();r['checks'].append({'id':'b','status':'failed','candidate_revision':'abc123','evidence':['x']});self.assertEqual(cf.evaluate_gate(r)['status'],'blocked')
 def test_template_does_not_pass(self):
  r=json.loads((ROOT/'skills/co-founder/assets/templates/verification.json').read_text());self.assertEqual(cf.evaluate_gate(r)['status'],'inconclusive')
 def test_no_fabricated_artifact_auth(self):self.assertIn('self-reported',cf.evaluate_gate(self.base())['limits'])

@unittest.skipUnless(shutil.which('git'),'git unavailable')
class GitTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();subprocess.run(['git','init','-q',str(self.root)],check=True);self.g(['config','user.email','fixture@example.invalid']);self.g(['config','user.name','Synthetic Fixture']);(self.root/'a.txt').write_text('a');self.g(['add','a.txt']);self.g(['commit','-qm','fixture']);cf.init_project(self.root)
 def g(self,args):return subprocess.run(['git','-C',str(self.root),*args],capture_output=True,check=True)
 def tearDown(self):self.tmp.cleanup()
 def test_impact_changed(self):
  (self.root/'a.txt').write_text('b');r=cf.impact(self.root,'HEAD');self.assertIn('a.txt',r['changed_paths']);self.assertIn('a.txt',r['unmapped_paths'])
 def test_impact_relationship_closure(self):
  (self.root/'a.txt').write_text('b');m={'modules':[{'id':'a','paths':['a.txt']},{'id':'b','paths':['b/**']},{'id':'c','paths':['c/**']}],'relationships':[{'from':'a','to':'b'},{'from':'b','to':'c'},{'from':'c','to':'a'}]};(self.root/'.co-founder/product-map.json').write_text(json.dumps(m));r=cf.impact(self.root,'HEAD');self.assertEqual(r['direct_modules'],['a']);self.assertEqual(r['related_modules'],['b','c'])
 def test_impact_sensitive_untracked(self):
  (self.root/'.env').write_text('fixture-only');r=cf.impact(self.root,'HEAD');self.assertNotIn('.env',r['changed_paths']);self.assertGreater(r['excluded_sensitive_path_count'],0)
 def test_impact_bad_ref(self):
  with self.assertRaises(cf.CFError):cf.impact(self.root,'--help')
 def test_doctor_tracked_private(self):
  self.g(['add','-f','.co-founder/company.md']);self.assertIn('.co-founder/company.md',cf.doctor(self.root)['tracked_private_paths'])
if __name__=='__main__':unittest.main()
