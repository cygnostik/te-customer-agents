# Changes

## 0.1.1

- Document the complete organisation bearer format: token ID, underscore, secret.
- Add `scripts/compose_token.py` to assemble API creation responses into new private credential files without printing secrets or duplicating the prefix.
- Clarify HTTP 403 diagnostics: check token composition before changing permissions.
- Add regressions for composition, malformed/duplicate input, private output and overwrite refusal.

## 0.1.0

Initial schema-driven CLI, administrator/site-owner skills, scoped profiles and on-use API refresh guidance.

## Unreleased: public schema refresh

- Target separately obtained official OpenAPI 12.26.3 (498 operations); public release notes list 12.26.6, and live compatibility and permissions review remain pending.
- Refuse GitHub manifest/install callbacks and signed webhook, protect member-session tokens and Git deployment metadata/logs with private output, and add offline regressions.
