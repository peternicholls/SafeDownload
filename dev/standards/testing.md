# Testing Standards

**Constitution**: v1.5.0 - Development Workflow & Quality Gates  
**Status**: Active  
**Applies To**: All SafeDownload code and features

## Overview

Testing is mandatory before merge. This document defines testing requirements, coverage targets, and quality gates for SafeDownload.

## Testing Philosophy

### Core Principles

1. **Tests are executable specifications**: They document expected behavior
2. **Constitution gates are enforced**: Performance, security, accessibility tested
3. **Test coverage ≥ 80%**: For Go core (v1.0.0+)
4. **No flaky tests**: 100% pass rate on main branch
5. **Tests run fast**: Unit tests <5s, integration tests <30s

### Test Pyramid

```
        /\
       /  \  E2E Tests (10%)
      /────\  - Full CLI workflows
     /  Integration  \  - Multi-component interactions (30%)
    /────────────────\  - Download lifecycle, state persistence
   /   Unit Tests     \  - Pure functions, business logic (60%)
  /────────────────────\  - Fast, isolated, comprehensive
```

## Test Types

### 1. Unit Tests (60% of total)

**Purpose**: Test individual functions/methods in isolation

**Characteristics**:
- Fast (<1ms per test)
- No network, filesystem, or external dependencies (use mocks)
- High coverage (>90% for critical paths)

**Example (Go)**:
```go
// pkg/crypto/verify_test.go
package crypto

import (
	"os"
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestVerifyChecksum_SHA256_Valid(t *testing.T) {
	// Setup: Create temp file with known content
	tmpfile, _ := os.CreateTemp("", "test")
	defer os.Remove(tmpfile.Name())
	tmpfile.WriteString("hello world\n")
	tmpfile.Close()
	
	spec := &ChecksumSpec{
		Algorithm: "sha256",
		Expected:  "a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447",
	}
	
	err := VerifyChecksum(tmpfile.Name(), spec)
	assert.NoError(t, err)
}

func TestVerifyChecksum_SHA256_Mismatch(t *testing.T) {
	tmpfile, _ := os.CreateTemp("", "test")
	defer os.Remove(tmpfile.Name())
	tmpfile.WriteString("different content\n")
	tmpfile.Close()
	
	spec := &ChecksumSpec{
		Algorithm: "sha256",
		Expected:  "wronghash",
	}
	
	err := VerifyChecksum(tmpfile.Name(), spec)
	assert.ErrorIs(t, err, ErrVerificationFailed)
	// Constitution Principle IV: Fatal on mismatch
}
```

**Coverage Requirements**:
- Happy path: ✅ Valid input, expected output
- Error cases: ✅ Invalid input, network failures, permission errors
- Edge cases: ✅ Empty files, large files (>2GB), Unicode filenames
- Constitution gates: ✅ Exit codes, retry behavior, performance

### 2. Integration Tests (30% of total)

**Purpose**: Test interactions between components

**Characteristics**:
- Slower (<100ms per test)
- May use filesystem, but mock network
- Test full user scenarios

**Example (Go)**:
```go
// tests/integration/download_test.go
package integration

import (
	"context"
	"net/http/httptest"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/peternicholls/safedownload/pkg/downloader"
	"github.com/peternicholls/safedownload/pkg/state"
)

func TestDownloadLifecycle_ResumeAfterInterruption(t *testing.T) {
	// Setup: Mock HTTP server with 10MB file
	server := httptest.NewServer(mockRangeHandler(10 * 1024 * 1024))
	defer server.Close()
	
	// Create downloader
	d := downloader.New(&downloader.Config{MaxRetries: 3})
	
	// Create state manager
	tmpdir := t.TempDir()
	sm := state.New(tmpdir + "/state.json")
	
	// Step 1: Start download, cancel after 5MB
	ctx, cancel := context.WithCancel(context.Background())
	req := &downloader.Request{
		URL:        server.URL + "/file.bin",
		OutputPath: tmpdir + "/file.bin",
	}
	
	var downloaded int64
	req.Progress = func(current, total int64, speed float64) {
		downloaded = current
		if current >= 5*1024*1024 {
			cancel() // Simulate Ctrl+C
		}
	}
	
	err := d.Download(ctx, req)
	assert.ErrorIs(t, err, context.Canceled)
	
	// Verify .part file exists with ~5MB
	stat, _ := os.Stat(tmpdir + "/file.bin.part")
	assert.Greater(t, stat.Size(), int64(4*1024*1024))
	assert.Less(t, stat.Size(), int64(6*1024*1024))
	
	// Step 2: Resume download
	ctx2 := context.Background()
	err = d.Download(ctx2, req)
	assert.NoError(t, err)
	
	// Verify complete file
	stat, _ = os.Stat(tmpdir + "/file.bin")
	assert.Equal(t, int64(10*1024*1024), stat.Size())
	
	// Constitution Principle III: Resumable Downloads
	// Constitution Principle VII: State Persistence
}
```

### 3. E2E Tests (10% of total)

**Purpose**: Test full CLI workflows as users would use them

**Characteristics**:
- Slowest (1-10s per test)
- Use real CLI binary, real filesystem
- May use mock network or localhost server

**Example (Bash + BATS)**:
```bash
# tests/e2e/cli_test.bats
#!/usr/bin/env bats

setup() {
	export TMPDIR=$(mktemp -d)
	export SAFEDOWNLOAD_STATE_DIR="$TMPDIR/.safedownload"
}

teardown() {
	rm -rf "$TMPDIR"
}

@test "CLI: Basic download with checksum verification" {
	# Start local HTTP server with known file
	python3 -m http.server 8080 &
	SERVER_PID=$!
	trap "kill $SERVER_PID" EXIT
	
	# Download with checksum
	run safedownload http://localhost:8080/testfile.txt \
		--allow-http \
		-o "$TMPDIR/output.txt" \
		-c "sha256:expected_hash"
	
	# Verify exit code (Constitution: Exit Codes)
	[ "$status" -eq 0 ]
	
	# Verify file exists
	[ -f "$TMPDIR/output.txt" ]
}

@test "CLI: HTTPS-only enforcement" {
	# Try HTTP without --allow-http
	run safedownload http://example.com/file.txt
	
	# Should fail with exit code 1 (Constitution Principle X)
	[ "$status" -eq 1 ]
	[[ "$output" =~ "HTTPS required" ]]
}

@test "CLI: Resume after interruption" {
	# Download large file, kill after 2s
	timeout 2s safedownload https://example.com/large.iso \
		-o "$TMPDIR/large.iso" || true
	
	# Verify .part file exists
	[ -f "$TMPDIR/large.iso.part" ]
	
	# Resume download
	run safedownload https://example.com/large.iso \
		-o "$TMPDIR/large.iso"
	
	[ "$status" -eq 0 ]
	[ -f "$TMPDIR/large.iso" ]
	[ ! -f "$TMPDIR/large.iso.part" ]
}
```

## Constitution Gates Testing

### Performance Gates

**Constitution Requirements**:
- TUI startup: <500ms
- Queue listing: <100ms (even with 100+ items)
- Add download: <100ms
- Resume calculation: <50ms

**Implementation (Go Benchmarks)**:
```go
// pkg/ui/ui_bench_test.go
func BenchmarkTUIStartup(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ui := NewSimpleTUI()
		ui.Render()
	}
	// Enforce: Must be <500ms on CI hardware
}

func BenchmarkQueueList_100Items(b *testing.B) {
	queue := setupQueueWith100Items()
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = queue.List()
	}
	// Enforce: Must be <100ms
}
```

**CI Enforcement**:
```yaml
# .github/workflows/test.yml
- name: Benchmark Performance
  run: |
    go test -bench=. -benchtime=1s ./... > bench.txt
    # Parse bench.txt and fail if >500ms for TUIStartup
```

### Security Gates

**Constitution Requirements**:
- HTTPS-only by default (Principle X)
- No credentials in logs (Principle X)
- Checksum verification mandatory for production (Principle IV)

**Implementation**:
```go
// tests/security/https_test.go
func TestHTTPSEnforcement(t *testing.T) {
	d := downloader.New(nil) // Default config
	
	req := &downloader.Request{
		URL:        "http://example.com/file.zip", // HTTP, not HTTPS
		OutputPath: "/tmp/file.zip",
	}
	
	err := d.Download(context.Background(), req)
	
	// Must fail without --allow-http
	assert.ErrorIs(t, err, downloader.ErrHTTPNotAllowed)
	// Constitution Principle X: HTTPS-only default
}

func TestNoCredentialsInLogs(t *testing.T) {
	// Download with Basic Auth
	req := &downloader.Request{
		URL:    "https://user:pass@example.com/file.zip",
		Output: "/tmp/file.zip",
	}
	
	d.Download(context.Background(), req)
	
	// Read log file
	logContent, _ := os.ReadFile("~/.safedownload/safedownload.log")
	
	// Must NOT contain password
	assert.NotContains(t, string(logContent), "pass")
	// Constitution Principle X: No credential logging
}
```

### Accessibility Gates

**Constitution Requirements**:
- High-contrast mode support (Principle XI)
- Colorblind-safe indicators (Principle XI)
- No color-only status (Principle XI)

**Implementation (Manual + Automated)**:
```go
// tests/accessibility/theme_test.go
func TestHighContrastTheme(t *testing.T) {
	ui := NewSimpleTUI()
	ui.SetTheme("high-contrast")
	
	output := ui.RenderQueue([]*queue.Item{
		{Status: queue.StatusCompleted},
		{Status: queue.StatusFailed},
	})
	
	// Verify status indicators have text labels, not just emoji
	assert.Contains(t, output, "✅ Completed")
	assert.Contains(t, output, "❌ Failed")
	
	// Verify high contrast ANSI codes
	assert.Contains(t, output, "\033[1;37m") // Bold white
	assert.Contains(t, output, "\033[40m")   // Black background
}

func TestColorblindSafeIndicators(t *testing.T) {
	ui := NewSimpleTUI()
	
	// Status indicators MUST NOT rely on red/green only
	// Use shapes/symbols in addition to color
	output := ui.RenderStatus(queue.StatusCompleted)
	
	// Emoji + text label required
	assert.Regexp(t, `[✅✓] (Completed|Done)`, output)
}
```

**Manual Testing Checklist** (in `dev/checklists/accessibility.md`):
- [ ] TUI readable in Vim colorscheme (high contrast)
- [ ] Status distinguishable without color (grayscale screenshot test)
- [ ] Terminal width 80 columns: graceful degradation
- [ ] Screen reader test (VoiceOver on macOS, Orca on Linux)

## Coverage Requirements

### Go (v1.0.0+)

**Target**: ≥80% line coverage

**CI Enforcement**:
```yaml
- name: Test Coverage
  run: |
    go test -v -race -coverprofile=coverage.out ./...
    go tool cover -func=coverage.out | grep total | awk '{if ($3+0 < 80) exit 1}'
```

**Exclusions** (documented in code):
```go
// COVERAGE: Skip - unreachable in tests
if os.Getenv("NEVER_SET") == "true" {
	panic("impossible")
}
```

### Bash (v0.x)

**Target**: ≥60% function coverage (via BATS)

**Tool**: `kcov` for bash coverage

```bash
kcov --exclude-pattern=/usr coverage/ bats tests/
```

## Test Organization

### Directory Structure

```
tests/
├── unit/                      # Unit tests (co-located with pkg/)
│   └── pkg/
│       ├── downloader/
│       │   └── downloader_test.go
│       ├── crypto/
│       │   └── verify_test.go
│       └── state/
│           └── state_test.go
├── integration/               # Integration tests
│   ├── download_lifecycle_test.go
│   ├── state_migration_test.go
│   └── queue_parallel_test.go
├── e2e/                       # End-to-end CLI tests
│   ├── cli_test.bats
│   └── tui_test.bats
├── security/                  # Security-focused tests
│   ├── https_test.go
│   ├── credential_leak_test.go
│   └── checksum_tampering_test.go
├── accessibility/             # Accessibility tests
│   ├── theme_test.go
│   └── screen_reader_test.sh
├── performance/               # Performance benchmarks
│   └── benchmarks_test.go
└── fixtures/                  # Test data
    ├── state-v0.json
    ├── state-v1.json
    └── manifest-sample.txt
```

### Naming Conventions

**Go**:
- Test files: `*_test.go`
- Test functions: `Test<Function>_<Scenario>` (e.g., `TestDownload_ResumeAfterCancel`)
- Benchmark functions: `Benchmark<Function>` (e.g., `BenchmarkTUIStartup`)

**Bash**:
- Test files: `*_test.bats`
- Test names: Descriptive sentences (e.g., `@test "CLI: HTTPS-only enforcement"`)

## Mocking Strategy

### Network Mocking (Go)

**Use `httptest.Server` for HTTP mocking**:
```go
func mockRangeHandler(size int64) http.HandlerFunc {
	content := make([]byte, size)
	
	return func(w http.ResponseWriter, r *http.Request) {
		// Support Range requests for resume testing
		rangeHeader := r.Header.Get("Range")
		if rangeHeader != "" {
			// Parse "bytes=N-" and serve from offset N
			start := parseRangeStart(rangeHeader)
			w.Header().Set("Content-Range", fmt.Sprintf("bytes %d-%d/%d", start, size-1, size))
			w.WriteHeader(http.StatusPartialContent)
			w.Write(content[start:])
		} else {
			w.Header().Set("Content-Length", fmt.Sprintf("%d", size))
			w.Write(content)
		}
	}
}
```

### Filesystem Mocking (Go)

**Use `os.TempDir()` for real filesystem testing**:
```go
func TestStateManager_Save(t *testing.T) {
	tmpdir := t.TempDir() // Auto-cleanup
	sm := state.New(tmpdir + "/state.json")
	
	sm.AddDownload("https://example.com/file.zip", "/tmp/file.zip")
	err := sm.Save()
	
	assert.NoError(t, err)
	assert.FileExists(t, tmpdir + "/state.json")
}
```

**Alternative**: Use `afero` for in-memory filesystem if needed

### Time Mocking (Go)

**Use injection for time-dependent code**:
```go
// pkg/downloader/downloader.go
type Downloader struct {
	now func() time.Time // Injected for testing
}

func New(config *Config) *Downloader {
	return &Downloader{
		now: time.Now, // Default to real time
	}
}

// In tests:
func TestDownload_Timeout(t *testing.T) {
	d := downloader.New(nil)
	d.now = func() time.Time {
		return time.Date(2025, 12, 24, 10, 0, 0, 0, time.UTC)
	}
	// Now time is fixed for deterministic testing
}
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      
      - name: Unit Tests
        run: go test -v -race -coverprofile=coverage.out ./...
      
      - name: Coverage Check
        run: |
          go tool cover -func=coverage.out | tee coverage.txt
          COVERAGE=$(grep total coverage.txt | awk '{print $3}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.out

  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
      
      - name: Integration Tests
        run: go test -v ./tests/integration/...

  e2e:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
      
      - name: Build Binary
        run: make build
      
      - name: E2E Tests
        run: |
          export PATH=$PWD/bin:$PATH
          bats tests/e2e/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
      
      - name: Security Tests
        run: go test -v ./tests/security/...
      
      - name: Security Scan (gosec)
        uses: securego/gosec@master
        with:
          args: '-no-fail -fmt sarif -out results.sarif ./...'
      
      - name: Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'

  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
      
      - name: Benchmark
        run: |
          go test -bench=. -benchmem ./... | tee bench.txt
      
      - name: Performance Gate Check
        run: |
          # Parse bench.txt and verify <500ms for TUIStartup
          # Parse bench.txt and verify <100ms for QueueList
          python3 scripts/check_benchmarks.py bench.txt
```

## Test Data Management

### Fixtures

**Location**: `tests/fixtures/`

**Examples**:
- `state-v0.json`: v0.x state for migration testing
- `state-v1.json`: v1.0.0 state with 100+ items
- `manifest-sample.txt`: Sample manifest file
- `testfile-1mb.bin`: Known checksum for verification tests

**Generation**:
```bash
# Generate test file with known SHA256
dd if=/dev/urandom of=tests/fixtures/testfile-1mb.bin bs=1M count=1
sha256sum tests/fixtures/testfile-1mb.bin > tests/fixtures/testfile-1mb.bin.sha256
```

### Test Database Seeding

**For integration tests**:
```go
func seedTestQueue(sm *state.StateManager, count int) {
	for i := 0; i < count; i++ {
		sm.AddDownload(
			fmt.Sprintf("https://example.com/file%d.zip", i),
			fmt.Sprintf("/tmp/file%d.zip", i),
		)
	}
	sm.Save()
}
```

## Testing Best Practices

### Do's ✅

- ✅ **Table-driven tests** for multiple scenarios
- ✅ **Setup/teardown** via `t.Cleanup()` or BATS setup/teardown
- ✅ **Parallel tests** via `t.Parallel()` when safe
- ✅ **Test names** describe scenario, not implementation
- ✅ **Assert errors** with `assert.ErrorIs()`, not string matching
- ✅ **Mock external dependencies** (network, time, random)
- ✅ **Test constitution gates** explicitly (performance, security, a11y)

### Don'ts ❌

- ❌ **Flaky tests** (random failures due to timing/concurrency)
- ❌ **Test implementation details** (test behavior, not internals)
- ❌ **Shared state** between tests (use fresh setup per test)
- ❌ **Hardcoded sleeps** (use proper synchronization or mocks)
- ❌ **Ignoring test failures** (fix or skip with `t.Skip()` + issue link)
- ❌ **Tests without assertions** (test must verify something)

### Example: Table-Driven Test

```go
func TestVerifyChecksum(t *testing.T) {
	tests := []struct {
		name      string
		content   string
		algorithm string
		expected  string
		wantErr   error
	}{
		{
			name:      "SHA256 valid",
			content:   "hello world\n",
			algorithm: "sha256",
			expected:  "a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447",
			wantErr:   nil,
		},
		{
			name:      "SHA256 mismatch",
			content:   "hello world\n",
			algorithm: "sha256",
			expected:  "wronghash",
			wantErr:   ErrVerificationFailed,
		},
		{
			name:      "SHA512 valid",
			content:   "test\n",
			algorithm: "sha512",
			expected:  "0e3e75234abc68f4378a86b3f4b32a198ba301845b0cd6e50106e874345700cc6663a86c1ea125dc5e92be17c98f9a0f85ca9d5f595db2012f7cc3571945c123",
			wantErr:   nil,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			tmpfile, _ := os.CreateTemp("", "test")
			defer os.Remove(tmpfile.Name())
			tmpfile.WriteString(tt.content)
			tmpfile.Close()
			
			spec := &ChecksumSpec{
				Algorithm: tt.algorithm,
				Expected:  tt.expected,
			}
			
			err := VerifyChecksum(tmpfile.Name(), spec)
			
			if tt.wantErr != nil {
				assert.ErrorIs(t, err, tt.wantErr)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}
```

## Summary

Testing Requirements Checklist:

- [ ] Unit tests: >80% coverage (Go), >60% (Bash)
- [ ] Integration tests: Full lifecycle scenarios
- [ ] E2E tests: CLI workflows on Tier 1 platforms
- [ ] Performance benchmarks: Enforce constitution gates
- [ ] Security tests: HTTPS, credentials, checksums
- [ ] Accessibility tests: Themes, indicators, screen readers
- [ ] CI/CD: Automated testing on push/PR
- [ ] No flaky tests: 100% pass rate on main
- [ ] Test documentation: Table-driven, clear names, setup/teardown
