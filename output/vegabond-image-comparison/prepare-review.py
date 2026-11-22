"""Generate labeled review sheets and hold the workflow key separately."""

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ARMS = ('baseline-1', 'baseline-2', 'vegabond-1', 'vegabond-2')
CHECKS = {
    '01': ('exact 16:9 file', 'one left-side domed base', 'one right-side rover', 'exactly two separate red lights on entry', 'low viewpoint', 'light from frame left', 'photographic rendering', 'no writing'),
    '02': ('exact 16:9 file', 'one left-side domed base', 'one right-side rover', 'exactly two separate red lights on entry', 'bold outer contours and cel shading', 'no writing'),
    '03': ('exact 16:9 file', 'one left-side domed base', 'one ground-contact rover on the right', 'exactly two separate red lights on entry', 'dome visibly floats with an air gap and a ground shadow', 'oil painting treatment', 'no writing'),
    '04': ('small garden', 'visible signs of recent rain', 'quiet mood'),
    '05': ('exactly two blue square boxes', 'exactly one orange cylindrical box', 'blue boxes left and orange box right', 'nonoverlapping objects, no additional objects', 'white background', 'direct overhead view, with no substantial oblique faces'),
    '06': ('portrait frame', 'top line exactly 달 기지에 오신 것을 환영합니다!', 'bottom line exactly 출입 안내 09:30', 'top and bottom positions, one line each', 'no extra text or text-like glyphs'),
    '07': ('PNG at exactly 512×512', 'transparent outer background and visible subject', 'one purple ink bottle', 'oblique 3/4 view', 'no separate shadow or writing'),
    '08': ('lower-left fountain with water', 'upper-right arch', 'diagonal path connects the two'),
    '09': ('two standalone images', 'first: greenhouse and holds a pot', 'second: stop and waits empty-handed', 'orange spherical head in both', 'teal box torso in both', 'exactly one black antenna on the recurring robot in each', 'recurring reference robot identity clear in both without an ambiguous extra robot'),
    '10': ('lower-left fountain', 'upper-right arch', 'continuous diagonal path', 'navy and ochre visibly dominate', 'rough relief print texture', 'no prominent leaf subject from style reference'),
    '11': ('deep navy background wall', 'mug and lemon shape, color, position preserved', 'table, lighting and framing preserved'),
    '12': ('jacket changed to teal', 'face, hair and pose preserved', 'composition and background preserved'),
}
REFERENCES = {
    '08': ('layout.png',), '09': ('robot.png',),
    '10': ('layout.png', 'print-style.png'),
    '11': ('still-life.png',), '12': ('portrait.png',),
}


def describe(path):
    with Image.open(path) as im:
        desc = f'{im.format} {im.width}x{im.height}'
        if 'A' not in im.getbands():
            return desc
        alpha = im.getchannel('A')
        edge_rects = [(0, 0, im.width, 1), (0, im.height - 1, im.width, im.height),
                      (0, 0, 1, im.height), (im.width - 1, 0, im.width, im.height)]
        peak = max(alpha.crop(rect).getextrema()[1] for rect in edge_rects)
        return f'{desc} alpha range {alpha.getextrema()}, edge max {peak}'


def paint_sheet(cards, root, destination):
    width, height = 800, 515
    rows = (len(cards) + 1) // 2
    sheet = Image.new('RGB', (width * 2, height * rows), '#ededed')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=20)
    for index, (label, files) in enumerate(cards):
        x, y = index % 2 * width, index // 2 * height
        draw.text((x + 12, y + 6), label, fill='#111111', font=font)
        slot_width = width // len(files)
        for j, file in enumerate(files):
            with Image.open(root / file) as im:
                tile = ImageOps.contain(im.convert('RGBA'), (slot_width - 12, height - 58))
                tile_x = x + slot_width * j + (slot_width - tile.width) // 2
                sheet.paste(tile, (tile_x, y + 30), tile)
                draw.text((x + slot_width * j + 8, y + height - 25), describe(root / file), fill='#111111', font=font)
    sheet.save(destination, quality=93, optimize=True)


def make_review(root, review, key_path):
    review.mkdir(parents=True, exist_ok=True)
    rng = random.Random(119064)
    mapping = {}
    for case, checks in CHECKS.items():
        ids = ('09a', '09b') if case == '09' else (case,)
        available = set()
        chosen = {}
        for arm in ARMS:
            first = tuple(f'{arm}/{item}-initial.png' for item in ids)
            for file in first:
                if not (root / file).is_file():
                    raise FileNotFoundError(root / file)
            final = tuple(f'{arm}/{item}-final.png' if (root / f'{arm}/{item}-final.png').is_file()
                          else first[i] for i, item in enumerate(ids))
            chosen[arm] = {'first': first, 'final': final}
            available.update((first, final))
        candidates = sorted(available)
        rng.shuffle(candidates)
        opaque = {files: f'{case}-{chr(65 + i)}' for i, files in enumerate(candidates)}
        mapping[case] = {arm: {stage: opaque[files] for stage, files in stages.items()}
                         for arm, stages in chosen.items()}
        cards = [(opaque[files], files) for files in candidates]
        for i, file in enumerate(REFERENCES.get(case, ()), 1):
            cards.append((f'REFERENCE {i}', (f'fixtures/{file}',)))
        paint_sheet(cards, root, review / f'{case}.jpg')
        case_manifest = {
            'case': case, 'checks': checks,
            'candidates': {opaque[files]: [describe(root / file) for file in files] for files in candidates},
        }
        (review / f'{case}.json').write_text(json.dumps(case_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    key_path.write_text(json.dumps(mapping, indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--key', type=Path, required=True)
    args = parser.parse_args()
    make_review(Path(__file__).parent, args.review, args.key)
