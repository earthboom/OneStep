"""Prepare anonymous review sheets or aggregate completed blind scores."""

import argparse
import json
import random
import runpy
from collections import Counter
from pathlib import Path


HERE = Path(__file__).parent
ROOT = HERE.parent
ARMS = ('old', 'revised')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def prepare():
    paint_sheet = runpy.run_path(str(ROOT / 'prepare-review.py'))['paint_sheet']
    protocol = read_json(HERE / 'protocol.json')
    repetitions = protocol['repetitions_per_arm']
    review = HERE / 'review'
    review.mkdir(exist_ok=True)
    rng = random.Random(513822)
    key = {}
    for case in ('05', '09'):
        frames = ('05',) if case == '05' else ('09a', '09b')
        choices = [(arm, repeat) for arm in ARMS for repeat in range(1, repetitions + 1)]
        rng.shuffle(choices)
        cards = []
        key[case] = {}
        for i, (arm, repeat) in enumerate(choices):
            label = f'{case}-{chr(65 + i)}'
            files = tuple(f'targeted-retest/{arm}/{frame}-r{repeat}.png' for frame in frames)
            cards.append((label, files))
            key[case][label] = {'arm': arm, 'repeat': repeat, 'files': files}
        checks = [f'{frame} {check}' for frame in frames for check in protocol['cases'][frame]['checks']]
        if case == '09':
            checks.append('The recurring character matches across the two scenes.')
            cards.append(('SHARED IDENTITY REFERENCE', ('fixtures/robot.png',)))
        paint_sheet(cards, ROOT, review / f'{case}.jpg')
        write_json(review / f'{case}.json', {'checks': checks, 'labels': list(key[case])})
    write_json(HERE / 'review-key.json', key)


def score():
    key = read_json(HERE / 'review-key.json')
    ratings = read_json(HERE / 'review-scores.json')
    if set(key) != set(ratings):
        raise ValueError('Review must contain both cases.')
    totals = {}
    for case, candidates in key.items():
        manifest = read_json(HERE / 'review' / f'{case}.json')
        checks = manifest['checks']
        if set(candidates) != set(ratings[case]):
            raise ValueError(f'Incomplete ratings for {case}.')
        totals[case] = {arm: Counter() for arm in ARMS}
        for label, candidate in candidates.items():
            rating = ratings[case][label]
            marks = rating['marks']
            if len(marks) != len(checks) or set(marks) - set('PFU'):
                raise ValueError(f'Invalid checks for {label}: {marks}')
            if set(marks) - {'P'} and not rating.get('note'):
                raise ValueError(f'Missing rationale for {label}.')
            tally = totals[case][candidate['arm']]
            tally.update(marks)
            tally['total'] += 1
            tally['pass'] += set(marks) == {'P'}
    write_json(HERE / 'metrics.json', totals)
    print(json.dumps(totals, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'score'))
    args = parser.parse_args()
    (prepare if args.action == 'prepare' else score)()
