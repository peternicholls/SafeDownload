# Speckit Research Agent - Generalization Plan

**Created**: 2025-12-28  
**Purpose**: Transform the SafeDownload-specific research agent into a generic, reusable research agent for any project  
**Status**: In Progress

---

## Executive Summary

The current `speckit.research` agent is tightly coupled to SafeDownload's specific research areas, constitution, and project structure. To make it work harmoniously with its sibling agents (specify, plan, tasks, implement, etc.) across any project, we need to:

1. **Extract project-specific context** from agent definition into project configuration
2. **Create generic research framework** that adapts to any project structure
3. **Define standard interfaces** that integrate with other speckit agents
4. **Document adaptation patterns** for different project types

---

## Current State Analysis

### What Works Well

✅ **Clear workflow structure**: Select → Brief → Execute → Record → Integrate  
✅ **Confidence-based answers**: LOW/MEDIUM/HIGH/CERTAIN framework  
✅ **Decision framework**: Weighted criteria scoring  
✅ **Integration hooks**: Files to update, handoffs to other agents  
✅ **Template-driven**: research.yaml and findings.md templates

### SafeDownload-Specific Dependencies

❌ **Hardcoded research areas**: R01-R10 are SafeDownload features  
❌ **Constitution references**: Assumes `.specify/memory/constitution.md` with specific principles  
❌ **File structure**: Hardcoded paths like `dev/research/`, `dev/specs/features/`  
❌ **Decision criteria**: Weights tailored to SafeDownload values (minimal deps, etc.)  
❌ **Performance gates**: Specific metrics like "<500ms startup"  
❌ **Feature blocking**: Assumes feature-based development (F001, F002, etc.)

---

## Speckit Agent Family

### Current Siblings

| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| **constitution** | Define project principles | User values | Constitution document |
| **specify** | Create feature specs | Feature description | spec.md + checklist |
| **clarify** | Resolve spec ambiguities | Spec with [NEEDS CLARIFICATION] | Clarified spec |
| **plan** | Create implementation plan | Feature spec | Technical plan |
| **tasks** | Break plan into tasks | Implementation plan | Task list |
| **implement** | Execute tasks | Task list | Working code |
| **analyze** | Validate consistency | Spec/plan/tasks | Analysis report |
| **checklist** | Generate QA checklists | Feature context | Checklist file |
| **taskstoissues** | Convert to GitHub issues | Task list | GitHub issues |

### Where Research Fits

**research** agent should:
- ✅ **Precede planning**: Inform technical decisions before `plan` agent runs
- ✅ **Integrate with constitution**: Align findings with project principles
- ✅ **Feed into specs**: Update feature specs with research outcomes
- ✅ **Inform tasks**: Unblock implementation by resolving unknowns
- ✅ **Produce decisions**: Create decision records for approval

---

## Generalization Strategy

### Phase 1: Configuration Schema

Create a project configuration file that replaces hardcoded SafeDownload context:

**File**: `.specify/config/research.yaml`

```yaml
# Research Agent Configuration
# Define how research works for this project

metadata:
  project_name: "SafeDownload"
  schema_version: "1.0.0"

# File paths (relative to project root)
paths:
  research_root: "dev/research"
  research_plan: "dev/research/research-plan.yaml"
  decision_log: "dev/research/decision-log.yaml"
  constitution: ".specify/memory/constitution.md"
  feature_specs: "dev/specs/features"
  architecture_docs: "dev/architecture"

# Decision criteria (project-specific values)
decision_criteria:
  weights:
    # Define criteria and their importance (must sum to 100)
    constitution_alignment: 25
    performance: 20
    maintainability: 20
    developer_experience: 15
    community_support: 10
    dependency_footprint: 10
  
  scoring:
    scale: "0-100"
    pass_threshold: 60
    recommend_threshold: 75

# Performance gates (optional - only if project has quantitative targets)
performance_gates:
  # Key: gate name, Value: threshold
  tui_startup: "<500ms"
  list_downloads: "<100ms"

# Research methodology preferences
methodology:
  confidence_levels: ["LOW", "MEDIUM", "HIGH", "CERTAIN"]
  
  # Source credibility ranking
  source_ranking:
    tier_1:
      - "Official documentation"
      - "Source code"
      - "Project maintainer communications"
    tier_2:
      - "Conference talks by experts"
      - "Technical blogs from known sources"
    tier_3:
      - "Community forums (Stack Overflow, etc.)"

  # Task types this project uses
  task_types:
    - library_evaluation
    - pattern_research
    - documentation_review
    - benchmark_comparison

# Integration with other speckit agents
integration:
  # Which agents can be called after research completes
  handoff_agents:
    - speckit.plan     # Update plans with findings
    - speckit.specify  # Update specs with decisions
    - speckit.analyze  # Validate research coverage

  # Where research findings go
  update_targets:
    - type: "feature_spec"
      pattern: "{feature_specs}/F{id}.yaml"
      section: "implementation"
    - type: "architecture"
      pattern: "{architecture_docs}/*.md"
    - type: "decision"
      pattern: "{decision_log}"
```

### Phase 2: Generic Research Area Schema

Update `research-template.yaml` to be project-agnostic:

**Remove**:
- Hardcoded feature IDs (F001, etc.) → Use dynamic feature references
- SafeDownload-specific constitution principles → Use generic principle IDs
- Specific version numbers (v1.0.0 Phoenix) → Use generic version placeholders

**Add**:
- `project_context` field for project-specific notes
- `research_type` taxonomy (library, pattern, tool, architecture)
- `stakeholder` field (who requested this research)

**Example**:

```yaml
metadata:
  id: "R001"
  name: "HTTP Client Selection"
  research_type: "library_evaluation"  # NEW
  target_version: "1.0.0"
  priority: "P0"
  stakeholder: "backend-team"  # NEW
  
  # Dynamic feature blocking (no hardcoded F-IDs)
  blocks:
    - id: "001"  # Project defines what "001" means
      name: "Core Download Engine"
      
  # Generic constitution alignment
  constitution_principles:
    - id: "minimal-dependencies"
      weight: "high"
    - id: "performance"
      weight: "medium"
```

### Phase 3: Agent Definition Updates

Update `.github/agents/speckit.research.agent.md`:

**Section 1: Configuration Loading**

```markdown
## Prerequisites

1. **Load Project Configuration**
   
   ```bash
   # Read research configuration for this project
   cat .specify/config/research.yaml
   ```
   
   Extract:
   - File paths for this project
   - Decision criteria weights
   - Performance gates (if any)
   - Integration targets

2. **Verify Research Infrastructure**
   
   Check that `paths.research_root` exists and contains:
   - `research-plan.yaml` (master list)
   - `research-template.yaml` (template)
   - `decision-log.yaml` (decisions)
   
   If missing, offer to create from templates.

3. **Load Constitution** (if exists)
   
   ```bash
   cat {paths.constitution}
   ```
   
   If no constitution exists, skip constitution alignment checks.
```

**Section 2: Dynamic Research Area Selection**

```markdown
## Research Area Selection

1. **Parse Arguments**:
   - Specific ID: `R001`, `R002`, etc.
   - Auto-select: `next`, `continue`
   - Version filter: `version X.Y.Z`
   - Research type filter: `type library_evaluation`

2. **Load Research Plan**:
   
   ```bash
   cat {paths.research_plan}
   ```
   
   Parse YAML to build available research areas dynamically.

3. **Apply Selection Logic**:
   - Priority order: P0 > P1 > P2 > P3
   - Within priority: earlier version first
   - Within version: lower R-number first
   - Filter by type if specified
```

**Section 3: Constitution Alignment (Optional)**

```markdown
## Constitution Alignment

**If `paths.constitution` exists**:

1. Load constitution document
2. Extract principle IDs and descriptions
3. For each research area, check `constitution_principles` field
4. Score alignment based on principle weights

**If no constitution**:

Skip constitution alignment scoring. Base decisions solely on:
- Performance benchmarks
- Community support
- Maintainability
- Developer experience
```

### Phase 4: Generic Helper Script

Update `.specify/scripts/bash/research.sh` to be project-agnostic:

```bash
#!/bin/bash
# Generic Research Helper Script
# Works with any project using speckit.research

# Load project configuration
CONFIG_FILE=".specify/config/research.yaml"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "ERROR: No research config found at $CONFIG_FILE"
    echo "Run 'speckit.research init' to create configuration"
    exit 1
fi

# Extract paths using yq or Python
RESEARCH_ROOT=$(yq '.paths.research_root' "$CONFIG_FILE")
RESEARCH_PLAN="$RESEARCH_ROOT/research-plan.yaml"

# Function: List all research areas
research_status() {
    if [[ ! -f "$RESEARCH_PLAN" ]]; then
        echo "No research plan found at $RESEARCH_PLAN"
        return 1
    fi
    
    # Parse research-plan.yaml dynamically
    yq '.research_areas[] | [.id, .name, .status, .priority] | @tsv' "$RESEARCH_PLAN" \
        | column -t -s $'\t'
}

# Function: Select next research area
research_select() {
    local version="$1"
    local type="$2"
    
    # Dynamic selection based on project's research areas
    # ...
}

# Execute command
case "$1" in
    status) research_status "$@" ;;
    select) research_select "$2" "$3" ;;
    init)   research_init ;;
    *)      research_help ;;
esac
```

---

## Adaptation Patterns

### Pattern 1: Web Application Project

```yaml
# .specify/config/research.yaml for a web app

paths:
  research_root: "docs/research"
  feature_specs: "specs"
  architecture_docs: "docs/architecture"

decision_criteria:
  weights:
    security: 30              # Higher for web apps
    scalability: 25           # Critical for web
    developer_experience: 20
    cost: 15                  # Cloud costs matter
    maintainability: 10

performance_gates:
  page_load: "<2s"
  api_response: "<200ms"
  time_to_interactive: "<3s"
```

### Pattern 2: Library/SDK Project

```yaml
# .specify/config/research.yaml for a library

paths:
  research_root: "research"
  architecture_docs: "docs/design"

decision_criteria:
  weights:
    api_design: 30            # Critical for libraries
    backward_compatibility: 25
    documentation: 20
    dependency_footprint: 15
    performance: 10

methodology:
  task_types:
    - api_design_research
    - ecosystem_compatibility
    - benchmark_comparison
```

### Pattern 3: Infrastructure/DevOps Project

```yaml
# .specify/config/research.yaml for infrastructure

paths:
  research_root: "runbooks/research"
  architecture_docs: "architecture"

decision_criteria:
  weights:
    reliability: 30
    operational_complexity: 25
    cost: 20
    security: 15
    vendor_lock_in: 10

performance_gates:
  deployment_time: "<5min"
  recovery_time: "<15min"
```

---

## Integration with Speckit Siblings

### Workflow Integration

```
User describes feature
         ↓
   speckit.specify  ← Creates spec.md
         ↓
   [Research needed?]
         ↓ YES
   speckit.research ← Answers technical questions
         ↓
   [Updates spec.md with findings]
         ↓
   speckit.clarify  ← Resolves remaining ambiguities
         ↓
   speckit.plan     ← Creates technical plan
         ↓
   speckit.tasks    ← Breaks into tasks
         ↓
   speckit.implement ← Executes implementation
```

### Data Flow Between Agents

**specify → research**:
- Spec contains `[NEEDS RESEARCH: ...]` markers
- Research agent extracts these and creates research areas

**research → plan**:
- Decision log contains approved decisions
- Plan agent reads decisions to inform technology choices

**research → specify**:
- Research updates spec with `implementation.libraries` section
- Spec tracks research completion status

**research → analyze**:
- Analyze agent validates all research questions answered
- Checks that decisions align with constitution

### Shared Data Structures

All speckit agents should use consistent structure:

```yaml
# Common metadata block
metadata:
  agent: "speckit.research"
  version: "1.0.0"
  created: "2025-12-28"
  updated: "2025-12-28"

# Common status field
status: "not_started | in_progress | completed | blocked"

# Common traceability
trace:
  created_by: "speckit.specify"
  updated_by: "speckit.research"
  related_artifacts:
    - type: "spec"
      path: "specs/001-feature.md"
    - type: "decision"
      id: "D001"
```

---

## Migration Path for Existing Projects

### Step 1: Create Configuration

```bash
# Generate initial config from current setup
speckit.research init --analyze-current

# This creates .specify/config/research.yaml by:
# 1. Detecting current file structure
# 2. Inferring decision criteria from decision-log.yaml
# 3. Extracting performance gates from constitution
```

### Step 2: Validate Research Areas

```bash
# Check all research areas are compatible with new schema
speckit.research migrate --validate

# Reports:
# - ✓ R01: Compatible
# - ⚠ R02: Missing 'research_type' field
# - ✗ R03: Uses deprecated 'blocks_features' format
```

### Step 3: Update Research Areas

```bash
# Auto-update research areas to new schema
speckit.research migrate --apply

# Creates backups before updating
# Logs all changes made
```

### Step 4: Test Agent

```bash
# Verify agent works with new configuration
speckit.research validate

# Checks:
# - Can load configuration
# - Can parse research-plan.yaml
# - Can select next area
# - Can execute research workflow
```

---

## Documentation Updates

### New Documents to Create

1. **`.specify/docs/research-framework.md`**
   - Generic research methodology
   - Adaptation guide for different project types
   - Configuration schema reference

2. **`.specify/docs/agent-integration.md`**
   - How speckit agents work together
   - Data flow between agents
   - Shared interfaces and contracts

3. **`.specify/examples/research-configs/`**
   - Example configurations for web apps
   - Example configurations for libraries
   - Example configurations for infrastructure projects

### Updates to Existing Docs

1. **`dev/research/README.md`**
   - Remove SafeDownload-specific content
   - Add "Configuration" section
   - Add "Adapting to Your Project" section

2. **`.github/agents/speckit.research.agent.md`**
   - Replace hardcoded paths with `{paths.*}` references
   - Add configuration loading steps
   - Make constitution alignment optional

3. **`dev/dev-docs/README-research.md`**
   - Rename to `.specify/docs/research-agent.md`
   - Remove SafeDownload-specific examples
   - Add generic workflow diagrams

---

## Implementation Checklist

### Phase 1: Configuration Framework ✓
- [ ] Create `.specify/config/research.yaml` schema
- [ ] Document configuration options
- [ ] Create example configs for different project types
- [ ] Add configuration validation

### Phase 2: Template Updates
- [ ] Update `research-template.yaml` to be generic
- [ ] Remove hardcoded feature IDs
- [ ] Add `research_type` taxonomy
- [ ] Add `project_context` field

### Phase 3: Agent Updates
- [ ] Modify agent to load configuration at startup
- [ ] Make constitution alignment optional
- [ ] Replace hardcoded paths with config references
- [ ] Add dynamic research area selection

### Phase 4: Helper Scripts
- [ ] Update `research.sh` to be project-agnostic
- [ ] Add `research.sh init` command
- [ ] Add `research.sh migrate` command
- [ ] Add `research.sh validate` command

### Phase 5: Integration
- [ ] Define shared metadata structure for all agents
- [ ] Document data flow between agents
- [ ] Create integration tests
- [ ] Update handoff mechanisms

### Phase 6: Documentation
- [ ] Create `research-framework.md`
- [ ] Create `agent-integration.md`
- [ ] Update existing agent documentation
- [ ] Create migration guide

### Phase 7: Testing
- [ ] Test with SafeDownload (existing project)
- [ ] Test with web app project
- [ ] Test with library project
- [ ] Test with infrastructure project

---

## Success Criteria

The generalized research agent is successful when:

✅ **Can be dropped into any project** with minimal configuration  
✅ **Adapts to project structure** without code changes  
✅ **Integrates seamlessly** with other speckit agents  
✅ **Supports multiple project types** (web, library, infra, etc.)  
✅ **Maintains SafeDownload compatibility** (backward compatible)  
✅ **Has clear documentation** for adaptation and configuration  
✅ **Provides migration path** for existing projects

---

## Next Steps

1. **Review this plan** with project stakeholders
2. **Create configuration schema** (Phase 1)
3. **Update one research area** as proof-of-concept
4. **Test with speckit.plan integration**
5. **Iterate based on findings**
6. **Roll out to all research areas**
7. **Document lessons learned**

---

## Related Documents

- [Current Research README](README.md)
- [Research Agent Definition](.github/agents/speckit.research.agent.md)
- [Research Agent Context](.specify/context/research-agent-context.yaml)
- [Decision Log](decision-log.yaml)
