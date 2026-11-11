# Verification scope

Release baseline: public Enhance OpenAPI 12.26.3, retrieved 2026-11-11. Client execution was checked with Python 3.9.6 on macOS. The runtime is standard-library Python; Linux and Windows client behavior has not been exercised on native machines for this release.

The offline suite uses synthetic profiles, responses, files and loopback HTTP servers. It covers operation inventory/construction, typed requests, exact org/site guards, side-effect GETs, credential handling, redirect refusal, uploads, response limits, partial batches and refresh comparisons. Developer tests live outside the installable skill in the source repository. Run its `tools/test_skill.py` with an explicit private scratch directory; it assembles a disposable copy and obtains the official schema there. Maintenance YAML checks use PyYAML when available.

Live compatibility was exercised with operator authority against matching Enhance 12.25.8: website identity, domain mappings, database listing, backup listing and persistent-app listing. This does not establish the permissions of your customer credential. Verify your own-site success and required out-of-scope denial with the actual provider-issued credential before deployment.

The API catalog contains 498 operations. Offline request construction covers 489; these nine are deliberately discoverable but not constructed:

- `manifestCallback`, `installComplete`, `githubWebhook`: unsupported callback and signed-webhook protocols.
- `verify2FA`, `resendPin`: cookie/session authentication rather than supported bearer authentication.
- `uploadSql`: inconsistent declared path parameter names.
- `deleteEmailAutoresponder`, `updateEmailAutoresponder`: missing `autoresponder_id` parameter declarations; check the live publisher contract before use.
- `updateServerRole`: identical `oneOf` alternatives make the declared request schema ambiguous.

Request construction is not proof that each operation completed against a live server. Production writes, restore/rollback and customer-principal isolation require their own approved target tests.

Known response compatibility: `/version` returns plain version text; a website response can repeat `phpVersion` identically. The client accepts identical response duplicates but rejects conflicts and rejects all duplicate keys in local configuration, request and schema files.

For each actual task, read back the exact changed target and check the functional outcome. A passing local test suite, HTTP 200/201 or accepted job is not a substitute for that result.

## 2026-11-11 public schema refresh

Public OpenAPI 12.26.3 lags the public release notes, which list 12.26.6. No live controller query, customer allowed/denied check, production write, restore or rollback was performed for this refresh; earlier 12.25.8 live checks are historical only. The freshness review remains due pending those gates and a complete permission/behavior review. This work changes neither an installed skill nor a controller.
