"""Join the blind ratings to the workflow key and report paired counts."""

import json
from collections import Counter
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def summarize(root):
    key = read_json(root / 'review-key.json')
    scored = read_json(root / 'review-scores.json')
    if set(key) != set(scored) or len(key) != 12:
        raise ValueError('The scores must cover all 12 cases.')
    totals = {group: {stage: Counter() for stage in ('first', 'final')}
              for group in ('baseline', 'vegabond')}
    paired = {stage: Counter() for stage in ('first', 'final')}
    result = {}
    for case, arms in key.items():
        manifest = read_json(root / 'review' / f'{case}.json')
        checks = manifest['checks']
        labels = set(manifest['candidates'])
        if set(scored[case]) != labels:
            raise ValueError(f'{case} has missing or unexpected ratings.')
        for label in labels:
            rating = scored[case][label]
            marks = rating['marks']
            if len(marks) != len(checks) or set(marks) - set('PFU'):
                raise ValueError(f'{label} has invalid marks: {marks}')
            if set(marks) - {'P'} and not rating.get('note'):
                raise ValueError(f'{label} needs a reason for each failed or unverified check.')
        case_result = {}
        for arm, stages in arms.items():
            group = arm.split('-')[0]
            case_result[arm] = {}
            for stage, label in stages.items():
                rating = scored[case][label]
                marks = rating['marks']
                passed = set(marks) == {'P'}
                counts = totals[group][stage]
                counts.update(marks)
                counts['passed_tasks'] += passed
                counts['tasks'] += 1
                case_result[arm][stage] = {
                    'label': label, 'passed': passed,
                    'failed': [check for check, mark in zip(checks, marks) if mark == 'F'],
                    'unverified': [check for check, mark in zip(checks, marks) if mark == 'U'],
                    'note': rating['note'],
                }
        for repeat in (1, 2):
            for stage in ('first', 'final'):
                old = case_result[f'baseline-{repeat}'][stage]['passed']
                new = case_result[f'vegabond-{repeat}'][stage]['passed']
                difference = int(new) - int(old)
                paired[stage][{1: 'vegabond_only', 0: 'same', -1: 'baseline_only'}[difference]] += 1
        result[case] = case_result
    return {'totals': totals, 'paired': paired, 'cases': result}


if __name__ == '__main__':
    root = Path(__file__).parent
    result = summarize(root)
    (root / 'metrics.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('totals', 'paired')}, indent=2))
