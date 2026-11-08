"""Validate sustained-stream evidence, per-ID dispositions and whole frames.

Standard library, Python 3.9+. CPU work maps to the FOLLOWING wall interval.
Pending external requests count toward response latency. Infinity is not observed.
"""
import gzip
import hashlib
import json
from datetime import datetime
from pathlib import Path
from analyze_dynamic import stats
from analysis_evidence import add_expected, emit_summary, parse_options

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'Results/Stream'


def read(name):
    p=RESULTS/name
    raw=p.read_bytes() if p.exists() else gzip.decompress(Path(str(p)+'.gz').read_bytes())
    return json.loads(raw.decode('utf-8-sig'))


def behavior(report):
    assert report['finished'] and report['phase']=='finished' and report['failures']==0
    assert len(report['checks'])==23 and len({c['name'] for c in report['checks']})==23 and all(c['passed'] for c in report['checks'])
    assert len(report['behavior'])==10
    out=[]
    for b in report['behavior']:
        a=b['audit'];jobs=b['jobs'];name=b['name'];assert b['passed']
        assert [j['id'] for j in jobs]==list(range(len(jobs)))
        assert a['observations']==b['epochs'] and b['nativeMappingErrors']==0
        assert b['nativeInteriorChecks']*5==b['nativeChecks']*3
        assert b['nativeTerminalChecks']==b['completed']
        completed=[j for j in jobs if j['completed']>=0]
        rejected=[j for j in jobs if j['rejected']>=0]
        unfinished=[j for j in jobs if j['completed']<0 and j['rejected']<0]
        ages=[((j['completed'] if j['completed']>=0 else b['epochs'])-j['requested'])*.5 for j in jobs if j['rejected']<0]
        assert sum(age>240 for age in ages)==a['deadlineViolations']
        assert max(ages)==a['maximumResponseSeconds']
        assert b['deadlineMet']==(a['deadlineViolations']==0)
        assert b['completed']==len(completed) and b['rejected']==len(rejected)
        assert all(j['requested']<=j['admitted']<j['completed'] and 0<j['routeActions']<=96 and j['completed']-j['admitted']==j['routeActions'] for j in completed)
        if name=='reservation-disabled-control':
            assert a['pairPenetrations']>0 and a['minimumSurfaceGap']<0 and b['negative']
        else:
            assert all(a[k]==0 for k in ('pairPenetrations','wallPenetrations','teleports','invalidSegments'))
            assert b['nativeHits']==0 and a['minimumSurfaceGap']>=-.0001 and a['minimumWallGap']>=-.0001
            assert a['maximumGlobalStall']<5
            if name=='lifo-starvation-control':
                assert b['negative'] and not b['deadlineMet'] and jobs[0]['admitted']==-1 and b['completed']>50
                assert len(unfinished)>0 and b['epochs']==b['inflow'] and b['epochs']*.5>240
            else:
                assert not unfinished and b['completed']+b['rejected']==len(jobs) and b['fifo']
                assert len(jobs)==b['rate']*b['inflow']+(1 if name=='unreachable-request' else 0)
                assert b['epochs']<=b['inflow']+1200 and b['atInflowCompleted']>0
                admitted=[j['admitted'] for j in jobs if j['admitted']>=0]
                assert admitted==sorted(admitted)
                assert min(sum(j['radius']<.3 for j in jobs),sum(.3<j['radius']<.5 for j in jobs),sum(j['radius']>.5 for j in jobs))>0
                assert any(j['turns']>1 for j in completed), 'No evidence of searched turns'
                if name=='choke-overload':
                    assert b['negative'] and b['stress'] and not b['deadlineMet'] and b['atInflowPending']>0
                else: assert not b['negative'] and b['deadlineMet']
                if name=='unreachable-request': assert len(rejected)==1 and rejected[0]['rejected']==0 and rejected[0]['rejection']
        out.append(dict(name=name,expectation=b['expectation'],requests=len(jobs),completed=b['completed'],rejected=b['rejected'],unfinished=len(unfinished),
                        seconds=b['epochs']*.5,maxActive=b['maxActive'],maxPending=b['maxPending'],inflowCompleted=b['atInflowCompleted'],inflowPending=b['atInflowPending'],
                        deadlineMet=b['deadlineMet'],lateIDs=a['deadlineViolations'],responseSeconds=stats(ages),maxPendingSeconds=a['maximumPendingSeconds'],
                        maxIndividualMotionWaitSeconds=max(j['maxWaitActions'] for j in jobs)*.5,
                        minimumSurfaceGap=a['minimumSurfaceGap'],minimumWallGap=a['minimumWallGap'],maximumGlobalStall=a['maximumGlobalStall'],
                        nativeSamples=b['nativeChecks'],nativeInteriorSamples=b['nativeInteriorChecks'],nativeTerminalSamples=b['nativeTerminalChecks']))
    return out


def case(c):
    rows,engine=c['frames'],c['engineFrames'];assert len(rows)>=100 and len(engine)>=60
    assert all(b['frame']==a['frame']+1 for a,b in zip(rows,rows[1:]))
    assert all(r['wallIntervalMs']>0 and r['visible']==r['renderedActive']>0 and 0<=r['steps']<=8 and 0<=r['epochs']<=1 for r in rows)
    assert all(b['renderedActive']==a['active'] and b['requested']>=a['requested'] and b['completed']>=a['completed'] for a,b in zip(rows,rows[1:]))
    assert c['minimumActive']==min(r['active'] for r in rows)>0 and c['maximumActive']==max(r['active'] for r in rows)
    assert c['minimumVisible']==min(r['visible'] for r in rows)>0
    assert c['inflowEnd']-c['inflowStart']==c['rate']*sum(r['epochs'] for r in rows)>0
    assert c['completionEnd']>c['completionStart']
    assert 5.8<c['measuredSeconds']<10
    assert abs(sum(r['wallIntervalMs'] for r in rows)/1000-c['measuredSeconds']-rows[0]['wallIntervalMs']/1000)<.00001
    assert all(b['timestamp']>a['timestamp'] for a,b in zip(engine,engine[1:]))
    assert all(e['cpuMs']>0 for e in engine)
    assert sum(e['renderMs']>0 for e in engine)/len(engine)>=.95
    assert sum(e['gpuMs']>0 for e in engine)>=60
    assert all((r['planningMs']>0)==(r['epochs']>0) for r in rows)
    planning=[i for i,r in enumerate(rows) if r['epochs']>0];assert len(planning)>=10
    tick=[i for i,r in enumerate(rows) if r['steps']>0]
    wall=[r['wallIntervalMs'] for r in rows]
    def following(indices):return [rows[i+1]['wallIntervalMs'] for i in indices if i+1<len(rows)]
    out=dict(name=c['name'],layout=c['layout'],requestsPerSecond=c['rate']*2,minimumActive=c['minimumActive'],maximumActive=c['maximumActive'],wallMs=stats(wall),
             updateMs=stats([r['updateMs'] for r in rows]),tickUpdateMs=stats([rows[i]['updateMs'] for i in tick]),
             planningMs=stats([rows[i]['planningMs'] for i in planning]),planningUpdateMs=stats([rows[i]['updateMs'] for i in planning]),
             planningFollowingWallMs=stats(following(planning)),planningUnmatchedRows=sum(i+1==len(rows) for i in planning),
             planningFollowingOver16_67=sum(v>16.67 for v in following(planning)),
             tickFollowingWallMs=stats(following(tick)),active=stats([r['active'] for r in rows]),visible=stats([r['visible'] for r in rows]),
             pending=stats([r['pending'] for r in rows]),oldestPendingSeconds=stats([r['oldestPending']*.5 for r in rows]),
             requestedDuringCapture=c['inflowEnd']-c['inflowStart'],completedDuringCapture=c['completionEnd']-c['completionStart'],
             over16_67Count=sum(v>16.67 for v in wall),over16_67Percent=100*sum(v>16.67 for v in wall)/len(wall),
             maximumBacklog=c['maximumBacklog'],measuredSeconds=c['measuredSeconds'],gc=[c[f'gen{i}'] for i in range(3)],
             engineSamples=len(engine),gpuMissing=sum(e['gpuMs']<=0 for e in engine))
    for key in ('cpuMs','mainMs','renderMs','presentWaitMs','gpuMs'):
        values=[e[key] for e in engine];positive=[v for v in values if v>0]
        out[key]=dict(positive=len(positive),missing=len(values)-len(positive),validOnly=stats(positive)) if key=='gpuMs' else dict(allSamples=stats(values))
    return out


def main(argv=None):
    options = parse_options(argv)
    expected_binaries = {}
    editor=read('editor-final.json');behavior(editor);assert editor['editor'] and editor['batch'] and not editor['cases']
    build=read('build.json');assert build['result']=='Succeeded' and build['errors']==0 and not build['development']
    snapshot=read('build-source.json');built={s['path']:s['sha256'] for s in snapshot['sources']}
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper()==h for p,h in built.items())
    reports=[];records=[];runs=[]
    for i in range(1,4):
        session=f'stream-run-{i}';report=read(session+'.json');record=read(session+'-process.json')
        behavior(report);assert not report['editor'] and not report['batch'] and report['frameTimingEnabled']
        assert report['screenWidth']==1280 and report['screenHeight']==720 and report['vSync']==0
        assert record['exitCode']==0 and record['visible'] and not record['interactive'] and record['order']==(1 if i==2 else 0)
        assert [c['rate'] for c in report['cases']]==([4,2,1]*2 if i==2 else [1,2,4]*2)
        assert [c['layout'] for c in report['cases']]==([1]*3+[0]*3 if i==2 else [0]*3+[1]*3)
        assert {p.replace('\\','/'):h for p,h in record['sourceSha256'].items()}==built
        for p,key in [('StreamBuild/StreamLab.exe','playerSha256'),('StreamBuild/StreamLab_Data/Managed/Assembly-CSharp.dll','managedAssemblySha256')]:
            add_expected(expected_binaries, p, record[key])
        reports.append(report);records.append(record);runs.append(dict(session=session,cases=[case(c) for c in report['cases']]))
    assert len({r['buildGuid'] for r in reports})==1 and len({r['managedAssemblySha256'] for r in records})==1
    assert all(datetime.fromisoformat(a['utcEnd'].replace('Z','+00:00'))<=datetime.fromisoformat(b['utcStart'].replace('Z','+00:00')) for a,b in zip(records,records[1:]))
    ui=read('stream-ui-process.json');assert read('ui-observation.json')['allPassed'] and ui['exitCode']==0 and ui['interactive'] and ui['visible']
    pilot={s['path']:s['sha256'] for s in read('pilot-build-source.json')['sources']}
    assert {p.replace('\\','/'):h for p,h in ui['sourceSha256'].items()}==pilot
    assert hashlib.sha256(gzip.decompress((RESULTS/'pilot-Assembly-CSharp.dll.gz').read_bytes())).hexdigest().upper()==ui['managedAssemblySha256']
    assert [p for p in built if built[p]!=pilot[p]]==['Assets/TechniqueLab/StreamRunner.cs'], 'UI evidence predates only the automated matrix expansion'
    assert sum(not c['passed'] for c in read('red-audit-sensitivity.json')['checks'])==2
    allcases=[c for run in runs for c in run['cases']]
    out=dict(ok=True,checksPerProcess=23,ordinaryDeadlineFixtures=7,overloadDeadlineFailureFixtures=1,otherNegativeControls=2,
             hardware={k:reports[0][k] for k in ('unity','cpu','gpu','os','graphicsApi','screenWidth','screenHeight','antiAliasing','buildGuid')},
             behavior=behavior(reports[-1]),runs=runs,totalFrames=sum(c['wallMs']['samples'] for c in allcases),
             totalEngineFrames=sum(c['engineSamples'] for c in allcases),gpuMissing=sum(c['gpuMissing'] for c in allcases),
             over16_67Count=sum(c['over16_67Count'] for c in allcases),
             limitation='Finite sustained streams and conditional FIFO/complete-route argument; external pending queue and unlaned cardinal graph, not unrestricted physical crowd or observed infinity.')
    exit_code = emit_summary(out, options, ROOT, expected_binaries, omit=('runs','behavior'))
    for name in sorted({c['name'] for c in allcases}):
        sub=[c for c in allcases if c['name']==name]
        print(name,'whole p95', [round(c['wallMs']['p95'],3) for c in sub],
              'planning-following p95',[round(c['planningFollowingWallMs']['p95'],3) for c in sub],
              'misses',[c['over16_67Count'] for c in sub],
              'active ranges',[(c['active']['median'],c['active']['maximum']) for c in sub])
    return exit_code


if __name__=='__main__':raise SystemExit(main())
