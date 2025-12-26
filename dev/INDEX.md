# Development Documentation Index

Quick reference guide to all planning and architecture documents in `dev/`.

**Last Updated**: 2025-12-26  
**Constitution**: v1.5.0

## Quick Start

**New to the project?** Start here:
1. Read [README.md](README.md) - Development organization overview
2. Review [../README.md](../README.md) - Project README
3. Check [roadmap.yaml](roadmap.yaml) - Product roadmap
4. Browse [constitution](../.specify/memory/constitution.md) - Project principles

**Planning a sprint?** 
1. Read [SPRINT_PLANNING_GUIDE.md](SPRINT_PLANNING_GUIDE.md)
2. Copy [sprints/sprint-template.yaml](sprints/sprint-template.yaml)
3. Select features from [roadmap.yaml](roadmap.yaml)

**Implementing a feature?**
1. Read feature spec in `specs/features/F###-*.yaml`
2. Follow [standards/testing.md](standards/testing.md)
3. Follow [standards/documentation.md](standards/documentation.md)

## Document Inventory

### Planning Documents

| File | Purpose | When to Use |
|------|---------|-------------|
| [README.md](README.md) | Development organization guide | Understanding dev/ folder structure |
| [SPRINT_PLANNING_GUIDE.md](SPRINT_PLANNING_GUIDE.md) | Sprint planning workflow | Planning a 2-week sprint |
| [roadmap.yaml](roadmap.yaml) | Product roadmap (v0.1→v2.0) | Feature prioritization, release planning |

### Architecture Documents

| File | Status | Purpose |
|------|--------|---------|
| [architecture/core-migration.md](architecture/core-migration.md) | Planned | Go core migration (v1.0.0) |
| [architecture/state-schema.md](architecture/state-schema.md) | Active | State schema versioning strategy |
| [architecture/tui-stack.md](architecture/tui-stack.md) | Planned | Bubble Tea TUI design (v1.1.0) |

### Feature Specifications

| File | Purpose |
|------|---------|
| [specs/feature-template.yaml](specs/feature-template.yaml) | Template for new feature specs |
| [specs/features/F006-security-posture.yaml](specs/features/F006-security-posture.yaml) | Example: Security posture feature |
| specs/features/F007-*.yaml | (To be created) |

### Sprint Plans

| File | Purpose |
|------|---------|
| [sprints/sprint-template.yaml](sprints/sprint-template.yaml) | Template for sprint planning |
| sprints/sprint-01.yaml | (To be created during sprint planning) |

### Checklists

| File | Purpose | When to Use |
|------|---------|-------------|
| [checklists/accessibility.md](checklists/accessibility.md) | Accessibility testing checklist | Before merging TUI changes |

### Standards & Guidelines

| File | Purpose | Audience |
|------|---------|----------|
| [standards/documentation.md](standards/documentation.md) | Code documentation standards | All developers |
| [standards/testing.md](standards/testing.md) | Testing requirements | All developers |

## Workflows by Role

### Product Planning

**Goal**: Define what to build and when

1. Review [roadmap.yaml](roadmap.yaml) for upcoming releases
2. Create feature specs using [specs/feature-template.yaml](specs/feature-template.yaml)
3. Prioritize features (P1 > P2 > P3)
4. Align with constitution principles

**Output**: Feature specs in `specs/features/`

### Sprint Planning

**Goal**: Plan a 2-week sprint

1. Read [SPRINT_PLANNING_GUIDE.md](SPRINT_PLANNING_GUIDE.md)
2. Select features from [roadmap.yaml](roadmap.yaml)
3. Copy [sprints/sprint-template.yaml](sprints/sprint-template.yaml)
4. Break features into tasks
5. Define constitution gates

**Output**: Sprint plan in `sprints/sprint-NN.yaml`

### Feature Development

**Goal**: Implement a feature

1. Read feature spec: `specs/features/F###-*.yaml`
2. Follow implementation section for package structure
3. Write tests per [standards/testing.md](standards/testing.md)
4. Document per [standards/documentation.md](standards/documentation.md)
5. Verify constitution gates

**Output**: Working code + tests + documentation

### Architecture Design

**Goal**: Design a major system change

1. Review existing architecture docs in `architecture/`
2. Create new architecture doc (Markdown with YAML frontmatter)
3. Include: Executive Summary, Goals, Architecture, Migration, Success Criteria
4. Reference constitution principles
5. Get feedback via PR review

**Output**: Architecture doc in `architecture/`

### Quality Assurance

**Goal**: Ensure code meets standards

1. Run tests per [standards/testing.md](standards/testing.md)
2. Check accessibility per [checklists/accessibility.md](checklists/accessibility.md)
3. Verify documentation per [standards/documentation.md](standards/documentation.md)
4. Confirm constitution gates pass

**Output**: Quality-approved code ready for merge

## Document Relationships

```
roadmap.yaml
  ├─> Feature Specs (specs/features/F###-*.yaml)
  │     ├─> Implementation packages
  │     ├─> Testing requirements
  │     └─> Documentation updates
  │
  └─> Sprint Plans (sprints/sprint-NN.yaml)
        ├─> Tasks (breakdown of features)
        ├─> Daily logs (progress tracking)
        └─> Retrospective (lessons learned)

Architecture Docs (architecture/*.md)
  ├─> Inform feature specs
  └─> Guide implementation

Standards (standards/*.md)
  ├─> Apply to all code
  └─> Enforced in CI/CD

Checklists (checklists/*.md)
  └─> Quality gates before merge
```

## Finding Information

### "How do I...?"

**Plan a new feature?**
→ [README.md § Planning a New Feature](README.md#1-planning-a-new-feature)

**Start a sprint?**
→ [SPRINT_PLANNING_GUIDE.md](SPRINT_PLANNING_GUIDE.md)

**Understand the Go migration?**
→ [architecture/core-migration.md](architecture/core-migration.md)

**Know what version to use for a feature?**
→ [roadmap.yaml](roadmap.yaml) (find feature, check `version` field)

**Write good documentation?**
→ [standards/documentation.md](standards/documentation.md)

**Test accessibility?**
→ [checklists/accessibility.md](checklists/accessibility.md)

### "Where is...?"

**The feature template?**
→ [specs/feature-template.yaml](specs/feature-template.yaml)

**The sprint template?**
→ [sprints/sprint-template.yaml](sprints/sprint-template.yaml)

**The testing standards?**
→ [standards/testing.md](standards/testing.md)

**The project roadmap?**
→ [roadmap.yaml](roadmap.yaml)

**The constitution?**
→ [../.specify/memory/constitution.md](../.specify/memory/constitution.md)

## Conventions

### File Naming

- **Feature specs**: `F###-short-name.yaml` (e.g., `F006-security-posture.yaml`)
- **Sprint plans**: `sprint-NN.yaml` (e.g., `sprint-01.yaml`)
- **Architecture docs**: `descriptive-name.md` (e.g., `core-migration.md`)
- **Checklists**: `topic.md` (e.g., `accessibility.md`)

### Versioning

- **App versions**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Schema versions**: Independent semantic versioning (documented in specs)
- **Constitution**: Version tracked in constitution document

### Status Labels

**For features**:
- `planned` - Not started yet
- `in_progress` - Currently being worked on
- `completed` - Fully implemented and shipped
- `blocked` - Waiting on dependency

**For sprints**:
- `not_started` - Sprint hasn't begun
- `active` - Sprint in progress
- `completed` - Sprint finished with retrospective

## Maintenance

### Updating This Index

Update when:
- New documents added to `dev/`
- Document purposes change
- New workflows identified
- Dead links found

### Document Review Schedule

| Document Type | Review Frequency |
|---------------|------------------|
| Roadmap | Monthly or per release |
| Architecture | Per major version (v1.0, v2.0) |
| Standards | Quarterly |
| Checklists | Per sprint retrospective |
| Templates | When process changes |

## External References

- [Constitution](../.specify/memory/constitution.md) - Project principles
- [Main README](../README.md) - User-facing documentation
- [CHANGELOG](../CHANGELOG.md) - Release history
- [CONTRIBUTING](../CONTRIBUTING.md) - Contribution guidelines (when created)

---

**Questions?** Open a GitHub issue or discussion.  
**Contributing?** Follow [standards/documentation.md](standards/documentation.md) and [standards/testing.md](standards/testing.md).
