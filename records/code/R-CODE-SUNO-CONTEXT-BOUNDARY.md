---
id: R-CODE-SUNO-CONTEXT-BOUNDARY
title: Exclude chat and memory from a Suno integration
summary: The user rejected plugin context sharing. A standalone client with a checked fetch gate connected Suno while accepting only reviewed lyrics and style for future generation, without a chat or memory input.
kind: suggestion
scope: OneStep standalone Suno client; its unchanged source and explicitly reviewed input only
keywords: [Suno, MCP, privacy, memory, chat-history, exact-content, allowlist, egress, approved-payload, DPAPI]
status: resolved
checked_at: 2026-11-10
context:
  platform: Windows; Node.js 22.19.0; PowerShell 7
  sdk: '@modelcontextprotocol/client 2.4.0'
trigger: Connecting Suno when the user permits only lyrics and music instructions as creative content
symptom: Plugin disclosure allowed relevant chat and enabled memory context, which the user declined; no actual context leak was observed
cause_status: confirmed
prevention: Use the tested standalone client with an exact reviewed lyrics/style payload and verify its code hashes and gate tests after changes
prevention_status: verified
---

## Expected and observed

The user requested excluding existing chats and memory before directly connecting Suno. The ChatGPT plugin's disclosure allowed relevant context, and the user declined that flow. The request was then refined to a direct connection with a verified content boundary. This is a compatibility concern, not evidence that Suno received private context.

The dedicated client accepted fixed protocol/auth traffic and authenticated tools listing. It received no transcript, memory API, filesystem roots or model input. Live OAuth succeeded, 41 tools were listed and encrypted credential reuse succeeded. Actual `audio-create` accepts `lyrics` and `style` without another required field. No song-generation call or account/library tool was executed.

## Cause and resolution

Generic plugin context handling did not satisfy the requested exclusion. A tool-name allowlist alone would still permit private content inside a valid lyrics field. Hooks were not selected as the sole boundary because documented hook failures can let a call continue and support depends on orchestration.

The [dedicated client](../../prototypes/SunoRestricted/README.md) uses official SDK 2.4.0 with empty optional capabilities. Its fetch gate permits only fixed protocol traffic and one `audio-create` call exactly matching a reviewed file and SHA-256, with only lyrics/style strings. Modified allowed values, extra fields, other methods, query-based content, custom headers and redirects are blocked before fetch. Unknown server-initiated requests cannot extract local context because there is no context handler or model attached. Credentials are DPAPI-encrypted in ignored local storage. Native unrestricted Suno MCP was disabled; the cloud plugin remains unconnected.

During implementation, the SDK's automatic fixed `application_type: native` field was initially blocked. Installed SDK source established the cause; a failing test was added before permitting that exact value. Windows PowerShell 5 could not load its security module/assembly in this environment; a synthetic-token probe established that installed PowerShell 7 could complete DPAPI encryption and decryption. The client now requires PowerShell 7 rather than using plaintext storage. Repeated network authentication was not needed to diagnose that local failure.

## Recheck and prevention

[Nine final tests](../../prototypes/SunoRestricted/verification-tests.txt) passed. Controlled broken behavior first failed the checks. Demonstrations include a real local HTTP receiver that sees no blocked sentinel, rejection of private text substituted into an otherwise allowed lyrics field, an official-SDK simulated approved send, rejection of extra context protocols/headers/queries, fixed native OAuth metadata and a DPAPI round trip. [Verification evidence](../../prototypes/SunoRestricted/verification.json) pins the tested source hashes and live authenticated listing with zero content calls.

The verified safeguard applies to this client's path, not arbitrary shell execution, modified source, other apps or OS-wide traffic. The hash verifies integrity, not a human's identity or semantic privacy. The user must review the exact lyrics/style file; private information deliberately included in approved lyrics would be sent. OAuth identity/token and fixed protocol metadata are necessary exceptions to the creative-content limit. Real music generation and result polling were not performed as part of this check. Recheck the tests and live schema after changing SDK/source.

## Evidence

- [Source, contract and use](../../prototypes/SunoRestricted/README.md).
- [Tests](../../prototypes/SunoRestricted/guard.test.mjs), [final run](../../prototypes/SunoRestricted/verification-tests.txt), [live evidence and hashes](../../prototypes/SunoRestricted/verification.json).
- [Original authentication record](R-CODE-SUNO-MCP-AUTH.md).
- [OpenAI connected-app context disclosure](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt).
- [Official hook limitations](https://learn.chatgpt.com/docs/hooks).
- [Official MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk) and installed 2.4.0 source inspected during the task.
