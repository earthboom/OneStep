---
id: K-CODE-UE-OFFICIAL-FEATURE-SOURCES
title: Compile an official Unreal Engine feature list from sources an agent can actually read
summary: Combine the marketing features page with the documentation section pages and the forum release announcement; www.unrealengine.com refuses plain fetches and some documentation pages return an empty shell, so use a rendered browser or the readable pages.
kind: reference
scope: Research that lists or classifies Epic's official Unreal Engine technologies or their release status
keywords: [Unreal Engine, official features, feature list, release notes, documentation index, unrealengine.com/features, dev.epicgames.com, forums.unrealengine.com, Experimental, Beta, Production-Ready, WebFetch, HTTP 403, JavaScript-rendered page, 언리얼 공식 기술]
status: active
checked_at: "2026-11-20"
context:
  engine: "Unreal Engine 5.8 stable, 5.9 Preview documentation"
---

## Guidance

Use two complementary sources, then confirm status separately:

1. **Features page** (`https://www.unrealengine.com/features`): Epic's product-level grouping (pipeline integration, world building, characters and animation, rendering, simulation and so on). It is marketing wording, not a module list.
2. **Documentation section pages** (`https://dev.epicgames.com/documentation/unreal-engine` and its top-level sections such as gameplay systems, rendering and graphics, networking, AI, animation, audio, testing): system-level names and the child topics each section links to.
3. **Release status**: take the stable version and maturity labels (Experimental, Beta, Production-Ready) from the release notes or the official forum release announcement, not from search-result summaries. For a source-built engine, the plugin's folder under `Engine/Plugins/Experimental` is a further check.

Access observed with an agent's tools:

- `www.unrealengine.com` pages (features, news, product pages) returned HTTP 403 to a plain fetch tool but loaded in a rendered browser pane. In the browser, the features page's category content was extractable from the page text by category heading.
- Some `dev.epicgames.com` pages returned a 29-character "Table of Contents" shell to a plain fetch (the 5.8 release notes, the features documentation page), while the documentation landing page, the section pages and the 5.9 release notes returned full text.
- The forum release announcement (`forums.unrealengine.com`) returned full text.
- A documentation URL naming an older version displayed the latest documentation (titled 5.9). Read the page title for the version instead of trusting the URL.

## Applicability and exceptions

Access behavior depends on the site, the client and the date; recheck before relying on it. The features page omits many engine systems and plugins, and the documentation index omits marketing groupings, so neither alone is a complete list. Preview documentation can name features absent from the stable release.

## Checks

- Each listed item has an Epic page or announcement naming it.
- The version in the page title matches the version you claim.
- Maturity labels come from release notes, the forum announcement or the engine plugin folder.
- If a page returns 403 or an empty shell, retry in a rendered browser before reporting it unreadable.

## Evidence

Two research sessions on 2026-11-20. One used a browser pane for the features page and documentation sections; the other used plain fetches through subagents and recorded HTTP 403 for three `www.unrealengine.com` URLs, 29-character responses for the 5.8 release notes and the features documentation page, and full text for eight documentation section pages, the 5.9 release notes and the forum 5.8 announcement. In the fetch session, two maturity claims from search summaries (Iris, MCP) were not found in the original announcement text.
