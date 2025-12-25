# Migration Guide

**Constitution**: v1.5.0  
**Last Updated**: 2025-12-25

This document provides migration instructions between SafeDownload versions, particularly for major version upgrades that include breaking changes.

## Table of Contents

- [Version Compatibility](#version-compatibility)
- [v0.x to v1.0.0 Migration](#v0x-to-v100-migration)
- [v1.x to v2.0.0 Migration](#v1x-to-v200-migration)
- [State File Migration](#state-file-migration)
- [Configuration Migration](#configuration-migration)
- [Troubleshooting](#troubleshooting)
- [Rollback Instructions](#rollback-instructions)

## Version Compatibility

| From Version | To Version | Migration Required | Breaking Changes |
|--------------|------------|-------------------|------------------|
| 0.1.x | 0.2.x | No | No |
| 0.2.x | 1.0.0 | Yes | State schema |
| 1.0.x | 1.1.x | No | No |
| 1.1.x | 1.2.x | No | No |
| 1.2.x | 1.3.x | No | No |
| 1.3.x | 2.0.0 | Yes | API changes |

## v0.x to v1.0.0 Migration

### Overview

v1.0.0 ("Phoenix") introduces the Go core migration, replacing the Bash/Python implementation with a compiled Go binary. This is a **major version** with **state schema changes**.

**Key Changes:**
- Core engine rewritten in Go
- State schema upgraded to v1.0.0
- Shell wrapper preserved for compatibility
- CLI interface unchanged (backward compatible)

### Prerequisites

Before migrating:
1. Ensure all downloads are completed or paused (no active downloads)
2. Backup your state directory: `cp -r ~/.safedownload ~/.safedownload.backup`
3. Note your current version: `safedownload --version`

### Migration Steps

#### Automatic Migration (Recommended)

```bash
# 1. Update to latest version
curl -fsSL https://raw.githubusercontent.com/peternicholls/SafeDownload/main/install.sh | bash

# 2. Run migration check
safedownload --version
# Should show v1.0.0+

# 3. Launch SafeDownload - automatic migration runs
safedownload

# 4. Verify migration
cat ~/.safedownload/state.json | grep schema_version
# Should show "schema_version": "1.0.0"
```

#### Manual Migration

If automatic migration fails:

```bash
# 1. Backup current state
cp ~/.safedownload/state.json ~/.safedownload/state.json.v0.bak

# 2. Download migration tool
curl -fsSL https://github.com/peternicholls/SafeDownload/releases/download/v1.0.0/migrate-state -o migrate-state
chmod +x migrate-state

# 3. Run migration
./migrate-state ~/.safedownload/state.json

# 4. Verify
cat ~/.safedownload/state.json | jq '.schema_version'
```

### State Schema Changes (v0.x → v1.0.0)

#### v0.x Schema
```json
{
  "schema_version": "0.1.0",
  "downloads": [
    {
      "id": 1,
      "url": "https://example.com/file.zip",
      "output": "/tmp/file.zip",
      "status": "completed",
      "progress": 10485760,
      "total": 10485760,
      "checksum": "sha256:abc123..."
    }
  ],
  "config": {
    "parallel": 3
  }
}
```

#### v1.0.0 Schema
```json
{
  "schema_version": "1.0.0",
  "created_at": "2025-12-24T10:00:00Z",
  "updated_at": "2025-12-24T15:30:00Z",
  "downloads": [
    {
      "id": 1,
      "url": "https://example.com/file.zip",
      "output": "/tmp/file.zip",
      "status": "completed",
      "progress": 10485760,
      "total": 10485760,
      "checksum": {
        "algorithm": "sha256",
        "expected": "abc123...",
        "verified": true
      },
      "started_at": "2025-12-24T10:00:00Z",
      "completed_at": "2025-12-24T10:05:30Z",
      "speed_avg": 349525
    }
  ],
  "config": {
    "parallel": 3,
    "allow_http": false,
    "verify_tls": true,
    "theme": "dark"
  },
  "statistics": {
    "total_downloaded": 10485760,
    "total_downloads": 1,
    "successful_downloads": 1,
    "failed_downloads": 0
  }
}
```

#### Migration Transformations

| v0.x Field | v1.0.0 Field | Transformation |
|------------|--------------|----------------|
| `checksum` (string) | `checksum` (object) | Parse "algo:hash" → `{algorithm, expected, verified: false}` |
| (none) | `created_at` | Set to current timestamp |
| (none) | `updated_at` | Set to current timestamp |
| (none) | `started_at` | Set to null (unknown) |
| (none) | `completed_at` | Set to current timestamp if completed |
| (none) | `speed_avg` | Set to 0 (unknown) |
| (none) | `statistics` | Calculate from downloads array |

### CLI Changes

**No CLI changes** - v1.0.0 maintains 100% backward compatibility with v0.x CLI:

```bash
# All these commands work identically in v0.x and v1.0.0
safedownload https://example.com/file.zip
safedownload https://example.com/file.zip -o output.zip
safedownload https://example.com/file.zip -c sha256:abc123...
safedownload --manifest urls.txt
safedownload --parallel 5
```

### Performance Improvements

After migration to v1.0.0:
- ✅ Checksum verification 10x faster (parallel chunks)
- ✅ TUI startup <200ms (was ~800ms)
- ✅ Native concurrency (no subprocess overhead)

---

## v1.x to v2.0.0 Migration

### Overview

v2.0.0 ("Horizon") introduces the HTTP API server and web dashboard. This is a **major version** with potential **configuration changes**.

**Key Changes:**
- New `safedownload serve` command for server mode
- JWT authentication for API access
- Web dashboard at `http://localhost:8080`
- Multi-user support (optional)

### Prerequisites

1. Backup state: `cp -r ~/.safedownload ~/.safedownload.backup`
2. Complete any active downloads
3. Review new configuration options

### Migration Steps

```bash
# 1. Update to v2.0.0
brew upgrade safedownload
# or
curl -fsSL https://raw.githubusercontent.com/peternicholls/SafeDownload/main/install.sh | bash

# 2. Verify version
safedownload --version
# Should show v2.0.0

# 3. CLI mode works unchanged
safedownload https://example.com/file.zip

# 4. (Optional) Start server mode
safedownload serve --port 8080
```

### New Configuration Options (v2.0.0)

```json
{
  "config": {
    "server": {
      "enabled": false,
      "port": 8080,
      "bind": "127.0.0.1",
      "auth": {
        "enabled": true,
        "jwt_secret": "auto-generated"
      }
    }
  }
}
```

---

## State File Migration

### Location

State files are stored in:
- **Default**: `~/.safedownload/`
- **Custom**: Set via `SAFEDOWNLOAD_STATE_DIR` environment variable

### Files Affected

| File | Migration Action |
|------|------------------|
| `state.json` | Schema upgraded automatically |
| `config.json` | New fields added with defaults |
| `safedownload.log` | No change (text format) |
| `pids/*.pid` | No change (PID numbers) |

### Backup Before Migration

Always backup before major version upgrades:

```bash
# Create timestamped backup
BACKUP_DIR=~/.safedownload.backup.$(date +%Y%m%d_%H%M%S)
cp -r ~/.safedownload "$BACKUP_DIR"
echo "Backup created: $BACKUP_DIR"
```

---

## Configuration Migration

### v0.2.0 New Configuration

The following configuration options were added in v0.2.0:

```json
{
  "config": {
    "allow_http": false,      // New: HTTPS-only by default
    "verify_tls": true,       // New: TLS verification enabled
    "theme": "dark",          // New: TUI theme
    "log_rotation_mb": 10     // New: Log rotation threshold
  }
}
```

### Migrating from Defaults

If upgrading from v0.1.x, new configuration fields are automatically added with secure defaults:

- `allow_http`: `false` (HTTPS-only, Constitution Principle X)
- `verify_tls`: `true` (TLS verification, Constitution Principle X)
- `theme`: `"dark"` (Default theme)
- `log_rotation_mb`: `10` (10MB log cap, Constitution Principle IX)

---

## Troubleshooting

### Migration Failed: Invalid JSON

**Symptom**: Error parsing state.json

**Solution**:
```bash
# 1. Check JSON validity
python3 -m json.tool ~/.safedownload/state.json

# 2. If invalid, restore from backup
cp ~/.safedownload/state.json.v0.bak ~/.safedownload/state.json

# 3. Or start fresh (lose queue)
rm ~/.safedownload/state.json
safedownload  # Creates new state
```

### Migration Failed: Permission Denied

**Symptom**: Cannot write to state directory

**Solution**:
```bash
# Fix permissions
chmod 700 ~/.safedownload
chmod 600 ~/.safedownload/state.json
```

### Go Binary Not Found

**Symptom**: "Go binary not found" error after upgrade

**Solution**:
```bash
# Re-run installer
curl -fsSL https://raw.githubusercontent.com/peternicholls/SafeDownload/main/install.sh | bash

# Or install Go binary manually
curl -fsSL https://github.com/peternicholls/SafeDownload/releases/latest/download/safedownload-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m) -o /usr/local/bin/safedownload-core
chmod +x /usr/local/bin/safedownload-core
```

### Downloads Lost After Migration

**Symptom**: Queue empty after upgrade

**Solution**:
```bash
# 1. Check backup
ls ~/.safedownload.backup/state.json

# 2. Restore backup
cp ~/.safedownload.backup/state.json ~/.safedownload/state.json

# 3. Re-run migration
safedownload --migrate
```

---

## Rollback Instructions

### Rolling Back to Previous Version

If migration fails or you need to revert:

#### v1.0.0 → v0.2.x Rollback

```bash
# 1. Download previous version
curl -fsSL https://github.com/peternicholls/SafeDownload/releases/download/v0.2.0/install.sh | bash

# 2. Restore state backup
cp ~/.safedownload/state.json.v0.bak ~/.safedownload/state.json

# 3. Verify
safedownload --version
# Should show v0.2.x
```

#### Keeping Both Versions

You can keep multiple versions installed:

```bash
# Install v1.0.0 to different location
curl -fsSL https://github.com/peternicholls/SafeDownload/releases/download/v1.0.0/safedownload-linux-amd64 -o ~/bin/safedownload-v1

# Use specific version
~/bin/safedownload-v1 https://example.com/file.zip
```

---

## Getting Help

- **Documentation**: https://github.com/peternicholls/SafeDownload#readme
- **Issues**: https://github.com/peternicholls/SafeDownload/issues
- **Discussions**: https://github.com/peternicholls/SafeDownload/discussions

When reporting migration issues, include:
1. Source version: `safedownload --version` (before upgrade)
2. Target version
3. Error message (full output)
4. State file snippet (redact sensitive URLs)
