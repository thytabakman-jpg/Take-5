# Security Policy

## Credentials

Never commit passwords, API keys, personal access tokens, private keys, `.env` contents, or other credentials.

Use GitHub repository or environment secrets for automation credentials. Use fine-grained tokens with the minimum repository scope and the shortest practical lifetime.

When a credential enters Git history, rotate or revoke it first. History rewriting is a separate cleanup operation and is not a substitute for credential rotation.

## Account hardening

The repository security baseline includes:

- two-factor authentication or passkeys on the GitHub account;
- securely stored recovery methods;
- private commit-email configuration for public repositories;
- least-privilege personal access tokens;
- secret scanning and push protection where the account/repository plan makes them available.

These account-level settings are verified separately from repository files.

## Reporting

Treat a suspected credential exposure or unauthorized repository mutation as a blocking security event. Do not post the secret itself in an issue.
