# Get started

Obtain usage permission from TrustEdge before customer deployment; proprietary rights are retained.

## 1. Review and install the complete skill

Read [security](security.md), then [Hermes installation](hermes-catalog.md). Do not install only SKILL.md: scripts, references, templates and metadata must accompany it.

The standalone entrypoint is `skills/enhance-site-owner/SKILL.md`. An agent needs file-reading and terminal execution capabilities, Python 3.9+, and approved outbound HTTPS for schema setup and account calls. If those capabilities or credentials are missing, stop and report the missing prerequisite. Other agent runtimes are not certified or tested here.

## 2. Set up the vendor schema

From the repository root, through Hermes `terminal` (or your own terminal). If you installed the skill separately, replace `skills/enhance-site-owner` in these commands with the actual installed skill directory:

```sh
python3 skills/enhance-site-owner/scripts/enhance.py --help
python3 skills/enhance-site-owner/scripts/setup_schema.py
python3 skills/enhance-site-owner/scripts/enhance.py ops --search dns
python3 skills/enhance-site-owner/scripts/enhance.py describe getWebsite
python3 skills/enhance-site-owner/scripts/enhance.py refresh-status
```

Use a Python environment with PyYAML already available for the one-time conversion. Obtain approval before installing a dependency. Normal account calls need only the Python standard library. The setup helper fetches the official Enhance schema over verified HTTPS without hosting credentials, refuses redirects and existing-file overwrites, and requires the baseline version in `scripts/assets/freshness.json`. A changed publisher version requires review, not bypassing that check. The full schema is deliberately not distributed here.

## 3. Configure private customer access

These tools require the Enhance API key for your customer account. Follow [first installation](../skills/enhance-site-owner/references/first-install.md) and [permissions](../skills/enhance-site-owner/references/permissions.md). Copy the site or organisation template to a private directory outside this repository, the installed skill and all served web directories. Fill in your account details using the information supplied by TrustEdge.gt.

- Use a site profile for an additional exact-website local guard.
- Use an organisation profile only if access to that customer's permitted organisation-wide resources is intended.
- Supply the complete `token-id_secret` credential using an approved private file or environment source. Do not paste it into chat, command arguments or documentation.
- Restrict credential-file permissions (0600 on POSIX; a suitable private ACL on Windows).
- Have the provider verify allowed and denied access directly at Enhance, independently of the local guard.

## 4. Make an approved own-site read

Replace `<private-profile.json>` with the private configuration path; keep secrets out of the command itself:

```text
python3 skills/enhance-site-owner/scripts/enhance.py --config <private-profile.json> call getWebsite
python3 skills/enhance-site-owner/scripts/enhance.py --config <private-profile.json> batch skills/enhance-site-owner/templates/site-read-plan.json
```

Check the returned target IDs. Batch exit 1 is partial failure; inspect each result instead of claiming everything succeeded.

## 5. Review changes before execution

Use `describe` for exact operation parameters. Mutations without `--apply` are local request plans. Obtain actual approval for the target and consequences before adding `--apply`; then read back the exact record and test the user-visible effect. Do not replay an ambiguous timeout until state is reconciled.

Suggested first instruction: “Use enhance-site-owner to inspect my approved website configuration. Do not change anything. Report the exact site and any missing permissions without printing credentials.”

## Removal and revocation

Remove only the installed skill copy you selected, after checking its path. Removing a directory does not revoke API credentials or close existing sessions. Credential revocation is a separate provider-authorized task. Do not delete private rollback material without the customer's retention decision.
