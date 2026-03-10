# Project Context Manager - Examples

Real-world usage examples of the Project Context Manager skill.

## Example 1: Video Editor Project (VideoCut)

### Initial Setup

```bash
cd ~/projects/videocut
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "VideoCut" \
  --description "Retro Macintosh-style video editor" \
  --tech-stack "C++17,Dear ImGui,FFmpeg,OpenGL,CMake"
```

### Session 1: Project Setup

**User**: Please read docs/agent/ and start working.

**Agent**:
1. Reads START_HERE.md - Understands it's a retro video editor
2. Reads PROJECT_STATUS.md - Sees Phase 1 tasks
3. Creates project directory structure
4. Sets up CMakeLists.txt
5. Updates PROJECT_STATUS.md:
   ```markdown
   ## ✅ Completed Tasks
   - [x] Project directory structure created
   - [x] CMakeLists.txt configured

   ## 🚧 In Progress
   **Task**: Integrate ImGui + GLFW
   **Progress**: 30% - GLFW window created, ImGui pending
   **Next**: Initialize ImGui context and apply retro theme
   ```

### Session 2: UI Implementation

**User**: Please read docs/agent/ and continue.

**Agent**:
1. Reads PROJECT_STATUS.md
2. Sees "In Progress: Integrate ImGui + GLFW"
3. Continues from 30% progress
4. Completes ImGui integration
5. Applies retro Mac theme
6. Updates status to completed
7. Starts next task: FFmpeg decoder

### Session 3: Bug Fix

**User**: There's a crash when opening large videos. Please investigate.

**Agent**:
1. Adds to PROJECT_STATUS.md "Known Issues":
   ```markdown
   | #001 | Crash on large videos | High | Investigating | 2026-03-10 |
   ```
2. Investigates and finds memory issue
3. Records in CONTEXT.md:
   ```markdown
   ### Debug #001: Large Video Crash
   **Problem**: Out of memory when loading 4K video
   **Attempted**: Increased buffer size - didn't help
   **Solution**: Implemented streaming decoder
   **Code**: src/video/decoder.cpp:145-180
   ```
4. Updates issue status to "Resolved"

---

## Example 2: Web API Project

### Initial Setup

```bash
cd ~/projects/myapi
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "MyAPI" \
  --description "RESTful API for task management" \
  --tech-stack "Python,FastAPI,PostgreSQL,Docker"
```

### Session 1: Database Schema

**Agent Progress**:
```markdown
## ✅ Completed
- [x] Database schema designed
- [x] SQLAlchemy models created
- [x] Alembic migrations set up

## 📝 Context Recorded
- Database design decisions in CONTEXT.md
- ER diagram in docs/agent/database-schema.png
```

### Session 2: API Endpoints

**Agent Progress**:
```markdown
## ✅ Completed
- [x] User CRUD endpoints
- [x] Task CRUD endpoints
- [x] Authentication middleware

## 🚧 In Progress
**Task**: Implement task assignment endpoint
**Progress**: 70% - Logic done, tests pending
**Files**: api/routes/tasks.py, tests/test_tasks.py
```

---

## Example 3: Machine Learning Pipeline

### Initial Setup

```bash
cd ~/projects/ml-pipeline
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "ML Pipeline" \
  --description "Automated ML training pipeline" \
  --tech-stack "Python,PyTorch,MLflow,Airflow"
```

### Multi-Agent Collaboration

**Agent A** (Data Processing):
```markdown
## 🚧 In Progress (Agent A)
**Task**: Data preprocessing pipeline
**Progress**: 80%
**Files**: src/preprocessing/pipeline.py
**Next**: Add data validation step
```

**Agent B** (Model Training):
```markdown
## 🚧 In Progress (Agent B)
**Task**: Model training script
**Progress**: 60%
**Files**: src/training/trainer.py
**Blocked By**: Waiting for data pipeline completion
```

### Merge and Integration

After both complete:
```markdown
## ✅ Completed
- [x] Data preprocessing pipeline (Agent A)
- [x] Model training script (Agent B)

## 🚧 In Progress
**Task**: Integration testing
**Progress**: 0%
**Next**: Test end-to-end pipeline
```

---

## Example 4: Mobile App Backend

### Architecture Change

**Original Plan**: Monolithic architecture

**Change Decision** (in CONTEXT.md):
```markdown
### Architecture Change #001: Microservices

**Date**: 2026-03-10
**Reason**: Scalability requirements increased
**Impact**:
- Split into 3 services: Auth, API, Notifications
- Add message queue (RabbitMQ)
- Update deployment strategy

**Migration Plan**:
1. Extract Auth service
2. Extract Notifications service
3. Refactor API service
4. Set up message queue
5. Update tests
```

**Updated PROJECT_STATUS.md**:
```markdown
## Phase 2: Microservices Migration

### TODO (Prioritized)
1. Extract Auth service (High)
2. Set up RabbitMQ (High)
3. Extract Notifications service (Medium)
4. Update API service (Medium)
5. Integration tests (High)
```

---

## Example 5: Game Development

### Initial Setup

```bash
cd ~/projects/retro-game
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "RetroGame" \
  --description "2D platformer with retro graphics" \
  --tech-stack "C++,SDL2,Box2D,Tiled"
```

### Feature Development Cycle

**Week 1**:
```markdown
## ✅ Completed
- [x] Game engine core
- [x] Sprite rendering
- [x] Input handling

## 📊 Progress: 20%
```

**Week 2**:
```markdown
## ✅ Completed
- [x] Physics integration (Box2D)
- [x] Collision detection
- [x] Player movement

## 📊 Progress: 40%
```

**Week 3**:
```markdown
## ✅ Completed
- [x] Level loading (Tiled)
- [x] Enemy AI
- [x] Sound system

## 📊 Progress: 60%
```

### Bug Tracking

```markdown
## 🐛 Known Issues

| ID | Description | Severity | Status | Date |
|----|-------------|----------|--------|------|
| #001 | Player falls through floor | High | Resolved | 2026-03-10 |
| #002 | Sound crackling on Linux | Medium | Investigating | 2026-03-11 |
| #003 | Memory leak in level loader | High | Resolved | 2026-03-12 |
```

---

## Example 6: Documentation Website

### Initial Setup

```bash
cd ~/projects/docs-site
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "Documentation Site" \
  --description "Technical documentation with search" \
  --tech-stack "Next.js,MDX,Algolia,Vercel"
```

### Content-Driven Development

**PROJECT_STATUS.md**:
```markdown
## Phase 1: Core Features

### ✅ Completed
- [x] Next.js setup
- [x] MDX integration
- [x] Basic layout

### 🚧 In Progress
**Task**: Implement search with Algolia
**Progress**: 50%
**Files**: components/Search.tsx, lib/algolia.ts

### 📝 TODO
- [ ] Add code syntax highlighting
- [ ] Implement dark mode
- [ ] Add table of contents
- [ ] Deploy to Vercel
```

**CONTEXT.md** (Content Notes):
```markdown
## Content Structure

### Documentation Sections
1. Getting Started
2. API Reference
3. Guides
4. Examples

### Writing Guidelines
- Use MDX for interactive examples
- Include code snippets with syntax highlighting
- Add "Try it" buttons where applicable
```

---

## Example 7: DevOps Automation

### Initial Setup

```bash
cd ~/projects/devops-tools
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "DevOps Automation" \
  --description "Infrastructure automation scripts" \
  --tech-stack "Python,Terraform,Ansible,AWS"
```

### Infrastructure as Code

**PROJECT_STATUS.md**:
```markdown
## Phase 1: AWS Infrastructure

### ✅ Completed
- [x] VPC setup (Terraform)
- [x] ECS cluster (Terraform)
- [x] RDS database (Terraform)

### 🚧 In Progress
**Task**: CI/CD pipeline (GitHub Actions)
**Progress**: 70%
**Files**: .github/workflows/deploy.yml

### 📝 Technical Decisions

#### Decision #001: ECS vs EKS
**Date**: 2026-03-10
**Choice**: ECS
**Reason**: Simpler for our use case, lower cost
**Trade-off**: Less Kubernetes ecosystem benefits
```

---

## Example 8: Data Analysis Tool

### Initial Setup

```bash
cd ~/projects/data-analyzer
python /path/to/skill/scripts/init_project.py \
  --project-dir . \
  --project-name "Data Analyzer" \
  --description "Interactive data analysis dashboard" \
  --tech-stack "Python,Pandas,Plotly,Streamlit"
```

### Iterative Development

**Session 1**: Data loading
**Session 2**: Basic visualizations
**Session 3**: Interactive filters
**Session 4**: Export functionality

**CONTEXT.md** (Performance Notes):
```markdown
## Performance Optimization

### Optimization #001: Large Dataset Handling
**Date**: 2026-03-10
**Problem**: Slow loading for 1M+ rows
**Solution**: Implemented chunked loading + caching
**Result**: 10x faster load time
**Code**: src/data/loader.py:45-80
```

---

## Common Patterns Across Examples

### 1. Clear Task Breakdown
All examples show tasks broken into small, manageable pieces.

### 2. Progress Tracking
Every session updates progress percentage and next steps.

### 3. Context Recording
Important decisions and solutions are documented in CONTEXT.md.

### 4. Issue Management
Bugs and blockers are tracked in "Known Issues" table.

### 5. Seamless Handoffs
Each session ends with clear status for next session.

---

## Tips from Real Usage

### Tip 1: Start Small
Don't try to document everything upfront. Start with basics and expand as needed.

### Tip 2: Update Frequently
Update PROJECT_STATUS.md after each significant change, not just at session end.

### Tip 3: Use Checklists
Break complex tasks into checkboxes for easy progress tracking.

### Tip 4: Link Everything
Cross-reference between documents (PROJECT_STATUS ↔ CONTEXT ↔ Code).

### Tip 5: Keep It Current
Remove obsolete information regularly to avoid confusion.

---

**Remember**: These are real patterns that work. Adapt them to your project!
