"""Black-box checks: build Release and fetch fixtures before running discovery."""
import hashlib
import json
from pathlib import Path
import subprocess
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DLL = ROOT / 'src/bin/Release/net8.0/OneStep.UnrealAssets.dll'
FIXTURES = ROOT / 'tests/fixtures'


def invoke(*args):
    process = subprocess.run(['dotnet', str(DLL), *map(str, args)],
                             capture_output=True, encoding='utf-8', timeout=30)
    return process, json.loads(process.stdout)


class ReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DLL.is_file():
            raise RuntimeError('Build the Release CLI before running tests')
        manifest = json.loads((ROOT / 'tests/fixtures.json').read_text())
        for item in manifest['files']:
            path = FIXTURES / item['name']
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                raise RuntimeError('Run tests/fetch_fixtures.py; fixture missing or changed: ' + item['name'])

    def test_help_is_reachable(self):
        p = subprocess.run(['dotnet', str(DLL), '--help'], capture_output=True, text=True)
        self.assertEqual(0, p.returncode)
        self.assertIn('--properties', p.stdout)

    def test_structure_does_not_claim_properties_were_decoded(self):
        p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27')
        self.assertEqual(0, p.returncode, data)
        self.assertEqual('complete', data['status'])
        self.assertEqual(14, data['package']['export_count'])
        self.assertEqual(18, data['package']['import_count'])
        self.assertEqual('blueprint', data['analysis']['family'])
        first = data['objects'][0]
        self.assertEqual('TestActorBP', first['name'])
        self.assertEqual('Blueprint', first['class_name'])
        self.assertEqual('not_requested', first['property_status'])
        self.assertNotIn('properties', first)

    def test_property_value_and_hard_reference_are_not_confused(self):
        p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27',
                         '--object', 'TestActorBP', '--properties')
        self.assertEqual(0, p.returncode, data)
        obj = data['objects'][0]
        props = {x['name']: x for x in obj['properties']}
        self.assertEqual(2, props['BlueprintSystemVersion']['data']['Value'])
        refs = obj['references']
        parent = next(x for x in refs if 'ParentClass' in x['locator'])
        self.assertEqual(-7, parent['index'])
        self.assertEqual('/Script/Engine.Actor', parent['target'])
        self.assertFalse(any('BlueprintSystemVersion' in x['locator'] for x in refs))
        graph = next(x for x in refs if x['index'] == 3)
        self.assertEqual('TestActorBP.EventGraph', graph['target'])

    def test_filter_and_nested_values_keep_type_information(self):
        p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27',
                         '--object', 'TestActorBP', '--property', 'UbergraphPages')
        self.assertEqual(0, p.returncode, data)
        props = data['objects'][0]['properties']
        self.assertEqual(['UbergraphPages'], [x['name'] for x in props])
        self.assertIn('ObjectPropertyData', props[0]['data']['Value'][0]['$type'])
        self.assertEqual(3, props[0]['data']['Value'][0]['Value'])

    def test_soft_path_payload_is_preserved_in_reference_summary(self):
        p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27',
                         '--object', 'TestActorBP', '--property', 'LastEditedDocuments')
        self.assertEqual(0, p.returncode, data)
        refs = [x for x in data['objects'][0]['references'] if x['kind'] == 'soft_object']
        self.assertTrue(any(isinstance(x['value'], dict) and
                            x['value']['AssetPath']['AssetName'] == '/Game/TestActorBP.TestActorBP_C'
                            for x in refs), refs)

    def test_actual_ue57_blueprint(self):
        p, data = invoke(FIXTURES / 'BP_FirstPersonGameMode.uasset', '--engine', '5.7',
                         '--object', 'BP_FirstPersonGameMode', '--property', 'ParentClass')
        self.assertEqual(0, p.returncode, data)
        self.assertEqual('blueprint', data['analysis']['family'])
        self.assertEqual('Blueprint', data['objects'][0]['class_name'])
        self.assertTrue(any(x['target'] == '/Script/Engine.GameModeBase'
                            for x in data['objects'][0]['references']))

    def test_opaque_node_bytes_are_partial_not_empty_success(self):
        p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27',
                         '--object', 'K2Node_Event_0', '--properties')
        self.assertEqual(1, p.returncode, data)
        self.assertEqual('partial', data['status'])
        self.assertGreater(data['objects'][0]['opaque_bytes'], 0)
        self.assertEqual('partial', data['objects'][0]['property_status'])

    def test_generic_class_does_not_get_inferred_from_filename(self):
        p, data = invoke(FIXTURES / 'TestSoundClass.uasset', '--engine', '4.27', '--properties')
        self.assertIn(p.returncode, (0, 1), data)
        self.assertEqual('generic', data['analysis']['family'])
        sound = next(x for x in data['objects'] if x['name'] == 'TestSoundClass')
        self.assertEqual('SoundClass', sound['class_name'])

    def test_unknown_selector_and_property_fail(self):
        for extra in [('--object', 'NoSuchObject'),
                      ('--object', 'TestActorBP', '--property', 'NoSuchProperty')]:
            with self.subTest(extra=extra):
                p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27', *extra)
                self.assertEqual(2, p.returncode, data)
                self.assertEqual('error', data['status'])

    def test_invalid_engine_and_arguments_fail(self):
        for extra in [('--engine', '99.9'), ('--engine', '0'), ('--engine', '5.7', '--bogus'),
                      ('--engine',), ('--engine', '5.7', '--engine', '4.27')]:
            with self.subTest(extra=extra):
                p, data = invoke(FIXTURES / 'TestActorBP.uasset', *extra)
                self.assertEqual(2, p.returncode, data)
                self.assertEqual('error', data['status'])

    def test_truncated_missing_and_nonasset_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            bad = folder / 'cut.uasset'
            bad.write_bytes((FIXTURES / 'TestActorBP.uasset').read_bytes()[:100])
            text = folder / 'fake.txt'
            text.write_text('not a package')
            for path in [bad, folder / 'missing.uasset', text]:
                with self.subTest(path=path.name):
                    p, data = invoke(path, '--engine', '4.27', '--properties')
                    self.assertEqual(2, p.returncode, data)
                    self.assertEqual('error', data['status'])

    def test_cooked_input_is_rejected_even_in_structure_mode(self):
        p, data = invoke(FIXTURES / 'Items.uasset', '--engine', '4.23')
        self.assertEqual(2, p.returncode, data)
        self.assertEqual('error', data['status'])
        self.assertEqual('unsupported_package', data['error']['code'])

    def test_readonly_original_hashes_and_no_neighbour_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            asset = folder / 'renamed.uasset'
            original = (FIXTURES / 'TestActorBP.uasset').read_bytes()
            asset.write_bytes(original)
            sentinel = folder / 'renamed.uexp'
            sentinel.write_bytes(b'not part of this uncooked package')
            before = {x.name: x.read_bytes() for x in folder.iterdir()}
            p, data = invoke(asset, '--engine', '4.27', '--object', 'TestActorBP', '--properties')
            self.assertEqual(0, p.returncode, data)
            self.assertEqual('blueprint', data['analysis']['family'])
            self.assertEqual(hashlib.sha256(original).hexdigest(), data['input']['sha256'])
            self.assertEqual(before, {x.name: x.read_bytes() for x in folder.iterdir()})

    def test_family_extension_uses_class_identity_and_reads_properties(self):
        # Synthetic normal-export bodies exercise dispatch, not real animation/widget serializers.
        writer = ROOT / 'tests/writer/bin/Release/net8.0/FixtureWriter.dll'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['dotnet', str(writer), str(FIXTURES / 'TestSoundClass.uasset'), tmp],
                           check=True, capture_output=True, timeout=30)
            for family in ['animation', 'montage', 'data', 'widget']:
                with self.subTest(family=family):
                    p, data = invoke(Path(tmp) / (family + '.uasset'), '--engine', '4.27',
                                     '--object', 'TestSoundClass', '--property', 'FixtureValue')
                    self.assertEqual(0, p.returncode, data)
                    self.assertEqual(family, data['analysis']['family'])
                    self.assertEqual(37, data['objects'][0]['properties'][0]['data']['Value'])

    def test_oversized_input_is_rejected_without_loading_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'oversized.uasset'
            with path.open('wb') as output:
                output.truncate(256 * 1024 * 1024 + 1)
            p, data = invoke(path)
            self.assertEqual(2, p.returncode, data)
            self.assertEqual('input_size', data['error']['code'])

    def test_interface_and_delegate_targets_are_reported(self):
        writer = ROOT / 'tests/writer/bin/Release/net8.0/FixtureWriter.dll'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['dotnet', str(writer), str(FIXTURES / 'TestSoundClass.uasset'), tmp],
                           check=True, capture_output=True, timeout=30)
            p, data = invoke(Path(tmp) / 'data.uasset', '--engine', '4.27',
                             '--object', 'TestSoundClass', '--properties')
            self.assertEqual(0, p.returncode, data)
            refs = data['objects'][0]['references']
            for name in ['FixtureInterface', 'FixtureDelegate']:
                self.assertTrue(any(name in x['locator'] and x['target'] == 'TestSoundClass' for x in refs), refs)

    def test_legacy_text_does_not_consume_a_modern_dev_notes_field(self):
        writer = ROOT / 'tests/writer/bin/Release/net8.0/FixtureWriter.dll'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['dotnet', str(writer), str(FIXTURES / 'TestSoundClass.uasset'), tmp],
                           check=True, capture_output=True, timeout=30)
            p, data = invoke(Path(tmp) / 'data.uasset', '--engine', '4.27',
                             '--object', 'TestSoundClass', '--properties')
            self.assertEqual(0, p.returncode, data)
            props = {x['name']: x['data'] for x in data['objects'][0]['properties']}
            self.assertEqual('Legacy text 37', props['FixtureText']['CultureInvariantString'])
            self.assertEqual('Key37', props['FixtureText']['Value'])
            self.assertIsNone(props['FixtureText']['DevNotes'])
            self.assertEqual(37, props['FixtureValue']['Value'])

    def test_same_class_name_in_another_package_does_not_select_native_analyzer(self):
        writer = ROOT / 'tests/writer/bin/Release/net8.0/FixtureWriter.dll'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['dotnet', str(writer), str(FIXTURES / 'TestSoundClass.uasset'), tmp],
                           check=True, capture_output=True, timeout=30)
            p, data = invoke(Path(tmp) / 'spoof.uasset', '--engine', '4.27')
            self.assertEqual(0, p.returncode, data)
            self.assertEqual('generic', data['analysis']['family'])

    def test_ambiguous_name_fails_but_qualified_path_selects_one(self):
        writer = ROOT / 'tests/writer/bin/Release/net8.0/FixtureWriter.dll'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['dotnet', str(writer), str(FIXTURES / 'TestSoundClass.uasset'), tmp],
                           check=True, capture_output=True, timeout=30)
            path = Path(tmp) / 'ambiguous.uasset'
            p, data = invoke(path, '--engine', '4.27', '--object', 'Duplicate')
            self.assertEqual(2, p.returncode, data)
            self.assertEqual('object_selection', data['error']['code'])
            p, data = invoke(path, '--engine', '4.27', '--object', 'TestSoundClass.Duplicate', '--properties')
            self.assertEqual(0, p.returncode, data)
            self.assertEqual(['TestSoundClass.Duplicate'], [x['path'] for x in data['objects']])

    def test_soft_path_subclasses_do_not_disappear_from_references(self):
        writer = ROOT / 'tests/writer/bin/Release/net8.0/FixtureWriter.dll'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['dotnet', str(writer), str(FIXTURES / 'TestSoundClass.uasset'), tmp],
                           check=True, capture_output=True, timeout=30)
            p, data = invoke(Path(tmp) / 'data.uasset', '--engine', '4.27',
                             '--object', 'TestSoundClass', '--properties')
            self.assertEqual(0, p.returncode, data)
            refs = [x for x in data['objects'][0]['references'] if x['kind'] == 'soft_object']
            for struct_name in ['SoftClassPath', 'SoftAssetPath', 'StringAssetReference', 'StringClassReference']:
                matching = [x for x in refs if 'Fixture' + struct_name in x['locator']]
                self.assertEqual(1, len(matching), refs)
                self.assertEqual('/Game/Example.Example_C', matching[0]['value']['AssetPath']['AssetName'])

    def test_full_properties_exposes_partial_graph_and_preserves_all_objects(self):
        p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27', '--properties')
        self.assertEqual(1, p.returncode, data)
        self.assertEqual(14, len(data['objects']))
        self.assertTrue(any(x['property_status'] == 'partial' for x in data['objects']))

    def test_data_table_rows_are_not_reported_as_an_empty_asset(self):
        writer = ROOT / 'tests/writer/bin/Release/net8.0/FixtureWriter.dll'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['dotnet', str(writer), str(FIXTURES / 'TestSoundClass.uasset'), tmp],
                           check=True, capture_output=True, timeout=30)
            p, data = invoke(Path(tmp) / 'table.uasset', '--engine', '4.27',
                             '--object', 'TestSoundClass', '--properties')
            self.assertEqual(0, p.returncode, data)
            obj = data['objects'][0]
            self.assertIn('rows', obj)
            self.assertEqual('Alpha', obj['rows'][0]['name'])
            self.assertEqual(42, obj['rows'][0]['data']['Value'][0]['Value'])

    def test_auto_version_and_qualified_object_path(self):
        p, data = invoke(FIXTURES / 'TestActorBP.uasset', '--object', 'TestActorBP.EventGraph', '--properties')
        self.assertEqual(0, p.returncode, data)
        self.assertEqual(['EventGraph'], [x['name'] for x in data['objects']])
        self.assertEqual('TestActorBP.EventGraph', data['objects'][0]['path'])

    def test_broken_export_body_is_visible_as_partial_or_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'broken.uasset'
            original = bytearray((FIXTURES / 'TestActorBP.uasset').read_bytes())
            # Locate the body through the public structure query, then invalidate its name index.
            _, structure = invoke(FIXTURES / 'TestActorBP.uasset', '--engine', '4.27')
            offset = structure['objects'][0]['serial_offset']
            struct.pack_into('<i', original, offset, 0x7fffffff)
            path.write_bytes(original)
            p, data = invoke(path, '--engine', '4.27', '--object', 'TestActorBP', '--properties')
            self.assertIn(p.returncode, (1, 2), data)
            self.assertIn(data['status'], ('partial', 'error'))
            if p.returncode == 1:
                self.assertEqual('unsupported', data['objects'][0]['property_status'])
                self.assertGreater(data['objects'][0]['opaque_bytes'], 0)

    def test_declared_export_size_cannot_be_ignored(self):
        # The pinned fixture's first export declares SerialSize=942 at this header offset.
        source = (FIXTURES / 'TestActorBP.uasset').read_bytes()
        # Derive the field location from a literal serialized int64 in the first export header,
        # not from the code under test. The independently reviewed fixture starts its body at 14011.
        needle = struct.pack('<qq', 942, 14011)
        self.assertEqual(1, source.count(needle))
        size_offset = source.index(needle)
        with tempfile.TemporaryDirectory() as tmp:
            for size in [0, 1]:
                with self.subTest(size=size):
                    data_bytes = bytearray(source)
                    struct.pack_into('<q', data_bytes, size_offset, size)
                    path = Path(tmp) / 'short.uasset'
                    path.write_bytes(data_bytes)
                    p, data = invoke(path, '--engine', '4.27', '--object', 'TestActorBP', '--properties')
                    self.assertIn(p.returncode, (1, 2), data)
                    self.assertNotEqual('complete', data['status'])

    def test_native_verifier_refuses_source_content_as_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            content = project / 'Content'
            content.mkdir()
            process = subprocess.run([sys.executable, str(ROOT / 'tests/verify_engine_assets.py'),
                                      '--project', str(project), '--output', str(content)],
                                     capture_output=True, text=True, timeout=30)
            self.assertEqual(2, process.returncode, process.stderr)
            self.assertEqual([], list(content.iterdir()))


if __name__ == '__main__':
    unittest.main()
