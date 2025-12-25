# Contributing to SafeDownload

Thank you for your interest in contributing to SafeDownload! This document provides guidelines and instructions for contributing.

**Constitution**: v1.5.0  
**Last Updated**: 2025-12-25

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Documentation Standards](#documentation-standards)
- [Testing Requirements](#testing-requirements)
- [Constitution Compliance](#constitution-compliance)

## Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive environment. We expect all contributors to:

- Be respectful and constructive in discussions
- Welcome newcomers and help them get started
- Focus on what is best for the community and project
- Accept constructive criticism gracefully

## Getting Started

### Prerequisites

**For v0.x (Bash/Python):**
- Bash 4.0+ or Zsh 5.0+
- curl 7.60+
- Python 3.7+
- Git

**For v1.x+ (Go core):**
- Go 1.21+
- Make
- Git

**Optional (enhanced TUI):**
- [Gum](https://github.com/charmbracelet/gum) for enhanced TUI

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/SafeDownload.git
cd SafeDownload
git remote add upstream https://github.com/peternicholls/SafeDownload.git
```

## Development Setup

### v0.x (Current - Bash/Python)

```bash
# Make scripts executable
chmod +x safedownload install.sh

# Run tests
./tests/test.sh

# Test installation locally
./install.sh --local
```

### v1.x+ (Go Core - Future)

```bash
# Install dependencies
go mod download

# Build
make build

# Run tests
make test

# Run with coverage
make test-coverage

# Lint
make lint
```

### Directory Structure

```
SafeDownload/
├── archive/              # Previous versions
├── dev/                  # Development documentation
│   ├── architecture/     # System design docs
│   ├── checklists/       # Quality gate checklists
│   ├── specs/            # Feature specifications
│   │   └── features/     # Individual feature specs
│   ├── sprints/          # Sprint planning
│   └── standards/        # Coding standards
├── docs/                 # User documentation
├── scripts/              # Build and utility scripts
├── tests/                # Test suites
│   ├── e2e/              # End-to-end tests
│   ├── fixtures/         # Test data
│   ├── integration/      # Integration tests
│   └── unit/             # Unit tests
└── .github/              # GitHub workflows
```

## Making Changes

### 1. Create a Feature Branch

```bash
git checkout main
git pull upstream main
git checkout -b feature/F006-security-posture
```

**Branch naming conventions:**
- `feature/F###-short-name` - New features
- `fix/issue-number-description` - Bug fixes
- `docs/description` - Documentation only
- `chore/description` - Maintenance tasks

### 2. Create or Update Feature Spec

Before implementing, create/update the feature spec:

```bash
# Copy template for new feature
cp dev/specs/feature-template.yaml dev/specs/features/F###-name.yaml

# Edit the spec with your feature details
```

**Feature specs MUST include:**
- Metadata (ID, version, priority, story points)
- User stories with acceptance criteria
- Constitution compliance (principles, gates)
- Implementation plan (packages, CLI changes)
- Testing plan (unit, integration, E2E)
- Documentation updates

### 3. Implement Changes

Follow these guidelines:

**Code Style:**
- Go: `gofmt` and `golangci-lint`
- Bash: `shellcheck`
- Python: PEP 8

**Commit Messages:**
```
type(scope): short description

Longer description if needed.

Refs: #issue-number
Constitution: Principle X
```

**Types:** `feat`, `fix`, `docs`, `test`, `chore`, `refactor`, `perf`

**Examples:**
```bash
git commit -m "feat(F006): implement HTTPS-only enforcement

- Add HTTPS check before download
- Add --allow-http flag for override
- Log security warning when HTTP allowed

Refs: #42
Constitution: Principle X (Security Posture)"
```

### 4. Write Tests

**Coverage Requirements:**
- Go code: ≥80% line coverage
- Bash code: ≥60% function coverage
- All public APIs: 100% documentation

**Test Organization:**
- Unit tests (60%): Fast, isolated, no external deps
- Integration tests (30%): Component interactions
- E2E tests (10%): Full CLI workflows

See [dev/standards/testing.md](dev/standards/testing.md) for details.

### 5. Update Documentation

**Required updates:**
- Code: Idiomatic documentation (godoc, docstrings, comments)
- README.md: If user-facing changes
- CHANGELOG.md: Add entry under `[Unreleased]`
- Feature spec: Update status to `completed`

## Pull Request Process

### 1. Pre-PR Checklist

- [ ] Feature spec created/updated in `dev/specs/features/`
- [ ] Tests pass locally (`make test` or `./tests/test.sh`)
- [ ] Test coverage meets requirements (≥80% Go, ≥60% Bash)
- [ ] Documentation updated (code + README + CHANGELOG)
- [ ] No linting errors (`make lint` or `shellcheck`)
- [ ] Constitution compliance verified (see checklist below)
- [ ] Commits are atomic and well-described

### 2. Submit PR

```bash
git push origin feature/F006-security-posture
# Open PR on GitHub
```

**PR Title Format:** `feat(F###): Short description`

**PR Description Template:**
```markdown
## Summary
Brief description of changes.

## Related
- Feature Spec: dev/specs/features/F###-name.yaml
- Issue: #NN

## Constitution Compliance
- [ ] Principle X: Security Posture
- [ ] Principle IX: Privacy

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

## Documentation
- [ ] Code documentation (godoc/docstrings)
- [ ] README.md updated
- [ ] CHANGELOG.md updated

## Screenshots (if TUI changes)
[Add screenshots here]
```

### 3. Review Process

**Approval Requirements:**
- Bug fixes/docs (PATCH): 1 maintainer approval or auto-merge if CI passes
- New features (MINOR): 1 maintainer approval
- Breaking changes (MAJOR): 2+ maintainer approvals + migration plan
- Constitution amendments: 2+ maintainer approvals

**Review Criteria:**
- Constitution compliance
- Test coverage
- Documentation quality
- Performance (no regressions)
- Security (for relevant changes)
- Accessibility (for TUI changes)

### 4. After Merge

- Delete your feature branch
- Update local main: `git checkout main && git pull upstream main`
- Close related issues

## Documentation Standards

See [dev/standards/documentation.md](dev/standards/documentation.md) for complete guidelines.

### Quick Reference

**Go (v1.x+):**
```go
// Package downloader provides HTTP download functionality.
//
// Constitution Principle III: Resumable Downloads
package downloader

// Download downloads a file with resume support.
//
// Returns ErrNetworkFailure (exit code 2) on network errors.
func Download(ctx context.Context, req *Request) error {
    // Implementation
}
```

**Bash (v0.x):**
```bash
##
# Download a file with resume support.
#
# Arguments:
#   $1 - URL to download
#   $2 - Output path
#
# Returns:
#   0 - Success
#   2 - Network error
##
download_file() {
    # Implementation
}
```

**Python:**
```python
def add_download(url: str, output: str) -> int:
    """Add a download to the queue.
    
    Args:
        url: Download URL (HTTPS required unless --allow-http)
        output: Output file path
    
    Returns:
        Download ID (sequential integer)
    
    Raises:
        ValueError: If URL is HTTP without allow_http flag
    
    Constitution: Principle VII (State Persistence)
    """
```

## Testing Requirements

See [dev/standards/testing.md](dev/standards/testing.md) for complete guidelines.

### Quick Reference

**Run all tests:**
```bash
# v0.x
./tests/test.sh

# v1.x+
make test
```

**Run specific test types:**
```bash
# Unit tests only
go test ./pkg/...

# Integration tests
go test ./tests/integration/...

# E2E tests
bats tests/e2e/
```

**Check coverage:**
```bash
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep total
# Must be ≥80%
```

## Constitution Compliance

All contributions MUST comply with the [SafeDownload Constitution](.specify/memory/constitution.md).

### Key Principles Checklist

Before submitting a PR, verify:

- [ ] **Principle II**: No new required dependencies (optional only)
- [ ] **Principle III**: Downloads are resumable
- [ ] **Principle IV**: Checksums verified, mismatches fatal
- [ ] **Principle IX**: No telemetry, credentials not logged
- [ ] **Principle X**: HTTPS-only default, TLS verified
- [ ] **Principle XI**: Accessibility (high-contrast, colorblind-safe)

### Performance Gates

- [ ] TUI startup < 500ms
- [ ] Queue list < 100ms (100+ items)
- [ ] Add download < 100ms

### Exit Codes

Ensure correct exit codes:
- `0`: Success
- `1`: General error
- `2`: Network error
- `3`: Verification failure
- `4`: Permission error
- `130`: User interrupt (Ctrl+C)

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: Report via GitHub Security Advisories (private)

## Recognition

Contributors are recognized in:
- Git commit history
- CHANGELOG.md (for significant contributions)
- GitHub contributors page

Thank you for contributing to SafeDownload! 🎉
