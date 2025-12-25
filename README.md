# SafeDownload

[![CI](https://github.com/peternicholls/SafeDownload/actions/workflows/test.yml/badge.svg)](https://github.com/peternicholls/SafeDownload/actions/workflows/test.yml)
[![Release](https://img.shields.io/github/v/release/peternicholls/SafeDownload)](https://github.com/peternicholls/SafeDownload/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional CLI download manager with terminal UI, supporting resumable downloads, checksum verification, parallel downloads, and persistent state management.

**Constitution**: v1.5.0 | **Current Version**: v0.1.0 "Bootstrap"

## Features

### ✅ Core Features (v0.1.0)

| Feature | Description | Status |
|---------|-------------|--------|
| **Resumable Downloads** | Automatically resume interrupted downloads | ✅ Complete |
| **Checksum Verification** | SHA256, SHA512, SHA1, MD5 verification | ✅ Complete |
| **Progress Tracking** | Visual progress bar with speed display | ✅ Complete |
| **Terminal UI** | Interactive two-column interface | ✅ Complete |
| **Persistent State** | Queue survives restarts (`~/.safedownload/`) | ✅ Complete |
| **Batch Downloads** | Manifest files and parallel downloads | ✅ Complete |
| **Error Handling** | Graceful recovery from failures | ✅ Complete |

### 🔜 Planned Features

| Version | Codename | Features |
|---------|----------|----------|
| v0.2.0 | Shield | HTTPS-only default, TLS verification, security hardening |
| v1.0.0 | Phoenix | Go core migration, performance boost, BubbleTea TUI |
| v1.1.0 | Prism | Queue visualization, notifications |
| v2.0.0 | Horizon | REST API, web dashboard, multi-user |

See [dev/roadmap.yaml](dev/roadmap.yaml) for the complete roadmap.

## Installation

### Quick Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/peternicholls/SafeDownload/main/install.sh | bash
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/peternicholls/SafeDownload.git
cd SafeDownload

# Install to ~/bin (or your preferred location)
mkdir -p ~/bin
cp safedownload ~/bin/
chmod +x ~/bin/safedownload

# Ensure ~/bin is in your PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Homebrew (Coming in v1.0.0)

```bash
brew install peternicholls/tap/safedownload
```

## Quick Start

### Basic Download

```bash
# Simple download
safedownload https://example.com/file.zip

# Download with custom output filename
safedownload https://example.com/file.zip -o myfile.zip

# Download with checksum verification
safedownload https://example.com/file.zip -c sha256:abc123...
```

### Terminal UI Mode

```bash
# Launch interactive TUI
safedownload
```

In TUI mode, use these commands:
- `add <url>` - Add download to queue
- `start <id>` - Start specific download
- `stop <id>` - Pause download
- `remove <id>` - Remove from queue
- `list` - Show all downloads
- `clear` - Clear completed downloads
- `quit` - Exit (downloads persist)

### Batch Downloads

```bash
# Download from manifest file
safedownload --manifest urls.txt

# Parallel downloads (3 concurrent)
safedownload --parallel 3 --manifest urls.txt
```

### Manifest File Format

```text
# urls.txt - Lines starting with # are comments
https://example.com/file1.zip
https://example.com/file2.zip sha256:abc123...
https://example.com/file3.zip -o custom-name.zip
```

## Configuration

SafeDownload stores state and configuration in `~/.safedownload/`:

```
~/.safedownload/
├── state.json        # Download queue and history
├── config.json       # User preferences
├── safedownload.log  # Application logs
└── pids/             # Process ID files for active downloads
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SAFEDOWNLOAD_STATE_DIR` | `~/.safedownload` | State directory location |
| `SAFEDOWNLOAD_PARALLEL` | `3` | Default parallel downloads |
| `SAFEDOWNLOAD_TIMEOUT` | `30` | Connection timeout (seconds) |

## CLI Reference

```
safedownload [OPTIONS] [URL]

Options:
  -o, --output FILE      Output filename
  -c, --checksum HASH    Verify checksum (format: algo:hash)
  -m, --manifest FILE    Load URLs from manifest file
  -p, --parallel N       Number of parallel downloads (default: 3)
  -r, --retries N        Retry attempts on failure (default: 3)
  -q, --quiet            Suppress progress output
  -v, --verbose          Verbose output
  --version              Show version
  --help                 Show help

Examples:
  safedownload https://example.com/file.zip
  safedownload https://example.com/file.zip -o output.zip
  safedownload https://example.com/file.zip -c sha256:abc...
  safedownload --manifest urls.txt --parallel 5
```

## Constitution Principles

SafeDownload follows a strict constitution (v1.5.0) ensuring:

- **Principle III**: Downloads are always resumable
- **Principle IV**: Checksums are verified when provided
- **Principle VII**: State persists in `~/.safedownload/`
- **Principle IX**: No user data leaves the machine
- **Principle X**: HTTPS-only by default (v0.2.0+)
- **Principle XI**: Accessible without mouse/color dependency

See [.specify/memory/constitution.md](.specify/memory/constitution.md) for the complete constitution.

## Development

### Project Structure

```
SafeDownload/
├── safedownload           # Main executable (Bash)
├── dev/
│   ├── roadmap.yaml       # Version roadmap
│   ├── specs/features/    # Feature specifications
│   └── sprints/           # Sprint planning
├── tests/                 # Test suite
├── docs/                  # Documentation
└── scripts/               # Build and CI scripts
```

### Running Tests

```bash
# Run all tests
./tests/test.sh

# Run specific test suite
./tests/e2e/cli_test.bats
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- **Repository**: https://github.com/peternicholls/SafeDownload
- **Issues**: https://github.com/peternicholls/SafeDownload/issues
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Migration Guide**: [docs/MIGRATION.md](docs/MIGRATION.md)

