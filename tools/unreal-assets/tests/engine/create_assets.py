import hashlib
import json
import traceback
from pathlib import Path
import unreal

root = Path(unreal.Paths.project_dir())
if (root / 'oracle.json').exists():
    raise RuntimeError('Fixtures are frozen after native observation; use a fresh fixture project for generation')
tools = unreal.AssetToolsHelpers.get_asset_tools()
dest = '/Game/ReaderChecks'
unreal.EditorAssetLibrary.make_directory(dest)
report = {'engine': unreal.SystemLibrary.get_engine_version(), 'assets': {}, 'errors': []}


def save(obj):
    assert obj is not None
    assert obj.get_path_name().startswith(dest + '/')
    assert unreal.EditorAssetLibrary.save_loaded_asset(obj, False)
    return obj


def step(name, action):
    try:
        result = action()
        report['assets'][name] = result
        unreal.log('ONESTEP_ASSET_OK ' + name)
    except Exception:
        report['errors'].append({'step': name, 'trace': traceback.format_exc()})
        unreal.log_warning(traceback.format_exc())
    (root / 'creation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


def animation():
    source = unreal.load_asset('/Engine/Tutorial/SubEditors/TutorialAssets/Character/Tutorial_Idle')
    assert source is not None
    seq = unreal.load_asset(dest + '/A_Sequence') or tools.duplicate_asset('A_Sequence', dest, source)
    assert seq is not None
    unreal.AnimationLibrary.set_rate_scale(seq, 1.25)
    unreal.AnimationLibrary.set_root_motion_enabled(seq, True)
    import_data = seq.get_editor_property('asset_import_data')
    import_data.set_editor_property('import_translation', unreal.Vector(1, 2, 3))
    for field, asset_path in [('bone_compression_settings', '/Engine/Animation/DefaultAnimBoneCompressionSettings'),
                              ('curve_compression_settings', '/Engine/Animation/DefaultAnimCurveCompressionSettings')]:
        seq.set_editor_property(field, unreal.load_asset(asset_path))
    save(seq)
    return {'path': seq.get_path_name(), 'class': seq.get_class().get_path_name(),
            'rate_scale': unreal.AnimationLibrary.get_rate_scale(seq),
            'root_motion': unreal.AnimationLibrary.is_root_motion_enabled(seq),
            'length': unreal.AnimationLibrary.get_sequence_length(seq),
            'import_translation': [float(import_data.get_editor_property('import_translation').x),
                                   float(import_data.get_editor_property('import_translation').y),
                                   float(import_data.get_editor_property('import_translation').z)],
            'skeleton': seq.get_editor_property('skeleton').get_path_name()}


def montage():
    seq = unreal.load_asset(dest + '/A_Sequence')
    factory = unreal.AnimMontageFactory()
    factory.set_editor_property('target_skeleton', seq.get_editor_property('skeleton'))
    factory.set_editor_property('source_animation', seq)
    obj = unreal.load_asset(dest + '/AM_Montage') or tools.create_asset('AM_Montage', dest, unreal.AnimMontage, factory)
    obj.set_editor_property('rate_scale', 0.75)
    save(obj)
    return {'path': obj.get_path_name(), 'class': obj.get_class().get_path_name(),
            'rate_scale': obj.get_editor_property('rate_scale'),
            'sections_text': unreal.ReaderFixtureLibrary.property_text(obj, 'CompositeSections'),
            'slots_text': unreal.ReaderFixtureLibrary.property_text(obj, 'SlotAnimTracks'),
            'skeleton': obj.get_editor_property('skeleton').get_path_name()}


def widget():
    factory = unreal.WidgetBlueprintFactory()
    factory.set_editor_property('parent_class', unreal.UserWidget)
    bp = unreal.load_asset(dest + '/WBP_Status') or tools.create_asset('WBP_Status', dest, unreal.WidgetBlueprint, factory)
    tree = unreal.find_object(bp, 'WidgetTree')
    assert tree is not None
    label = unreal.ReaderFixtureLibrary.configure_widget(bp)
    save(bp)
    return {'path': bp.get_path_name(), 'class': bp.get_class().get_path_name(),
            'tree': tree.get_path_name(), 'root': 'RootCanvas',
            'text_object': label.get_name(), 'text': str(label.get_text()),
            'opacity': label.get_editor_property('render_opacity')}


def data_asset():
    factory = unreal.DataAssetFactory()
    factory.set_editor_property('data_asset_class', unreal.PrimaryAssetLabel)
    obj = unreal.load_asset(dest + '/DA_References') or tools.create_asset('DA_References', dest, unreal.PrimaryAssetLabel, factory)
    assets = [unreal.load_asset(dest + '/' + name) for name in ['A_Sequence', 'AM_Montage', 'WBP_Status']]
    assert all(assets)
    obj.set_editor_property('ExplicitAssets', assets)
    rules = obj.get_editor_property('Rules')
    rules.set_editor_property('priority', 37)
    rules.set_editor_property('chunk_id', 7)
    obj.set_editor_property('Rules', rules)
    save(obj)
    return {'path': obj.get_path_name(), 'class': obj.get_class().get_path_name(),
            'priority': obj.get_editor_property('Rules').get_editor_property('priority'),
            'chunk_id': obj.get_editor_property('Rules').get_editor_property('chunk_id'),
            'references': [x.get_path_name() for x in obj.get_editor_property('ExplicitAssets')]}


def data_table():
    factory = unreal.DataTableFactory()
    row_struct = unreal.load_object(None, '/Script/GameplayTags.GameplayTagTableRow')
    assert row_struct is not None
    factory.set_editor_property('struct', row_struct)
    obj = unreal.load_asset(dest + '/DT_Tags') or tools.create_asset('DT_Tags', dest, unreal.DataTable, factory)
    rows = [{'Name': 'Alpha', 'Tag': 'OneStep.Alpha', 'DevComment': 'engine-written 37'},
            {'Name': 'Beta', 'Tag': 'OneStep.Beta', 'DevComment': 'second row'}]
    assert unreal.DataTableFunctionLibrary.fill_data_table_from_json_string(obj, json.dumps(rows))
    save(obj)
    return {'path': obj.get_path_name(), 'class': obj.get_class().get_path_name(),
            'row_struct': obj.get_editor_property('row_struct').get_path_name(),
            'json': unreal.DataTableFunctionLibrary.export_data_table_to_json_string(obj)}


for name, action in [('animation', animation), ('montage', montage), ('widget', widget),
                      ('data_asset', data_asset), ('data_table', data_table)]:
    step(name, action)
if report['errors']:
    raise RuntimeError('Some native fixture creation steps failed; inspect creation.json')
unreal.log('ONESTEP_NATIVE_ASSETS_COMPLETE')
