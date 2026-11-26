import copy,io,json,sys,tempfile,unittest,urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from fetch_github_data import ROOT,request,parse_calendar,validate_snapshot,publish,collect
from generate_telemetry import render,streaks
from visual import lorenz

# Keep atomic-replace tests on the workspace volume (Windows virtual temp
# volumes may reject os.replace despite source and destination sharing a path).
(ROOT/'.dist').mkdir(exist_ok=True)
tempfile.tempdir=str(ROOT/'.dist')

class PipelineTests(unittest.TestCase):
    def setUp(self):self.s=json.loads((ROOT/'data/github_snapshot.json').read_text(encoding='utf-8'))
    def test_real_snapshot_calendar_consistency(self):
        validate_snapshot(self.s);self.assertEqual(len(self.s['calendar']['days']),365)
    def test_missing_data_rejected(self):
        self.s['calendar']['days'].pop(100)
        with self.assertRaises(ValueError):validate_snapshot(self.s)
    def test_duplicate_date_rejected(self):
        self.s['calendar']['days'][1]=self.s['calendar']['days'][0]
        with self.assertRaises(ValueError):validate_snapshot(self.s)
    def test_private_metadata_rejected(self):
        self.s['repositories'][0]['private']=True
        with self.assertRaises(ValueError):validate_snapshot(self.s)
    def test_missing_count_is_not_zero(self):
        del self.s['repositories'][0]['stargazers_count']
        with self.assertRaises(ValueError):validate_snapshot(self.s)
    def test_changed_calendar_markup_rejected(self):
        with self.assertRaises(ValueError):parse_calendar('<html>Sign in</html>')
    def test_429_retries_bounded(self):
        calls=[];sleeps=[]
        def fail(*args,**kwargs):
            calls.append(kwargs);raise urllib.error.HTTPError('url',429,'limit',{'Retry-After':'3600'},None)
        with self.assertRaises(RuntimeError):request('https://api.github.com/test',fail,sleeps.append)
        self.assertEqual(len(calls),3);self.assertEqual(sleeps,[60,60]);self.assertTrue(all(c['timeout']==30 for c in calls))
    def test_403_retains_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s.json';publish(self.s,p);before=p.read_bytes()
            def fail(*args,**kwargs):raise urllib.error.HTTPError('url',403,'limit',{},None)
            with self.assertRaises(RuntimeError):request('https://api.github.com/test',fail,lambda _:None)
            self.assertEqual(before,p.read_bytes())
    def test_network_retries_and_fails(self):
        sleeps=[]
        def fail(*args,**kwargs):raise urllib.error.URLError('offline')
        with self.assertRaises(RuntimeError):request('https://github.com/test',fail,sleeps.append)
        self.assertEqual(sleeps,[1,2])
    def test_no_timestamp_only_commit(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s.json';publish(self.s,p);before=p.read_bytes();self.s['fetched_at']='2026-11-27T12:00:00Z'
            self.assertFalse(publish(self.s,p));self.assertEqual(before,p.read_bytes())
    def test_invalid_publish_preserves_last_good(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s.json';publish(self.s,p);before=p.read_bytes();self.s['repositories']=[]
            with self.assertRaises(ValueError):publish(self.s,p)
            self.assertEqual(before,p.read_bytes())
    def test_streak_today_grace_and_window_boundary(self):
        self.assertEqual(streaks([{'count':n} for n in [1,2,0,3,4,0]]),(2,2))
        self.assertEqual(streaks([{'count':0}]*5),(0,0))
        self.assertEqual(streaks([{'count':2}]*5),(5,5))
    def test_all_zero_calendar_is_valid_data(self):
        for d in self.s['calendar']['days']:d['count']=0
        with tempfile.TemporaryDirectory() as d:
            render(self.s,Path(d));self.assertIn('MAX 0',(Path(d)/'assets/skyline/skyline.svg').read_text())
    def test_deterministic_render(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            render(self.s,Path(a));render(self.s,Path(b))
            for p in Path(a).rglob('*'):
                if p.is_file():self.assertEqual(p.read_bytes(),(Path(b)/p.relative_to(a)).read_bytes())
    def test_lorenz_reproducibility_and_boundedness(self):
        a=lorenz();self.assertEqual(a,lorenz());self.assertEqual(len(a),5300)
        self.assertTrue(all(-30<x<30 and -40<y<40 and 0<z<60 for x,y,z in a))
    def test_rest_pagination(self):
        first=[dict(self.s['repositories'][0],name=f'R{i}') for i in range(100)]
        second=[dict(self.s['repositories'][0],name='last')]
        with patch('fetch_github_data.request',side_effect=[json.dumps(first).encode(),json.dumps(second).encode(),b'calendar']),patch('fetch_github_data.make_snapshot',return_value={}) as make:
            collect();self.assertEqual(len(make.call_args.args[0]),101)

if __name__=='__main__':unittest.main()
