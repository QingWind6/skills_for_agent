# Project Context Manager

A skill for managing long-term, multi-session software development projects with structured documentation and seamless agent handoffs.

## Why This Skill?

Complex software projects often span multiple sessions and require collaboration between different agents or developers. Without proper context management:

- ❌ Agents repeat work already done
- ❌ Progress is lost between sessions
- ❌ Important decisions are forgotten
- ❌ Bugs resurface because solutions weren't documented
- ❌ New agents can't quickly understand the project

This skill solves these problems with a structured documentation system.

## Quick Start

### 1. Initialize Your Project

```bash
python scripts/init_project.py \
  --project-dir /path/to/your/project \
  --project-name "MyProject" \
  --description "What your project does" \
  --tech-stack "Python,FastAPI,PostgreSQL"
```

This creates a `docs/agent/` directory with all necessary documentation.

### 2. Start Working

Tell your agent:
```
Please read docs/agent/ directory and start working.
```

That's it! The agent will:
1. Read the documentation
2. Understand the project
3. Check current status
4. Start working on the right task
5. Update documentation before ending

### 3. Continue in Next Session

Same instruction:
```
Please read docs/agent/ directory and continue working.
```

The agent automatically knows what was done and what's next.

## What You Get

### Documentation Structure

```
docs/agent/
├── README.md              # Documentation hub
├── START_HERE.md          # 5-minute project overview
├── PROJECT_STATUS.md      # Current status (most important!)
├── SESSION_HANDOFF.md     # Workflow guide
└── CONTEXT.md             # Detailed development context
```

### Key Features

- ✅ **Single Source of Truth**: PROJECT_STATUS.md tracks everything
- ✅ **Self-Documenting**: Agents know what to read and update
- ✅ **Seamless Handoffs**: No information loss between sessions
- ✅ **Progress Tracking**: Clear task lists and completion status
- ✅ **Issue Management**: Built-in bug and blocker tracking
- ✅ **Context Preservation**: Important decisions and solutions recorded

## How It Works

### Session Start (3-5 minutes)

1. Agent reads `START_HERE.md` - Understands project
2. Agent reads `PROJECT_STATUS.md` - Checks current status
3. Agent identifies work:
   - Continue "In Progress" tasks, or
   - Start next "TODO" task
4. Agent begins working

### During Work

- Agent implements features
- Agent tests frequently
- Agent updates status as tasks complete

### Session End (5 minutes)

1. Agent updates `PROJECT_STATUS.md`:
   - Mark completed tasks ✅
   - Update in-progress tasks
   - Add new issues
2. Agent records important context in `CONTEXT.md`
3. Agent leaves clear handoff message

### Next Session

Repeat! The cycle continues seamlessly.

## Real-World Example

### VideoCut Project

**Session 1**:
```
User: Please read docs/agent/ and start working.

Agent:
- Reads documentation
- Creates project structure
- Sets up CMake
- Updates status: "Project structure created ✅"
```

**Session 2**:
```
User: Please read docs/agent/ and continue.

Agent:
- Reads PROJECT_STATUS.md
- Sees next task: "Integrate ImGui"
- Implements ImGui integration
- Updates status: "ImGui integrated ✅"
```

**Session 3**:
```
User: Please read docs/agent/ and continue.

Agent:
- Reads PROJECT_STATUS.md
- Sees next task: "FFmpeg decoder"
- Implements video decoder
- Updates status: "Decoder implemented ✅"
```

No repeated instructions needed! The documentation guides everything.

## Benefits

### For Solo Developers

- 📝 Never forget what you were doing
- 🔄 Pick up where you left off instantly
- 📊 Track progress automatically
- 🐛 Remember bug solutions

### For Teams

- 👥 Seamless collaboration between agents
- 📚 Shared understanding of project state
- 🎯 Clear task ownership
- 📖 Onboarding new agents in minutes

### For Long-Term Projects

- 🗓️ Maintain context over weeks/months
- 📈 Track progress over time
- 🔍 Audit trail of decisions
- 🎓 Knowledge base builds automatically

## Advanced Features

### Multiple Agents in Parallel

Each agent can work on different tasks and update their own status. Merge documentation along with code.

### Custom Templates

Customize templates for your project type (web app, game, ML pipeline, etc.).

### Automated Checks

```bash
python scripts/check_status.py --project-dir .
```

Verify documentation is up-to-date.

### Integration with CI/CD

Add documentation checks to your CI pipeline.

## Documentation

- **[SKILL.md](./SKILL.md)** - Complete skill reference
- **[references/workflow.md](./references/workflow.md)** - Detailed workflows
- **[references/examples.md](./references/examples.md)** - Real-world examples

## Scripts

- **init_project.py** - Initialize project documentation
- **check_status.py** - Verify documentation status
- **generate_report.py** - Generate progress reports (coming soon)

## Requirements

- Python 3.7+
- No external dependencies

## Installation

1. Clone this skill repository
2. Add to your Claude Code skills directory
3. Use the scripts to initialize projects

## Best Practices

1. **Always read PROJECT_STATUS.md first**
2. **Update documentation frequently**
3. **Keep task descriptions clear and specific**
4. **Record important decisions in CONTEXT.md**
5. **Small iterations, frequent updates**

## Common Use Cases

- ✅ Long-term software projects
- ✅ Multi-session development
- ✅ Team collaboration
- ✅ Complex projects with many moving parts
- ✅ Projects requiring detailed context
- ✅ Learning projects (track your progress)

## Not Suitable For

- ❌ One-off scripts (too much overhead)
- ❌ Trivial projects (documentation overkill)
- ❌ Projects with no sessions (single sitting work)

## Examples

See [references/examples.md](./references/examples.md) for detailed examples:

- Video editor (VideoCut)
- Web API
- Machine learning pipeline
- Mobile app backend
- Game development
- Documentation website
- DevOps automation
- Data analysis tool

## Contributing

Contributions welcome! Please:

1. Test your changes
2. Update documentation
3. Follow existing patterns
4. Add examples if applicable

## License

MIT License - See LICENSE file

## Support

- Issues: GitHub Issues
- Questions: GitHub Discussions
- Examples: See references/examples.md

---

**Remember**: Good documentation habits are the key to long-term project success!

**Version**: 1.0.0
**Created**: 2026-03-10
**Author**: Claude Sonnet 4.6
