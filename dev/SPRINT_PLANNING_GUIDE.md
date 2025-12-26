# Sprint Planning Guide

**Constitution**: v1.5.0 - Development Workflow  
**Purpose**: Guide for planning and executing 2-week sprints  
**Audience**: Maintainers, contributors

## Overview

SafeDownload uses 2-week sprints to deliver features incrementally while maintaining constitution compliance and quality gates.

## Sprint Cycle

### Timeline
- **Duration**: 2 weeks (10 working days)
- **Cadence**: Continuous (Sprint N+1 starts immediately after Sprint N)
- **Velocity**: 20-25 story points per sprint (single developer)

### Ceremonies

| Ceremony | When | Duration | Purpose |
|----------|------|----------|---------|
| Sprint Planning | Day 1 | 2 hours | Select features, break into tasks |
| Daily Standup | Daily | 15 min | Progress update, blockers |
| Sprint Review | Last day (AM) | 1 hour | Demo completed features |
| Retrospective | Last day (PM) | 1 hour | Reflect and improve |

## Sprint Planning Process

### Step 1: Review Roadmap

**Input**: `dev/roadmap.yaml`

```bash
# Find features for target version
yq '.releases[] | select(.version == "0.2.0") | .features[]' dev/roadmap.yaml
```

**Output**: List of features with IDs, story points, priorities

### Step 2: Select Features for Sprint

**Criteria**:
- Sum of story points ≤ 25 (with 20% buffer)
- Dependencies resolved (prerequisite features completed)
- High-priority features first (P1 > P2 > P3)
- Constitution gates clearly defined

**Example Selection**:
```yaml
# Sprint 1 for v0.2.0
features:
  - F006: Security Posture (8 SP, P1)
  - F007: Privacy & Data Minimization (5 SP, P1)
  - F009: Error Handling (5 SP, P2)
Total: 18 SP (within 20-25 target with buffer)
```

### Step 3: Create Sprint YAML

```bash
# Copy template
cp dev/sprints/sprint-template.yaml dev/sprints/sprint-01.yaml

# Edit sprint-01.yaml
vim dev/sprints/sprint-01.yaml
```

**Fill in**:
- `metadata`: Sprint number, version, dates, goal
- `features`: Selected feature IDs from roadmap
- `capacity`: Team size, available days, planned story points

### Step 4: Break Features into Tasks

**For each feature**, consult its spec in `dev/specs/features/F###-*.yaml`:

**Example for F006 (Security Posture)**:
```yaml
tasks:
  # From F006 spec implementation section
  - id: "T006-001"
    feature: "F006"
    title: "Add --allow-http and --insecure flags to CLI parser"
    assignee: "@peternicholls"
    estimate: "1 SP"
    status: "not_started"
    day: 1
    
  - id: "T006-002"
    feature: "F006"
    title: "Implement HTTPS enforcement in download logic"
    assignee: "@peternicholls"
    estimate: "2 SP"
    status: "not_started"
    day: 2
    dependencies: ["T006-001"]
  
  # ... continue for all 8 SP
```

**Task Distribution**:
- Days 1-2: Setup and infrastructure
- Days 3-6: Core implementation
- Days 7-8: Testing
- Days 9-10: Documentation and polish

### Step 5: Dependency Audit

**Before the sprint can begin**, complete the dependency audit checklist in the sprint YAML:

**Dependency Audit Checklist**:

| Check | Description | How to Verify |
|-------|-------------|---------------|
| DEP-001 | All feature dependencies documented in spec files | Review each feature's `dependencies.internal` section |
| DEP-002 | Prerequisite features completed or in sprint | Cross-reference with `dev/specs/features/` status |
| DEP-003 | External dependencies available and licensed | Check library availability, verify license compatibility |
| DEP-004 | No circular dependencies | Draw dependency graph, ensure no cycles |
| DEP-005 | Task dependencies correctly sequenced | Verify task `dependencies` arrays in sprint YAML |

**Example Audit**:
```yaml
dependency_audit:
  completed: true
  completed_date: "2026-01-05"
  auditor: "@peternicholls"
  
  checks:
    - id: "DEP-001"
      status: "passed"
      notes: "F006 and F007 specs have complete dependency sections"
    
    - id: "DEP-002"
      status: "passed"
      notes: "F001-F005 completed in v0.1.0, no blockers"
    
    - id: "DEP-003"
      status: "passed"
      notes: "No new external deps for F006/F007, only curl (already required)"
    
    - id: "DEP-004"
      status: "passed"
      notes: "F006 ↛ F007, F007 ↛ F006 (independent features)"
    
    - id: "DEP-005"
      status: "passed"
      notes: "Task sequence verified: T006-001 → T006-002 → T006-003..."
  
  blockers_identified: []
```

**If blockers found**:
1. Document blocker in `blockers_identified`
2. Create resolution plan
3. Adjust sprint scope if necessary
4. Re-run audit after resolution

### Step 6: Validate Constitution Compliance

For each feature, identify **gates** from spec:

```yaml
# In sprint-01.yaml
retrospective:
  constitution_compliance:
    gates_passed:
      - "F006: HTTPS-only enforcement ✅"
      - "F006: No credentials in logs ✅"
      - "F007: /purge command removes all data ✅"
    gates_failed: []
```

**Gates must be defined BEFORE sprint starts** (from feature spec).

### Step 7: Commit Sprint Plan

```bash
git add dev/sprints/sprint-01.yaml
git commit -m "docs: Sprint 1 planning for v0.2.0"
git push
```

## Daily Sprint Execution

### Daily Standup (Self or Team)

**Format**: 3 questions
1. What did I complete yesterday?
2. What will I work on today?
3. Any blockers?

**Update sprint YAML**:
```yaml
daily_log:
  day_1:
    date: "2026-01-06"
    completed_tasks: ["T006-001"]
    blockers: []
    notes: "CLI flag parsing straightforward"
```

### Working on Tasks

**Workflow**:
1. Pick next task from sprint plan (follow `day` sequence)
2. Update task status to `in_progress`
3. Implement (follow feature spec)
4. Write tests (TDD encouraged)
5. Run constitution gates
6. Update task status to `completed`
7. Commit with semantic message

**Commit Message Format**:
```bash
git commit -m "feat(F006): implement HTTPS-only enforcement

- Add HTTPS check before download
- Add --allow-http flag for override
- Log security warning when HTTP allowed

Refs: T006-002
Constitution: Principle X (Security Posture)
"
```

### Handling Blockers

**If blocked**:
1. Document blocker in `daily_log`
2. Update task status to `blocked`
3. Move to next independent task
4. Resolve blocker ASAP (ask for help, research, spike)

**Example**:
```yaml
day_3:
  date: "2026-01-08"
  completed_tasks: []
  blockers:
    - task: "T006-003"
      issue: "TLS verification requires OpenSSL, not available on macOS"
      resolution_plan: "Use Go crypto/tls instead of curl for v1.0.0"
```

## Sprint Review (Last Day AM)

### Prepare Demo

**What to demo**:
- Completed features (end-to-end user scenarios)
- Constitution gates passing
- Updated documentation

**Demo Script**:
```bash
# F006: Security Posture Demo
# 1. Show HTTPS enforcement
safedownload http://example.com/file.txt
# Expected: Error "HTTPS required. Use --allow-http to allow HTTP."

# 2. Show --allow-http with warning
safedownload http://example.com/file.txt --allow-http
# Expected: Download succeeds, warning logged

# 3. Show credential sanitization
cat ~/.safedownload/safedownload.log
# Expected: No passwords visible
```

### Update Sprint YAML

```yaml
review:
  completed_story_points: 18
  velocity_percentage: 100 # (18 / 18) * 100
  features_completed: ["F006", "F007", "F009"]
  features_carried_over: []
  demo_notes: |
    Successfully demoed:
    - HTTPS-only enforcement (F006)
    - /purge command (F007)
    - Standardized exit codes (F009)
    
    All constitution gates passed.
```

## Sprint Retrospective (Last Day PM)

### Template

**What went well?**
```yaml
retrospective:
  what_went_well:
    - "HTTPS enforcement simpler than expected"
    - "TDD approach caught edge cases early"
    - "Documentation stayed in sync with code"
```

**What to improve?**
```yaml
  what_to_improve:
    - "TLS testing setup was manual, need fixtures"
    - "Underestimated credential sanitization (1 SP → 2 SP actual)"
    - "CHANGELOG updates batched at end, should be per-commit"
```

**Action items** (for next sprint):
```yaml
  action_items:
    - action: "Create TLS mock server helper in tests/fixtures/"
      owner: "@peternicholls"
      due_date: "2026-01-20" # Sprint 2, Day 1
      status: "pending"
    
    - action: "Update CONTRIBUTING.md: CHANGELOG per commit"
      owner: "@peternicholls"
      due_date: "2026-01-20"
      status: "pending"
```

### Velocity Analysis

**Formula**: `(completed_story_points / planned_story_points) * 100`

**Interpretation**:
- 100%: Perfect velocity (rare)
- 80-99%: Good velocity (expected range)
- <80%: Underperformance (analyze why)
- >100%: Overachievement (may indicate underestimation)

**Adjust next sprint**:
- If velocity <80%: Reduce planned story points
- If velocity >100%: Can increase planned story points

## Sprint Metrics

### Track in `metrics` section:

```yaml
metrics:
  burndown_chart: "dev/sprints/sprint-1-burndown.png"
  code_coverage: "83%" # From go test -coverprofile
  tests_passing: "145/145" # All tests pass
  bugs_found: 2
  bugs_fixed: 2
```

### Generate Burndown Chart (Optional)

Use a script or tool like `gh-sprint` to generate burndown:

```bash
# Example using simple script
python3 scripts/generate_burndown.py dev/sprints/sprint-01.yaml
# Outputs: dev/sprints/sprint-1-burndown.png
```

## Constitution Gates Checklist

**Before closing sprint, verify**:

### Performance Gates
```bash
# TUI startup <500ms
go test -bench=BenchmarkTUIStartup ./pkg/ui/ | grep "ns/op"

# Queue list <100ms (100 items)
go test -bench=BenchmarkQueueList_100Items ./pkg/queue/
```

### Security Gates
```bash
# HTTPS enforcement
go test ./tests/security/https_test.go

# No credentials in logs
go test ./tests/security/credential_leak_test.go
```

### Code Coverage
```bash
# Must be ≥80%
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep total
```

**Document results**:
```yaml
retrospective:
  constitution_compliance:
    gates_passed:
      - "Performance: TUI startup 287ms ✅ (<500ms)"
      - "Performance: Queue list 56ms ✅ (<100ms)"
      - "Security: HTTPS-only ✅"
      - "Security: No credentials logged ✅"
      - "Coverage: 83% ✅ (≥80%)"
    gates_failed: []
```

## Release Process (End of Sprint)

**If sprint completes a version (e.g., v0.2.0)**:

### Step 1: Update VERSION.yaml
```yaml
version: "0.2.0"
release_date: "2026-01-17"
codename: "Shield"
notes: "Security and privacy hardening"
```

### Step 2: Update CHANGELOG.md
```markdown
## [0.2.0] - 2026-01-17

### Added
- HTTPS-only enforcement (F006, Principle X)
- --allow-http flag for HTTP override (F006)
- /purge command (F007, Principle IX)
- Standardized exit codes (F009)

### Security
- TLS verification via system CA trust store (F006)
- Credential sanitization in logs (F006)

[0.2.0]: https://github.com/peternicholls/SafeDownload/releases/tag/v0.2.0
```

### Step 3: Tag Release
```bash
git tag -a v0.2.0 -m "Release v0.2.0: Shield

Security and privacy hardening sprint.

Features:
- F006: Security Posture
- F007: Privacy & Data Minimization
- F009: Error Handling & Exit Codes

Constitution: v1.5.0
All gates passed.
"
git push origin v0.2.0
```

### Step 4: Update Roadmap
```yaml
# In dev/roadmap.yaml
- version: "0.2.0"
  status: completed  # was: planned
  release_date: "2026-01-17"
```

## Common Pitfalls

### Pitfall 1: Overcommitting
**Symptom**: Planning 30+ story points for single-developer sprint

**Fix**: Stick to 20-25 SP with 20% buffer. Remember: documentation and testing count as work.

### Pitfall 2: Under-specified Tasks
**Symptom**: Tasks like "Implement feature" without breakdown

**Fix**: Tasks should be <1 day (≤5 SP). If >5 SP, break down further.

### Pitfall 3: Ignoring Constitution Gates
**Symptom**: Merging code without running benchmarks or security tests

**Fix**: Gates are **mandatory**. Add to CI pipeline to enforce.

### Pitfall 4: Documentation Debt
**Symptom**: "Will update docs later" → docs never updated

**Fix**: Documentation is part of Definition of Done. Code + tests + docs = completed task.

### Pitfall 5: Skipping Retrospectives
**Symptom**: Repeating same mistakes sprint after sprint

**Fix**: Retrospective action items are commitments. Track in next sprint.

## Tips for Success

1. **Start with highest-priority features** (P1 first)
2. **Write tests first** (TDD prevents rework)
3. **Commit frequently** (small atomic commits)
4. **Update sprint YAML daily** (track progress)
5. **Ask for help early** (don't stay blocked)
6. **Celebrate wins** (completed features, passing gates)

## Example Sprint Schedule

### Sprint 1 (v0.2.0)

**Week 1**:
- **Day 1 (Mon)**: Sprint planning, start T006-001 (CLI flags)
- **Day 2 (Tue)**: T006-002 (HTTPS enforcement), T006-003 (TLS verification)
- **Day 3 (Wed)**: T006-004 (Proxy support), T007-001 (/purge command)
- **Day 4 (Thu)**: T006-005 (Credential sanitization), T007-002 (Log rotation)
- **Day 5 (Fri)**: T009-001 (Exit codes), T009-002 (Retry logic)

**Week 2**:
- **Day 6 (Mon)**: T006-006 (Unit tests), T007-003 (Tests)
- **Day 7 (Tue)**: T006-007 (E2E tests), T009-003 (Tests)
- **Day 8 (Wed)**: T006-008 (README update), CHANGELOG
- **Day 9 (Thu)**: Polish, bug fixes, constitution gate verification
- **Day 10 (Fri)**: Sprint review (AM), retrospective (PM), release v0.2.0

## References

- [Scrum Guide](https://scrumguides.org/)
- [Story Points Estimation](https://www.mountaingoatsoftware.com/blog/what-are-story-points)
- Constitution: Development Workflow & Quality Gates
- Feature Template: `dev/specs/feature-template.yaml`
- Sprint Template: `dev/sprints/sprint-template.yaml`

---

**Last Updated**: 2025-12-25  
**Owner**: @peternicholls
