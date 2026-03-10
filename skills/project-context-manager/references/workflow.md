# Project Context Manager - Workflow Guide

## Overview

This guide provides detailed workflows for using the Project Context Manager skill in various scenarios.

## Scenario 1: Starting a Brand New Project

### Step 1: Initialize Documentation

```bash
cd /path/to/your/project
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "MyAwesomeProject" \
  --description "A revolutionary video editor" \
  --tech-stack "C++,Python,CMake,FFmpeg"
```

### Step 2: Customize Documentation

1. Edit `docs/agent/START_HERE.md`:
   - Update project description
   - Add specific tech stack details
   - Define initial goals

2. Edit `docs/agent/PROJECT_STATUS.md`:
   - Define Phase 1 tasks
   - Set initial TODO list
   - Add any known constraints

3. (Optional) Add architecture docs:
   - Create `docs/agent/技术方案书.md` for architecture
   - Create `docs/agent/开发指南.md` for implementation guide

### Step 3: Start First Session

Tell your agent:
```
Please read docs/agent/ directory and start working.
```

The agent will:
1. Read START_HERE.md (understand project)
2. Read PROJECT_STATUS.md (see TODO tasks)
3. Start working on highest priority task
4. Update PROJECT_STATUS.md before ending

---

## Scenario 2: Continuing an Existing Project

### New Session Start

```
Please read docs/agent/ directory and continue working.
```

The agent will:
1. Read PROJECT_STATUS.md
2. Check "In Progress Tasks"
3. If found, continue that work
4. If not, pick next TODO task
5. Update status before ending

### Mid-Session Check

If you want to check progress mid-session:
```
Please update PROJECT_STATUS.md with your current progress.
```

---

## Scenario 3: Multiple Agents Working in Parallel

### Setup

1. Each agent works on different branches
2. Each agent updates their own PROJECT_STATUS.md
3. Merge documentation along with code

### Workflow

**Agent A** (working on UI):
```
Please read docs/agent/ and work on UI tasks.
Update PROJECT_STATUS.md when done.
```

**Agent B** (working on backend):
```
Please read docs/agent/ and work on backend tasks.
Update PROJECT_STATUS.md when done.
```

### Merge Strategy

1. Merge code first
2. Merge PROJECT_STATUS.md (resolve conflicts manually)
3. Update CONTEXT.md with integration notes

---

## Scenario 4: Debugging a Complex Issue

### Step 1: Record the Problem

Tell agent:
```
Please record this issue in PROJECT_STATUS.md "Known Issues" section:
- Description: [problem]
- Severity: High
- Status: Investigating
```

### Step 2: Investigation

Agent should:
1. Try solutions
2. Record attempts in CONTEXT.md "Debugging Information"
3. Update issue status in PROJECT_STATUS.md

### Step 3: Resolution

When fixed:
1. Update issue status to "Resolved"
2. Record solution in CONTEXT.md
3. Add test case to prevent regression

---

## Scenario 5: Major Architecture Change

### Step 1: Document Decision

Create entry in CONTEXT.md "Architecture Evolution":
```markdown
### Change #001: Switch from Qt to ImGui

**Date**: 2026-03-10
**Reason**: User wants retro Mac UI style
**Impact**: Complete UI rewrite
**Migration**: [steps]
```

### Step 2: Update Technical Docs

1. Update `技术方案书.md` with new architecture
2. Update `开发指南.md` with new implementation steps

### Step 3: Update Status

In PROJECT_STATUS.md:
1. Mark old tasks as obsolete
2. Add new tasks for migration
3. Update "Technical Decisions" section

---

## Scenario 6: Onboarding a New Agent

### Minimal Onboarding

```
Please read docs/agent/ directory to understand the project,
then continue working on the highest priority task.
```

That's it! The documentation is self-explanatory.

### Detailed Onboarding

If the agent needs more context:
```
1. Read docs/agent/START_HERE.md for project overview
2. Read docs/agent/技术方案书.md for architecture
3. Read docs/agent/开发指南.md for implementation details
4. Read docs/agent/PROJECT_STATUS.md for current status
5. Start working on TODO tasks
```

---

## Scenario 7: Project Handoff to Human

### Generate Report

```bash
python scripts/generate_report.py --project-dir /path/to/project
```

This creates a human-readable report:
- Overall progress
- Completed features
- Known issues
- Next steps

### Documentation Review

Human should review:
1. `PROJECT_STATUS.md` - Current state
2. `CONTEXT.md` - Important decisions and solutions
3. Code comments - Implementation details

---

## Scenario 8: Emergency Recovery

### Documentation Lost or Corrupted

1. Check Git history:
```bash
git log -- docs/agent/
git checkout HEAD~1 -- docs/agent/
```

2. If no Git history, reconstruct from code:
   - Read code comments
   - Check commit messages
   - Rebuild PROJECT_STATUS.md manually

### Agent Forgot to Update

If agent didn't update documentation:
```
Please review the code changes since last update,
and update PROJECT_STATUS.md accordingly.
```

---

## Best Practices

### 1. Frequent Updates

Update PROJECT_STATUS.md:
- After completing each task
- Before taking a break
- Before ending session

### 2. Clear Task Descriptions

Good task description:
```markdown
**Task**: Implement FFmpeg video decoder

**Files**: src/video/decoder.h, src/video/decoder.cpp

**Requirements**:
- Support MP4, MKV, AVI formats
- Handle errors gracefully
- Return RGB24 frames

**Acceptance**: Can decode test video and display first frame
```

Bad task description:
```markdown
**Task**: Video stuff
```

### 3. Link Related Information

In PROJECT_STATUS.md:
```markdown
**Related**:
- See CONTEXT.md "FFmpeg Integration" section
- See 开发指南.md section 3.3
- Reference: http://dranger.com/ffmpeg/
```

### 4. Use Checklists

For complex tasks:
```markdown
**Progress**:
- [x] Design API
- [x] Implement open()
- [ ] Implement readFrame()
- [ ] Implement seek()
- [ ] Write tests
```

### 5. Record Decisions

In CONTEXT.md:
```markdown
### Decision: Use GLFW instead of SDL2

**Date**: 2026-03-10
**Reason**: Better ImGui integration
**Trade-off**: Less game-oriented features
```

---

## Common Patterns

### Pattern 1: Feature Development

```
1. Add task to PROJECT_STATUS.md TODO
2. Agent reads status and starts work
3. Agent implements feature
4. Agent tests feature
5. Agent updates status to completed
6. Agent records implementation notes in CONTEXT.md
```

### Pattern 2: Bug Fix

```
1. Add bug to PROJECT_STATUS.md "Known Issues"
2. Agent investigates
3. Agent records attempts in CONTEXT.md
4. Agent fixes bug
5. Agent updates issue status to "Resolved"
6. Agent adds test case
```

### Pattern 3: Refactoring

```
1. Document reason in CONTEXT.md
2. Add refactoring tasks to PROJECT_STATUS.md
3. Agent refactors incrementally
4. Agent tests after each change
5. Agent updates status
```

---

## Troubleshooting

### Problem: Agent Ignores Documentation

**Solution**: Be explicit:
```
IMPORTANT: You MUST read docs/agent/PROJECT_STATUS.md
before starting any work.
```

### Problem: Documentation Out of Sync

**Solution**: Run status checker:
```bash
python scripts/check_status.py --project-dir .
```

### Problem: Too Much Documentation

**Solution**: Focus on essentials:
- START_HERE.md - Keep under 1 page
- PROJECT_STATUS.md - Only current status
- CONTEXT.md - Only important context

### Problem: Agent Doesn't Update

**Solution**: Add to session end prompt:
```
Before ending, you MUST update PROJECT_STATUS.md
with your progress.
```

---

## Advanced Usage

### Custom Templates

1. Copy templates from `templates/` directory
2. Customize for your project type
3. Use custom templates with init script

### Integration with CI/CD

```yaml
# .github/workflows/check-docs.yml
name: Check Documentation
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check documentation
        run: python scripts/check_status.py --project-dir .
```

### Automated Reports

```bash
# Generate weekly report
python scripts/generate_report.py --project-dir . > weekly-report.md
```

---

**Remember**: The goal is seamless collaboration across sessions!
