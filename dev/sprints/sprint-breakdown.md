# Sprint Breakdown

> Comprehensive sprint planning for SafeDownload roadmap v0.1.0 - v2.0.0

## Summary

| Release | Sprints | Story Points | Features |
|---------|---------|--------------|----------|
| v0.1.0 Bootstrap | 1-2 | ~40 SP | F001-F006 (existing) |
| v0.2.0 Shield | 3-4 | 21 SP | F007-F010 |
| v1.0.0 Phoenix | 5-6 | 34 SP | F011-F013 |
| v1.1.0 Bubble | 7-8 | 26 SP | F014-F016 |
| v1.2.0 Velocity | 9-11 | 37 SP | F017-F020 |
| v1.3.0 Ecosystem | 12-13 | 26 SP | F021-F024 |
| v2.0.0 Horizon | 14-21 | 55 SP | F025-F027 |

**Total: ~21 sprints (42 weeks), ~239 story points**

---

## v0.1.0 "Bootstrap" (Existing)

> Foundation release - already implemented

### Sprint 1-2: Foundation (Complete)
- F001: Basic Download
- F002: Progress Display
- F003: Resume Support
- F004: Checksum Verification
- F005: Parallel Downloads
- F006: Basic TUI

---

## v0.2.0 "Shield"

> Security, accessibility, and stability hardening

### Sprint 3: Privacy & Accessibility (13 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F007 | T007-001 | 1 | Configure logging sanitization |
| F007 | T007-002 | 1.5 | Implement URL sanitization |
| F007 | T007-003 | 2 | Build privacy audit mode |
| F007 | T007-004 | 0.5 | Write privacy tests |
| F008 | T008-001 | 2 | Implement high contrast mode |
| F008 | T008-002 | 2 | Add screen reader support |
| F008 | T008-003 | 2 | Create keyboard navigation |
| F008 | T008-004 | 1 | Test with assistive tech |
| F008 | T008-005 | 1 | Write accessibility docs |

### Sprint 4: Error Handling & Schema (8 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F009 | T009-001 | 2 | Implement error classification |
| F009 | T009-002 | 1.5 | Add recovery strategies |
| F009 | T009-003 | 1 | Build error logging |
| F009 | T009-004 | 0.5 | Write error documentation |
| F010 | T010-001 | 1 | Implement schema versioning |
| F010 | T010-002 | 1.5 | Build migration system |
| F010 | T010-003 | 0.5 | Write migration tests |

**Sprint 3-4 Total: 21 SP**

---

## v1.0.0 "Phoenix"

> Go rewrite - the core migration

### Sprint 5: Go Core Library (21 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F011 | T011-001 | 3 | Design and implement download engine |
| F011 | T011-002 | 3 | Implement progress tracking |
| F011 | T011-003 | 2 | Build checksum verification |
| F011 | T011-004 | 3 | Implement parallel downloads |
| F011 | T011-005 | 2 | Create state persistence |
| F011 | T011-006 | 3 | Implement resume support |
| F011 | T011-007 | 3 | Write unit tests (80%+) |
| F011 | T011-008 | 2 | Write integration tests |

### Sprint 6: CLI Contract & Build (13 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F012 | T012-001 | 2 | Implement flag parsing |
| F012 | T012-002 | 2 | Build output formatting |
| F012 | T012-003 | 1.5 | Implement exit codes |
| F012 | T012-004 | 1.5 | Write CLI tests |
| F012 | T012-005 | 1 | Write CLI documentation |
| F013 | T013-001 | 1.5 | Set up Go cross-compilation |
| F013 | T013-002 | 2 | Create GitHub Actions workflow |
| F013 | T013-003 | 1 | Verify on all platforms |
| F013 | T013-004 | 0.5 | Update installation docs |

**Sprint 5-6 Total: 34 SP**

---

## v1.1.0 "Bubble"

> Modern TUI with Bubble Tea framework

### Sprint 7: Bubble Tea TUI (13 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F014 | T014-001 | 3 | Implement Bubble Tea model |
| F014 | T014-002 | 2 | Build progress components |
| F014 | T014-003 | 2 | Create keyboard shortcuts |
| F014 | T014-004 | 2 | Implement Lip Gloss themes |
| F014 | T014-005 | 2 | Build accessibility features |
| F014 | T014-006 | 2 | Write TUI tests |

### Sprint 8: Queue & Notifications (13 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F015 | T015-001 | 2 | Implement tree view |
| F015 | T015-002 | 2 | Build filtering/sorting |
| F015 | T015-003 | 2 | Create search functionality |
| F015 | T015-004 | 1 | Write visualization tests |
| F015 | T015-005 | 1 | Document queue features |
| F016 | T016-001 | 1.5 | Implement toast notifications |
| F016 | T016-002 | 1.5 | Build desktop notifications |
| F016 | T016-003 | 1 | Add sound alerts |
| F016 | T016-004 | 1 | Write notification tests |

**Sprint 7-8 Total: 26 SP**

---

## v1.2.0 "Velocity"

> Power features for advanced users

### Sprint 9: GPG & Auto-Upgrade (16 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F017 | T017-001 | 2 | Implement signature verification |
| F017 | T017-002 | 2 | Build keyring management |
| F017 | T017-003 | 1.5 | Create verification logging |
| F017 | T017-004 | 1.5 | Write GPG tests |
| F017 | T017-005 | 1 | Document GPG usage |
| F018 | T018-001 | 2 | Implement version checking |
| F018 | T018-002 | 2 | Build upgrade mechanism |
| F018 | T018-003 | 2 | Implement rollback support |
| F018 | T018-004 | 1 | Write upgrade tests |
| F018 | T018-005 | 1 | Document upgrade process |

### Sprint 10: Scheduling (8 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F019 | T019-001 | 2 | Implement cron parser |
| F019 | T019-002 | 2 | Build scheduler service |
| F019 | T019-003 | 1.5 | Implement quiet hours |
| F019 | T019-004 | 1.5 | Create bandwidth throttling |
| F019 | T019-005 | 0.5 | Write scheduling tests |
| F019 | T019-006 | 0.5 | Document scheduling |

### Sprint 11: Plugin System (13 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F020 | T020-001 | 3 | Design plugin architecture |
| F020 | T020-002 | 2 | Implement hook system |
| F020 | T020-003 | 2 | Build plugin loading |
| F020 | T020-004 | 2 | Implement sandboxing |
| F020 | T020-005 | 2 | Create example plugins |
| F020 | T020-006 | 1 | Write plugin tests |
| F020 | T020-007 | 1 | Document plugin API |

**Sprint 9-11 Total: 37 SP**

---

## v1.3.0 "Ecosystem"

> Distribution and packaging

### Sprint 12: Homebrew & Debian (13 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F021 | T021-001 | 1.5 | Create Homebrew formula |
| F021 | T021-002 | 1.5 | Set up tap repository |
| F021 | T021-003 | 1 | Create auto-update action |
| F021 | T021-004 | 0.5 | Test Homebrew install |
| F021 | T021-005 | 0.5 | Update README |
| F022 | T022-001 | 2 | Create debian packaging |
| F022 | T022-002 | 1.5 | Set up package signing |
| F022 | T022-003 | 2 | Create APT repository |
| F022 | T022-004 | 1.5 | Build GitHub Action |
| F022 | T022-005 | 0.5 | Test on Ubuntu/Debian |

### Sprint 13: RPM & Docker (13 SP)

| Feature | Task | SP | Description |
|---------|------|-----|-------------|
| F023 | T023-001 | 2 | Create RPM spec file |
| F023 | T023-002 | 1 | Set up package signing |
| F023 | T023-003 | 2 | Create YUM/DNF repository |
| F023 | T023-004 | 1.5 | Create GitHub Action |
| F023 | T023-005 | 1 | Test on Fedora/RHEL |
| F023 | T023-006 | 0.5 | Update README |
| F024 | T024-001 | 1 | Create multi-stage Dockerfile |
| F024 | T024-002 | 1.5 | Create GitHub Action |
| F024 | T024-003 | 1 | Set up registry publishing |
| F024 | T024-004 | 1 | Test on amd64/arm64 |
| F024 | T024-005 | 0.5 | Document Docker usage |

**Sprint 12-13 Total: 26 SP**

---

## v2.0.0 "Horizon"

> Server mode, web dashboard, multi-user

### Sprint 14-16: REST API Server (21 SP)

| Sprint | Feature | Task | SP | Description |
|--------|---------|------|-----|-------------|
| 14 | F025 | T025-001 | 3 | Implement HTTP server |
| 14 | F025 | T025-002 | 4 | Implement download endpoints |
| 14 | F025 | T025-003 | 2 | Implement control endpoints |
| 15 | F025 | T025-004 | 3 | Implement WebSocket handler |
| 15 | F025 | T025-005 | 3 | Implement JWT authentication |
| 15 | F025 | T025-006 | 1 | Add TLS support |
| 16 | F025 | T025-007 | 3 | Write unit tests |
| 16 | F025 | T025-008 | 1 | Write integration tests |
| 16 | F025 | T025-009 | 1 | Write OpenAPI spec |

### Sprint 17-19: Web Dashboard (21 SP)

| Sprint | Feature | Task | SP | Description |
|--------|---------|------|-----|-------------|
| 17 | F026 | T026-001 | 2 | Set up React/Vite project |
| 17 | F026 | T026-002 | 2 | Implement login flow |
| 17 | F026 | T026-003 | 3 | Build dashboard layout |
| 18 | F026 | T026-004 | 3 | Implement queue view |
| 18 | F026 | T026-005 | 2 | Implement WebSocket updates |
| 18 | F026 | T026-006 | 2 | Build download controls |
| 19 | F026 | T026-007 | 2 | Implement stats/history |
| 19 | F026 | T026-008 | 1 | Add dark mode/a11y |
| 19 | F026 | T026-009 | 2 | Write unit tests |
| 19 | F026 | T026-010 | 1 | Write E2E tests |
| 19 | F026 | T026-011 | 1 | Write user guide |

### Sprint 20-21: Multi-User Support (13 SP)

| Sprint | Feature | Task | SP | Description |
|--------|---------|------|-----|-------------|
| 20 | F027 | T027-001 | 2 | Implement user model |
| 20 | F027 | T027-002 | 2 | Implement authentication |
| 20 | F027 | T027-003 | 2 | Implement download isolation |
| 21 | F027 | T027-004 | 2 | Implement RBAC |
| 21 | F027 | T027-005 | 2 | Implement quotas |
| 21 | F027 | T027-006 | 1.5 | Build admin dashboard |
| 21 | F027 | T027-007 | 1 | Write unit tests |
| 21 | F027 | T027-008 | 0.5 | Write documentation |

**Sprint 14-21 Total: 55 SP**

---

## Sprint Velocity Planning

Based on constitution guidelines (20-25 SP per sprint):

| Phase | Sprints | Avg SP/Sprint | Notes |
|-------|---------|---------------|-------|
| v0.2.0 | 2 | 10.5 | Lower velocity, focus on quality |
| v1.0.0 | 2 | 17 | Go rewrite, higher complexity |
| v1.1.0 | 2 | 13 | TUI work, moderate complexity |
| v1.2.0 | 3 | 12.3 | Mixed complexity features |
| v1.3.0 | 2 | 13 | Packaging, lower complexity |
| v2.0.0 | 8 | 6.9 | Complex features, careful pacing |

---

## Milestones

| Milestone | Target | Features | Blockers |
|-----------|--------|----------|----------|
| v0.2.0 Release | Sprint 4 | F007-F010 | None |
| v1.0.0 Release | Sprint 6 | F011-F013 | v0.2.0 complete |
| v1.1.0 Release | Sprint 8 | F014-F016 | v1.0.0 complete |
| v1.2.0 Release | Sprint 11 | F017-F020 | v1.1.0 complete |
| v1.3.0 Release | Sprint 13 | F021-F024 | v1.2.0 complete |
| v2.0.0 Release | Sprint 21 | F025-F027 | v1.3.0 complete |

---

## Risk Assessment

### High Risk
- **F011 Go Core**: Largest feature, entire rewrite
  - Mitigation: Extensive testing, parallel development with Bash

### Medium Risk
- **F025-F026 Server/Dashboard**: New domain (web)
  - Mitigation: Use established patterns, good libraries
- **F020 Plugin System**: Security concerns
  - Mitigation: Sandboxing, careful permission model

### Low Risk
- Packaging features (F021-F024): Well-documented processes
- TUI features (F014-F016): Charm libraries well-supported

---

## Dependencies

```
F001-F006 (Complete)
    │
    ▼
F007-F010 (v0.2.0 Shield)
    │
    ▼
F011-F013 (v1.0.0 Phoenix) ◀── Go rewrite
    │
    ▼
F014-F016 (v1.1.0 Bubble) ◀── Requires Go core
    │
    ▼
F017-F020 (v1.2.0 Velocity)
    │
    ├── F021-F024 (v1.3.0 Ecosystem) ◀── Packaging
    │
    ▼
F025-F027 (v2.0.0 Horizon) ◀── Server mode
```

---

## Notes

- Sprint dates not included - determined at sprint planning
- Story points may adjust during sprint planning
- Feature scope may change based on feedback
- All estimates assume single developer
