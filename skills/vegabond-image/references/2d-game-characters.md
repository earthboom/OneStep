# 2D game character art

## Choose the view the player will see

| Requested asset | Base the generation on | Accept it when |
| --- | --- | --- |
| Dialogue portrait or key illustration | Character design, emotion or story beat, crop and focal point. In dialogue UI, use the actual slot and text overlay when available. | The intended attitude reads in the final crop. The eye line, face and identifying features survive framing and UI overlap. |
| In-game character image | Gameplay camera, facing, on-screen height, nearby scenery and the established rendering medium. Start with one neutral or representative action pose. | At normal play size the character, facing and action are recognizable against representative light and dark scenery. The full pose fits its intended bounds. |
| Animation frames or a sprite sheet | An accepted gameplay pose plus a plan for the action, views, origin, timing and export layout. | The imported or sliced frames play in order at the intended speed. Identity, transitions, ground contact and canvas alignment hold up during playback. |

For a single illustration, finish at its own acceptance check. If several deliverables depict the same character, choose a design reference with visible identifying features. Record a few landmarks that survive a scale change, such as a notched hood, an amber scarf and a lantern in the character’s left hand. State which features may simplify at gameplay size. Assign other references a specific job such as camera, pose or palette. Only request another view if it resolves something the deliverable actually shows.

## Generate a portrait and a playable pose

- **Illustration.** Give the character an acting beat a viewer can read. Specify the relationship among gaze, gesture and the main prop. Generate or edit from the design reference. Inspect the face and costume in the final crop. For expression variants, edit the accepted neutral portrait and compare eye shape, apparent age and clothing as well as the requested expression.
- **Gameplay.** Use the design reference to draw the character from the game camera. Choose a clear outer contour and large light/dark shapes. View at the intended play size on a representative background before adding small trim. For pixel art, work on the intended logical grid, clean stray pixels and check the palette across frames. For painted or inked sprites, preserve line weight and intentional translucent edges at target size.
- **Example prompts for the same lighthouse keeper.** For a dialogue portrait, “Use the keeper design for identity. Chest up in the dialogue slot, listening toward the sea. Let the lantern light catch one cheek. Keep the notch in the hood visible above the text panel.” For a gameplay pose, “Use the keeper design and the side-view gameplay reference. Full body facing right, approximately 40 pixels tall in play. Separate the amber scarf and left-hand lantern into clear shapes. Transparent background, room for the lantern swing.” The example dimensions belong to this brief.

## Plan motion before generating more frames

1. Name the action and the moments the player must distinguish. For a walk, mark left contact, passing, right contact and the opposite passing pose. For a jump, mark push-off, apex and landing. Use the project's state timing or cues when they exist. Decide which poses hold and whether the action loops. Match a locomotion cycle to the character's travel speed.
2. Fix camera, character scale, facing, canvas and origin across the action. Decide whether the engine moves the character or displacement lives in the frames. Keep the lantern on the anatomical left when the character turns. Mirroring works only if the design, light and gameplay tolerate it.
3. With a still-image generator, use the accepted pose and any available pose sketches as inputs. Generate the distinctive poses first, then edit or fill only the transitions the action needs. An artist's pose sketch can replace a failed automatic skeleton on a stylized body. For multi-view characters with many reusable motions, an existing rig or pose sequence can supply consistent views if the project has one. A generated strip or video can supply candidates. Inspect and register the selected frames before packing them.
4. Play the action at target speed and size, then step through neighboring poses or overlay them. Watch the last-to-first transition for loops, silhouette changes, limb or prop swaps, and costume or palette flicker. A fixed pivot keeps the character registered while the torso rises and falls. Evaluate a planted foot against the moving **world** during locomotion. An in-place cycle played over a static floor has a different contact trajectory. Keep intentional squash, airborne motion and holds.

## Package and repair

If early pixelation erases the cues needed to generate the next pose, try posing at a larger working size and applying the same downsampling and palette to all frames. Compare against a hand-cleaned key pose on the target grid. Keep the route that preserves the character and action there.

Use equal canvases with a common origin for uniform grid slicing. If frames are tightly packed or trimmed, retain the source canvas size, trim offset and frame rectangle so the importer can reconstruct each pose. Preserve frame order, duration, loop mode and action/direction names in the form the consumer uses. Inspect real alpha over contrasting colors, outer-cell clipping, and atlas bleed under the intended texture filter. For hard-edged pixel art, preview with nearest-neighbor at the intended scale. For smooth art, use the project's filter. Play exported files after slicing, or disclose precisely which preview was available.

| Observed failure | Smallest useful repair |
| --- | --- |
| The portrait and sprite look like different people | Compare identifying landmarks side by side at their display sizes. Restore the missing contour or color block in the gameplay pose, then reuse that corrected pose. |
| Well-drawn frames look motionless or the step slides | Check contact versus passing silhouettes and foot travel against game speed. Correct the key pose or its duration before adding in-betweens. |
| The whole body jitters or a lantern disappears at a cell boundary | Overlay the original canvases at the intended pivot, then inspect the sliced result. Repair alignment, padding or trim metadata if the originals agree. |
| The action reads but scarf color or pixel clusters shimmer | Compare the offending frames with the accepted pose. Repair the local area or apply a common palette in the finishing pass, then replay the loop. |
