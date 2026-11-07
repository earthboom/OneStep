---
id: "K-CODE-CONFIGURATION-POLICY"
title: "Separate invariant constants, tunable policy, deployment config and secrets"
summary: "Classify embedded values by meaning, owner and change lifecycle before externalizing them. Use named constants for invariants, validated data/configuration for genuine variation, and appropriate secret handling for credentials."
kind: "reference"
scope: "Configuration and data design across applications and games; Twelve-Factor deployment advice and Unreal data workflows retain their own context"
keywords: ["hardcoding", "magic-number", "configuration", "constant", "data-driven", "secrets", "validation", "하드코딩", "매직넘버", "설정", "상수", "데이터주도", "비밀정보"]
status: "active"
checked_at: "2026-11-07"
context: {"evidence_check": "Named original author papers or official text sections inspected; specific limits in Evidence", "application_status": "Source-based reference and proposed synthesis; no local implementation or runtime validation"}
---

# Separate invariant constants, tunable policy, deployment config and secrets

## Guidance

Source observations: C++ Core Guidelines ES.45 favors meaningful symbolic constants over unexplained literals [S1]. Twelve-Factor distinguishes deploy-varying configuration from internal application structure [S2]. Epic documents externally authored tables/curves for gameplay tuning [S3]. OWASP treats secrets as an access and lifecycle concern, not merely a file-location choice [S4].

Proposed method: classify each value as a domain/protocol invariant, a product policy or tuning value, environment-specific configuration, a secret, or example/test data. Identify who changes it, how often, and whether changing it requires a build, content release, deployment or runtime reload. Use the simplest representation supporting that lifecycle.

For configurable values, define type, unit, valid range, required/default behavior, precedence and compatibility. Validate at the input boundary and make the effective nonsecret configuration inspectable. Treat reload as a state transition with consistency and failure behavior; avoid spreading reads of mutable global settings through business logic.

## Applicability and exceptions

A literal is not automatically a defect. Small obvious values, specification constants and explicit test vectors can be clearest in code. Externalizing every number adds schema, distribution and compatibility costs. Environment variables are not a universal game-content format or sufficient secret protection. A table changes values, not necessarily behavior or executable policy; keep authority and validation explicit.

## Checks

Proposed checks: can the intended owner change one policy without editing unrelated logic? Are invalid, missing and conflicting values handled deliberately? Can a release reproduce its effective settings without exposing credentials? Check content/configuration revisions and tests at the actual boundary; a constant-to-file rewrite alone does not prove maintainability.

## Evidence

- [S1] [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-magic), ES.45, Reason/Example/Enforcement; only this rule used here.
- [S2] [Twelve-Factor: Config](https://www.12factor.net/config), deploy variation and exclusion of internal application configuration.
- [S3] Epic, [Data Driven Gameplay Elements](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine), DataTables/CurveTables and authored data workflow; UE5.8 documentation at inspection.
- [S4] OWASP, [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), Introduction / General Secrets Management / Secret Lifecycle.
- Primary official text sections checked 2026-11-07. Proposed classification/checks were not applied to project code or secrets in this task.
