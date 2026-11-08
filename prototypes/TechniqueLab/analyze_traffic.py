"""Validate TrafficLab's bounded behavior and three complete rendered runs.

Python 3.9+, standard library. Missing GPU values remain missing. Tick-bearing
updates map to the following wall interval; engine timings are asynchronous.
"""
import gzip
import hashlib
import json
from datetime import datetime
from pathlib import Path
from analyze_dynamic import stats
from analysis_evidence import add_expected, emit_summary, parse_options

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'Results/Traffic'


def read(name):
    p = RESULTS / name
    raw = p.read_bytes() if p.exists() else gzip.decompress(Path(str(p)+'.gz').read_bytes())
    return json.loads(raw.decode('utf-8-sig'))


def behavior(report):
    assert report['finished'] and report['phase'] == 'finished' and report['failures'] == 0
    assert len(report['checks']) == 21 and all(c['passed'] for c in report['checks'])
    assert len({c['name'] for c in report['checks']}) == 21
    rows = report['behavior']
    assert len(rows) == 11 and len({b['name'] for b in rows}) == 11
    for b in rows:
        a = b['audit']
        assert b['passed'] and a['observations'] == b['ticks']
        assert b['nativeSamples'] > 0 and b['nativeWallHits'] == 0
        assert all(e['poseChange'] == 0 for e in b['events'])
        if b['name'] == 'collision-control':
            assert a['pairPenetrations'] > 0 and a['minimumSurfaceGap'] < -.0001
            continue
        assert all(a[k] == 0 for k in ('pairPenetrations','wallPenetrations','teleports','wrongLeases','forbiddenNarrow','diagonalSteps'))
        assert a['minimumSurfaceGap'] >= -.0001 and a['minimumWallGap'] >= -.0001
        assert a['maximumStep'] <= 3/60 + .0002
        if b['name'] == 'deadlock-control':
            assert b['maximumStall'] >= 5 and b['arrived'] == 0
            continue
        assert b['arrived'] == b['agents'] and b['eastArrived'] == b['westArrived'] == b['agents']//2
        assert b['narrowOpposingTicks'] == 0 and b['maximumStall'] < 5 and b['maxBatch'] <= 4
        assert b['simulatedSeconds'] <= (300 if b['agents']==256 else 120 if b['agents']==2 else 180)
        if b['agents'] >= 64:
            assert min(b['small'],b['medium'],b['large']) > 0 and b['profiles'] == 3
            assert b['narrowCrossEast'] == b['narrowCrossWest'] == b['agents']//8
            assert b['wideCrossEast'] == b['wideCrossWest'] == b['agents']*3//8
            assert b['wideOpposingTicks'] > 0
        if b['name'] == 'narrow-headon':
            assert b['narrowCrossEast'] == b['narrowCrossWest'] == 1 and b['switches'] > 0
        if b['name'] == 'wide-opposing': assert b['wideOpposingTicks'] > 0
        if b['name'] == 'large-redirect': assert b['redirected'] == 1
        if b['name'] == 'reverse-128': assert b['firstPhase'] == -1
        if b['name'] == 'late-west-64': assert b['firstEastRequest'] == 1 and b['firstWestRequest'] >= 90
        if b['name'] == 'admission-pause': assert b['pauseVerified'] and len(b['events']) == 2
    return [{k:b[k] for k in ('name','agents','arrived','eastArrived','westArrived','simulatedSeconds','wideOpposingTicks','maxBatch','maximumWait','maximumStall','firstEastRequest','firstWestRequest','firstPhase')} | {'audit':b['audit']} for b in rows]


def case(c):
    rows,engine,n = c['frames'],c['engineFrames'],c['agents']
    assert n in (64,128,256) and len(rows)>=100 and len(engine)>=60
    assert c['minimumActive'] == c['minimumVisible'] == n
    assert c['small']+c['medium']+c['large'] == n
    if c['mixed']: assert min(c['small'],c['medium'],c['large'])>0 and c['profiles']==3
    else: assert c['medium']==n and c['profiles']==1
    assert 5.8<c['measuredSeconds']<6.5
    assert all(b['frame']==a['frame']+1 for a,b in zip(rows,rows[1:]))
    assert all(r['active']==r['visible']==n and r['wallIntervalMs']>0 and 0<=r['steps']<=8 for r in rows)
    assert all(b['timestamp']>a['timestamp'] for a,b in zip(engine,engine[1:]))
    assert all(r['cpuMs']>0 for r in engine)
    assert sum(r['renderMs']>0 for r in engine)/len(engine)>=.95
    assert sum(r['gpuMs']>0 for r in engine)>=60
    assert abs(sum(r['wallIntervalMs'] for r in rows)/1000-c['measuredSeconds']-rows[0]['wallIntervalMs']/1000)<.00001
    by={r['frame']:r for r in rows}
    assert [e['action'] for e in c['events']]==['pause-admission','resume-admission']
    events=[]
    for e in c['events']:
        assert e['poseChange']==0 and e['frame'] in by and e['frame']+1 in by
        events.append(dict(action=e['action'],transactionMs=e['milliseconds'],updateMs=by[e['frame']]['updateMs'],followingWallMs=by[e['frame']+1]['wallIntervalMs']))
    wall=[r['wallIntervalMs'] for r in rows]
    tick=[r for r in rows if r['steps']>0]
    misses=sum(v>16.67 for v in wall)
    out=dict(name=c['name'],agents=n,mixed=c['mixed'],population=[c[k] for k in ('small','medium','large')],
             wallMs=stats(wall),updateMs=stats([r['updateMs'] for r in rows]),
             tickUpdateMs=stats([r['updateMs'] for r in tick]),
             tickFollowingWallMs=stats([by[r['frame']+1]['wallIntervalMs'] for r in tick if r['frame']+1 in by]),
             over16_67Count=misses,over16_67Percent=100*misses/len(rows),
             measuredSeconds=c['measuredSeconds'],steps=sum(r['steps'] for r in rows),maximumBacklog=c['maximumBacklog'],
             engineSamples=len(engine),gpuMissing=sum(r['gpuMs']<=0 for r in engine),gc=[c['gen0'],c['gen1'],c['gen2']],events=events)
    for key in ('cpuMs','mainMs','renderMs','presentWaitMs','gpuMs'):
        values=[r[key] for r in engine]
        valid=[v for v in values if v>0]
        if key=='gpuMs':
            out[key]=dict(positive=len(valid),missing=len(engine)-len(valid),validOnly=stats(valid) if valid else None)
        else:
            # Zero present-wait is legitimate; do not censor zero CPU subfields.
            out[key]=dict(positive=len(valid),zero=len(engine)-len(valid),allSamples=stats(values))
    return out


def main(argv=None):
    options = parse_options(argv)
    expected_binaries = {}
    editor=read('editor-final.json');behavior(editor)
    assert editor['editor'] and editor['batch'] and not editor['cases']
    build=read('build.json');assert build['result']=='Succeeded' and build['errors']==0 and not build['development']
    reports=[];records=[];runs=[]
    for i in range(1,4):
        session=f'traffic-run-{i}'
        report=read(session+'.json');record=read(session+'-process.json')
        behavior(report)
        assert not report['editor'] and not report['batch'] and report['frameTimingEnabled']
        assert report['screenWidth']==1280 and report['screenHeight']==720 and report['vSync']==0
        assert record['exitCode']==0 and record['visible'] and not record['interactive']
        assert record['order']==(1 if i==2 else 0)
        assert len(report['cases'])==6 and len({c['name'] for c in report['cases']})==6
        assert [c['mixed'] for c in report['cases']]==([False,True]*3 if i==2 else [True,False]*3)
        results=[case(c) for c in report['cases']]
        for relative,expected in record['sourceSha256'].items():
            assert hashlib.sha256((ROOT/relative.replace('\\','/')).read_bytes()).hexdigest().upper()==expected
        for relative,key in [('TrafficBuild/TrafficLab.exe','playerSha256'),('TrafficBuild/TrafficLab_Data/Managed/Assembly-CSharp.dll','managedAssemblySha256')]:
            add_expected(expected_binaries, relative, record[key])
        reports.append(report);records.append(record);runs.append(dict(session=session,cases=results))
    assert len({r['buildGuid'] for r in reports})==1
    assert len({r['managedAssemblySha256'] for r in records})==1
    assert all(datetime.fromisoformat(a['utcEnd'].replace('Z','+00:00')) <= datetime.fromisoformat(b['utcStart'].replace('Z','+00:00')) for a,b in zip(records,records[1:]))
    ui=read('ui-observation.json');assert ui['allPassed'] and read('traffic-ui-process.json')['exitCode']==0
    red=read('red-audit-sensitivity.json');assert sum(not c['passed'] for c in red['checks'])==2
    allcases=[c for run in runs for c in run['cases']]
    output=dict(ok=True,checksPerProcess=21,scenarioExpectationsPerProcess=11,safeScenariosPerProcess=9,
                hardware={k:reports[0][k] for k in ('unity','cpu','gpu','os','graphicsApi','screenWidth','screenHeight','antiAliasing','buildGuid')},
                behavior=behavior(reports[-1]),runs=runs,totalFrames=sum(c['wallMs']['samples'] for c in allcases),
                totalEngineFrames=sum(c['engineSamples'] for c in allcases),gpuMissing=sum(c['gpuMissing'] for c in allcases),
                over16_67Count=sum(c['over16_67Count'] for c in allcases),
                limitation='Bounded authored lanes, fixed radii, centralized authority; no universal deadlock freedom, arbitrary steering or GPU-tail claim.')
    exit_code = emit_summary(output, options, ROOT, expected_binaries, omit=('runs','behavior'))
    for name in sorted({c['name'] for c in allcases}):
        subset=[c for c in allcases if c['name']==name]
        print(name, 'wall p95', [round(c['wallMs']['p95'],4) for c in subset],
              'tick-update p95', [round(c['tickUpdateMs']['p95'],4) for c in subset],
              'max', [round(c['wallMs']['maximum'],4) for c in subset],
              'miss%', [round(c['over16_67Percent'],3) for c in subset])
    return exit_code


if __name__=='__main__': raise SystemExit(main())
