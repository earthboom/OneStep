"""Compare the real CLI with a fresh Unreal Editor oracle; never write source assets."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def property_data(obj, name):
    values = [p['data'] for p in obj['properties'] if p['name'] == name]
    assert len(values) == 1, f'Expected exactly one serialized {name}'
    return values[0]


def local_path(path):
    return path.split('.', 1)[1].replace(':', '.')


def soft_target(ref):
    value = ref['value']
    if isinstance(value, str):
        return value
    path = value['AssetPath']
    package = path.get('PackageName')
    target = f"{package}.{path['AssetName']}" if package else path['AssetName']
    return target + (':' + value['SubPathString'] if value.get('SubPathString') else '')


def verify(project, dll, output):
    oracle = json.loads((project / 'oracle.json').read_text(encoding='utf-8'))
    assert set(oracle['assets']) == {'animation', 'montage', 'data_asset', 'data_table', 'widget'}
    assert oracle['native_read_preserved_hashes'] is True
    content = project / 'Content/ReaderChecks'
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in content.glob('*.uasset')}
    assert before == oracle['sha256'], 'Fixture files changed after native observation'
    checks, reports = [], {}

    def check(name, action):
        try:
            action()
            checks.append({'name': name, 'passed': True})
        except (AssertionError, KeyError, ValueError, StopIteration) as error:
            checks.append({'name': name, 'passed': False, 'error': str(error) or type(error).__name__})

    def cli(path, *args):
        process = subprocess.run(['dotnet', str(dll), str(path), '--engine', '5.8', *args],
                                 capture_output=True, encoding='utf-8', timeout=90)
        data = json.loads(process.stdout)
        assert process.returncode in (0, 1), data
        return data

    def require(condition, message='Comparison failed'):
        assert condition, message

    for case, expected in oracle['assets'].items():
        asset_name = expected['path'].split('.')[-1]
        path = content / (asset_name + '.uasset')
        report = cli(path, '--properties')
        reports[case] = report
        obj = next(o for o in report['objects'] if o['path'] == asset_name)
        wanted_family = 'data' if case in ('data_asset', 'data_table') else case
        check(case + ':class-and-family', lambda: require(
            obj['class_path'] == expected['class'] and report['analysis']['family'] == wanted_family,
            f"{obj['class_path']} / {report['analysis']['family']}"))
        check(case + ':input-fingerprint', lambda: require(report['input']['sha256'] == before[path.name]))
        if case == 'animation':
            check('animation:rate', lambda: require(property_data(obj, 'RateScale')['Value'] == expected['rate_scale']))
            check('animation:root-motion', lambda: require(property_data(obj, 'bEnableRootMotion')['Value'] == expected['root_motion']))
            check('animation:length', lambda: require(abs(property_data(obj, 'SequenceLength')['Value'] - expected['length']) < 1e-6))
            check('animation:skeleton', lambda: require(any(r.get('target') == expected['skeleton'] for r in obj['references'])))
            model = next(o for o in report['objects'] if o['name'] == 'AnimDataModel')
            check('animation:model-frames', lambda: require(property_data(model, 'NumberOfFrames')['Value'] == int(expected['frames_text'])))
            check('animation:raw-track-state', lambda: require(
                model['property_status'] == 'partial' and any(p['name'] == 'BoneAnimationTracks' and p['status'] == 'unsupported'
                                                             for p in model['properties']),
                'Opaque raw track structs must not be labelled decoded'))
            def translation_check():
                imported = next(o for o in report['objects'] if o['path'] == local_path(expected['import_data']))
                data = property_data(imported, 'ImportTranslation')
                vector = next(v for v in walk(data) if all(k in v for k in ('X', 'Y', 'Z')))
                require([vector[k] for k in ('X', 'Y', 'Z')] == expected['import_translation'])
            check('animation:prefixed-import-properties', translation_check)
        elif case == 'montage':
            check('montage:rate', lambda: require(property_data(obj, 'RateScale')['Value'] == expected['rate_scale']))
            check('montage:skeleton', lambda: require(any(r.get('target') == expected['skeleton'] for r in obj['references'])))
            def section_check():
                require('SectionName="Default"' in expected['sections_text'] or 'SectionName=Default' in expected['sections_text'])
                require(any(v.get('Name') == 'SectionName' and v.get('Value') == 'Default'
                            for v in walk(property_data(obj, 'CompositeSections'))))
            check('montage:sections', section_check)
            def slot_check():
                # Native text export omits a default SlotName. Compare the actually exported
                # segment/reference rather than inventing an effective default-value oracle.
                require('AnimSegments' in expected['slots_text'] and 'A_Sequence' in expected['slots_text'])
                require(len(property_data(obj, 'SlotAnimTracks')['Value']) == 1)
                require(any('SlotAnimTracks' in r['locator'] and r.get('target') == '/Game/ReaderChecks/A_Sequence.A_Sequence'
                            for r in obj['references']))
            check('montage:slot-animation-reference', slot_check)
        elif case == 'data_asset':
            def rules_check():
                data = property_data(obj, 'Rules')
                values = {v.get('Name'): v.get('Value') for v in walk(data) if 'Name' in v}
                require(values['Priority'] == expected['priority'] and values['ChunkId'] == expected['chunk_id'])
            check('data_asset:rules', rules_check)
            check('data_asset:soft-references', lambda: require(sorted(soft_target(r) for r in obj['references']
                if r['kind'] == 'soft_object' and 'ExplicitAssets' in r['locator']) == sorted(expected['references'])))
        elif case == 'data_table':
            def rows_check():
                rows = {r['name']: r['data'] for r in obj['rows']}
                require(set(rows) == {r['Name'] for r in expected['rows']})
                for row in expected['rows']:
                    values = {v.get('Name'): v.get('Value') for v in walk(rows[row['Name']]) if 'Name' in v}
                    require(values['Tag'] == row['Tag'] and values['DevComment'] == row['DevComment'])
            check('data_table:all-rows', rows_check)
            check('data_table:row-struct-reference', lambda: require(any(r.get('target') == expected['row_struct']
                                                                       for r in obj['references'])))
        elif case == 'widget':
            label = next(o for o in report['objects'] if o['path'] == local_path(expected['label']))
            tree = next(o for o in report['objects'] if o['path'] == local_path(expected['tree']))
            check('widget:text', lambda: require(any(expected['text'] == v for node in walk(property_data(label, 'Text'))
                                                    for v in node.values() if isinstance(v, str))))
            check('widget:opacity', lambda: require(property_data(label, 'RenderOpacity')['Value'] == expected['opacity']))
            check('widget:tree-root-reference', lambda: require('RootCanvas' in expected['root_text'] and
                any(r.get('target') == local_path(expected['tree']) + '.RootCanvas' for r in tree['references'])))
            check('widget:slot-content-reference', lambda: require(any(r.get('target') == local_path(expected['label'])
                for node in report['objects'] for r in node.get('references', []))))
            def focused_check():
                focused = cli(path, '--object', local_path(expected['label']), '--property', 'Text')
                require(focused['status'] == 'complete' and len(focused['objects']) == 1)
            check('widget:focused-property', focused_check)

    after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in content.glob('*.uasset')}
    check('sources:unchanged-after-cli', lambda: require(before == after))
    output.mkdir(parents=True, exist_ok=True)
    for name, report in reports.items():
        (output / (name + '.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    result = {'engine': oracle['engine'], 'checks': checks, 'sha256_before': before, 'sha256_after': after,
              'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks)}
    (output / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return int(result['failed'] != 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True, help='Isolated engine fixture project containing oracle.json')
    parser.add_argument('--output', type=Path, required=True, help='Separate evidence directory, outside Content')
    parser.add_argument('--dll', type=Path, default=Path(__file__).resolve().parents[1] / 'src/bin/Release/net8.0/OneStep.UnrealAssets.dll')
    args = parser.parse_args()
    source_content = (args.project / 'Content').resolve()
    if args.output.resolve() == source_content or source_content in args.output.resolve().parents:
        parser.error('Output must not be inside source Content')
    raise SystemExit(verify(args.project.resolve(), args.dll.resolve(), args.output.resolve()))
