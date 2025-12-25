# Research Documentation

This directory contains all research artifacts for SafeDownload development, organized by topic area.

**Created**: 2025-12-25  
**Constitution**: v1.5.0  
**Status**: Active

## Purpose

Research is a critical pre-implementation phase that reduces risk, identifies optimal solutions, and ensures constitution compliance. This directory provides:

1. **Structured Research Planning** - Clear goals, sources, and success criteria
2. **Knowledge Capture** - Findings, links, decisions, and attributions
3. **Decision Tracking** - How and why choices were made
4. **Feedback Loop** - Integration of research into specifications and plans

## Directory Structure

```
dev/research/
├── README.md                           # This file
├── MASTER.md                           # Consolidated research overview
├── research-plan.yaml                  # Master checklist and timeline
├── research-template.yaml              # Template for new research areas
├── decision-log.yaml                   # Record of decisions made
├── feedback-integration.yaml           # How research feeds into planning
│
├── 01-go-http-client/                  # Go HTTP client libraries
│   ├── research.yaml                   # Research plan and findings
│   └── findings.md                     # Detailed notes
│
├── 02-bubble-tea-tui/                  # Bubble Tea TUI framework
│   ├── research.yaml
│   └── findings.md
│
├── 03-rate-limiting/                   # Rate limiting algorithms
│   ├── research.yaml
│   └── findings.md
│
├── 04-accessibility/                   # Accessible terminal UI patterns
│   ├── research.yaml
│   └── findings.md
│
├── 05-state-migration/                 # State migration strategies
│   ├── research.yaml
│   └── findings.md
│
├── 06-gpg-verification/                # GPG signature verification
│   ├── research.yaml
│   └── findings.md
│
├── 07-package-managers/                # Package manager publishing
│   ├── research.yaml
│   └── findings.md
│
├── 08-rest-api/                        # REST API design patterns
│   ├── research.yaml
│   └── findings.md
│
├── 09-plugin-system/                   # Plugin system architectures
│   ├── research.yaml
│   └── findings.md
│
└── 10-cross-platform/                  # Cross-platform distribution
    ├── research.yaml
    └── findings.md
```

## Workflow

### 1. Planning Phase
- Review `research-plan.yaml` for priorities and timeline
- Copy `research-template.yaml` to create new research areas
- Define clear goals, questions, and success criteria

### 2. Research Phase
- Investigate sources listed in `research.yaml`
- Document findings in `findings.md`
- Update `research.yaml` with status and discoveries

### 3. Decision Phase
- Record decisions in `decision-log.yaml`
- Link decisions to research findings
- Get approval if required (per constitution governance)

### 4. Integration Phase
- Update `feedback-integration.yaml` with impacts
- Create/update feature specs in `dev/specs/features/`
- Update architecture docs in `dev/architecture/`

## Research Priority Legend

| Priority | Meaning | Timeline |
|----------|---------|----------|
| P0 | Blocks implementation | Complete before sprint starts |
| P1 | High impact | Complete in first week of sprint |
| P2 | Important | Complete before feature implementation |
| P3 | Nice to have | Can proceed without, but improves quality |

## Research Agent

A specialized AI agent is available to conduct first-pass research automatically.

### Invoking the Agent

```
/speckit.research R01          # Research specific area
/speckit.research next         # Next priority area
/speckit.research version 1.0.0  # Next area for version
```

### Agent Capabilities

The research agent can:
- **Select** the next research area based on priority and version
- **Evaluate** libraries using GitHub data, documentation, code analysis
- **Answer** key questions with confidence levels and citations
- **Record** findings in structured YAML and Markdown formats
- **Propose** decisions with scoring against project criteria
- **Track** progress across all research areas

### Agent Files

| File | Location | Purpose |
|------|----------|---------|
| Agent Definition | `.github/agents/speckit.research.agent.md` | Full agent instructions |
| Prompt | `.github/prompts/speckit.research.prompt.md` | Activation prompt |
| Helper Script | `.specify/scripts/bash/research.sh` | Research management CLI |
| Tool Definitions | `.specify/tools/research-tools.yaml` | Custom tool guidance |

### Helper Script Usage

```bash
# Show status of all research areas
.specify/scripts/bash/research.sh status

# Get next research area as JSON
.specify/scripts/bash/research.sh select --json

# Get next research area for v1.0.0
.specify/scripts/bash/research.sh select --version 1.0.0

# Validate R01 has required files
.specify/scripts/bash/research.sh validate --id R01

# Get statistics
.specify/scripts/bash/research.sh stats
```

## Quick Links

- [Master Research Overview](MASTER.md)
- [Research Plan & Checklist](research-plan.yaml)
- [Research Template](research-template.yaml)
- [Decision Log](decision-log.yaml)
- [Feedback Integration](feedback-integration.yaml)
- [Constitution](../../.specify/memory/constitution.md)
- [Roadmap](../roadmap.yaml)

## Contributing

When adding research:
1. Use `research-template.yaml` as the basis
2. Follow the structured format for findings
3. Cite sources with URLs and access dates
4. Record decisions with rationale
5. Update `feedback-integration.yaml` with impacts

---

## Research Completion Workflow

When a research area is complete, the agent follows this workflow:

### 1. Validate Completion
- [ ] All key questions have answers with confidence ≥ MEDIUM
- [ ] At least one decision recorded in decision-log.yaml
- [ ] Summary section filled in research.yaml
- [ ] Executive summary written in findings.md

### 2. Update Status Files
- [ ] Update `research.yaml` metadata (status, actual_hours, completed date)
- [ ] Update `research-plan.yaml` statistics and checklist items
- [ ] Add decision to `decision-log.yaml` (if applicable)

### 3. Integration
- [ ] Identify feature specs that need updating
- [ ] Identify architecture docs that need updating
- [ ] Identify sprint tasks that are unblocked
- [ ] Update `feedback-integration.yaml` current_status

### 4. Handoff
- [ ] Generate completion report
- [ ] Suggest next research area
- [ ] Offer to update affected specs/plans
