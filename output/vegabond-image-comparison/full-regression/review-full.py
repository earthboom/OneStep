"""Prepare a blind regrade and compare it with the historical benchmark."""

import argparse
import json
import random
import runpy
from pathlib import Path

from PIL import Image


HERE = Path(__file__).parent
ROOT = HERE.parent
HELPERS = runpy.run_path(str(ROOT / 'prepare-review.py'))
CHECKS = HELPERS['CHECKS']
REFERENCES = HELPERS['REFERENCES']
STAGES = ('first', 'final')
TARGETS = {'05', '09'}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run_records():
    protocol = read_json(HERE / 'protocol.json')
    runs = {}
    for repetition, frozen in protocol['runs'].items():
        runs[repetition] = images = {item['id']: item for item in read_json(HERE / repetition / 'run.json')['images']}
        if set(images) != set(frozen):
            raise ValueError(f'{repetition} does not cover all requested images.')
        for image_id, item in images.items():
            expected = frozen[image_id]
            for field in ('prompt', 'references', 'transparent_background'):
                if item[field] != expected[field]:
                    raise ValueError(f'{repetition}/{image_id} differs from the frozen {field}.')
            for field in ('raw', 'initial', 'final'):
                with Image.open(HERE / repetition / item[field]) as image:
                    if image.format != 'PNG':
                        raise ValueError(f'{repetition}/{image_id} {field} is not PNG.')
                    image.verify()
            repair = item['repair']
            if repair and (not (HERE / repetition / repair['result']).is_file()
                           or repair['selected'] != (item['final'] == repair['result'])):
                raise ValueError(f'{repetition}/{image_id} repair and selection disagree.')
    return runs


def original_image(arm, image, stage):
    final = f'{arm}/{image}-final.png'
    return final if stage == 'final' and (ROOT / final).is_file() else f'{arm}/{image}-initial.png'


def prepare():
    runs = run_records()
    review = HERE / 'review'
    review.mkdir(exist_ok=True)
    key = {}
    for case, checks in CHECKS.items():
        ids = ('09a', '09b') if case == '09' else (case,)
        files_by_run = {}
        for number in (1, 2):
            old, new = f'vegabond-{number}', f'r{number}'
            files_by_run[old] = {stage: tuple(original_image(old, image, stage) for image in ids) for stage in STAGES}
            files_by_run[new] = {
                stage: tuple(f'full-regression/{new}/' + runs[new][image]['initial' if stage == 'first' else 'final']
                             for image in ids)
                for stage in STAGES
            }
        candidates = sorted({files for stages in files_by_run.values() for files in stages.values()})
        random.Random(641080 + int(case)).shuffle(candidates)
        labels = {files: f'{case}-{chr(65 + index)}' for index, files in enumerate(candidates)}
        key[case] = {run: {stage: labels[files] for stage, files in stages.items()} for run, stages in files_by_run.items()}
        cards = [(labels[files], files) for files in candidates]
        for index, ref in enumerate(REFERENCES.get(case, ()), 1):
            cards.append((f'REFERENCE {index}', (f'fixtures/{ref}',)))
        HELPERS['paint_sheet'](cards, ROOT, review / f'{case}.jpg')
        write_json(review / f'{case}.json', {
            'checks': checks,
            'candidates': {labels[files]: [HELPERS['describe'](ROOT / file) for file in files] for files in candidates},
        })
        if case in {'01', '02', '06'}:
            for label, (file,) in cards:
                with Image.open(ROOT / file) as image:
                    image.convert('RGB').save(review / f'{label}-detail.jpg', quality=95)
    write_json(HERE / 'review-key.json', key)


def historical(v1, case, number, stage):
    arm = f'vegabond-{number}' if v1 else f'baseline-{number}'
    return HISTORICAL['cases'][case][arm][stage]


def result_from_rating(checks, rating):
    marks = rating['marks']
    if len(marks) != len(checks) or set(marks) - set('PFU'):
        raise ValueError(f'Unexpected verification marks: {marks}.')
    if set(marks) - {'P'} and not rating['note']:
        raise ValueError('Every failed or unverified item needs an observation.')
    return {
        'passed': set(marks) == {'P'},
        'failed': [check for check, mark in zip(checks, marks) if mark == 'F'],
        'unverified': [check for check, mark in zip(checks, marks) if mark == 'U'],
        'note': rating['note'],
    }


def score():
    runs = run_records()
    key = read_json(HERE / 'review-key.json')
    ratings = read_json(HERE / 'review-scores.json')
    if set(key) != set(CHECKS) or set(ratings) != set(CHECKS):
        raise ValueError('All 12 original cases must be graded.')
    grades = {}
    scopes = {'all': list(CHECKS), 'targeted': [c for c in CHECKS if c in TARGETS],
              'other': [c for c in CHECKS if c not in TARGETS]}
    for case, checks in CHECKS.items():
        labels = {label for stages in key[case].values() for label in stages.values()}
        if set(ratings[case]) != labels:
            raise ValueError(f'{case} has missing or extra blind ratings.')
        grades[case] = {}
        for number in (1, 2):
            grades[case][f'r{number}'] = {}
            for stage in STAGES:
                previous_label = key[case][f'vegabond-{number}'][stage]
                new_label = key[case][f'r{number}'][stage]
                grades[case][f'r{number}'][stage] = {
                    'stock': historical(False, case, number, stage),
                    'v1_historical': historical(True, case, number, stage),
                    'v1_regraded': result_from_rating(checks, ratings[case][previous_label]),
                    'v2': result_from_rating(checks, ratings[case][new_label]),
                }
    methods = ('stock', 'v1_historical', 'v1_regraded', 'v2')
    totals = {}
    for scope, cases in scopes.items():
        totals[scope] = {method: {stage: sum(grades[case][run][stage][method]['passed']
                                             for case in cases for run in runs) for stage in STAGES}
                         for method in methods}
        totals[scope]['tasks_per_method'] = len(cases) * len(runs)
        totals[scope]['v2_repair_calls'] = sum(bool(image['repair']) for images in runs.values()
                                             for image_id, image in images.items() if image_id[:2] in cases)
    losses = {stage: [{'case': case, 'run': run, **stages[stage]['v2']}
                      for case, comparisons in grades.items() for run, stages in comparisons.items()
                      if stages[stage]['v1_regraded']['passed'] and not stages[stage]['v2']['passed']]
              for stage in STAGES}
    write_json(HERE / 'metrics.json', {'totals': totals, 'losses_vs_v1_regrade': losses, 'cases': grades})
    print(json.dumps({'totals': totals, 'losses_vs_v1_regrade': losses}, indent=2, ensure_ascii=False))


HISTORICAL = read_json(ROOT / 'metrics.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'score'))
    args = parser.parse_args()
    (prepare if args.action == 'prepare' else score)()
