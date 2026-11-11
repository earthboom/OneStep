---
id: R-CODE-SUNO-MCP-AUTH
title: Verify Suno MCP authentication after server registration
summary: Initial Suno account linking rejected AI-app access. After user-reported beta approval, a dedicated restricted client completed OAuth, authenticated tools listing and credential reuse; actual song generation remains untested.
kind: error
scope: Suno MCP beta setup in Codex CLI on Windows; observed integration only
keywords: [Suno, MCP, OAuth, invalid_scope, authentication, music-generation, connector]
status: resolved
checked_at: 2026-11-10
context:
  client: codex-cli 0.163.0
  platform: Windows
trigger: Registering the official Suno HTTP MCP server and starting its first OAuth login
symptom: After sign-in and explicit permission approval, account linking displayed Account Linking Error and said the account cannot yet connect AI apps to Suno
cause_status: suspected
prevention: Check provider beta eligibility, consent, OAuth completion, authenticated tools and actual generation separately
prevention_status: proposed
---

## Expected and observed

The user requested connecting Suno and checking whether the assistant could create songs directly. Plugin discovery returned no Suno results, but Suno's official documentation provided an MCP endpoint and account-authorization instructions. An empty plugin search therefore did not settle direct-integration availability.

`codex mcp add suno --url https://api.suno.com/mcp` reported `Added global MCP server 'suno'`. The first OAuth attempt reported `OAuth provider rejected discovered scopes. Retrying without scopes…`; its browser callback showed `invalid_scope`. The automatic retry opened Suno's sign-in page. At the evidence check, no account was signed in and the CLI was still waiting.

`codex mcp get suno --json` independently confirmed an enabled Streamable HTTP configuration pointing at the official endpoint. Account authorization, authenticated tool discovery, credit checks and audio generation remained unverified. The CLI operation's displayed local time differed from the user-facing client date; this record uses the supplied Asia/Seoul date.

On resumption, the original CLI process returned `timed out waiting for OAuth callback` / `deadline has elapsed`. A fresh `codex mcp login suno` again retried after scope rejection and reached the account-link consent page with a signed-in account. This confirmed website sign-in, not connector authorization. Automatic action review rejected the Connect action because explicit consent to the entire requested permission bundle had not been established. The user was shown the concrete scope and asked for approval; no alternative authorization mechanism was used to bypass that decision.

The user then explicitly approved the listed permission bundle. The Connect attempt was followed by the heading `Account Linking Error` and the visible message `계정에서 아직 AI 앱을 Suno에 연결할 수 없습니다.` (the account cannot yet connect AI apps to Suno). The click tool reported a detached node during the page change; a fresh accessibility observation established the actual provider-side error. A later CLI configuration check still showed Suno enabled with `auth_status: unknown`. The waiting login process was cancelled after the provider refusal. No account/credit tool or song-generation action was run.

The user subsequently explicitly requested a separate ChatGPT plugin. On the standard web Plugins page, Add custom MCP server accepted the name Suno, the official endpoint and OAuth authentication. Create as a plugin opened the account connection flow. The already-approved permission bundle was presented for chatgpt.com; its Connect action again returned the same account-eligibility error. Returning to Plugins confirmed a persistent Suno entry under Installed. Its detail page identified it as a personal cloud plugin, version 1.0.0, with Continue app connection. Thus plugin creation succeeded while account connection remained incomplete. This was a user-requested standard plugin setup, with no altered scopes or access-control workaround. No generation was attempted.

When the user later requested early-access application, the existing tab at the official linked Suno MCP Early Access Form already displayed `Thanks for completing this typeform`. The assistant did not submit a new response or duplicate the application. This establishes only the observed completion screen: the submission's account, answers, time, receipt and approval status were not available on that screen. Do not attribute the prior submission to the assistant or treat form completion as provider approval.

A later read-only inspection of the same official form in a fresh browser session established its notification instructions. The welcome screen states `you’ll hear from us within 24-48 hrs`; question 2 asks for email and states `We’ll use this to send your access and Suno updates.` No personal data was entered or response submitted during this inspection. Notifications therefore go to the email supplied in the application, which is not established by merely knowing the current Suno login email. The contact estimate is not a guarantee of approval or activation within that period.

## Cause and resolution

The initial requested scopes were rejected. A mismatch between discovered and accepted scopes is suspected; the exact rejected scope and provider-side cause were not established. Codex automatically retried and reached sign-in. No manual scope, credential or security-policy change was made.

The permission-review dependency was resolved by explicit user approval. The blocker at that stage was the provider's account-eligibility refusal. Suno's official MCP page offers `Get early access` and its release note identifies the service as a beta with early-access sign-up. Missing beta access was a supported hypothesis, but the exact account eligibility rule and internal reason were not exposed. Do not infer that paying for a plan fixes this: the official FAQ includes Free plans.

Keep plugin packaging status distinct from external account connection: a visible installed personal plugin with Continue app connection is a created plugin, not a usable authenticated integration. Neither an empty public plugin search nor a previous CLI setup attempt proves that the web custom-plugin creation path is unavailable. The standard browser UI was sufficient for the later explicit plugin-creation request.

The approved permission bundle includes account/profile/credit reads, music-library reads/searches and edits, credit spending, downloads and persistent access. The original incident remained open until the authenticated recheck below. Do not save account identifiers, OAuth state, challenges, callback URLs, authorization codes or tokens in project records.

On 2026-11-10, the user reported receiving beta approval and then requested a connection that excludes existing chats and memory. A dedicated official-SDK client completed DCR/PKCE OAuth, retrieved 41 authenticated tools and successfully reused DPAPI-encrypted credentials. Native unrestricted Suno MCP was disabled and the ChatGPT cloud plugin was left unconnected. The authentication incident is resolved for this dedicated route. The approval email itself was not read, and approval versus the changed client route was not independently isolated as the sole cause. No song generation was performed. See [the separate content-boundary record](R-CODE-SUNO-CONTEXT-BOUNDARY.md) and [live evidence](../../prototypes/SunoRestricted/verification.json).

## Recheck and prevention

Observed checks: official setup documentation read; plugin lookup performed; server registration succeeded; configuration read back; login page inspected. These establish a setup path, not a working music-generation connection.

After user login, confirm CLI authentication completion, then inspect available Suno tools and make an authorized read-only account or credit request. Check actual generation separately when creating the requested demo. If tools need a new chat or server restart, verify that requirement rather than assuming registration reloads the current chat.

If an OAuth callback waiter has expired, reuse of its stale browser page cannot establish a new authorization. Start a fresh login flow and inspect its own consent/callback result. The fresh flow reached consent in this case but then encountered account-eligibility rejection. Obtain explicit consent to the visible permission bundle when required by action review.

Before another login attempt, check that the provider has enabled MCP access for the account, using the official early-access route or support. Account sign-in, a supported plan and permission consent cannot be substituted for provider eligibility. Do not retry identical authorization requests against a confirmed eligibility refusal, bypass it through another client or claim authenticated generation works. Ordinary Suno website generation is a separate capability and was not verified here.

The proposed future check is to distinguish server registration, account authorization, usable tools and a completed audio result in progress reports. No recurrence-prevention demonstration has been performed.

## Evidence

- [Suno official MCP setup](https://help.suno.com/en/articles/14551425), read 2026-11-10: endpoint and sign-in/authorization requirement.
- [Suno MCP overview](https://suno.com/mcp), read 2026-11-10: song generation, account credits and library storage.
- [Suno MCP beta release note](https://suno.com/release-notes/suno-mcp-beta), checked 2026-11-10: beta early-access sign-up.
- [Suno MCP FAQ](https://help.suno.com/en/articles/14486145), checked 2026-11-10: all plans including Free are supported; this does not verify eligibility of the observed account.
- [Official OpenAI MCP documentation](https://learn.chatgpt.com/docs/extend/mcp), read 2026-11-10: Codex HTTP MCP configuration and OAuth support.
- Current chat's tool results: Suno plugin search (empty); `codex --version`; `codex mcp add suno`; `codex mcp get suno --json`; subsequent login timeout and retry; explicit user permission approval; browser observations of consent and Account Linking Error; final filtered MCP listing. The record retains only the non-sensitive diagnostic text above.
- [Restricted client and verification](../../prototypes/SunoRestricted/README.md), checked 2026-11-10: authenticated listing, credential reuse, nine passing checks and no content calls.
