---
name: caveman-commit
description: Ultra-compressed commit message generator. Cuts noise from commit messages while preserving intent and reasoning. Conventional Commits format. Subject ≤50 chars. Use when user says "write a commit", "commit message", "generate commit", "/commit", or invokes /caveman-commit.
---

# Caveman Commit

## Purpose
Write commit messages terse and exact. Conventional Commits format. No fluff. Focus on *why* over *what*.

## Activation
Triggered when user says "write a commit", "commit message", "generate commit", "/commit", or invokes `/caveman-commit`. Also auto-triggers when staging changes.

## Rules
* **Subject line**:
  - `<type>(<scope>): <imperative summary>` — `<scope>` is optional.
  - Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`.
  - Imperative mood: "add", "fix", "remove" — not "added", "adds", "adding".
  - Length: ≤50 chars when possible, hard cap 72.
  - No trailing period.
* **Body (only if needed)**:
  - Skip entirely when subject is self-explanatory.
  - Add body only for: non-obvious *why*, breaking changes, migration notes, linked issues.
  - Wrap at 72 chars.
  - Bullets `-` not `*`.
  - Reference issues/PRs at end: `Closes #42`, `Refs #17`.
* **Prohibited Phrases**:
  - Do not include "This commit does X", "I", "we", "now", "currently" — the diff already explains the *what*.
  - "Generated with AI" or similar developer signatures.
