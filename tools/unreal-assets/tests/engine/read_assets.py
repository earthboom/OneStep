import hashlib
import json
from pathlib import Path
import unreal

root = Path(unreal.Paths.project_dir())
names = {'animation': 'A_Sequence', 'montage': 'AM_Montage', 'widget': 'WBP_Status',
         'data_asset': 'DA_References', 'data_table': 'DT_Tags'}
files = sorted((root / 'Content/ReaderChecks').glob('*.uasset'))
before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
report = {'engine': unreal.SystemLibrary.get_engine_version(), 'assets': {}, 'sha256': before}
for family, name in names.items():
    obj = unreal.load_asset('/Game/ReaderChecks/' + name)
    assert obj is not None
    item = {'path': obj.get_path_name(), 'class': obj.get_class().get_path_name()}
    if family == 'animation':
        item.update(rate_scale=unreal.AnimationLibrary.get_rate_scale(obj),
                    root_motion=unreal.AnimationLibrary.is_root_motion_enabled(obj),
                    length=unreal.AnimationLibrary.get_sequence_length(obj),
                    skeleton=obj.get_editor_property('skeleton').get_path_name())
        model = unreal.find_object(obj, 'AnimDataModel')
        item['frames_text'] = unreal.ReaderFixtureLibrary.property_text(model, 'NumberOfFrames')
        item['frame_rate_text'] = unreal.ReaderFixtureLibrary.property_text(model, 'FrameRate')
        data = obj.get_editor_property('asset_import_data')
        vector = data.get_editor_property('import_translation')
        item['import_translation'] = [float(vector.x), float(vector.y), float(vector.z)]
        item['import_data'] = data.get_path_name()
    elif family == 'montage':
        item.update(rate_scale=obj.get_editor_property('rate_scale'),
                    skeleton=obj.get_editor_property('skeleton').get_path_name(),
                    sections_text=unreal.ReaderFixtureLibrary.property_text(obj, 'CompositeSections'),
                    slots_text=unreal.ReaderFixtureLibrary.property_text(obj, 'SlotAnimTracks'))
    elif family == 'widget':
        tree = unreal.find_object(obj, 'WidgetTree')
        label = unreal.find_object(tree, 'StatusLabel')
        item.update(tree=tree.get_path_name(), root_text=unreal.ReaderFixtureLibrary.property_text(tree, 'RootWidget'),
                    label=label.get_path_name(), text=str(label.get_text()), opacity=label.get_editor_property('render_opacity'))
    elif family == 'data_asset':
        rules = obj.get_editor_property('Rules')
        item.update(priority=rules.get_editor_property('priority'), chunk_id=rules.get_editor_property('chunk_id'),
                    references=[x.get_path_name() for x in obj.get_editor_property('ExplicitAssets')])
    else:
        item.update(row_struct=obj.get_editor_property('row_struct').get_path_name(),
                    rows=json.loads(unreal.DataTableFunctionLibrary.export_data_table_to_json_string(obj)))
    report['assets'][family] = item
after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
assert before == after, 'Native read must not save packages'
report['native_read_preserved_hashes'] = True
(root / 'oracle.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
unreal.log('ONESTEP_NATIVE_ORACLE_COMPLETE')
