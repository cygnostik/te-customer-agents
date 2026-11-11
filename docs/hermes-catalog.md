# Install the skill in Hermes

Installing the skill does not connect it to your account. To use it with your hosting account, you will need your customer API key; Enhance controls what that key can access.

This is a third-party skill, not a Hermes plugin, MCP server or official catalog listing. Review the complete skill and [security guidance](security.md) before installing it. Customer use requires permission or terms from TrustEdge.gt.

## Manual installation

Copy the entire `skills/enhance-site-owner` directory into the skills directory for the intended Hermes profile. Check the destination first and do not overwrite an existing skill. The copy must include `SKILL.md`, `NOTICE.md`, `CHANGELOG.md`, `scripts/`, `references/`, and `templates/`. Start a fresh session and verify that Hermes resolves the intended skill path and its support files. Then follow [getting started](getting-started.md) to set up the vendor schema and private customer profile. Schema setup must run against the installed copy.

You can also use the skill in the repository directory without installing it. This does not register it in Hermes.

## GitHub installation

```sh
hermes skills tap add cygnostik/te-customer-agents
hermes skills inspect cygnostik/te-customer-agents/skills/enhance-site-owner
hermes skills install cygnostik/te-customer-agents/skills/enhance-site-owner
```

Inspect the identifier and scanner findings first. Adding a tap does not install a skill. After installation, verify the actual location and complete set of support files. Do not use a direct raw SKILL.md URL: support-file behavior differs by source adapter and runtime revision. A scanner result is not an endorsement or proof of server-side authorization.

The complete skill bundle has been tested through a public-network Hermes install into a disposable Hermes home. Live customer access and server-side permission boundaries have not been verified by that test. Older Hermes versions may differ; verify the installed files before account use.

## References

- [Creating Hermes skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
- [Working with skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)
