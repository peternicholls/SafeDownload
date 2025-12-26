# Development Organization Guide

This document explains the structure of the `dev/` folder and how to use it for SafeDownload development.

## Folder Structure

```
dev/
├── README.md                 # This file - development organization guide
├── SPRINT_PLANNING_GUIDE.md  # Detailed sprint planning workflow
├── roadmap.yaml              # Master roadmap with all releases (v0.1.0 → v2.0.0)
├── architecture/             # Architecture design documents
│   ├── core-migration.md     # Go core migration plan (v1.0.0)
│   ├── state-schema.md       # State schema versioning strategy
│   └── tui-stack.md          # Bubble Tea TUI design (v1.1.0)
├── specs/                    # Feature specifications
│   ├── feature-template.yaml # Template for new feature specs
│   └── features/             # Individual feature specs
│       ├── F006-security-posture.yaml
│       └── F007-privacy.yaml (to be created)
├── sprints/                  # Sprint planning documents
│   ├── sprint-template.yaml  # Template for sprint planning
│   └── sprint-01.yaml        # Sprint 1 plan (to be created)
├── checklists/               # Quality gate checklists
│   └── accessibility.md      # Accessibility testing checklist
└── standards/                # Development standards
    ├── documentation.md      # Code documentation guidelines
    └── testing.md            # Testing requirements and best practices
```

## How to Use This Structure

### 1. Planning a New Feature

**Step 1**: Check `roadmap.yaml` for the feature

```bash
# Find feature F006 in roadmap.yaml
grep -A 10 "id: F006" dev/roadmap.yaml
```

**Step 2**: Create feature spec from template

```bash
cp dev/specs/feature-template.yaml dev/specs/features/F007-privacy.yaml

# Edit with feature details
vim dev/specs/features/F007-privacy.yaml

# Fill in required sections:
# - metadata (id, name, version, story_points)
# - description
# - user_stories with acceptance_criteria
# - constitution_compliance (principles and gates)
# - implementation (packages, CLI changes)
# - testing (unit, integration, e2e)
```

**Step 3**: Align with constitution

- Check `.specify/memory/constitution.md` for applicable principles
- Add principle references to feature spec
- Define constitution gates (performance, security, a11y)

### 2. Sprint Planning

**Step 1**: Create sprint YAML from features

```bash
# Example: Sprint 1 with F006 and F007
cat > dev/sprints/sprint-01.yaml <<EOF
metadata:
  sprint: 1
  version: "0.2.0"
  start_date: "2026-01-06"
  end_date: "2026-01-17"
  goal: "Security and privacy hardening"

features:
  - F006  # Security Posture (8 SP)
  - F007  # Privacy & Data Minimization (5 SP)

velocity:
  planned_story_points: 13
EOF
```

**Step 2**: Break features into tasks

- Use feature specs (`dev/specs/features/F006-*.yaml`) to create task list
- Assign tasks to sprint days
- Track progress daily

### 3. Implementing a Feature

**Step 1**: Read feature spec

```bash
# Read full spec for F006
cat dev/specs/features/F006-security-posture.yaml
```

**Step 2**: Follow implementation section

- Check `implementation.packages` for files to create/modify
- Check `implementation.cli` for new flags/commands
- Check `implementation.schema_changes` for state/config updates

**Step 3**: Write tests FIRST (TDD)

- Refer to `testing` section in feature spec
- Follow `dev/standards/testing.md` for test structure
- Run tests: `make test`

**Step 4**: Document as you code

- Follow `dev/standards/documentation.md` for GoDoc/docstring format
- Reference constitution principles in code comments
- Update README/CHANGELOG per `documentation` section in feature spec

### 4. Validating Constitution Compliance

**Before merge**:

```bash
# Check constitution compliance
# 1. Performance gates
go test -bench=BenchmarkTUIStartup ./pkg/ui/
# Must be <500ms

# 2. Security gates
go test ./tests/security/
# All must pass

# 3. Accessibility gates (if TUI changes)# Follow accessibility checklist
cat dev/checklists/accessibility.md# Manual test with high-contrast mode
safedownload --theme high-contrast

# 4. Code coverage
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep total
# Must be ≥80%
```

### 5. Creating Architecture Documents

**When**: Major architectural changes (e.g., Go migration, new subsystem)

**Template**:

```markdown
---
title: "Architecture Decision"
version: "X.Y.Z"
status: "planned | active | deprecated"
constitution: "v1.5.0"
principles:
  - "Principle Roman Numeral: Name"
---

# Architecture Title

## Executive Summary
[What, why, constitution alignment]

## Goals
### Primary
- ✅ Goal 1
- ✅ Goal 2

### Secondary
- ✅ Goal 3

## Architecture
[Diagrams, package structure, key types]

## Migration Strategy
[Phases, timeline, risks]

## Success Criteria
[How to measure success]

## Future Foundation
[What this enables]
```

**Examples**:
- `dev/architecture/core-migration.md` (Go core)
- `dev/architecture/state-schema.md` (Schema versioning)

### 6. Release Process

**Step 1**: Update VERSION.yaml

```yaml
version: "0.2.0"
release_date: "2026-01-31"
codename: "Shield"
notes: "Security and privacy hardening"
```

**Step 2**: Update CHANGELOG.md

```markdown
## [0.2.0] - 2026-01-31

### Added
- HTTPS-only enforcement (F006, Principle X)
- /purge command (F007, Principle IX)
...
```

**Step 3**: Tag release

```bash
git tag -a v0.2.0 -m "Release v0.2.0: Shield"
git push origin v0.2.0
```

**Step 4**: Update roadmap status

```yaml
# In dev/roadmap.yaml
- version: "0.2.0"
  status: completed  # was: planned
  release_date: "2026-01-31"
```

## Quick Reference

### File Naming Conventions

- Feature specs: `F###-feature-name.yaml` (e.g., `F006-security-posture.yaml`)
- Sprint plans: `sprint-##.yaml` (e.g., `sprint-01.yaml`)
- Architecture docs: `feature-name.md` (e.g., `core-migration.md`)

### YAML vs Markdown

- **Use YAML for**: Structured data (roadmap, feature specs, sprint plans)
- **Use Markdown for**: Narrative docs (architecture, standards, guides)

**Why YAML for specs**: Precise, minimal prose, easy to parse, grep-friendly

**Why Markdown for architecture**: Complex explanations, diagrams, code examples

### Constitution References

Always reference constitution in specs:

```yaml
constitution_compliance:
  principles:
    - id: "X"
      name: "Security Posture"
      notes: "HTTPS-only enforcement"
  
  gates:
    - gate: "Security"
      requirement: "No credentials in logs"
      test: "TestNoCredentialsInLogs"
```

### Common Workflows

**Add a new feature**:
```bash
# 1. Check roadmap
grep -i "feature name" dev/roadmap.yaml

# 2. Create spec from template
cp dev/specs/feature-template.yaml dev/specs/features/F###-name.yaml

# 3. Fill in spec (use F006 as reference)
vim dev/specs/features/F###-name.yaml

# 4. Add to sprint plan
echo "  - F###  # Feature Name (8 SP)" >> dev/sprints/sprint-01.yaml

# 5. Verify accessibility requirements (if TUI changes)
cat dev/checklists/accessibility.md
```

**Start a sprint**:
```bash
# 1. Read sprint planning guide
cat dev/SPRINT_PLANNING_GUIDE.md

# 2. Create sprint plan from template
cp dev/sprints/sprint-template.yaml dev/sprints/sprint-01.yaml

# 3. Add features from roadmap
vim dev/sprints/sprint-01.yaml

# 4. Break into tasks (use feature specs)
# See dev/SPRINT_PLANNING_GUIDE.md for detailed workflow

# 5. Track progress daily (update sprint YAML)
```

**Review before merge**:
```bash
# 1. Tests pass
make test

# 2. Coverage >80%
make coverage

# 3. Documentation updated
git diff README.md CHANGELOG.md

# 4. Constitution gates met
# Check feature spec's `constitution_compliance.gates`
```

## Integration with .specify/

The `dev/` folder complements `.specify/` but serves different purposes:

| Folder | Purpose | Audience | Format |
|--------|---------|----------|--------|
| `.specify/` | Spec-kit workflow templates, constitution | AI agents, maintainers | Markdown templates |
| `dev/` | Project roadmap, feature specs, standards | Developers, contributors | YAML + Markdown docs |

**Workflow**:
1. `.specify/memory/constitution.md` defines principles
2. `dev/roadmap.yaml` defines releases and features
3. `dev/specs/features/` defines implementation details
4. `.specify/templates/` used for new feature branches (via `/speckit.specify`)

## Tips

- **Keep specs up-to-date**: When implementation deviates, update the spec
- **Cross-reference**: Link between roadmap ↔ feature specs ↔ sprints
- **Version everything**: Specs have version field matching target release
- **Constitution-first**: Always start with constitution compliance section
- **YAML for speed**: Specs in YAML = easy to grep, parse, and review

## Tools

**Recommended**:
- YAML linter: `yamllint dev/**/*.yaml`
- YAML query: `yq '.features[] | select(.id == "F006")' dev/roadmap.yaml`
- Markdown linter: `markdownlint dev/**/*.md`
- Constitution check: `grep -r "Principle" dev/specs/features/`
- Sprint progress: `yq '.daily_log' dev/sprints/sprint-01.yaml`
- Roadmap query: `yq '.releases[] | select(.status == "planned")' dev/roadmap.yaml`

**VS Code Extensions**:
- YAML (Red Hat)
- Markdown All in One
- markdownlint

## See Also

- **[INDEX.md](INDEX.md)** - Quick reference index to all dev/ documents
- **[SPRINT_PLANNING_GUIDE.md](SPRINT_PLANNING_GUIDE.md)** - Detailed sprint planning workflow
- **[roadmap.yaml](roadmap.yaml)** - Product roadmap (v0.1.0 → v2.0.0)
- **[Constitution](../.specify/memory/constitution.md)** - Project principles and guidelines

---

**Last Updated**: 2025-12-26  
**Constitution**: v1.5.0  
**Roadmap**: dev/roadmap.yaml
