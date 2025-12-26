# Documentation Standards

**Constitution**: v1.5.0 - Development Workflow & Quality Gates  
**Status**: Active  
**Applies To**: All SafeDownload code, specs, and design documents

## Overview

SafeDownload maintains high documentation standards to ensure maintainability, onboarding efficiency, and alignment with constitution principles. This document defines documentation requirements for all code, specifications, and design documents.

## Code Documentation Standards

### Language-Specific Documentation

Documentation must be **idiomatic** for each language:

#### Bash/Shell (v0.x)

**Standard**: Comments using `#`, function headers

```bash
#!/usr/bin/env bash
# safedownload - Professional download manager with resumable downloads
# Version: 0.2.0
# Constitution: v1.5.0
#
# Usage: safedownload <url> [options]
# See --help for full documentation

##
# Download a file with resume support and checksum verification.
#
# Arguments:
#   $1 - URL to download
#   $2 - Output file path (optional)
#
# Returns:
#   0 - Success
#   2 - Network error
#   3 - Checksum verification failure
#
# Example:
#   download_file "https://example.com/file.zip" "/path/to/output.zip"
##
download_file() {
    local url="$1"
    local output="${2:-$(basename "$url")}"
    
    # Implementation...
}
```

**Rules**:
- File header: Purpose, version, constitution version
- Function header: Purpose, arguments, returns, example
- Inline comments: Explain WHY, not WHAT
- Complex logic: Explain edge cases and assumptions

#### Go (v1.x+)

**Standard**: GoDoc-style comments

```go
// Package downloader provides HTTP download functionality with resume support,
// checksum verification, and parallel execution.
//
// This package implements Constitution Principle III (Resumable Downloads) and
// Principle IV (Verification & Trust).
//
// Example usage:
//
//	d := downloader.New(downloader.Config{
//		MaxRetries: 3,
//		Timeout:    30 * time.Second,
//	})
//
//	req := &downloader.Request{
//		URL:        "https://example.com/file.zip",
//		OutputPath: "/path/to/file.zip",
//		Checksum:   &downloader.ChecksumSpec{Algorithm: "sha256", Expected: "abc..."},
//	}
//
//	if err := d.Download(ctx, req); err != nil {
//		log.Fatal(err)
//	}
package downloader

// Downloader manages HTTP downloads with resume support and verification.
//
// Downloader is thread-safe and can handle concurrent downloads up to the
// configured parallelism limit. Each download runs in its own goroutine with
// context-based cancellation.
//
// Constitution compliance:
//   - HTTPS-only by default (Principle X: Security Posture)
//   - Exponential backoff retry: 1s, 2s, 4s (Technical Constraints)
//   - TLS verification via system CA trust store (Principle X)
type Downloader struct {
	client     *http.Client
	maxRetries int
	timeout    time.Duration
}

// New creates a new Downloader with the given configuration.
//
// If config is nil, defaults are used:
//   - MaxRetries: 3
//   - Timeout: 30 seconds
//   - HTTPS-only: true
//
// Example:
//
//	d := downloader.New(&downloader.Config{
//		MaxRetries: 5,
//		AllowHTTP:  false,
//	})
func New(config *Config) *Downloader {
	// Implementation...
}

// Download downloads a file from the given URL with resume support.
//
// If the file already exists as a .part file, Download resumes from the last
// byte. Otherwise, it starts a fresh download. Progress is reported via the
// optional ProgressCallback in the request.
//
// Download respects the context for cancellation. If ctx is canceled, the
// download is paused (not deleted) and can be resumed later.
//
// Returns:
//   - nil on success
//   - ErrNetworkFailure for network errors (exit code 2)
//   - ErrVerificationFailed for checksum mismatches (exit code 3)
//   - ErrPermissionDenied for write failures (exit code 4)
//
// Example:
//
//	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
//	defer cancel()
//
//	req := &Request{
//		URL:        "https://example.com/large.zip",
//		OutputPath: "/tmp/large.zip",
//		Checksum:   &ChecksumSpec{Algorithm: "sha256", Expected: "abc..."},
//		Progress:   func(current, total int64, speed float64) {
//			fmt.Printf("Progress: %d/%d (%.2f MB/s)\n", current, total, speed/1024/1024)
//		},
//	}
//
//	if err := d.Download(ctx, req); err != nil {
//		return err
//	}
func (d *Downloader) Download(ctx context.Context, req *Request) error {
	// Implementation...
}
```

**Rules**:
- Package comment: Purpose, principles implemented, example
- Type comment: Purpose, thread-safety, constitution compliance
- Function comment: Purpose, parameters (implicit), returns with exit codes, example
- Exported symbols: MUST have GoDoc comments
- Unexported symbols: Document if non-obvious
- Examples: Use `Example` suffix for testable examples

**GoDoc Guidelines**:
- First sentence: Summary (appears in package index)
- Subsequent sentences: Details
- Link to constitution principles when relevant
- Exit codes in error returns (align with constitution)

#### Python (v0.x state management, future v2.x)

**Standard**: Docstrings (Google style)

```python
"""State management for SafeDownload.

This module provides persistent state storage for download queue and progress.
Implements Constitution Principle VII (State Persistence) with JSON-based storage.

Example:
    >>> state = StateManager("~/.safedownload/state.json")
    >>> state.add_download(url="https://example.com/file.zip", output="/tmp/file.zip")
    >>> state.save()

Constitution: v1.5.0
Schema Version: 1.0.0
"""

from typing import Optional, List
import json

class StateManager:
    """Manages download state persistence with schema versioning.
    
    StateManager handles loading, saving, and migrating state.json files. All
    operations are atomic (write to temp, rename) to prevent corruption.
    
    Thread-safety: NOT thread-safe. Use locks for concurrent access.
    
    Attributes:
        path (str): Path to state.json file
        schema_version (str): Current schema version (e.g., "1.0.0")
        downloads (List[DownloadItem]): List of download items
    
    Constitution Compliance:
        - Principle VII: State Persistence & Auto-Resume
        - Principle IX: Privacy & Data Minimization (local-only storage)
    """
    
    def __init__(self, path: str):
        """Initialize StateManager with given file path.
        
        Args:
            path: Absolute path to state.json file
        
        Raises:
            PermissionError: If path is not writable
        """
        self.path = path
        self.schema_version = "1.0.0"
        self.downloads = []
    
    def add_download(self, url: str, output: str, checksum: Optional[str] = None) -> int:
        """Add a new download to the queue.
        
        Args:
            url: Download URL (must be HTTPS unless --allow-http)
            output: Output file path
            checksum: Optional checksum in format "algo:hash" (e.g., "sha256:abc...")
        
        Returns:
            int: Download ID (sequential, starting from 1)
        
        Raises:
            ValueError: If URL is HTTP without allow_http flag
            ValueError: If output path is not writable
        
        Example:
            >>> state.add_download(
            ...     url="https://example.com/file.zip",
            ...     output="/tmp/file.zip",
            ...     checksum="sha256:abc123..."
            ... )
            1
        """
        # Implementation...
```

**Rules**:
- Module docstring: Purpose, principles, example
- Class docstring: Purpose, attributes, thread-safety, constitution compliance
- Method docstring: Args, Returns, Raises, Example (Google style)
- Use type hints (PEP 484)
- Constitution references in module/class docstrings

### Documentation Coverage Requirements

| Code Type | Coverage | Required Sections |
|-----------|----------|-------------------|
| Public API | 100% | Purpose, args/returns, example, constitution refs |
| Internal functions | >50% | Purpose if non-obvious, complex logic explained |
| Complex algorithms | 100% | WHY (not what), edge cases, performance notes |
| Error handling | 100% | Error conditions, exit codes, recovery |

### Constitution References

When implementing or documenting code that enforces constitution principles:

```go
// VerifyChecksum verifies the downloaded file against the expected checksum.
//
// Constitution Principle IV: Verification & Trust
// "Checksum mismatches are fatal—files are marked failed, not silently accepted."
//
// Supports SHA256, SHA512, SHA1, MD5. SHA256/SHA512 recommended for production.
//
// Returns ErrVerificationFailed (exit code 3) on mismatch.
func VerifyChecksum(path string, spec *ChecksumSpec) error {
    // Implementation...
}
```

**Format**: `Constitution Principle <Roman numeral>: <Principle name>`

## Specification Documentation

### Feature Specifications (`dev/specs/features/`)

**Template**: [dev/specs/feature-template.yaml](../specs/feature-template.yaml)

**Required Sections**:
```yaml
metadata:
  id: F006
  name: "Security Posture"
  version: "0.2.0"
  sprint: 2
  status: planned

description: |
  Brief description of the feature and its purpose.

user_stories:
  - id: US006-1
    priority: P1
    title: "HTTPS-only downloads"
    acceptance_criteria:
      - HTTP URLs rejected by default
      - --allow-http flag enables HTTP with warning
      - TLS verification via system CA trust

constitution_compliance:
  principles:
    - X: Security Posture (HTTPS-only, TLS verification)
  gates:
    - No credentials in logs
    - Checksum verification mandatory

implementation:
  packages:
    - pkg/downloader (HTTPS enforcement)
    - pkg/config (--allow-http flag)
  tests:
    - HTTPS enforcement with mock server
    - TLS verification with invalid cert
  documentation:
    - README security section update
    - CHANGELOG security advisory format

dependencies:
  - None (stdlib only)

risks:
  - title: "Breaking existing HTTP workflows"
    mitigation: "--allow-http flag for backward compatibility"
```

### Architecture Documents (`dev/architecture/`)

**Required Sections**:
1. **Executive Summary**: Goal, scope, constitution principles
2. **Architecture**: Diagrams, package structure, key types
3. **Migration Strategy**: Phases, risks, success criteria
4. **Constitution Compliance**: Principle checklist
5. **Future Foundation**: How this enables future features

**Format**: Markdown with YAML frontmatter

```markdown
---
title: "Go Core Migration"
version: "1.0.0"
status: planned
constitution: v1.5.0
principles:
  - VIII: Polyglot Architecture & Forward Compatibility
---

# Go Core Migration Architecture

[Content...]
```

## Design Documents (`dev/specs/`)

### Sprint Plans (`dev/sprints/sprint-NN.yaml`)

**Template**:
```yaml
metadata:
  sprint: 1
  version: "0.2.0"
  start_date: "2026-01-06"
  end_date: "2026-01-17"
  goal: "Implement security posture and privacy features"

features:
  - id: F006
    name: "Security Posture"
    story_points: 8
    status: in_progress
    
  - id: F007
    name: "Privacy & Data Minimization"
    story_points: 5
    status: not_started

tasks:
  - id: T001
    feature: F006
    title: "Implement HTTPS-only enforcement"
    assignee: "@peternicholls"
    status: completed
    
  - id: T002
    feature: F006
    title: "Add --allow-http flag with warning"
    assignee: "@peternicholls"
    status: in_progress

velocity:
  planned_story_points: 13
  completed_story_points: 8
  burndown_chart_path: "dev/sprints/sprint-1-burndown.png"

retrospective:
  what_went_well:
    - "HTTPS enforcement simpler than expected"
  what_to_improve:
    - "Need better TLS testing fixtures"
  action_items:
    - "Create TLS mock server helper"
```

## README & User Documentation

### README.md (Repository Root)

**Required Sections**:
1. **Title & Badges**: Name, version, build status, license
2. **Quick Start**: Install, basic usage, 3-5 examples
3. **Features**: Bullet list with constitution principle refs
4. **Installation**: All platforms (macOS, Linux, from source)
5. **Usage**: CLI examples, TUI walkthrough, configuration
6. **Configuration**: config.json reference, env vars
7. **Troubleshooting**: Common issues, error codes
8. **Contributing**: Link to CONTRIBUTING.md
9. **License**: Link to LICENSE
10. **Changelog**: Link to CHANGELOG.md

**Example Feature Section**:
```markdown
## Features

- ✅ **Resumable Downloads** (Principle III): HTTP range requests, automatic retry, `.part` tracking
- ✅ **Verification & Trust** (Principle IV): SHA256/SHA512 checksums, size validation, fatal on mismatch
- ✅ **Privacy First** (Principle IX): No telemetry, local-only storage, `/purge` command
- ✅ **Security Posture** (Principle X): HTTPS-only default, TLS verification, no credential logging
- ✅ **Accessible TUI** (Principle XI): High-contrast mode, colorblind-safe indicators, screen-reader compatible
```

### MIGRATION.md

**Required for MAJOR versions**:
- Schema version changes
- Breaking changes
- Migration steps (automated + manual)
- Rollback instructions
- Troubleshooting

### CONTRIBUTING.md

**Required Sections**:
- Code of conduct link
- Development setup (Go install, dependencies)
- Running tests (`make test`)
- Documentation standards (link to this doc)
- Pull request process
- Constitution compliance checklist

## CHANGELOG.md

**Format**: [Keep a Changelog](https://keepachangelog.com/)

**Example**:
```markdown
## [1.0.0] - 2026-06-15

### Added
- Go core migration (Principle VIII: Polyglot Architecture)
- Cross-platform binary releases (darwin/linux, amd64/arm64)
- State schema versioning with auto-migration (Configuration & State Schema Versioning)

### Changed
- **BREAKING**: State file schema upgraded to v1.0.0 (auto-migration provided)
- Performance: TUI startup now <200ms (was ~800ms in v0.x)

### Fixed
- #42: Resume calculation incorrect for files >2GB
- #38: Checksum verification failed on empty files

### Security
- CVE-2026-1234: Fixed path traversal in manifest parsing (CRITICAL)
- Enforced HTTPS-only by default (Principle X)

[1.0.0]: https://github.com/peternicholls/SafeDownload/releases/tag/v1.0.0
```

**Rules**:
- Semantic commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `BREAKING:`
- Link to GitHub releases
- Security section for CVEs
- Constitution principle refs for major features

## Comment Style Guide

### Inline Comments

**Good**:
```go
// Exponential backoff: 1s, 2s, 4s (constitution requirement)
time.Sleep(time.Second << attempt)
```

```go
// Resume calculation must handle files >2GB (int64, not int32)
offset := int64(stat.Size())
```

**Bad**:
```go
// Sleep for 1 second (obvious from code)
time.Sleep(time.Second)
```

```go
// Set offset (not explaining WHY)
offset := stat.Size()
```

### TODO Comments

**Format**: `// TODO(username): Description [Issue #NN]`

```go
// TODO(peternicholls): Implement GPG signature verification [Issue #45]
// Currently only supports checksum verification (SHA256/SHA512).
// Principle IV extension planned for v1.2.0.
func VerifySignature(path string, sigPath string) error {
	return errors.New("not implemented")
}
```

### Deprecation Comments

**Format**: `// Deprecated: Use <alternative> instead. Removed in <version>.`

```go
// Deprecated: Use NewDownloaderWithConfig instead. Removed in v2.0.0.
//
// This constructor does not support HTTPS enforcement (Principle X violation).
func NewDownloader() *Downloader {
	return &Downloader{client: http.DefaultClient}
}
```

## Documentation Testing

### GoDoc Examples

```go
func ExampleDownloader_Download() {
	d := New(&Config{MaxRetries: 3})
	
	req := &Request{
		URL:        "https://example.com/file.zip",
		OutputPath: "/tmp/file.zip",
	}
	
	if err := d.Download(context.Background(), req); err != nil {
		log.Fatal(err)
	}
	
	fmt.Println("Download complete")
	// Output: Download complete
}
```

**Rules**:
- Testable examples with `// Output:` comment
- Run via `go test`
- Verify examples in CI

### README Code Validation

Use `embedmd` or similar tool to embed actual code in README:

```markdown
<!-- embedmd: examples/basic.sh -->
```bash
safedownload https://example.com/file.zip -o file.zip
```
<!-- /embedmd -->
```

## Documentation Review Checklist

Before merging:

- [ ] All public APIs have GoDoc/docstrings
- [ ] Examples are testable and pass
- [ ] Constitution principles referenced where relevant
- [ ] Exit codes documented in error returns
- [ ] CHANGELOG.md updated with semantic commits
- [ ] README updated if user-facing changes
- [ ] Architecture docs updated if structure changes
- [ ] Migration guide created for breaking changes
- [ ] Spelling and grammar checked (use `aspell` or similar)

## Tools

### Recommended

- **Go**: `golangci-lint` (includes `godot` for GoDoc validation)
- **Markdown**: `markdownlint`, `embedmd`
- **Spell check**: `aspell`, `codespell`
- **Link check**: `markdown-link-check`
- **YAML validation**: `yamllint`

### CI Integration

```yaml
# .github/workflows/docs.yml
name: Documentation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint Markdown
        run: markdownlint '**/*.md'
      - name: Check Links
        run: markdown-link-check README.md CHANGELOG.md
      - name: Validate GoDoc
        run: go doc -all ./... | grep -i 'warning'
```

## Summary

Documentation is **not optional**—it's a first-class deliverable. Every feature must ship with:

1. Code documentation (GoDoc/docstrings)
2. Feature spec (YAML)
3. README/CHANGELOG updates
4. Constitution compliance notes
5. Examples (testable)

**Documentation SLA**: Documentation merged same PR as code, not "TODO later."
