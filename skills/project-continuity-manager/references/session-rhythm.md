# Session Rhythm

This guide describes the recommended operating rhythm for large repositories that move across many sessions and agents.

## Start of Session

### Minimum read set

1. `docs/agent/START_HERE.md`
2. `docs/agent/PROJECT_STATUS.md`

### Read next only if needed

- `docs/agent/TASKS.md` for backlog context
- `docs/agent/ARCHITECTURE.md` when changing system design or touching integration boundaries
- `docs/agent/DECISIONS.md` when rationale matters
- `docs/agent/CONTEXT.md` when debugging or dealing with environment quirks
- latest relevant handoff when resuming paused work

### Start checklist

- Confirm current task is still valid
- Check blockers and known risks
- Verify branch and working tree state
- Decide whether the docs need a quick correction before coding

## During the Session

Update durable docs when the information becomes true, not only at the very end.

### Update PROJECT_STATUS.md when

- the active task changes
- the scope changes
- a blocker appears or disappears
- the next step becomes clearer
- a meaningful milestone is reached

### Update TASKS.md when

- priorities move
- backlog items are split, merged, or deferred
- acceptance criteria change

### Update ARCHITECTURE.md or DECISIONS.md when

- module boundaries change
- a new subsystem is introduced
- a dependency choice is made or reversed
- a non-obvious tradeoff matters for future work

### Update CONTEXT.md when

- a tricky debugging path was necessary
- setup or runtime quirks would waste the next agent's time
- a command sequence is likely to be reused

## End of Session

Create a handoff whenever you stop after meaningful progress.

### End checklist

- `PROJECT_STATUS.md` reflects the real state
- `TASKS.md` reflects changed priorities or scope
- `ARCHITECTURE.md` and `DECISIONS.md` reflect lasting design changes
- a new handoff was created
- the handoff passed validation
- the latest handoff path is recorded in `PROJECT_STATUS.md`

## What Makes a Good Handoff

A strong handoff is:
- specific
- short enough to scan quickly
- rich in next actions
- explicit about blockers and assumptions
- free of secrets

A weak handoff is:
- vague
- only a changelog
- missing the first next step
- inconsistent with `PROJECT_STATUS.md`

## Recommended User Prompts

These prompts should trigger this skill naturally:

- "Set up durable agent docs for this project."
- "Read docs/agent and continue working."
- "Create a handoff before we stop."
- "Resume from the latest handoff."
- "Audit whether our project docs are still trustworthy."
