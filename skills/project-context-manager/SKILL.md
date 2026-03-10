---
name: project-context-manager
description: Manage long-term, multi-session project development with structured documentation. Automatically initialize project documentation, track progress across sessions, maintain context between agent handoffs, and ensure seamless collaboration. Use when starting a complex project that will span multiple sessions, or when continuing work on an existing project with established documentation.
---

# Project Context Manager

A skill for managing long-term, multi-session software development projects with structured documentation and seamless agent handoffs.

## Quick Start

### Initialize a New Project

```bash
python scripts/init_project.py --project-dir /path/to/project --project-name "MyProject"
```

This creates a `docs/agent/` directory with all necessary documentation templates.

### Continue Existing Project

When starting a new session on an existing project:

1. Read `docs/agent/START_HERE.md` (5 minutes)
2. Read `docs/agent/PROJECT_STATUS.md` (3 minutes)
3. Start working based on "In Progress" or "TODO" tasks
4. Update `docs/agent/PROJECT_STATUS.md` before ending session

### One-Line Instruction for Users

Tell the agent:
```
Please read docs/agent/ directory and start working.
```

## What This Skill Provides

### Document Structure

```
docs/agent/
├── README.md              # Documentation hub
├── START_HERE.md          # 5-minute project overview
├── PROJECT_STATUS.md      # Current status (most important)
├── SESSION_HANDOFF.md     # Session handoff workflow
├── CONTEXT.md             # Detailed development context
├── 技术方案书.md          # Architecture design (optional)
└── 开发指南.md            # Implementation guide (optional)
```

### Core Documents

1. **START_HERE.md** - Quick project overview
   - What is the project?
   - Tech stack summary
   - Current phase
   - What to do next

2. **PROJECT_STATUS.md** - Single source of truth ⭐⭐⭐
   - Completed tasks checklist
   - In-progress tasks (with detailed progress)
   - TODO tasks (prioritized)
   - Known issues table
   - File structure status

3. **SESSION_HANDOFF.md** - Standard workflow
   - Session start checklist
   - Session end checklist
   - Best practices
   - Common mistakes to avoid

4. **CONTEXT.md** - Deep context storage
   - Code snippets and design thoughts
   - Debugging information
   - Technical research notes
   - Performance optimization records

## Workflow

### Session Start

1. **Read documentation** (10-15 minutes first time, 3-5 minutes after)
   - `START_HERE.md` - Understand the project
   - `PROJECT_STATUS.md` - Check current status
   - `CONTEXT.md` - Review detailed context (if needed)

2. **Identify work**
   - Check "In Progress Tasks" - Continue unfinished work
   - Check "TODO Tasks" - Start new work if nothing in progress
   - Check "Known Issues" - Address blockers

3. **Start working**
   - Update `PROJECT_STATUS.md` to mark task as "in_progress"
   - Follow architecture and implementation guides
   - Test frequently

### Session End

1. **Update PROJECT_STATUS.md** (5 minutes)
   - Mark completed tasks ✅
   - Update in-progress tasks with current status
   - Add new issues to "Known Issues"
   - Update file structure status
   - Update metadata (last updated time, updater name)

2. **Update CONTEXT.md** (optional, 5-10 minutes)
   - Record important code snippets
   - Document debugging solutions
   - Add technical research notes

3. **Leave clear handoff message**
   - What was completed
   - What's next
   - Any blockers or important notes

## Task Rules

### Always Read First

- **Never** start working without reading `PROJECT_STATUS.md`
- Risk: Duplicate work, wrong direction, wasted time

### Always Update Before Ending

- **Never** end session without updating `PROJECT_STATUS.md`
- Risk: Next session cannot continue, information loss

### Keep Documents Synchronized

- Update documentation immediately after code changes
- Don't wait until session end

### Small Iterations

- Complete small modules one at a time
- Test after each module
- Update status frequently

## Document Responsibilities

| Document | Purpose | Read Frequency | Update Frequency |
|----------|---------|----------------|------------------|
| `README.md` (agent/) | Navigation hub | First time | Rarely |
| `START_HERE.md` | Quick intro | First time | When project changes significantly |
| `PROJECT_STATUS.md` | Project status | Every session ⭐⭐⭐ | Every session ⭐⭐⭐ |
| `SESSION_HANDOFF.md` | Workflow guide | First time | Rarely |
| `CONTEXT.md` | Deep context | As needed | When important info needs recording |

## Best Practices

### 1. PROJECT_STATUS.md is King

- It's the single source of truth
- Always read it first
- Always update it last
- Keep it accurate and up-to-date

### 2. Clear Task Descriptions

- Be specific, not vague
- Include acceptance criteria
- List related file paths
- Provide enough context for another agent to continue

### 3. Record Problems Immediately

- Don't wait to document issues
- Include error messages and attempted solutions
- Record the final solution

### 4. Small Commits

- Commit frequently
- Update docs with each commit
- Clear commit messages

### 5. Test Driven

- Test each module immediately after completion
- Record test results in `CONTEXT.md`
- Fix issues immediately or record as known issues

## Common Mistakes

### ❌ Mistake 1: Not Reading Documentation

**Consequence**: Duplicate work, wrong direction

**Solution**: Always spend 10-15 minutes reading docs first

### ❌ Mistake 2: Not Updating Documentation

**Consequence**: Next session cannot continue, information loss

**Solution**: Update `PROJECT_STATUS.md` before ending session

### ❌ Mistake 3: Unclear Task Descriptions

**Consequence**: Next session doesn't know how to continue

**Solution**: Detailed progress, next steps, related files

### ❌ Mistake 4: Not Recording Problems

**Consequence**: Next session encounters same problems

**Solution**: Record problems and solutions in `CONTEXT.md`

### ❌ Mistake 5: Doing Too Much at Once

**Consequence**: Session ends with incomplete work, hard to handoff

**Solution**: Small iterations, complete one module at a time

## Scripts

### init_project.py

Initialize project documentation structure.

```bash
python scripts/init_project.py \
  --project-dir /path/to/project \
  --project-name "MyProject" \
  --description "Project description" \
  --tech-stack "C++,Python,CMake"
```

### check_status.py

Check if documentation is up-to-date.

```bash
python scripts/check_status.py --project-dir /path/to/project
```

### generate_report.py

Generate progress report from PROJECT_STATUS.md.

```bash
python scripts/generate_report.py --project-dir /path/to/project
```

## Templates

All document templates are in `templates/` directory:

- `README.template.md`
- `START_HERE.template.md`
- `PROJECT_STATUS.template.md`
- `SESSION_HANDOFF.template.md`
- `CONTEXT.template.md`

## References

- `references/workflow.md` - Detailed workflow guide
- `references/examples.md` - Example usage scenarios
- `references/troubleshooting.md` - Common issues and solutions

## Integration with Other Skills

This skill works well with:

- **imgui-repo-navigator** - For ImGui-based UI projects
- **Code generation skills** - For implementing features
- **Testing skills** - For validating implementations

## Output Expectations

When using this skill:

- Always reference which document you're reading from
- Clearly state current project phase and progress
- Explain what you're doing and why
- Update documentation before ending session
- Leave clear handoff message for next session

## Resources

- `templates/` - All document templates
- `scripts/` - Automation scripts
- `references/` - Detailed guides and examples

---

**Remember**: Good documentation habits are the key to long-term project success!

**Version**: 1.0.0
**Created**: 2026-03-10
