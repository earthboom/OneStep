# Feedback on direct image briefs with a missing production specification

- Date: 2026-11-25
- OneStep version used: working tree based on a9fb9f8, before and after the image entry revision
- Relevant skills: vegabond-image, vegabond-scout, vegabond-knowledge, vegabond-research
- Kind: problem
- Status: verifying
- Task context: read-only synthetic stationery order brief, with the supplier sheet available or withheld

## Expected and observed

A direct image request should reach the same scoped investigation as Scout when a missing supplier tolerance affects production. Before revision the direct performer left the dimension open correctly, but its trace documented only the image entry, its reference and project files. The Scout performer documented a research step.

## Evidence and suspected cause

The image entry introduced use within create or revise but gave no direct-entry handoff for a missing specification. The trials establish a difference in reported procedure. They did not show an invented dimension or defective physical product.

## Review and verification

The revised entry connects the existing brief, scoped knowledge and research when needed. Fresh direct and Scout trials both retained the design requirements, used the approved specification when present, and investigated the missing sheet without inventing a dimension. AI checks passed; maintainer review pending. [Implementation evidence](../docs/designs/skill-distribution-and-knowledge-routing.md)
