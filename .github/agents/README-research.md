# Research Agent (`/speckit.research`)

A specialized AI agent for conducting first-pass research on SafeDownload development topics. The agent evaluates libraries, researches patterns, answers technical questions, and produces structured findings that feed into project planning.

## Quick Start

```bash
# Research a specific area
/speckit.research R01

# Research the next priority area
/speckit.research next

# Research next area needed for a version
/speckit.research version 1.0.0
```

## Overview

The research agent automates the discovery phase of development by:

1. **Selecting** research areas based on priority and version targets
2. **Gathering** information from documentation, GitHub, and web sources
3. **Evaluating** libraries against project criteria
4. **Answering** key questions with confidence levels and citations
5. **Recording** findings in structured formats
6. **Proposing** decisions with scoring rationale
7. **Tracking** progress across all research areas

## Research Areas

| ID | Name | Priority | Version | Blocks |
|----|------|----------|---------|--------|
| R01 | Go HTTP Client Libraries | P0 | v1.0.0 | F011 |
| R02 | Bubble Tea TUI Framework | P0 | v1.1.0 | F014 |
| R03 | Rate Limiting Algorithms | P1 | v1.0.0 | F011 |
| R04 | Accessible Terminal UI Patterns | P1 | v0.2.0 | F008, F014 |
| R05 | State Migration Strategies | P1 | v1.0.0 | F010, F011 |
| R06 | GPG Signature Verification | P2 | v1.2.0 | F017 |
| R07 | Package Manager Publishing | P2 | v1.3.0 | F021-F023 |
| R08 | REST API Design Patterns | P3 | v2.0.0 | F025 |
| R09 | Plugin System Architectures | P3 | v1.2.0 | F020 |
| R10 | Cross-Platform Distribution | P1 | v1.0.0 | F013 |

**Priority Legend**: P0 (Critical) → P1 (High) → P2 (Medium) → P3 (Low)

## Agent Files

| File | Location | Purpose |
|------|----------|---------|
| Agent Definition | `.github/agents/speckit.research.agent.md` | Full agent instructions |
| Agent Prompt | `.github/prompts/speckit.research.prompt.md` | Activation prompt |
| Helper Script | `.specify/scripts/bash/research.sh` | CLI utilities |
| Tool Definitions | `.specify/tools/research-tools.yaml` | Custom tool guidance |
| Agent Context | `.specify/context/research-agent-context.yaml` | Complete context |

## Research Infrastructure

| File | Location | Purpose |
|------|----------|---------|
| Master Plan | `dev/research/research-plan.yaml` | All areas, checklists, timeline |
| Template | `dev/research/research-template.yaml` | Template for new areas |
| Decision Log | `dev/research/decision-log.yaml` | Decisions from research |
| Integration Plan | `dev/research/feedback-integration.yaml` | How research feeds into planning |
| Master Doc | `dev/research/MASTER.md` | Consolidated overview |

## Workflow

### 1. Selection

The agent selects a research area based on:

1. **Explicit ID**: `/speckit.research R01` → research R01
2. **Auto-select**: `/speckit.research next` → highest priority not-started area
3. **Version filter**: `/speckit.research version 1.0.0` → next area blocking v1.0.0

Priority order: P0 > P1 > P2 > P3, then earlier version, then lower R-number.

### 2. Research Brief

Before starting, the agent presents:

```markdown
## Research Brief: Go HTTP Client Libraries

**ID**: R01
**Target Version**: v1.0.0 Phoenix
**Priority**: P0 (Critical)
**Estimated Time**: 4 hours
**Blocks Features**: F011 (Go Core Library)

### Critical Questions
- [ ] Q1: Should we use grab library or stdlib net/http?
- [ ] Q2: How to implement range header requests for resume?
- [ ] Q3: Connection pooling strategy for parallel downloads?

### Sources to Investigate
- **Libraries**: grab (★3200), resty (★9000)
- **Documentation**: Go net/http package docs

Ready to begin research? (yes/continue/skip)
```

### 3. Research Execution

For each task, the agent:

**Library Evaluation**:
- Fetches GitHub metadata (stars, license, last update)
- Reads documentation and examples
- Checks dependencies
- Scores against decision criteria

**Pattern Research**:
- Searches authoritative sources
- Studies reference implementations
- Extracts code examples
- Documents pros/cons

**Documentation Review**:
- Identifies official docs
- Extracts relevant sections
- Notes version-specific info

### 4. Findings Recording

The agent updates two files per research area:

**`research.yaml`** - Structured data:
```yaml
key_questions:
  critical:
    - question: "Should we use grab or stdlib?"
      answer: "Recommend stdlib with custom wrapper"
      confidence: "HIGH"
      sources:
        - "https://pkg.go.dev/net/http"
```

**`findings.md`** - Detailed notes:
```markdown
## Library Evaluation

### grab (github.com/cavaliercoder/grab)

**Strengths**:
- Resume support built-in
- Progress callbacks

**Weaknesses**:
- Not actively maintained
```

### 5. Decision Proposal

When research produces a clear recommendation:

```yaml
decisions:
  - id: "D001"
    title: "HTTP Client Library Selection"
    category: "LIBRARY_SELECTION"
    research_id: "R01"
    status: "PROPOSED"
    
    options_considered:
      - name: "grab library"
        score: 65
      - name: "stdlib net/http"
        score: 85
    
    decision:
      selection: "stdlib net/http with custom wrapper"
      rationale: "Best aligns with constitution, proven stable"
```

### 6. Completion Report

```markdown
## Research Complete: R01 - Go HTTP Client Libraries

### Summary
- **Time Spent**: 3.5 hours (estimated: 4 hours)
- **Questions Answered**: 4/4
- **Confidence**: HIGH
- **Decision Proposed**: D001

### Next Steps
1. Review decision D001 for approval
2. Update feature spec F011
3. Continue to R03 (Rate Limiting)
```

## Helper Script

The research agent uses a helper script for status and selection:

```bash
# Show all research areas
.specify/scripts/bash/research.sh status

# JSON output
.specify/scripts/bash/research.sh status --json

# Select next priority area
.specify/scripts/bash/research.sh select

# Select next area for specific version
.specify/scripts/bash/research.sh select --version 1.0.0

# Validate research area has required files
.specify/scripts/bash/research.sh validate --id R01

# Show statistics
.specify/scripts/bash/research.sh stats
```

## Decision Criteria

The agent scores options against weighted criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Constitution Alignment | 25% | Adheres to project principles |
| Performance | 20% | Meets performance gates |
| Maintainability | 20% | Easy to maintain long-term |
| Developer Experience | 15% | Good DX for contributors |
| Community Support | 10% | Active community, docs |
| Dependency Footprint | 10% | Minimal dependencies |

**Pass threshold**: 60/100  
**Recommend threshold**: 75/100

## Constitution Alignment

The agent checks findings against constitution principles:

- **I**: Resumable Downloads (core feature)
- **II**: Optional Features (enhanced features optional)
- **V**: Privacy (no telemetry)
- **VIII**: Minimal Dependencies (prefer stdlib)
- **IX**: Accessibility (screen reader support)
- **X**: Security Posture (defense in depth)
- **XI**: Professional UX (high visual standards)

**Performance Gates**:
- TUI startup: <500ms
- List downloads: <100ms
- Resume calculation: <50ms

## Confidence Levels

| Level | Definition | When to Use |
|-------|------------|-------------|
| CERTAIN | 100% confident | Official docs, tested locally |
| HIGH | 90%+ confident | Multiple reliable sources agree |
| MEDIUM | 70-90% confident | Single good source |
| LOW | <70% confident | Limited or conflicting sources |

## Integration

When research completes, findings integrate into:

| Target | When | Update |
|--------|------|--------|
| Feature Specs | Library/architecture decision | Implementation section |
| Architecture Docs | Significant insight | Relevant section |
| Sprint Plans | Research unblocks tasks | Remove blockers |
| Decision Log | Clear recommendation | New decision entry |

## Handoffs

From the research agent, you can:

- **Continue research**: `/speckit.research next`
- **Create decision**: Finalize and add to decision log
- **Update plan**: `/speckit.plan` to incorporate findings
- **Start implementation**: `/speckit.implement` (after decisions approved)

## Troubleshooting

### "Research area not found"

```bash
# Check available areas
.specify/scripts/bash/research.sh status
```

### "Prerequisites missing"

Ensure research infrastructure exists:
```
dev/research/
├── research-plan.yaml
├── research-template.yaml
├── decision-log.yaml
└── {area-folder}/
    ├── research.yaml
    └── findings.md
```

### "Cannot answer question"

The agent will:
1. Mark confidence as LOW
2. Document what was tried
3. Add to "Open Questions" in findings.md
4. Suggest how to resolve (e.g., local testing)

## Best Practices

1. **Run in order**: Complete P0 areas before P1
2. **Verify decisions**: Review proposed decisions before implementation
3. **Update specs**: Integrate findings into feature specs promptly
4. **Track time**: Actual hours help improve estimates
5. **Cite sources**: Always include URLs and access dates

## Related Commands

| Command | Purpose |
|---------|---------|
| `/speckit.specify` | Create feature specification |
| `/speckit.plan` | Create implementation plan |
| `/speckit.tasks` | Generate task breakdown |
| `/speckit.implement` | Execute implementation |
| `/speckit.analyze` | Analyze spec consistency |
