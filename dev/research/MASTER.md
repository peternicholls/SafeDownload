# SafeDownload Research Master Document

**Created**: 2025-12-25  
**Last Updated**: 2025-12-25  
**Constitution**: v1.5.0  
**Status**: Planning

---

## Executive Summary

This document consolidates all research areas identified for SafeDownload development. Research reduces implementation risk, ensures optimal technical decisions, and maintains constitution compliance.

**Total Research Areas**: 10  
**Estimated Total Research Time**: 30-50 hours  
**Critical Path Items**: Go HTTP Client, Bubble Tea TUI, State Migration

---

## Research Area Summary

| ID | Area | Version | Priority | Est. Time | Status |
|----|------|---------|----------|-----------|--------|
| R01 | Go HTTP Client Libraries | v1.0.0 | P0 | 2-4 hrs | 🟢 Complete |
| R02 | Bubble Tea TUI Framework | v1.1.0 | P0 | 4-8 hrs | 🟢 Complete |
| R03 | Rate Limiting Algorithms | v1.0.0 | P1 | 1-2 hrs | 🟢 Complete |
| R04 | Accessible Terminal UI Patterns | v0.2.0+ | P1 | 3-4 hrs | 🟢 Complete |
| R05 | State Migration Strategies | v1.0.0 | P1 | 2-3 hrs | 🔴 Not Started |
| R06 | GPG Signature Verification | v1.2.0 | P2 | 2-4 hrs | 🔴 Not Started |
| R07 | Package Manager Publishing | v1.3.0 | P2 | 4-6 hrs | 🔴 Not Started |
| R08 | REST API Design Patterns | v2.0.0 | P3 | 4-6 hrs | 🔴 Not Started |
| R09 | Plugin System Architectures | v1.2.0 | P3 | 3-4 hrs | 🔴 Not Started |
| R10 | Cross-Platform Distribution | v1.0.0 | P1 | 2-3 hrs | 🔴 Not Started |

**Status Legend**: 🔴 Not Started | 🟡 In Progress | 🟢 Complete | ⏸️ Blocked

---

## R01: Go HTTP Client Libraries & Patterns

**Target Version**: v1.0.0 Phoenix  
**Priority**: P0 (Blocks implementation)  
**Estimated Time**: 2-4 hours  
**Related Features**: F011 (Go Core Library)

### Research Objectives

1. Evaluate HTTP client libraries for resumable downloads
2. Understand Range header implementation patterns in Go
3. Determine optimal approach: stdlib vs third-party library
4. Ensure constitution compliance (minimal dependencies)

### Key Questions

- Should we use a library like `grab` or build from stdlib `net/http`?
- How does `grab` handle partial downloads vs custom Range header logic?
- What's the performance overhead of external HTTP libraries?
- How to handle connection pooling for concurrent downloads?
- Best practices for context cancellation and graceful shutdown?

### Libraries to Evaluate

| Library | GitHub | Stars | License | Notes |
|---------|--------|-------|---------|-------|
| [grab](https://github.com/cavaliercoder/grab) | cavaliercoder/grab | 1.3k | BSD-3 | HTTP download manager with resume |
| [resty](https://github.com/go-resty/resty) | go-resty/resty | 9k+ | MIT | HTTP client with retry |
| [go-retryablehttp](https://github.com/hashicorp/go-retryablehttp) | hashicorp/go-retryablehttp | 1.8k | MPL-2.0 | Retryable HTTP client |
| stdlib `net/http` | golang/go | - | BSD-3 | Built-in, no dependencies |

### Constitution Alignment

- **Principle VIII**: Polyglot Architecture mandates Go core
- **Principle II**: Minimal dependencies preferred (stdlib over third-party)
- **Principle III**: Resumable downloads are non-negotiable

### Expected Outcome

- Decision: stdlib vs specific library
- Implementation pattern documentation
- Performance benchmarks for chosen approach
- Code examples for resumable downloads

### Research Path

```
dev/research/01-go-http-client/
├── research.yaml      # Detailed plan and findings
└── findings.md        # Notes, code samples, benchmarks
```

---

## R02: Bubble Tea TUI Framework

**Target Version**: v1.1.0 Bubble  
**Priority**: P0 (Blocks TUI implementation)  
**Estimated Time**: 4-8 hours  
**Related Features**: F014 (Bubble Tea TUI Framework)

### Research Objectives

1. Master Elm Architecture (Model/Update/View) in Go context
2. Study large-scale Bubble Tea applications
3. Understand performance optimization techniques
4. Learn component composition patterns
5. Evaluate testing strategies for TUI code

### Key Questions

- How do large Bubble Tea apps handle 100+ list items without lag?
- Best practices for real-time updates (WebSocket-like patterns in terminal)?
- How to implement virtual scrolling in Bubble Tea?
- Testing strategies for TUI components (golden files, snapshot testing)?
- How to handle terminal resize events gracefully?
- Theme switching implementation patterns?

### Open Source Examples to Study

| Project | GitHub | Stars | Relevance |
|---------|--------|-------|-----------|
| [lazygit](https://github.com/jesseduffield/lazygit) | jesseduffield/lazygit | 44k+ | Complex panels, large data handling |
| [glow](https://github.com/charmbracelet/glow) | charmbracelet/glow | 14k+ | Charm's own showcase app |
| [soft-serve](https://github.com/charmbracelet/soft-serve) | charmbracelet/soft-serve | 4.5k+ | Server with TUI |
| [plandex](https://github.com/plandex-ai/plandex) | plandex-ai/plandex | 10k+ | AI agent TUI |
| [circumflex](https://github.com/bensadeh/circumflex) | bensadeh/circumflex | 3k+ | News reader TUI |

### Constitution Alignment

- **Principle I**: Professional UX requires modern TUI
- **Principle XI**: Accessibility (themes, keyboard navigation)
- **Performance Gate**: TUI startup <500ms

### Expected Outcome

- Elm architecture implementation guide
- Component library design
- Performance optimization checklist
- Testing strategy documentation
- Theme system architecture

### Research Path

```
dev/research/02-bubble-tea-tui/
├── research.yaml      # Detailed plan and findings
└── findings.md        # Notes, patterns, code examples
```

---

## R03: Rate Limiting Algorithms

**Target Version**: v1.0.0 Phoenix  
**Priority**: P1  
**Estimated Time**: 1-2 hours  
**Related Features**: F011 (Go Core Library)

### Research Objectives

1. Understand token bucket vs leaky bucket algorithms
2. Evaluate Go rate limiting libraries
3. Implement bandwidth-level throttling (bytes/second)
4. Meet constitution accuracy requirement (±5%)

### Key Questions

- Does `golang.org/x/time/rate` provide bandwidth-level limiting (bytes/sec)?
- How to integrate rate limiting with `io.Reader` wrapper pattern?
- Should rate limiting be per-download or global?
- How to handle burst traffic vs smooth throttling?

### Libraries to Evaluate

| Library | Approach | Notes |
|---------|----------|-------|
| [golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate) | Token bucket | Official Go extended library |
| [juju/ratelimit](https://github.com/juju/ratelimit) | Leaky bucket | Popular, well-tested |
| Custom `io.Reader` wrapper | Token bucket | Full control, minimal deps |

### Constitution Alignment

- **Performance Gate**: Rate limiting ±5% accuracy
- **Principle II**: Prefer stdlib/extended libraries

### Expected Outcome

- Algorithm selection with rationale
- `io.Reader` wrapper implementation
- Accuracy verification tests
- Integration guide for downloader

### Research Path

```
dev/research/03-rate-limiting/
├── research.yaml
└── findings.md
```

---

## R04: Accessible Terminal UI Patterns

**Target Version**: v0.2.0 Shield, v1.1.0 Bubble  
**Priority**: P1  
**Estimated Time**: 3-4 hours  
**Related Features**: F008 (Accessibility), F014 (Bubble Tea TUI)

### Research Objectives

1. Understand screen reader compatibility for terminal apps
2. Define WCAG 2.1 AA compliant color palettes for terminal
3. Validate emoji + text pattern for status indicators
4. Research keyboard-only navigation standards

### Key Questions

- How do screen readers (VoiceOver, NVDA, Orca) handle terminal applications?
- What ANSI escape sequences work best for screen readers?
- Should `--plain` flag output plain text for piping AND accessibility?
- What are colorblind-safe color combinations for terminal?
- How to test accessibility without specialized hardware?

### Resources to Study

| Resource | Topic | URL |
|----------|-------|-----|
| Inclusive Components | General a11y patterns | inclusive-components.design |
| termenv | Terminal capability detection | github.com/muesli/termenv |
| WCAG 2.1 Guidelines | Contrast ratios | w3.org/WAI/WCAG21/quickref |
| a11y Project | CLI accessibility | a11yproject.com |

### Constitution Alignment

- **Principle XI**: Accessibility is non-negotiable
- **Accessibility Checklist**: `dev/checklists/accessibility.md`

### Expected Outcome

- High-contrast color palette definition
- Screen reader compatibility guidelines
- Accessibility testing checklist expansion
- `--plain` flag specification

### Research Path

```
dev/research/04-accessibility/
├── research.yaml
└── findings.md
```

---

## R05: State Migration Strategies

**Target Version**: v1.0.0 Phoenix  
**Priority**: P1  
**Estimated Time**: 2-3 hours  
**Related Features**: F010 (Schema Versioning), F011 (Go Core)

### Research Objectives

1. Define JSON schema evolution patterns
2. Implement atomic file operations in Go
3. Research cross-platform file locking
4. Design migration testing strategy

### Key Questions

- Should we use a formal schema validation library (e.g., JSON Schema)?
- How to handle corrupted state files gracefully?
- What's the strategy for v0.x Python-generated JSON vs Go-generated JSON?
- How does flock() behave across macOS/Linux/BSD?
- Rollback strategy if migration fails?

### Patterns to Study

| Pattern | Use Case |
|---------|----------|
| Versioned schemas | `schema_version` field evolution |
| Transformer pattern | v0.x → v1.0.0 data transformation |
| Backup-on-migrate | Safety net for failed migrations |
| Multi-version reader | Reading multiple schema versions |

### Constitution Alignment

- **Schema Versioning**: Required in constitution (Technical Constraints)
- **Principle VII**: State persistence is non-negotiable

### Expected Outcome

- Migration strategy document
- Atomic write implementation
- File locking cross-platform guide
- Migration testing framework

### Research Path

```
dev/research/05-state-migration/
├── research.yaml
└── findings.md
```

---

## R06: GPG Signature Verification

**Target Version**: v1.2.0 Velocity  
**Priority**: P2  
**Estimated Time**: 2-4 hours  
**Related Features**: F017 (GPG Signatures)

### Research Objectives

1. Evaluate pure Go vs system `gpg` binary approach
2. Understand GPG keyring integration
3. Define key management UX
4. Ensure security best practices

### Key Questions

- Pure Go vs subprocess to `gpg`? (Constitution prefers minimal deps)
- How to handle GPG key verification (trust model)?
- What UX for "key not found" scenarios?
- Should we support keyservers for key retrieval?

### Libraries to Evaluate

| Library | Approach | Notes |
|---------|----------|-------|
| [ProtonMail/go-crypto](https://github.com/ProtonMail/go-crypto) | Pure Go OpenPGP | Fork of golang.org/x/crypto |
| [keybase/go-crypto](https://github.com/keybase/go-crypto) | Enhanced OpenPGP | Keybase's fork |
| System `gpg` binary | Subprocess | External dependency |

### Constitution Alignment

- **Principle X**: Security Posture (defense-in-depth)
- **Principle II**: Optional features, no forced deps

### Expected Outcome

- Library selection with rationale
- Key management workflow
- Error handling patterns
- User documentation requirements

### Research Path

```
dev/research/06-gpg-verification/
├── research.yaml
└── findings.md
```

---

## R07: Package Manager Publishing

**Target Version**: v1.3.0 Ecosystem  
**Priority**: P2  
**Estimated Time**: 4-6 hours  
**Related Features**: F021-F024 (Distribution)

### Research Objectives

1. Master Homebrew tap creation and maintenance
2. Understand Debian packaging (.deb)
3. Learn RPM packaging (.rpm)
4. Integrate with goreleaser for automation

### Key Questions

- Self-hosted apt/yum repo vs GitHub Releases only?
- Goreleaser for all formats or separate tooling?
- Signing keys for packages (GPG)?
- How to handle version updates automatically?

### Resources

| Resource | Topic |
|----------|-------|
| [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook) | Formula creation |
| [goreleaser docs](https://goreleaser.com/) | Release automation |
| [fpm](https://github.com/jordansissel/fpm) | Multi-format packaging |
| [deb-s3](https://github.com/deb-s3/deb-s3) | S3-hosted apt repo |

### Constitution Alignment

- **Release Cycle**: Defined distribution channels
- **Platform Support**: Tier 1 platforms prioritized

### Expected Outcome

- Homebrew tap setup guide
- Debian packaging workflow
- RPM packaging workflow
- CI/CD integration plan

### Research Path

```
dev/research/07-package-managers/
├── research.yaml
└── findings.md
```

---

## R08: REST API Design Patterns

**Target Version**: v2.0.0 Horizon  
**Priority**: P3 (Future)  
**Estimated Time**: 4-6 hours  
**Related Features**: F025 (REST API Server)

### Research Objectives

1. Evaluate Go HTTP frameworks
2. Design WebSocket for real-time updates
3. Define JWT authentication approach
4. Plan API versioning strategy

### Key Questions

- Constitution principle II (zero deps)—does this apply to v2.0.0 API?
- WebSocket vs Server-Sent Events for progress updates?
- How to share core download logic between CLI and API?
- REST vs GraphQL for download management?

### Frameworks to Evaluate

| Framework | Performance | Ecosystem | Learning Curve |
|-----------|-------------|-----------|----------------|
| stdlib `net/http` | Excellent | Minimal | Low |
| [gin](https://github.com/gin-gonic/gin) | Excellent | Large | Low |
| [echo](https://github.com/labstack/echo) | Excellent | Medium | Low |
| [fiber](https://github.com/gofiber/fiber) | Best | Growing | Medium |

### Constitution Alignment

- **Principle I**: Professional UX extends to API
- **Principle VIII**: API is alternate frontend to Go core

### Expected Outcome

- Framework selection
- API design document
- Authentication strategy
- Real-time updates architecture

### Research Path

```
dev/research/08-rest-api/
├── research.yaml
└── findings.md
```

---

## R09: Plugin System Architectures

**Target Version**: v1.2.0 Velocity  
**Priority**: P3  
**Estimated Time**: 3-4 hours  
**Related Features**: F020 (Plugin System)

### Research Objectives

1. Evaluate Go plugin approaches
2. Design plugin discovery mechanism
3. Define stable plugin API
4. Address security considerations

### Key Questions

- Go native plugins vs subprocess vs RPC?
- How to version plugin API for stability?
- Sandboxing for untrusted plugins?
- Plugin manifest format?

### Approaches

| Approach | Pros | Cons |
|----------|------|------|
| Go native plugins | Fast, typed | Platform-specific, brittle |
| Subprocess/exec | Isolated, any language | Slower, IPC overhead |
| WASM plugins | Sandboxed, portable | Complex, performance overhead |
| gRPC plugins | Battle-tested | Heavy for simple plugins |

### Reference Implementations

- [HashiCorp go-plugin](https://github.com/hashicorp/go-plugin): Terraform's plugin system
- [Caddy plugins](https://github.com/caddyserver/caddy): Build-time plugins

### Constitution Alignment

- **Principle VIII**: Forward compatibility
- **Principle II**: Plugins are optional enhancements

### Expected Outcome

- Plugin architecture selection
- API contract definition
- Security guidelines
- Example plugin implementation

### Research Path

```
dev/research/09-plugin-system/
├── research.yaml
└── findings.md
```

---

## R10: Cross-Platform Binary Distribution

**Target Version**: v1.0.0 Phoenix  
**Priority**: P1  
**Estimated Time**: 2-3 hours  
**Related Features**: F013 (Cross-Platform Build)

### Research Objectives

1. Understand CGO implications for cross-compilation
2. Learn static linking for Linux
3. Research macOS code signing requirements
4. Optimize binary size

### Key Questions

- Should we avoid CGO entirely for simpler cross-compilation?
- macOS notarization required for distribution outside App Store?
- What's acceptable binary size? (Go binaries typically 10-20MB)
- How to create truly static Linux binaries?

### Topics

| Topic | Consideration |
|-------|---------------|
| CGO | DNS resolution, TLS, SQLite |
| Static linking | musl libc for Linux |
| Code signing | macOS Gatekeeper, notarization |
| Binary size | UPX compression, build flags |

### Constitution Alignment

- **Platform Support**: Tier 1 platforms (macOS, Ubuntu, Debian)
- **Principle VIII**: Distributable binary

### Expected Outcome

- Cross-compilation Makefile
- Code signing process
- Binary size optimization guide
- CI/CD build matrix

### Research Path

```
dev/research/10-cross-platform/
├── research.yaml
└── findings.md
```

---

## Research Timeline

### Phase 1: Pre-v0.2.0 (Immediate)

```
Week 1:
├── R04 Accessibility ────────────── 3-4 hours
└── R03 Rate Limiting (basic) ────── 1-2 hours
```

### Phase 2: Pre-v1.0.0 (Sprint 3-5)

```
Weeks 2-4:
├── R01 Go HTTP Client ───────────── 2-4 hours
├── R05 State Migration ──────────── 2-3 hours
├── R10 Cross-Platform ───────────── 2-3 hours
└── R03 Rate Limiting (complete) ─── 1-2 hours
```

### Phase 3: Pre-v1.1.0 (Sprint 6-7)

```
Weeks 5-6:
└── R02 Bubble Tea TUI ───────────── 4-8 hours
```

### Phase 4: v1.2.0+ (Sprint 8+)

```
Weeks 7+:
├── R06 GPG Verification ─────────── 2-4 hours
├── R09 Plugin System ────────────── 3-4 hours
└── R07 Package Managers ─────────── 4-6 hours
```

### Phase 5: v2.0.0 (Backlog)

```
Future:
└── R08 REST API ─────────────────── 4-6 hours
```

---

## Decision Summary

| Decision | Status | Research | Date | Rationale |
|----------|--------|----------|------|-----------|
| HTTP library choice | Pending | R01 | - | - |
| TUI framework | Decided | R02 | 2025-12-24 | Bubble Tea (constitution) |
| Rate limiting approach | Pending | R03 | - | - |
| Schema validation | Pending | R05 | - | - |
| Plugin architecture | Pending | R09 | - | - |

See [decision-log.yaml](decision-log.yaml) for full decision history.

---

## Integration Points

Research findings feed into:

1. **Feature Specifications** (`dev/specs/features/`)
2. **Architecture Documents** (`dev/architecture/`)
3. **Sprint Planning** (`dev/sprints/`)
4. **Standards** (`dev/standards/`)

See [feedback-integration.yaml](feedback-integration.yaml) for the feedback loop process.

---

## Contributing

1. Claim a research area by updating status in `research-plan.yaml`
2. Use `research-template.yaml` for consistent structure
3. Document findings with citations
4. Propose decisions in `decision-log.yaml`
5. Update this master document with summaries

---

**Next Actions**:
1. Complete R04 (Accessibility) before v0.2.0 sprint
2. Begin R01 (Go HTTP Client) in preparation for v1.0.0
3. Schedule R02 (Bubble Tea) deep-dive before v1.1.0

