---
name: caveman-compress
description: Compress natural language memory files (CLAUDE.md, todos, preferences) into caveman format to save input tokens. Preserves all technical substance, code blocks, URLs, and file paths. Human-readable backup saved as FILE.original.md.
---

# Caveman Compress

## Purpose
Compress natural language files (such as `CLAUDE.md`, to-do lists, and configuration guidelines) into caveman-speak. This drastically reduces the number of input tokens read at the beginning of each agent session (~45% input token reduction), saving cost and context window space.

## Activation
Triggered when the user says "compress memory file", "/caveman-compress <filepath>", or when a file has grown too large and needs token optimization.

## Compression Rules
* **Remove**:
  - Articles: a, an, the.
  - Filler: just, really, basically, actually, simply, essentially, generally, specifically.
  - Pleasantries: "sure", "certainly", "of course", "happy to", "I'd recommend".
  - Hedging: "it might be worth", "you could consider", "it would be good to".
  - Redundant phrasing: "in order to" → "to", "make sure to" → "ensure", "the reason is because" → "because".
  - Connective fluff: "however", "furthermore", "additionally", "in addition".
* **Preserve EXACTLY (never modify or compress)**:
  - Code blocks (fenced ``` and indented).
  - Inline code (`backtick content`).
  - URLs and links (full URLs, markdown links).
  - File paths (`/src/components/...`, `./config.yaml`).
  - Commands (`npm install`, `git commit`, `docker build`).
  - Technical terms (library names, API names, protocols, algorithms).
  - Proper nouns (project names, people, companies).

## Process
When requested to compress a file:
1. Create a backup of the original file at `<filename>.original.md`.
2. Parse and compress the natural language portions of the file using the rules above.
3. Keep all headers, code blocks, and URLs intact.
4. Overwrite the original file with the compressed text.
5. Verify that no code blocks, URLs, or markdown links were lost or modified in the process.
