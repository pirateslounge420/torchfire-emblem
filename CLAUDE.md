# torchfire-emblem — notes for Claude

This repo is **Fighter**, Game 1 of Mike's I Ching / Ba Gua trilogy: a turn-based fantasy tournament fighter. Games 2 and 3 (the tactics RPGs) aren't in this repo yet.

**Source of truth:** `docs/fighter-design-doc.md`. Read it before building anything. Its mentions of `changelog.md` and the Game 2/3 docs refer to files kept outside this repo for now.

## Working with Mike

- Mike is the creative director and doesn't write code. He describes what he wants in plain English, so explain what you changed the same way, without jargon.
- Handle files and git yourself. Commit and push your changes instead of asking Mike to move, rename or edit files.
- Write a decision into the design doc only after Mike confirms it's locked. While he's brainstorming, keep ideas in the conversation.
- If the doc doesn't cover something you need, ask Mike instead of inventing a design decision. You can pick small, easy-to-change implementation details yourself, but say what you picked.

## Tech

- Planned engine: Godot (not set up yet).
- The repo is public, so keep ripped reference art (like the Fire Emblem sprite sheets) out of it.
