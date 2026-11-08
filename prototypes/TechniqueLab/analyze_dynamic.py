"""Verify final dynamic-scene evidence and summarize actual rendered frame distributions.

Python 3.9+, no dependencies. Keep assertions enabled. Run after three sequential
Run-Dynamic.ps1 -Visible sessions named dynamic-run-1/2/3 and final Editor PlayMode.
"""
import hashlib
import gzip
import json
import math
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'Results/Dynamic'


def read(name):
    path=RESULTS/name
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8-sig'))
    with gzip.open(str(path)+'.gz','rt',encoding='utf-8-sig') as stream:
        return json.load(stream)


def stats(values):
    assert values and all(math.isfinite(v) and v >= 0 for v in values)
    ordered = sorted(values)
    return dict(samples=len(values), median=median(values),
                p95=ordered[math.ceil(.95 * len(values)) - 1],
                p99=ordered[math.ceil(.99 * len(values)) - 1],
                maximum=max(values), mean=mean(values))


def validate_behavior(report):
    assert report['finished'] and report['phase'] == 'finished' and report['failures'] == 0
    assert len(report['checks']) == 12 and all(c['passed'] for c in report['checks'])
    assert len({c['name'] for c in report['checks']}) == 12
    assert len(report['behavior']) == 6
    for behavior in report['behavior']:
        assert behavior['passed']
        audit = behavior['audit']
        assert audit['observations'] == behavior['ticks']
        assert behavior['nativeChecks'] > 0 and behavior['nativeWallOverlaps'] == 0
        assert all(e['maximumPoseChange'] == 0 for e in behavior['events'])
        if behavior['name'] == 'avoidance-disabled-control':
            assert audit['pairPenetrations'] > 0
            continue
        assert behavior['arrived'] == behavior['agents']
        assert all(audit[k] == 0 for k in ('pairPenetrations', 'wallPenetrations', 'teleports', 'reservationErrors', 'staleReads'))
        assert audit['minimumSeparation'] >= .4 - .0001
        assert audit['maximumStep'] <= 3 / 60 + .0002
        if behavior['name'] in ('occupied-door', 'moving-crate'):
            assert behavior['triggered'] and behavior['closeCommitTick'] > behavior['closeRequestTick']
        if behavior['name'] == 'occupied-door':
            assert behavior['bodyOccupiedAtRequest'] and behavior['events'][0]['moving'] > 0
            assert behavior['alternateCrossings'] > 0
            assert (behavior['closeCommitTick'] - behavior['closeRequestTick']) / 60 <= 2
        if behavior['name'] == 'all-blocked':
            assert behavior['triggered'] and len(behavior['events']) == 3
        if behavior['name'] == 'dense-64':
            assert behavior['simulatedSeconds'] <= 60
        if behavior['name'] == 'dense-256':
            assert behavior['simulatedSeconds'] <= 120


def validate_case(case):
    rows, engine = case['frames'], case['engineFrames']
    assert len(rows) >= 100 and len(engine) >= 60
    assert case['minimumActive'] == case['maximumActive'] == case['agents']
    assert len(case['events']) == 3 and case['rebuilds'] == 4
    assert 5.8 < case['measuredSeconds'] < 6.5
    assert all(b['frame'] == a['frame'] + 1 for a, b in zip(rows, rows[1:])), 'Dropped wall-frame rows'
    assert all(r['active'] == case['agents'] and r['wallIntervalMs'] > 0 and 0 <= r['steps'] <= 8 for r in rows)
    assert all(b['timestamp'] > a['timestamp'] for a, b in zip(engine, engine[1:]))
    assert all(r['cpuMs'] > 0 for r in engine)
    # A zero GPU field means unavailable data, not a free frame. The actual whole-frame
    # interval and CPU/render samples remain uncensored; do not infer a GPU tail from
    # the available subset. Unity documents that GPU resources can fail to return timings.
    assert sum(r['gpuMs'] > 0 for r in engine) >= 60, 'No usable GPU observations'
    assert sum(r['renderMs'] > 0 for r in engine) / len(engine) >= .95, 'Render timing coverage insufficient'
    assert abs(sum(r['wallIntervalMs'] for r in rows) / 1000 - case['measuredSeconds']
               - rows[0]['wallIntervalMs'] / 1000) < .00001
    by_frame = {r['frame']: r for r in rows}
    events = []
    for event in case['events']:
        assert event['maximumPoseChange'] == 0
        frame = event['engineFrame']
        assert frame in by_frame and frame + 1 in by_frame
        events.append(dict(action=event['action'], transactionMs=event['milliseconds'],
                           updateMs=by_frame[frame]['updateMs'], followingWallIntervalMs=by_frame[frame + 1]['wallIntervalMs']))
    wall = [r['wallIntervalMs'] for r in rows]
    tick_rows=[r for r in rows if r['steps']>0]
    assert tick_rows
    result = dict(name=case['name'], agents=case['agents'], avoidance=case['avoidance'],
                  wallMs=stats(wall), updateMs=stats([r['updateMs'] for r in rows]),
                  achievedFPS=1000 / mean(wall), over16_67Percent=100 * sum(v > 16.67 for v in wall) / len(wall),
                  maximumBacklog=case['maximumBacklog'], simulationSteps=sum(r['steps'] for r in rows),
                  engineSamples=len(engine), gpuPositive=sum(r['gpuMs'] > 0 for r in engine),
                  renderPositive=sum(r['renderMs'] > 0 for r in engine),
                  gc=[case[f'gen{i}'] for i in range(3)], events=events)
    result['simulationBearingFrames']=len(tick_rows)
    result['tickUpdateMs']=stats([r['updateMs'] for r in tick_rows])
    # This row's work contributes to the next coroutine-to-coroutine wall interval.
    result['tickFollowingWallMs']=stats([by_frame[r['frame']+1]['wallIntervalMs'] for r in tick_rows if r['frame']+1 in by_frame])
    for name in ('cpuMs', 'mainMs', 'renderMs', 'presentWaitMs'):
        result[name] = stats([r[name] for r in engine])
    result['gpuMissing'] = len(engine)-result['gpuPositive']
    result['gpuCoveragePercent'] = 100*result['gpuPositive']/len(engine)
    result['gpuValidOnlyMs'] = stats([r['gpuMs'] for r in engine if r['gpuMs']>0])
    result['gpuTailValidated'] = result['gpuMissing']==0
    return result


def main():
    editor = read('dynamic-editor-final.json')
    validate_behavior(editor)
    assert editor['editor'] and not editor['cases']
    build = read('build.json')
    assert build['result'] == 'Succeeded' and build['errors'] == 0
    assert build['frameTiming'] and not build['development'] and build['backend'] == 'Mono2x'
    reports, processes, cases = [], [], []
    for number in range(1, 4):
        report = read(f'dynamic-run-{number}.json')
        process = read(f'dynamic-run-{number}-process.json')
        validate_behavior(report)
        assert not report['editor'] and not report['batch'] and report['frameTimingEnabled']
        assert report['screenWidth'] == 1280 and report['screenHeight'] == 720 and report['vSync'] == 0
        assert report['cpuTimerFrequency'] > 0
        assert process['exitCode'] == 0 and process['visible'] and not process['interactive']
        for name, digest in process['sourceSha256'].items():
            assert hashlib.sha256((ROOT / name.replace('\\', '/')).read_bytes()).hexdigest().upper() == digest
        assert len(report['cases']) == 6
        assert {(c['agents'], c['avoidance']) for c in report['cases']} == {(n, b) for n in (64, 256, 512) for b in (False, True)}
        reports.append(report)
        processes.append(process)
        cases.append({c['name']: validate_case(c) for c in report['cases']})
    assert len({p['managedAssemblySha256'] for p in processes}) == 1
    assert len({p['playerSha256'] for p in processes}) == 1
    assert len({r['buildGuid'] for r in reports}) == 1
    assert all(processes[i]['utcEnd'] <= processes[i+1]['utcStart'] for i in range(2))
    assembly = ROOT / 'DynamicBuild/DynamicLab_Data/Managed/Assembly-CSharp.dll'
    if assembly.exists():
        assert hashlib.sha256(assembly.read_bytes()).hexdigest().upper() == processes[0]['managedAssemblySha256']
    summary = dict(sessions=3, checksPerSession=12, behaviorsPerSession=6,
                   environment={k: reports[0][k] for k in ('unity', 'cpu', 'gpu', 'graphicsApi', 'os', 'screenWidth', 'screenHeight', 'vSync', 'antiAliasing', 'cpuTimerFrequency')},
                   buildGuid=reports[0]['buildGuid'], managedAssemblySha256=processes[0]['managedAssemblySha256'],
                   behavior=[{**{k:b[k] for k in ('name','agents','arrived','simulatedSeconds','nativeChecks','alternateCrossings')},
                              'audit':b['audit'], 'deferredCloseSeconds': (b['closeCommitTick']-b['closeRequestTick'])/60 if b['closeRequestTick']>=0 else None}
                             for b in reports[0]['behavior']],
                   sessionsData=cases, ranges=[])
    for name in sorted(cases[0]):
        variants = [session[name] for session in cases]
        row = dict(name=name,agents=variants[0]['agents'],avoidance=variants[0]['avoidance'],
                   p95BudgetPassedAll=all(v['wallMs']['p95'] <= 16.67 for v in variants))
        for metric in ('wallMs','updateMs','tickUpdateMs','tickFollowingWallMs','cpuMs','mainMs','renderMs','presentWaitMs'):
            row[metric]={stat:[min(v[metric][stat] for v in variants),max(v[metric][stat] for v in variants)] for stat in ('median','p95','p99','maximum')}
        row['over16_67Percent']=[min(v['over16_67Percent'] for v in variants),max(v['over16_67Percent'] for v in variants)]
        row['gpuCoveragePercent']=[min(v['gpuCoveragePercent'] for v in variants),max(v['gpuCoveragePercent'] for v in variants)]
        row['gpuTailValidatedAll']=all(v['gpuTailValidated'] for v in variants)
        summary['ranges'].append(row)
    (RESULTS / 'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='sessionsData'},indent=2))


if __name__ == '__main__':
    main()
