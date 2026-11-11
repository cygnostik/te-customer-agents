![TrustEdge.gt](assets/trustedge-logo.png)

# TrustEdge.gt customer agents

Give your AI agent the instructions and tools it needs to work with your hosting account.

The included **Enhance site owner** skill can help your agent check your websites, domains, DNS, email, databases, backups and application settings. It can also prepare changes for your approval.

## Get started

1. Read the [installation guide](docs/getting-started.md) and [security guide](docs/security.md).
2. Set up the [Enhance site owner skill](skills/enhance-site-owner/SKILL.md) with your customer account details.
3. Ask your agent to check your website without making changes. Confirm it has found the right site before asking it to do anything else.

You'll need Python 3.9 or later and access to your hosting account. The one-time API setup also requires PyYAML. The full requirements and setup commands are in the installation guide.

## Your account and permissions

Use a credential issued for your own customer account. Don't give an agent a provider, administrator or reseller credential. Keep credentials out of chat, command arguments and website folders.

An agent's local website filter does not restrict what a credential can access on the server. Ask your provider to confirm the credential's actual permissions. The agent should ask before making changes and check the result afterward.

## Files in this repository

- [Enhance site owner skill](skills/enhance-site-owner/SKILL.md): instructions, scripts and templates.
- [Getting started](docs/getting-started.md): setup and a first account read.
- [Security](docs/security.md): credentials and access boundaries.
- [Hermes skills](docs/hermes-catalog.md): installation information for Hermes Agent.

## Usage

This material is proprietary. Customer use requires permission or terms from TrustEdge.gt. See [NOTICE](NOTICE.md).
