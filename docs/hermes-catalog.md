# Install the skill in Hermes

This is a third-party skill, not a Hermes plugin, MCP server or official catalog listing. Review the complete skill and [security guidance](security.md) before installing it. Customer use requires permission or terms from TrustEdge.gt.

## Manual installation

Copy the entire `skills/enhance-site-owner` directory into the skills directory for the intended Hermes profile. Check the destination first and do not overwrite an existing skill. The copy must include `SKILL.md`, `NOTICE.md`, `CHANGELOG.md`, `scripts/`, `references/`, and `templates/`. Start a fresh session and verify that Hermes resolves the intended skill path and its support files. Then follow [getting started](getting-started.md) to set up the vendor schema and private customer profile. Schema setup must run against the installed copy.

You can also use the skill in the repository directory without installing it. This does not register it in Hermes.

## GitHub installation

For a GitHub-hosted copy, substitute the repository's actual owner for `OWNER`:

```sh
hermes skills tap add OWNER/te-customer-agents
hermes skills inspect OWNER/te-customer-agents/skills/enhance-site-owner
hermes skills install OWNER/te-customer-agents/skills/enhance-site-owner
```

Inspect the identifier and scanner findings first. Adding a tap does not install a skill. After installation, verify the actual location and complete set of support files. Do not use a direct raw SKILL.md URL: support-file behavior differs by source adapter and runtime revision. A scanner result is not an endorsement or proof of server-side authorization.

The complete skill bundle has been tested through the Hermes GitHub adapter using synthetic local transport and a disposable Hermes home. A public-network install and live customer access have not been verified. GitHub adapter fallback behavior and older Hermes versions may differ; verify the installed files before account use.

## References

- [Creating Hermes skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
- [Working with skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)
