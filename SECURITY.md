# Security

MANABI is a small single-service app. This doc covers what is in scope, how to report something, and what we do about the known issues we have already accepted.

## Scope

This policy covers the MANABI web app, its FastAPI backend, the React frontend, the API, the OAuth flow, the chat feature, and anything deployed under a MANABI domain.

Out of scope for this doc: the security of GitHub itself, the LLM providers we call out to, your own database host, and anything you add on top of the app.

## How to report

If you find something that looks like a real vulnerability, please open a private report rather than a public issue. A short message describing what you did, what you expected, and what actually happened is enough to start.

Good reports include:
- The endpoint or page you touched
- The request you sent, if it is an API action
- Whether the issue needs an authenticated account or a specific role
- Whether it affects data that belongs to other users

Please do not test against other people's accounts or submissions. If you need a test account, use your own.

## What we fix first

Not everything is equally urgent. We tend to prioritize in this order:

1. Anything that lets one user read or change another user's data
2. Anything that bypasses the project submission rules or the admin gate
3. Anything that lets an anonymous visitor do something only a logged-in user should do
4. Anything that leaks a secret, a session, or another user's GitHub identity
5. Anything that degrades the app for other users, including spam or rate-limit bypasses
6. Low-severity issues like misleading error text or minor info leaks

## Known issues we have accepted

### GitHub token stored in the database

User GitHub access tokens are stored in plaintext in `users.github_token`. A database dump, SQL injection, or direct DB access could expose those tokens.

This is existing behavior and was not introduced by the verification work. The team has decided not to implement encryption here without a separate decision, because it touches session rotation, token refresh, and the re-verification script. If you want this hardened, that is a separate project, not a quick follow-up.

Recommended direction if someone takes it on: encrypt at rest with a key held outside the DB, decrypt only inside the GitHub service layer, and rotate or invalidate tokens when the key changes.

### LLM prompts include untrusted content

Problem briefs, repo README excerpts, and user summaries are passed into the LLM as delimited blocks. The prompt tells the model to treat that content as data and ignore instructions inside it. That is a reasonable mitigation, not a guarantee. A malicious README or brief could still try to steer the model.

We accept this risk because the model output is used for relevance checks and chat replies, not for executing commands or writing to the database directly. The downstream code treats the model output as advisory where it matters.

### OAuth and session cookies

Sessions are signed and, on a real HTTPS origin, set with Secure and HttpOnly flags. The app refuses to boot with the placeholder session secret when `BASE_URL` is not localhost. That fail-fast check is intentional: a predictable secret is worse than a crash.

If you deploy with a real domain, use a real `BASE_URL` and a real `SESSION_SECRET`. Do not skip that step and hope the platform TLS layer is enough.

### Rate limits are real, not cosmetic

Chat and submission limits are enforced on the backend. The UI shows the backend's messages honestly. If a limit is reached, the honest message is the intended behavior, not a bug.

## Things we do not want to see

- Testing against other people's repos, accounts, or submissions
- Spamming the admin review queue or the chat feature in a way that affects real users
- Sharing session secrets, OAuth secrets, or database URLs in public issues
- Opening a public issue for something that looks like a real exploit before it is handled

If you are unsure whether something counts, report it anyway. We would rather get a false alarm than miss a real one.

## What happens after a report

We look at reports as they come in. For a real issue, we confirm it, decide on a fix or a documented acceptance, and then close the loop. If the report is useful, we will say so. If we need more detail, we will ask.

This is a small project, so there is no SLA and no bounty program. A clear, honest report is reward enough.

## Security contacts

Use the project's issue tracker for non-sensitive questions. For anything you would rather not post publicly, contact the maintainer directly and we will figure out a private channel from there.
