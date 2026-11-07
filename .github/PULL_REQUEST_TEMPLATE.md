## What and why

One or two sentences on what this changes and the reason behind it. If it fixes a reported issue, link it here.

## What changed

- The main behavior or content change
- Any side effects worth calling out, even if they are small

## How to test

Steps a reviewer can follow without guessing. Include the relevant route, screen, API call, or test if there is one.

If this change touches auth, submissions, verification, admin review, or the LLM path, say so and note whether the tests cover it without real keys.

## Deploy or config impact

- Does this need a new env var, secret, migration, seed step, or build change?
- Does anything else need to happen after deploy, such as a re-verification run or a one-time setup step?

If there is no deploy impact, say so directly.

## Docs

Note any docs that need an update in the same PR. The usual suspects are README.md and DEPLOY.md, but docs/openapi.json and the issue templates count too when they drift.

## Checklist

- [ ] The change is scoped to one reasonable goal
- [ ] Backend and/or frontend tests cover the changed behavior
- [ ] I did not introduce public tests that touch other people's accounts or data
- [ ] I checked for doc drift if the behavior changed
- [ ] I removed any leftover debug logging or commented-out code I added while testing
