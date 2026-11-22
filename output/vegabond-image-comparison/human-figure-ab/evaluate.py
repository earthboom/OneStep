"""Blind, score and display the paired human-figure study."""
import json
import sys
from hashlib import sha256
from pathlib import Path
from random import SystemRandom

from PIL import Image, ImageDraw

D = Path(__file__).resolve().parent
ARMS = ("before", "after")
READERS = ("J", "K")
CASES = ("01", "02", "03", "04")


def read(name):
    return json.loads((D / name).read_text(encoding="utf-8-sig"))


def save(name, value):
    (D / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare():
    if (D / "key.json").exists():
        raise ValueError("Candidate identities have already been fixed")
    key = []
    candidates = {}
    for arm in ARMS:
        rows = read(f"{arm}/run.json")
        assert len(rows) == 8 and {(r["id"], r["repeat"]) for r in rows} == {(c, n) for c in CASES for n in (1, 2)}
        for r in rows:
            assert r["final"] in (r["initial"], r["repair"])
            for stage in ("initial", "final"):
                name = r[stage]
                candidates[arm, name] = r["id"]
                key.append(dict(arm=arm, case=r["id"], rep=r["repeat"], stage=stage, file=name))
    rng = SystemRandom()
    for reader in READERS:
        dest = D / reader
        dest.mkdir(exist_ok=True)
        ordered = rng.sample(list(candidates), len(candidates))
        labels = {}
        for i, (arm,name) in enumerate(ordered, 1):
            label = f"{i:02}"
            labels[arm,name] = label
            with Image.open(D / arm / name) as source:
                im = source.convert("RGB")
                im.info.clear()
                im.save(dest / f"{label}.png")
        for entry in key:
            entry[reader] = labels[entry["arm"],entry["file"]]
        save(f"{reader}/cases.json",{labels[c]:case for c,case in candidates.items()})
    save("key.json",key)
    gallery = ["# 인물 그림 익명 비교", "",
               "각 행은 같은 요청과 같은 반복에서 선택한 두 최종 그림이다. 좌우 순서는 행마다 섞었다. 어느 쪽이 자연스러운지, 또는 차이가 없는지 먼저 보고 손·발·얼굴에서 근거 한 곳을 짚어 볼 수 있다. 축소판 아래에 확대용 파일을 연결했다.", ""]
    lookup = {}
    for case in read("protocol.json")["cases"]:
        c = case["id"]
        gallery.extend([f"## {case['title']}", "", case["brief"], ""])
        for rep in (1,2):
            pair = [k for k in key if (k["case"],k["rep"],k["stage"])==(c,rep,"final")]
            rng.shuffle(pair)
            images = [(side,D/"J"/(k["J"]+".png")) for side,k in zip(("A","B"),pair)]
            f = f"blind-{c}-{rep}.jpg"
            panel(images,2,(480,375),D/f)
            gallery.extend([f"![익명 비교 {c}-{rep}]({f})", "",
                            " · ".join(f"[{side} 확대](J/{k['J']}.png)" for side,k in zip(("A","B"),pair)), ""])
            lookup[f] = {side:k["arm"] for side,k in zip(("A","B"),pair)}
    (D/"blind.md").write_text("\n".join(gallery),encoding="utf-8")
    save("gallery-key.json",lookup)


def panel(entries, cols, size, path):
    w,h = size
    page = Image.new("RGB",(cols*w, ((len(entries)+cols-1)//cols)*h),"#f3f1ee")
    draw = ImageDraw.Draw(page)
    for i,(label,f) in enumerate(entries):
        x,y = (i%cols)*w, (i//cols)*h
        with Image.open(f) as im:
            im.thumbnail((w-10,h-25), Image.Resampling.LANCZOS)
            page.paste(im,(x+(w-im.width)//2,y+23))
        draw.text((x+6,y+4),label,fill="#242321")
    page.save(path,quality=93)


def aggregate():
    key = read("key.json")
    scores = {}
    for reader in READERS:
        rows = read(f"{reader}/scores.json")
        scores[reader] = {r["label"]:r["marks"] for r in rows}
        assert len(rows)==len(scores[reader]) and set(scores[reader])=={k[reader] for k in key}
        assert all(len(r["marks"])==5 and set(r["marks"])<={0,1,2} and r["note"].strip() for r in rows)
    def counts(entries,readers=READERS):
        m=[scores[r][k[r]] for k in entries for r in readers]
        return dict(n=len(m),natural=sum(min(v[:4])==2 for v in m),full=sum(min(v)==2 for v in m),
                    points=[sum(v[i] for v in m) for i in range(5)])
    result={}
    for stage in ("initial","final"):
        result[stage]={}
        for arm in ARMS:
            selection=[k for k in key if (k["arm"],k["stage"])==(arm,stage)]
            result[stage][arm]=dict(overall=counts(selection),cases={c:counts([k for k in selection if k["case"]==c]) for c in CASES},
                                    readers={r:counts(selection,[r]) for r in READERS},
                                    both=sum(counts([k])["natural"]==2 for k in selection))
    result["repairs"]={arm:sum(bool(r["repair"]) for r in read(f"{arm}/run.json")) for arm in ARMS}
    save("metrics.json",result)
    hashes={f"{a}/{p.name}":sha256(p.read_bytes()).hexdigest() for a in ARMS for p in (D/a).glob("*.png")}
    assert len(hashes)==16+sum(result["repairs"].values()) and len(set(hashes.values()))==len(hashes)
    save("image-hashes.json",hashes)
    final=[k for k in key if k["stage"]=="final"]
    for c in CASES:
        rows=sorted((k for k in final if k["case"]==c),key=lambda k:(k["rep"],ARMS.index(k["arm"])))
        panel([(f"{k['arm']}   run {k['rep']}",D/k["arm"]/k["file"]) for k in rows],2,(600,480),D/f"case-{c}.jpg")
    rows=sorted((k for k in final if k["arm"]=="after" and k["rep"]==1),key=lambda k:k["case"])
    panel([(f"{k['case']}   {name}",D/k["arm"]/k["file"]) for k,name in zip(rows,("Stairs","Passing a cup","Listening","Tying a lace"))],2,(540,380),D/"people.jpg")


if __name__=="__main__":
    {"prepare":prepare,"aggregate":aggregate}[sys.argv[1]]()
