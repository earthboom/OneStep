# Visual Direction and Review Examples

Use the rows that serve the request. Treat references as selective instructions rather than mandatory ingredients.

| Requested treatment | Direction to specify | Verify in the image |
| --- | --- | --- |
| Photograph or photorealism | Viewpoint, framing, light direction and quality, materials, exposure cues, and degree of retouching. Use focal-length language when it helps convey angle of view or subject scale. | Subject geometry, material texture, credible lighting and contact shadows, and the requested framing. |
| Comic or graphic illustration | Outline weight, silhouette, shape language, flat or modeled shading, palette, visual focus, and panel layout when requested. | Readability at delivery size and consistency of line, form, and shading. In a sequence, compare repeated costume, props, and distinctive shapes. |
| Surreal or fantastical scene | Name the rendering medium and the impossible relationship. Specify what remains physically grounded and which visual cues make the exception legible. | The intended exception reads clearly and other cues establish the intended space. A fantastical scene can use photographic, painted, or graphic treatment. |

## Direct and test the reading

| When the request depends on… | Decide before generation | Inspect in the delivered image |
| --- | --- | --- |
| How color is applied | Bind color to its role (object, light, ink, or accent) and its location. For colored light, preserve the object's material through lit and shadowed planes. For a painting or print, specify a relevant mark, such as opaque gouache shapes, transparent washes, or broken ink on paper. | At viewing size, where does the eye land? Does the accent compete with the background? Inspect a lit area, a shadow, and a boundary when material identity matters. Sample flat interior pixels only for a requested numeric swatch, under the agreed color space and tolerance. |
| Different readings or treatments of one theme | Keep the premise, mandatory motifs, and requested medium fixed. Choose what the viewer witnesses in each version. For example, show someone setting a second place, or show the place left ready by the door after they leave. Change the viewpoint, gesture, or decisive moment according to the brief. | Describe each version without its caption. Identify what implies the shared theme and how each conveys it. An empty chair alone can also suggest abandonment. In a single-image request, choose one direction. |
| Why this moment makes sense | Identify who can do what, to whom or to what, and the visible consequence. Choose a cue that distinguishes the intended moment from the moments before and after it. For a tipped teapot, follow the grip, spout, stream and receiving cup. | Trace the action through the frame. A cup and a kettle can both be present while the stream misses the cup. For implied narrative, assess what the evidence supports and allow ambiguity the user invited. |
| What feels true in this world | Identify any deliberate exception and the ordinary relationships the scene depends on. Choose the relevant support, scale, occlusion, lighting, material, or setting cues. Respect stylized spatial rules and the user's fictional world. | Inspect the region outside the main subject as well. On the Moon, a hovering dome can be intentional while a second Moon-like body in the sky suggests a different setting. In a graphic print, overlapping silhouettes may establish contact without modeled shadows. |

## Material color and first glance

Choose where the viewer can recognize the larger object's own color under the specified light. A small patch of low-chroma lit fabric beside a tinted fold can establish white cotton. On colored glaze or dark leather, a patch of the body color beside a restrained reflection can do the same job. Keep enough surrounding illumination and texture to explain the material. Brightening a whole cuff or sharpening every seam can turn it into the focal point.

Place the requested small accent against an adjacent plane where it separates by value, hue, or edge clarity. Keep its specified scale. Subdue the strongest competing edge, reflection, or patch of detail if needed. For instance, a crisp orange paper edge against a quiet violet-gray fold can carry the focus while a softer pearl-gray seam elsewhere identifies the cloth.

View the whole image at a small, consistent size before zooming in. Name the first distinct object you notice, including a tie if two compete. Then inspect the larger object's lit and shaded surfaces at delivery size and name its material and apparent color. After a repair, repeat both checks on the same candidate. If the smaller accent loses focus, adjust its immediate surroundings or the competing highlight and retain the cue that established material identity.

When a broad silhouette keeps winning, look across its *outer* edge as well. If the background can change, try bringing the adjacent surface closer in value while preserving the material color and the accent's local contrast. Keep the setting legible. For a disputed first glance, a fresh viewer can name the first object before seeing the brief. Use that response to select a delivery and record a split reading when it persists.

## Examples

- **Count and binding.** Ask for two visibly separate red lights on the entry frame of a dome, one on each jamb, and a rover at frame right. If the request prohibits text, inspect the rover and background as well as the dome. Keep task-specific choices such as jamb placement flexible when they change the requested design.
- **Direct overhead product view.** For a strict flat lay of lidded boxes, put the camera straight above the tabletop with its optical axis perpendicular to the surface. Ask for square and circular lid planes, with the thin lid rim and edge bevel allowed. Inspect every object for any broad front face or continuous sidewall band that signals an oblique view. If the view fails, change the camera angle while retaining the count, materials, arrangement, and background.
- **One recurring character.** For two requested images of the same lone robot, send two standalone scene prompts using the same identity reference. Give each frame an explicit count of one robot and its own setting and action. Check the entire frame for additional figures, then compare the character's head, torso, antenna, and other identifying features across both images. If an extra figure appears, target that figure and its visible shadow during repair, then verify the intended robot, action, and framing again.
- **Role separation.** Use image 1 for the positions of the fountain, arch and diagonal path. Use image 2 for its ink palette and rough print texture. Inspect both the spatial relationships and whether the style reference introduced unintended subjects.
- **Edit preservation.** To recolor a jacket, identify the jacket by its current color and shape. Say which parts of the person, pose, framing, illumination and background must stay the same. Inspect beside the source at comparable scale. If visual preservation is insufficient for a pixel-exact request, use a supported region-limited workflow and check the protected pixels.
- **Exact wording.** Preserve case, spacing and punctuation in the supplied string. When a poster permits separate typography, render that text over a prepared background and check line breaks, font coverage, legibility and clipping in the exported file. When lettering must be integrated with perspective or texture, inspect it in place at full size.
- **Technical output.** Check the decoded file format and dimensions. For transparent assets, inspect alpha in the intended background and around subject edges. An alpha channel containing only opaque values does not make the background transparent.

## Match the repair to the failure

Inspect the first candidate at its intended size and, when the output has been laid out or exported, compare it with the source. Change the step that introduced the defect.

| Observed failure | Repair and recheck |
| --- | --- |
| Wrong camera, placement, or contact | Give the generator a simple sketch, silhouette or layout guide that makes the missing geometry visible. Assign a separate identity or style reference its own role. Inspect the deciding plane, overlap, gap, or point of contact. |
| Identity drift, duplicate subject or wrong attribute | Start from the accepted image. Limit the edit to the changed feature or extraneous subject and its visible traces using the supported controls. Scan the whole frame for subject count and compare the preserved features or areas with the source. |
| Unclear action or emotion | Read the image before reading the prompt or caption. Repair the visible cause, such as the gaze, hand placement or body angle, then reread it at the intended size. |
| Exact text, spacing, dimensions, or alpha residue | When the underlying art is usable, correct the target in layout, masking or export using the appropriate tool. Inspect the exported words, placement or decoded dimensions and transparency. |
