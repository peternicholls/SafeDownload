# R09: Plugin System Architectures - Research Findings

**Research ID**: R09  
**Status**: Complete  
**Last Updated**: 2025-12-28

---

## Executive Summary

Recommend a subprocess/exec plugin architecture using JSON-RPC over stdio. This maximizes portability, isolates failures for security, and aligns with the constitution’s minimal dependency principle. HashiCorp go-plugin is a strong alternative if richer RPC features are later required. Native Go plugins are rejected due to platform/version brittleness.

---

## Architecture Comparison

### Go Native Plugins

- Pros: Fast, type-safe.  
- Cons: Compiler/version coupling, limited platform support; buildmode=plugin constraints; not recommended for broad distribution.

### Subprocess/Exec

- Pros: Strong isolation, language-agnostic, simple to implement via stdio; better security posture.  
- Cons: IPC overhead; requires protocol design.

### HashiCorp go-plugin (gRPC)

- Pros: Battle-tested, structured RPC, discovery helpers.  
- Cons: Extra dependency and complexity for initial needs.

### WASM

- Pros: Sandboxed, portable across platforms.  
- Cons: Tooling/embedding complexity; performance overhead; not necessary initially.

---

## Plugin Discovery

### Directory Convention

- Host scans `~/.safedownload/plugins/` and `$XDG_DATA_HOME/safedownload/plugins/` for executables.  
- Optional system-wide path `/usr/local/lib/safedownload/plugins/` with warning for multi-user environments.

### Plugin Manifest (adjacent `.yaml`)

```yaml
name: example-plugin
schema_version: 1.0.0
api:
	min_version: 1.0.0
	max_version: 1.x
capabilities:
	- hook: post-download
	- command: verify
entrypoint: ./example-plugin
env_allowlist:
	- SAFEDOWNLOAD_CONFIG
args: []
```

---

## Plugin API Design

### Interface (JSON-RPC)

```json
{
	"jsonrpc": "2.0",
	"method": "Plugin.Init",
	"params": {"host_api_version": "1.0.0", "capabilities": ["post-download"]},
	"id": 1
}
```

Methods: `Plugin.Init`, `Plugin.Capabilities`, `Plugin.HandleEvent`, `Plugin.HandleCommand`.

### Versioning

- Semantic versioning for API; host supports range; plugins declare compatible ranges.  
- Capability discovery for optional features; unknown fields ignored.

---

## Security

### Sandboxing Options

- Process isolation by default. Optional: seccomp (Linux), macOS sandbox profiles, chroot/jail.  
- Strict allowlist for env vars and CLI args; no network access by default unless declared.

### Guidelines

- Least privilege; validate inputs; timeouts and memory limits; structured logs with no sensitive data.

---

## Decision

- Selection: Subprocess/exec + JSON-RPC over stdio.  
- Rationale: Portability, security isolation, minimal deps; aligns with constitution.  
- Fallback: Adopt HashiCorp go-plugin if complex RPC needs arise.

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-25 | Created document | - |
| 2025-12-28 | Completed research; architecture decision proposed | Agent |
