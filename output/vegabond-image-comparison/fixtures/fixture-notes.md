# Shared image fixtures

Both benchmark paths use these same PNG files for cases 08–12. The four images from the Codex built-in image tool were copied from the first generation for each prompt. All five PNGs were visually inspected, decoded with `System.Drawing.Image`, and hashed with SHA-256.

| File | Case | Source | Dimensions | Visual check |
| --- | --- | --- | --- | --- |
| `layout.png` | 08, 10 | Deterministic PowerShell/System.Drawing sketch | 1024 × 768 | Blue water and jets in the lower-left fountain, a stone arch at upper right, and a continuous paved diagonal between them. |
| `robot.png` | 09 | Codex built-in image tool | 1254 × 1254 | Full-body figure with a spherical orange head, a rectangular teal torso, exactly one black antenna, and a plain light studio backdrop. |
| `print-style.png` | 10 | Codex built-in image tool | 1254 × 1254 | Navy and yellow ochre relief print with dry ink, rough gouges, and oak and maple leaves. |
| `still-life.png` | 11 | Codex built-in image tool | 1536 × 1024 | Off-white mug and yellow lemon on a brown wood tabletop, with a clearly delineated beige wall and soft indirect light. |
| `portrait.png` | 12 | Codex built-in image tool | 1086 × 1448 | Original fictional adult in a warm orange jacket, angled naturally in front of a gray background. Jacket, hair, face, and background are separately visible. |

## SHA-256

```text
1bed60a691aafc72099d26fe440496d5b55cb3e336863d02de673b14f17c3787  layout.png
b4955c91de89a44def3bafb162410f4b4fcc2b2301c965832e3cb46ff064624d  portrait.png
7ea60eb21423bc7fd2dc97cf11c0a93b020798a4f71f3505a628c3ae6e0615b8  print-style.png
249e10e78ec318f1f9ede07018088c0be7b835590481260f7511111618f58218  robot.png
11b7032b749a503f8834acb444b073ee2541aa019a7129e849be9614f35703c9  still-life.png
```

## Drawing specification and generation prompts

### layout.png

Draw an oblique layout sketch on an off-white canvas. Place an oval fountain with blue water and visible arcs of falling water at lower left. Place a simple stone arch with an open passage at upper right. Link the two with a paved path that narrows toward the arch. Use clean charcoal contours and leave the rest of the canvas empty.

### robot.png

Create a single square full-body character reference image, stylized studio 3D rendering of a fictional friendly compact retro robot, standing in a relaxed upright three-quarter view. The head is one unmistakably spherical vivid tangerine-orange metal ball with two small dark eyes, with exactly one thin short black antenna projecting from the top and a small black round tip. No other protrusions on the head. The torso is clearly one box-shaped rectangular teal metal chassis with crisp edges and softened corners; its blue-green teal color contrasts with the orange head. Simple segmented muted dark-gray arms and legs with small hands and feet. Both hands empty and visible, entire silhouette in frame with generous margin, near-white plain seamless studio backdrop with only a soft ground contact shadow. One robot, no other objects, no writing, no watermark.

### print-style.png

Create a square monochrome two-ink woodcut print for use strictly as a style swatch. A close cluster of large overlapping oak and maple leaf silhouettes and carved veins fills the paper, with cropped foliage at the edges. Use exactly two apparent colors edge to edge: very dark desaturated navy ink and warm yellow ochre paper/ink. Both colors are clearly visible, no visible white. Visibly rough hand-carved edges, abundant dry ink flecks, broken hand-carved gouge lines, mottled grain and irregular pressure, aligned flattened shapes, high contrast. Treat this as a true rough relief print on fibrous paper, with no gradients, smooth vector edges, shadows, landscape, fountain, architecture, text, signature, frame or watermark.

### still-life.png

Create a single landscape editorial still-life photograph. One matte off-white ceramic mug with a small right-facing loop handle is slightly left of center, and one whole bright yellow lemon with visible peel is clearly separated just to the right of the mug. Both sit on a matte medium brown natural wood table. Show the tabletop and its straight back edge spanning the width near the lower third, with a plain smooth pale warm beige wall filling the background above the tabletop. Frame front-on at a slightly elevated natural angle so the rim of the mug is visible. Use soft indirect daylight from the upper left and delicate short shadows across the table. Clear stable outlines around the objects, medium framing with breathing room, authentic surface detail. Only one mug and one lemon, no labels, text, patterned wall, or other objects.

### portrait.png

Create a single vertical editorial portrait photograph of an original fictional adult woman with a distinctive face, dark brown shoulder-length wavy hair with a neat side part, and a natural composed expression. Chest-up, turned a little to her right, her face looking slightly past the camera back toward the viewer. She wears a plainly identifiable bright warm orange workwear jacket with a spread collar, matte twill texture, visible seams, and a plain ivory tee underneath. Jacket and hair are clearly separated at their outlines. Soft indirect window light, visible natural skin texture, restrained documentary realism. Simple pale gray studio wall behind her, evenly lit with slight tonal variation and no other objects. Keep the face and shoulders in frame, no jewelry, text, logos, or watermark.
