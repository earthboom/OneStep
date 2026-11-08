"""Exercise confirmation/idempotency contracts, not a game or durable award service."""
import json
from pathlib import Path


def awards(steps, *, confirmation_required):
    delivered = set()
    result = []
    for phase, match, tick, event, recipient, outcome, trusted in steps:
        if outcome != 'KO' or phase not in ('predict', 'confirm'):
            continue
        if confirmation_required and (phase != 'confirm' or not trusted):
            continue
        key = (match, tick, event, recipient)
        if key not in delivered:
            delivered.add(key)
            result.append(list(key))
    return result


def check(case):
    actual = awards(case['steps'], confirmation_required=True)
    assert actual == case['expected'], (case['name'], actual, case['expected'])
    if case.get('dedup_only_must_fail'):
        assert awards(case['steps'], confirmation_required=False) != case['expected'], case['name']
    return case['name']


if __name__ == '__main__':
    data = json.loads(Path(__file__).with_name('rollback-reward-cases.json').read_text(encoding='utf-8'))
    names = [check(case) for case in data['cases']]
    print(json.dumps(dict(passed=len(names), negative_controls=sum(bool(c.get('dedup_only_must_fail')) for c in data['cases']),
                          cases=names, limitation='Toy trusted-confirmation flag and in-memory keys only. No engine, protocol trust, restart, transaction or receiver validation.'), indent=2))
