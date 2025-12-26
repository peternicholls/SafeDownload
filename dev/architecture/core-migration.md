# Go Core Migration Architecture

**Version**: 1.0.0  
**Status**: Planned  
**Target**: Q2 2026  
**Constitution**: v1.5.0 Principle VIII

## Executive Summary

Migrate SafeDownload from Bash/Python to a compiled Go binary while preserving all CLI contracts and user experience. This enables cross-platform distribution, improved performance, and a foundation for future features (Bubble Tea TUI, API server).

## Goals

### Primary
- ✅ **Zero Breaking Changes**: Identical CLI interface, flags, exit codes, and behavior
- ✅ **Performance**: Meet constitution gates (TUI <500ms, list <100ms)
- ✅ **Cross-Platform**: Single binary for macOS/Linux (Darwin ARM64/AMD64, Linux AMD64/ARM64)
- ✅ **State Migration**: Seamless upgrade from v0.2.0 state files

### Secondary
- ✅ Eliminate Python dependency
- ✅ Foundation for Bubble Tea TUI (v1.1.0)
- ✅ Foundation for API server (v2.0.0)
- ✅ Improved error messages and logging

## Architecture

### Package Structure

```
safedownload/
├── cmd/
│   └── safedownload/
│       └── main.go              # CLI entrypoint, flag parsing, command routing
├── pkg/
│   ├── downloader/
│   │   ├── downloader.go        # Core download engine (HTTP client, resume, range requests)
│   │   ├── progress.go          # Progress tracking and callbacks
│   │   └── downloader_test.go
│   ├── state/
│   │   ├── state.go             # State management (load/save JSON)
│   │   ├── migration.go         # Schema migration logic
│   │   ├── schema.go            # Schema version definitions
│   │   └── state_test.go
│   ├── queue/
│   │   ├── queue.go             # Queue operations (add, remove, list, pause, resume)
│   │   ├── item.go              # Download item model
│   │   └── queue_test.go
│   ├── crypto/
│   │   ├── verify.go            # Checksum verification (SHA256, SHA512, SHA1, MD5)
│   │   └── verify_test.go
│   ├── config/
│   │   ├── config.go            # Configuration loading (flags + config.json)
│   │   └── config_test.go
│   ├── ui/
│   │   ├── simple.go            # Simple TUI (emoji-based, current v0.x style)
│   │   ├── progress.go          # Progress bar rendering
│   │   ├── commands.go          # Slash command parsing
│   │   └── ui_test.go
│   └── logger/
│       ├── logger.go            # Structured logging to safedownload.log
│       └── logger_test.go
├── internal/
│   └── version/
│       └── version.go           # Version info embedded at build time
├── scripts/
│   └── install.sh               # Shell wrapper (legacy compatibility)
├── Makefile                     # Build automation
└── go.mod                       # Dependency management
```

### Core Components

#### 1. Downloader (`pkg/downloader/`)

**Responsibilities**:
- HTTP client with retry logic (exponential backoff: 1s, 2s, 4s)
- Resume support via HTTP Range header
- Progress tracking with callbacks
- HTTPS enforcement (--allow-http opt-out)
- TLS verification via system CA trust store
- Proxy support (HTTP_PROXY, HTTPS_PROXY, NO_PROXY env vars)
- Graceful cancellation (context-based)

**Key Types**:
```go
type Downloader struct {
    client     *http.Client
    maxRetries int
    timeout    time.Duration
}

type DownloadRequest struct {
    URL        string
    OutputPath string
    Checksum   *ChecksumSpec
    Resume     bool
}

type ProgressCallback func(downloaded, total int64, speed float64)
```

**Dependencies**:
- `net/http` (stdlib)
- `context` (stdlib)
- `crypto/*` (via pkg/crypto)

#### 2. State Management (`pkg/state/`)

**Responsibilities**:
- Load/save JSON state to `~/.safedownload/state.json`
- Schema versioning and migration
- Thread-safe state updates
- Backup before migration

**Key Types**:
```go
type State struct {
    SchemaVersion string           `json:"schema_version"`
    Downloads     []DownloadItem   `json:"downloads"`
    Config        map[string]any   `json:"config"`
}

type DownloadItem struct {
    ID       int       `json:"id"`
    URL      string    `json:"url"`
    Output   string    `json:"output"`
    Status   string    `json:"status"` // queued, downloading, completed, failed, paused
    Progress int64     `json:"progress"`
    Total    int64     `json:"total"`
    Checksum string    `json:"checksum,omitempty"`
}
```

**Migration Path**:
1. Detect v0.x Python-generated state.json
2. Parse into v0.x schema struct
3. Transform to v1.0.0 schema
4. Write with `schema_version: "1.0.0"`
5. Backup old state to `state.json.v0.bak`

#### 3. Queue Management (`pkg/queue/`)

**Responsibilities**:
- Add/remove downloads
- List with filtering (by status)
- Pause/resume operations
- Parallel execution scheduler (configurable concurrency)
- PID tracking for background downloads

**Key Types**:
```go
type Queue struct {
    items      []*Item
    maxParallel int
    mu         sync.RWMutex
}

type Item struct {
    ID       int
    URL      string
    Output   string
    Status   Status
    Progress *Progress
    Checksum *ChecksumSpec
}

type Status int
const (
    StatusQueued Status = iota
    StatusDownloading
    StatusCompleted
    StatusFailed
    StatusPaused
)
```

#### 4. Crypto (`pkg/crypto/`)

**Responsibilities**:
- Checksum verification (SHA256, SHA512, SHA1, MD5)
- Size verification against Content-Length
- Streaming verification (for large files)

**Key Types**:
```go
type ChecksumSpec struct {
    Algorithm string // "sha256", "sha512", "sha1", "md5"
    Expected  string // hex-encoded hash
}

func VerifyFile(path string, spec *ChecksumSpec) error
```

#### 5. UI (`pkg/ui/`)

**Responsibilities**:
- Simple TUI rendering (v0.x emoji-based style)
- Slash command parsing (`/help`, `/stop`, `/resume`, etc.)
- Progress bar rendering
- Terminal dimension detection
- High-contrast mode support (--theme flag)

**Key Functions**:
```go
func RenderQueue(items []*queue.Item, theme Theme) string
func ParseCommand(input string) (Command, error)
func RenderProgressBar(current, total int64, width int) string
```

**Themes**:
- Light (default)
- Dark
- High-contrast

### CLI Contract Preservation

#### Flags (identical to v0.x)
```bash
safedownload <url> [options]
  -o, --output <file>       Output filename
  -c, --checksum <hash>     Expected checksum (algo:hash, e.g., sha256:abc...)
  -p, --parallel <n>        Concurrent downloads (default: 3)
  -m, --manifest <file>     Batch download manifest
  -b, --background          Run in background
  --allow-http              Allow HTTP (default: HTTPS-only)
  --insecure                Skip TLS verification (logs warning)
  --theme <name>            TUI theme (light, dark, high-contrast)
  --purge                   Delete all state/logs/PIDs
  --upgrade                 Self-update to latest version (v1.2.0+)
  -v, --version             Show version
  -h, --help                Show help
```

#### Exit Codes (identical to v0.x)
- `0`: Success
- `1`: General error (invalid args, missing deps)
- `2`: Network error (timeout, DNS failure)
- `3`: Verification failure (checksum/size mismatch)
- `4`: Permission error (cannot write)
- `130`: User interrupt (Ctrl+C)

#### State Directory (identical to v0.x)
```
~/.safedownload/
├── state.json          # Queue and download state
├── config.json         # User configuration
├── queue.json          # (deprecated in v1.0, merged into state.json)
├── safedownload.log    # Operation log (10MB cap, rotated)
├── pids/               # Background download PIDs
│   └── 1.pid
└── downloads/          # Default download directory
```

### Build System

#### Makefile
```makefile
.PHONY: build test lint install clean

VERSION := $(shell cat VERSION.yaml | grep '^version:' | awk '{print $$2}' | tr -d '"')
LDFLAGS := -X main.Version=$(VERSION)

build:
	go build -ldflags="$(LDFLAGS)" -o bin/safedownload cmd/safedownload/main.go

build-all:
	GOOS=darwin GOARCH=arm64 go build -ldflags="$(LDFLAGS)" -o bin/safedownload-$(VERSION)-darwin-arm64 cmd/safedownload/main.go
	GOOS=darwin GOARCH=amd64 go build -ldflags="$(LDFLAGS)" -o bin/safedownload-$(VERSION)-darwin-amd64 cmd/safedownload/main.go
	GOOS=linux GOARCH=amd64 go build -ldflags="$(LDFLAGS)" -o bin/safedownload-$(VERSION)-linux-amd64 cmd/safedownload/main.go
	GOOS=linux GOARCH=arm64 go build -ldflags="$(LDFLAGS)" -o bin/safedownload-$(VERSION)-linux-arm64 cmd/safedownload/main.go

test:
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

lint:
	golangci-lint run ./...

install: build
	cp bin/safedownload /usr/local/bin/safedownload

clean:
	rm -rf bin/ coverage.out coverage.html
```

#### GitHub Actions (`.github/workflows/release.yml`)
```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      - run: make build-all
      - run: sha256sum bin/* > bin/SHA256SUMS
      - uses: actions/create-release@v1
        with:
          files: bin/*
```

## Migration Strategy

### Phase 1: Development (Sprint 1-2)
1. Setup Go project structure
2. Implement core packages (downloader, state, queue, crypto)
3. Unit tests (>80% coverage)
4. CLI flag parsing and routing

### Phase 2: Integration (Sprint 3)
1. Implement simple TUI (pkg/ui)
2. State migration logic (v0.x → v1.0.0)
3. Integration tests (full download scenarios)
4. Performance benchmarks

### Phase 3: Testing (Sprint 4)
1. Beta release (v1.0.0-beta.1)
2. Community testing on Tier 1 platforms
3. Bug fixes and polish
4. Contract tests (regression against v0.2.0)

### Phase 4: Release (Sprint 4)
1. Final v1.0.0 tag
2. Build multi-platform binaries
3. Update install.sh to detect and install v1.0.0
4. Migration guide in docs/MIGRATION.md
5. CHANGELOG.md update

## Risk Mitigation

### Risk: State Migration Failures
**Mitigation**:
- Backup old state to `.bak` before migration
- Validate migrated state before deleting old
- Rollback instructions in MIGRATION.md
- Manual migration tool: `safedownload migrate --from v0 --to v1`

### Risk: Performance Regression
**Mitigation**:
- Performance benchmarks in CI
- Gate: TUI startup <500ms, list <100ms
- Profiling with `pprof` during development
- Load testing with 1000+ downloads in queue

### Risk: Platform Compatibility
**Mitigation**:
- CI testing on macOS (ARM64, AMD64) and Linux (AMD64, ARM64)
- Community testing program for Tier 2/3 platforms
- Clear platform support matrix in README

### Risk: Breaking User Workflows
**Mitigation**:
- Comprehensive contract tests
- Beta testing period (2-4 weeks)
- Dual installation support (keep v0.x until verified)
- Detailed MIGRATION.md guide

## Success Criteria

- ✅ All v0.2.0 CLI tests pass on v1.0.0
- ✅ State migration succeeds for 100+ sample state files
- ✅ Performance gates met (TUI <500ms, list <100ms)
- ✅ 80%+ code coverage
- ✅ Zero high/critical security vulnerabilities
- ✅ Positive beta tester feedback (>80%)
- ✅ Cross-platform builds successful on CI

## Future Foundation

This v1.0.0 Go core enables:

1. **v1.1.0 Bubble Tea TUI**: Replace `pkg/ui/simple.go` with Bubble Tea implementation
2. **v1.2.0 Auto-Upgrade**: Add `pkg/upgrade/` for self-update logic
3. **v2.0.0 API Server**: Add `cmd/safedownload-server/` and `pkg/api/` packages
4. **Plugins**: Add `pkg/plugin/` for Go plugin support

All future features build on this stable, compiled foundation.
