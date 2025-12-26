# State Schema & Versioning

**Version**: 1.0.0  
**Constitution**: v1.5.0 - Configuration & State Schema Versioning  
**Status**: Design Document

## Overview

SafeDownload persists state across sessions via JSON files in `~/.safedownload/`. This document defines the schema versioning strategy, migration approach, and compatibility guarantees.

## Schema Versioning Policy

### Semantic Versioning for Schemas

Schema versions follow semantic versioning (`MAJOR.MINOR.PATCH`):

- **MAJOR**: Breaking changes (field removal, type change, incompatible structure)
- **MINOR**: Backward-compatible additions (new optional fields)
- **PATCH**: Clarifications, documentation, no structural changes

### Schema Version vs App Version

| App Version | State Schema | Config Schema | Notes |
|-------------|--------------|---------------|-------|
| 0.1.0       | None         | None          | No schema_version field (Python-based) |
| 0.2.0       | 1.0.0        | 1.0.0         | Add schema_version field |
| 1.0.0       | 1.0.0        | 1.0.0         | Go migration, compatible schema |
| 1.1.0       | 1.0.0        | 1.1.0         | Add TUI preferences (config only) |
| 1.2.0       | 1.1.0        | 1.1.0         | Add scheduling fields (state) |
| 2.0.0       | 2.0.0        | 2.0.0         | Multi-user support (breaking) |

**Rule**: App version increments independently; schema versions increment only when structure changes.

## File Locations & Purposes

```
~/.safedownload/
├── state.json          # Download queue and progress (schema_version required)
├── config.json         # User preferences (schema_version required)
├── safedownload.log    # Operation log (no schema, plain text)
├── pids/               # Background process PIDs (no schema)
│   └── 1.pid
└── downloads/          # Default download directory (no schema)
```

### state.json

**Purpose**: Persistent download queue, progress tracking, item status

**Schema Evolution**:
- v1.0.0: Initial schema (Go migration)
- v1.1.0: Add `tags`, `group` fields (optional)
- v1.2.0: Add `schedule` field for cron-like scheduling (optional)
- v2.0.0: Add `user_id` field for multi-user support (breaking)

### config.json

**Purpose**: User preferences, TUI settings, defaults

**Schema Evolution**:
- v1.0.0: Basic config (parallel, theme, notifications)
- v1.1.0: Add TUI preferences (layout, colors, sounds)
- v2.0.0: Add API server config (port, auth, CORS)

## Schema Definitions

### state.json v1.0.0

```json
{
  "schema_version": "1.0.0",
  "downloads": [
    {
      "id": 1,
      "url": "https://example.com/file.zip",
      "output": "/path/to/file.zip",
      "status": "downloading",
      "progress": 1048576,
      "total": 10485760,
      "speed": 524288,
      "checksum": "sha256:abc123...",
      "created_at": "2025-12-24T10:00:00Z",
      "updated_at": "2025-12-24T10:01:00Z",
      "error": null
    }
  ],
  "metadata": {
    "last_id": 1,
    "created_at": "2025-12-24T10:00:00Z",
    "updated_at": "2025-12-24T10:01:00Z"
  }
}
```

**Fields**:
- `schema_version` (string, required): Schema version for migration detection
- `downloads` (array, required): List of download items
  - `id` (int, required): Unique sequential ID
  - `url` (string, required): Download URL
  - `output` (string, required): Output file path
  - `status` (string, required): `queued | downloading | completed | failed | paused`
  - `progress` (int, required): Bytes downloaded
  - `total` (int, required): Total bytes (from Content-Length)
  - `speed` (int, optional): Current download speed (bytes/sec)
  - `checksum` (string, optional): Expected checksum (format: `algo:hash`)
  - `created_at` (string, required): ISO 8601 timestamp
  - `updated_at` (string, required): ISO 8601 timestamp
  - `error` (string, nullable): Error message if failed
- `metadata` (object, required): State metadata
  - `last_id` (int, required): Last assigned download ID
  - `created_at` (string, required): State file creation timestamp
  - `updated_at` (string, required): Last state update timestamp

### state.json v1.1.0 (Minor: Add optional fields)

**Changes from v1.0.0**:
- Add `downloads[].tags` (array of strings, optional): User-defined tags for filtering
- Add `downloads[].group` (string, optional): Group name for organization

```json
{
  "schema_version": "1.1.0",
  "downloads": [
    {
      "id": 1,
      "url": "https://example.com/file.zip",
      "output": "/path/to/file.zip",
      "status": "downloading",
      "progress": 1048576,
      "total": 10485760,
      "speed": 524288,
      "checksum": "sha256:abc123...",
      "created_at": "2025-12-24T10:00:00Z",
      "updated_at": "2025-12-24T10:01:00Z",
      "error": null,
      "tags": ["large", "media"],
      "group": "Work Projects"
    }
  ],
  "metadata": {
    "last_id": 1,
    "created_at": "2025-12-24T10:00:00Z",
    "updated_at": "2025-12-24T10:01:00Z"
  }
}
```

**Backward Compatibility**: v1.0.0 readers ignore `tags` and `group` (optional fields)

### config.json v1.0.0

```json
{
  "schema_version": "1.0.0",
  "downloads": {
    "parallel": 3,
    "default_dir": "~/Downloads",
    "allow_http": false,
    "verify_tls": true,
    "max_retries": 3
  },
  "ui": {
    "theme": "dark",
    "show_speed": true,
    "show_eta": true
  },
  "logging": {
    "level": "info",
    "max_size_mb": 10
  }
}
```

### config.json v1.1.0 (Minor: Add TUI preferences)

**Changes from v1.0.0**:
- Add `ui.tui` object with Bubble Tea preferences

```json
{
  "schema_version": "1.1.0",
  "downloads": {
    "parallel": 3,
    "default_dir": "~/Downloads",
    "allow_http": false,
    "verify_tls": true,
    "max_retries": 3
  },
  "ui": {
    "theme": "dark",
    "show_speed": true,
    "show_eta": true,
    "tui": {
      "layout": "dashboard",
      "notifications": true,
      "sounds": false,
      "compact_mode": false
    }
  },
  "logging": {
    "level": "info",
    "max_size_mb": 10
  }
}
```

## Migration Strategy

### Detection

On app start:
1. Read `~/.safedownload/state.json`
2. Check `schema_version` field
3. If missing or < current: trigger migration
4. If > current: error (forward compatibility check)

### Migration Flow

```go
func MigrateState(path string) error {
    // 1. Read raw JSON
    data, err := os.ReadFile(path)
    if err != nil {
        return err
    }
    
    // 2. Detect schema version
    var meta struct {
        SchemaVersion string `json:"schema_version"`
    }
    json.Unmarshal(data, &meta)
    
    // 3. Backup before migration
    backupPath := path + ".v" + meta.SchemaVersion + ".bak"
    os.WriteFile(backupPath, data, 0644)
    
    // 4. Apply migration chain
    switch meta.SchemaVersion {
    case "": // v0.x (no schema_version)
        data = migrateV0ToV1(data)
        fallthrough
    case "1.0.0":
        // Already at target, no migration needed
        return nil
    default:
        return fmt.Errorf("unsupported schema version: %s", meta.SchemaVersion)
    }
    
    // 5. Write migrated state
    return os.WriteFile(path, data, 0644)
}
```

### Migration Functions

#### v0.x → v1.0.0

**Challenge**: v0.x state.json has different structure (Python-generated)

**Example v0.x state.json**:
```json
{
  "downloads": {
    "1": {
      "url": "https://example.com/file.zip",
      "output": "/path/to/file.zip",
      "status": "downloading",
      "progress": 1048576,
      "total": 10485760
    }
  }
}
```

**Migration Logic**:
```go
func migrateV0ToV1(data []byte) ([]byte, error) {
    var v0 struct {
        Downloads map[string]struct {
            URL      string `json:"url"`
            Output   string `json:"output"`
            Status   string `json:"status"`
            Progress int64  `json:"progress"`
            Total    int64  `json:"total"`
        } `json:"downloads"`
    }
    json.Unmarshal(data, &v0)
    
    v1 := StateV1{
        SchemaVersion: "1.0.0",
        Downloads:     []DownloadItem{},
        Metadata: Metadata{
            LastID:    0,
            CreatedAt: time.Now(),
            UpdatedAt: time.Now(),
        },
    }
    
    for idStr, item := range v0.Downloads {
        id, _ := strconv.Atoi(idStr)
        v1.Downloads = append(v1.Downloads, DownloadItem{
            ID:        id,
            URL:       item.URL,
            Output:    item.Output,
            Status:    item.Status,
            Progress:  item.Progress,
            Total:     item.Total,
            CreatedAt: time.Now(), // Best guess
            UpdatedAt: time.Now(),
        })
        if id > v1.Metadata.LastID {
            v1.Metadata.LastID = id
        }
    }
    
    return json.MarshalIndent(v1, "", "  ")
}
```

## Forward Compatibility

### Reading Newer Schemas

App v1.0.0 reading state.json v1.1.0:
- Parse successfully (JSON compatible)
- Ignore unknown fields (`tags`, `group`)
- No data loss (preserve unknown fields on write)

**Implementation**:
```go
type State struct {
    SchemaVersion string         `json:"schema_version"`
    Downloads     []DownloadItem `json:"downloads"`
    Metadata      Metadata       `json:"metadata"`
    Unknown       map[string]any `json:"-"` // Preserve unknown fields
}

func (s *State) UnmarshalJSON(data []byte) error {
    // Parse known fields
    type Alias State
    if err := json.Unmarshal(data, (*Alias)(s)); err != nil {
        return err
    }
    
    // Preserve unknown fields
    var raw map[string]any
    json.Unmarshal(data, &raw)
    // ... store unknown fields in s.Unknown
    
    return nil
}
```

### Breaking Changes (MAJOR)

v2.0.0 schema changes (multi-user support):
- Add `user_id` field (required)
- Change `downloads` structure to per-user buckets

**Migration Required**:
- v1.x → v2.0.0: Automatic migration with default `user_id: "default"`
- v2.0.0 → v1.x: **NOT SUPPORTED** (data loss risk)

**Error Handling**:
```go
if detectedVersion > currentVersion {
    return fmt.Errorf(
        "state file schema v%s is newer than app supports (v%s). Upgrade SafeDownload to continue.",
        detectedVersion, currentVersion,
    )
}
```

## Validation

### Schema Validation

On every state read:
1. Validate `schema_version` format (semver)
2. Validate required fields present
3. Validate field types
4. Validate enum values (e.g., `status` must be valid)

**Example**:
```go
func ValidateState(s *State) error {
    if s.SchemaVersion == "" {
        return errors.New("missing schema_version")
    }
    
    for _, item := range s.Downloads {
        if !isValidStatus(item.Status) {
            return fmt.Errorf("invalid status: %s", item.Status)
        }
        if item.Progress > item.Total {
            return errors.New("progress exceeds total")
        }
    }
    
    return nil
}
```

## Testing

### Migration Tests

```go
func TestMigrateV0ToV1(t *testing.T) {
    v0Data := `{"downloads": {"1": {"url": "...", ...}}}`
    v1Data, err := migrateV0ToV1([]byte(v0Data))
    assert.NoError(t, err)
    
    var v1 StateV1
    json.Unmarshal(v1Data, &v1)
    assert.Equal(t, "1.0.0", v1.SchemaVersion)
    assert.Len(t, v1.Downloads, 1)
}
```

### Forward Compatibility Tests

```go
func TestReadNewerSchema(t *testing.T) {
    // v1.0.0 app reading v1.1.0 state
    v11Data := `{"schema_version": "1.1.0", "downloads": [{"tags": ["test"]}]}`
    
    var state State
    err := json.Unmarshal([]byte(v11Data), &state)
    assert.NoError(t, err)
    
    // Re-marshal and verify tags preserved
    output, _ := json.Marshal(state)
    assert.Contains(t, string(output), "tags")
}
```

## Rollback Strategy

If migration fails or user wants to revert:

1. **Backup exists**: `.safedownload/state.json.v0.bak`
2. **Manual rollback**:
   ```bash
   cd ~/.safedownload
   mv state.json state.json.v1.failed
   mv state.json.v0.bak state.json
   ```
3. **Downgrade app**: Install previous version
4. **Report issue**: GitHub issue with failed state.json (sanitized)

## Documentation Requirements

### MIGRATION.md

Must include:
- Schema version table (app version → schema version)
- Migration checklist for major upgrades
- Rollback instructions
- Troubleshooting common migration errors

### README.md

Must include:
- State file location (`~/.safedownload/state.json`)
- Backup recommendation before major upgrades
- Link to MIGRATION.md

### Code Documentation

```go
// StateV1 represents the state.json schema version 1.0.0.
// Schema version: 1.0.0
// Added in: SafeDownload v0.2.0 (Bash/Python), v1.0.0 (Go)
// Breaking changes from v0.x:
//   - Added schema_version field
//   - Changed downloads from map to array
//   - Added created_at, updated_at timestamps
type StateV1 struct {
    SchemaVersion string         `json:"schema_version"` // Always "1.0.0"
    Downloads     []DownloadItem `json:"downloads"`
    Metadata      Metadata       `json:"metadata"`
}
```

## Future Considerations

### v2.0.0 Multi-User Schema

```json
{
  "schema_version": "2.0.0",
  "users": {
    "alice": {
      "downloads": [...],
      "quota_mb": 10240
    },
    "bob": {
      "downloads": [...],
      "quota_mb": 5120
    }
  },
  "metadata": {...}
}
```

**Migration v1.x → v2.0.0**:
- Create single user "default"
- Move all downloads under "default" user
- Set unlimited quota

### Alternative: SQLite

If state complexity grows (v2.x+), consider SQLite:
- Schema migrations via `github.com/golang-migrate/migrate`
- Atomic transactions
- Indexing for fast queries
- Still local-only (constitution compliance)

**Migration**: Export JSON → Import to SQLite, keep JSON as backup
