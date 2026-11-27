# Draw 2D effects in motion

## Decide what the player can infer

Describe one event in player terms. Who caused it, where, in which direction, and what changed? For a warning, establish when the player can still react and the footprint that matters. For ambient motion, establish how much attention it can take away from play. Borrow timing, camera, palette, draw order and event names from the target game when supplied. A standalone effect needs an on-screen size and a representative background even when no character art is requested.

Choose the form that preserves the important information. A drawn flipbook gives control over a distinctive silhouette at contact. A few reusable particles suit scattered grit with varied lifetimes. A hybrid can use a drawn core with optional particles around it. Separate layers when they have different anchors, lifetimes or suppression rules. One baked sequence is sufficient when those properties always coincide.

## Draw the changes between keys

| Effect | Key drawings to try | Inspect at normal speed |
| --- | --- | --- |
| Landing dust or splash | Mark the surface and incoming direction. Draw compression at the source, outward lobes or a crown, openings between masses, then detached fragments. A falling droplet can land while the main crown is already collapsing. | Does the material seem displaced from the contact? Does the widening footprint stay on the surface after the actor leaves? |
| Spark, glint or impact | Establish a compact origin and a directional silhouette at the strongest beat. Let a few streaks separate and shorten, with a clear end. | Does the result read on the first pass? Do bright pixels obscure the actor or a nearby warning? |
| Charge, aura or continuous flame | Separate entry, sustained cycle and exit when the state has them. Track one tongue, gap or pulse through its birth, travel and disappearance; stagger another so the entire mass does not reset together. | Watch the wrap repeatedly. Can the effect stop cleanly at a different point in the loop? Can the player tell when the state ended? |

Draw a few rough silhouettes first and play them on the planned clock. Timing is how long the drawing holds; spacing is how far its landmarks move or spread between drawings. Decide which beat needs a hold and which needs a quick change. Keep scale, camera and light consistent. Give curls, sparks and negative spaces an identifiable path. When a shape splits, a hand passes behind a prop, or the direction reverses, draw the intermediate pose that explains it before asking for interpolated frames. Keep purposeful shape changes and avoid uniform rescaling that makes material look inflated.

For image generation, give the character design, accepted key and pose/path sketch distinct roles. Describe the change from the last accepted key and the destination key. If one cell drifts, repair it against both neighbors. Inspect each generated strip for count, duplicates, margins and stray marks before slicing. Carry one scale and palette through the strip. Preserve intended height changes and airborne gaps when registering frames.

## Put the actor and the effect on one clock

Write the actor beat, event, effect beat and attachment beside each other. Record durations in an explicit unit. For the dock example below, times are illustrative, measured from clip start at normal speed. The contact is known in this authored preview; in a game with variable landing height, start the effect from the confirmed landing.

| Time | Character | Effect and space |
| --- | --- | --- |
| 0–120 ms | Descending, soles above the deck | No dust |
| 120–180 ms | First grounded, compressed pose | Emit dust once at the world contact point |
| 180–240 ms | Continue holding the compressed pose | Dust spreads from the same point |
| 240–300 ms | Recover upright | Spreading dust continues |
| 300–420 ms | Remain upright | Fragments dissipate; clear at 420 ms |

For a hand glow, follow a hand marker (a per-frame point or a socket). For an object released from the hand, sample that position at release and let the game move the object thereafter. For a one-shot on the floor, retain the contact position while the actor and camera move. Specify whether the effect draws behind or in front of the actor. Two layers can place the rear of a splash behind the legs and the near droplets in front. An action can cue a swing in the air; a result that depends on collision needs the actual result event. Decide what expires, follows or finishes if the state is canceled or triggered again.

## Inspect the export in play

- Preserve separate sheets when needed, cell rectangles or grid, common origin in stated coordinates, frame order and duration, loop or clear behavior, blend mode, draw order and event anchor in the consumer's preferred format. Record whether pixel values expect straight or premultiplied alpha. Preview using the intended material. Additive light may lose its shape on a bright surface; an opaque core or restrained alpha-blended layer can carry the cue there.
- Slice the **exported** sheets and play them together on contrasting representative scenery at target size and speed. Read the event first without labels. Then isolate actor, effect and composite, scrub the frames immediately before and after contact, and check the tail after the actor moves. Test a missed or canceled trigger when relevant. For loops check the seam; for one-shots check the empty end and a second trigger. Recheck effect priority during overlap when several instances can coexist.
- If the origin jumps, overlay the pivots and restore trim offsets. If a rim appears, inspect alpha convention, edge colors and filtering separately; if colors leak from another cell, inspect atlas padding and extrusion under the shipping filter. If the sequence feels sluggish, change the critical hold or spacing and replay before drawing additional cells. Distinguish a sliced preview from target-engine import, performance, and human readability tests.

## Draw a prop, a burst or an animated particle

| Requested sprite | Establish the keys | Review and repair |
| --- | --- | --- |
| Hinged chest, door or hatch | Draw closed and open at the same camera. Mark the footprint, hinge endpoints and moving lip. Design the newly revealed underside and cavity. Place an intermediate key where the moving edge clears the fixed rim. Reuse the accepted base when generating or editing each lid pose. | Overlay the two hinge marks and one fixed base corner after slicing. If the lid looks rubbery, redraw its projected depth and fittings at the middle key. Hold the final state until the game changes it. Give a slam its own closing timing when requested. |
| Burst or expanding ring | Mark its origin and intended footprint. Block a compact first shape, an outward displacement and a broken tail in silhouette. Follow a few lobes or streaks through the sequence. Set different peak times for the bright core and lingering smoke where the material calls for it. | Play the silhouette at game size. If it inflates evenly, change the leading edge, spacing or openings before polishing color. Inspect on light and dark scenery, clear the last fragment, and restart from the first cel. |
| Drifting dust, pollen or embers | For a standalone clip, draw several staggered paths on a common canvas. For an emitter, draw the local evolution of one particle around its pivot and specify birth times, travel, lifetime and variation separately. If both are needed, identify the reusable strip and the composed clip. | Freeze travel to inspect the local strip, then add wind and stagger births. Look for double travel, synchronized decay and visible rectangular edges. A one-shot ages within its chosen variant. Random phase suits a seamless cycle. Stop emission and check when the last live particle disappears. |

Record cell size, origin, order, exposures or age intervals, and the end behavior with the delivered sheet. Keep art direction in the brief: pixel art may break a silhouette by removing a cluster, while painted dust may soften its edge. Re-slice the export and compare the first, peak and ending states at the requested size. The full OneStep checkout has worked exposure sheets for all three forms in `docs/research/2026-11-24-2d-props-bursts-and-particles.md`.
