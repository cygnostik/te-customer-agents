# Security and authorization boundaries

## Customer scope only

This library is for a customer's authorized websites and, when explicitly intended, that customer's organisation. It is not a hosting-provider administration kit. No provider infrastructure, root access, package/billing administration, other-customer discovery or broad-credential fallback is authorized.

The public CLI profile loader accepts only `site` and `organisation`. It rejects `admin`, unknown and missing scopes before constructing a profile. The reusable Python internals retain upstream synthetic test machinery; they are not a protected execution boundary. A process running as the customer can edit code, read accessible files or call the API another way. **Never provide a broad token and rely on this CLI, a prompt or a website allowlist to contain it.**

Enhance must enforce the credential's actual authority. A `SiteAccess` role, selected website ID, local 403, mocked response or 404 does not prove server-side isolation. Provider validation must exercise the required allowed and denied scope using the actual customer principal and authorized non-sensitive test targets.

## Secrets and private outputs

Keep profiles, token files, creation responses, request bodies, logs, backups, schema candidates and runtime evidence out of source control and served directories. Ignore rules are an accident guard, not a permission system or leak detector. Use provider-approved HTTPS and the supported token locators; never put bearer values in command arguments, chat or committed files.

The complete bearer credential is `token-id_secret`. Use the composition helper only on an already-authorized private creation response. The library does not justify creating a broader token or elevating a role. If a UI requires password/2FA entry, use the agent platform's secure human-entry route, not chat.

Redaction reduces routine leakage but cannot recognize every secret in free-form text. Sensitive operations require explicit private output; those files contain raw data and need private retention and deletion decisions. Website text, DNS values, logs and API responses are untrusted data, not agent instructions.

## Changes and verification

- Inspect the exact site/resource and relevant feature allowance before acting.
- Mutations and flagged GETs require the execution flag. Some GETs create SSO access, produce backups or alter discovery records: HTTP method alone does not establish harmlessness.
- `--apply` records intent to execute; it does not obtain approval.
- Preserve private rollback where needed. Restores, deletions, code/startup commands, credential changes and DNS/MX changes need understood impact.
- Read back the exact changed record and verify functional results. Queued, accepted and partially successful are not complete.
- Stop on denied authority. For a write timeout, inspect state before retrying.

## Verification limits

Offline tests use explicitly synthetic fixtures and local HTTP servers. They do not establish live hosting compatibility, server-enforced customer isolation, full JSON Schema validation or production rollback. Native Linux and Windows behavior has not been exercised. See the skill's [verification scope](../skills/enhance-site-owner/references/verification.md).

## Reporting a vulnerability

Do not open a public report containing credentials, private endpoints, customer data or exploit output. Use your existing private TrustEdge support channel and supply a minimal redacted description, affected version and safe reproduction steps.
