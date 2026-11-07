---
id: "K-CODE-DATA-INVARIANTS"
title: "Represent valid data states explicitly and validate transitions"
summary: "Use types and encapsulated construction to distinguish valid states, absence and errors where the language supports it. Preserve runtime validation at external boundaries and check every mutation or transition that can invalidate the representation."
kind: "reference"
scope: "Data modeling and invariant design; OCaml and Rust examples require adaptation to the actual language, serialization and mutation paths"
keywords: ["invariant", "type", "state-machine", "enum", "validation", "encapsulation", "immutability", "불변식", "타입", "상태", "유효성검사", "캡슐화", "불변데이터"]
status: "active"
checked_at: "2026-11-07"
context: {"evidence_check": "Named original author papers or official text sections inspected; specific limits in Evidence", "application_status": "Source-based reference and proposed synthesis; no local implementation or runtime validation"}
---

# Represent valid data states explicitly and validate transitions

## Guidance

Source observations: Minsky replaces a connection-state record with state-specific payloads in his OCaml example [S1]. The Rust book uses enum variants and Option to distinguish alternatives and presence [S2], then shows private representation with a validated constructor [S3]. These are representational techniques, not proofs that all business rules hold.

Proposed method: list the states that actually belong to the domain, what data each requires, and permitted transitions. Avoid unrelated boolean flags and optional fields when they admit impossible combinations. Introduce a focused value type when it removes repeated interpretation or validation, not merely to wrap every primitive.

Keep construction, parsing, deserialization and mutation on the same invariant boundary. Decide how invalid external input is reported and where recovery belongs. Track units and identity where confusion is costly. Keep state transitions observable through the public contract so callers need not remember a hidden sequence of setters.

## Applicability and exceptions

Types cannot establish rules that were omitted, modeled incorrectly or bypassed through public mutation, reflection, unsafe code or an unchecked serializer. An unsigned type does not establish a business range. Deliberate intermediate states may be valid during a transaction or editor operation; model them rather than forbidding legitimate work. Choose exceptions, error results and panic/assert behavior under the actual language contract.

## Checks

Proposed checks: can invalid combinations be constructed through any supported entry point? Do transitions preserve required data and reject invalid input at the correct boundary? Review round-trip serialization, upgrades and mutation, not only the happy-path constructor. Verify claimed static guarantees with the actual compiler and runtime; no such exercise was run here.

## Evidence

- [S1] Yaron Minsky, [Effective ML Revisited](https://blog.janestreet.com/effective-ml-revisited/), 2011, Make illegal states unrepresentable; published examples read, linked lecture not watched.
- [S2] [The Rust Programming Language: Defining an Enum](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html), variant payloads / Option.
- [S3] [To panic! or Not to panic!](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html), Custom Types for Validation, including visibility and construction.
- Original author/official text checked 2026-11-07. Checks are a proposed synthesis, not a project compiler or serialization test.
