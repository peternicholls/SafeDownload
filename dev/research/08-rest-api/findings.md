# R08: REST API Design Patterns - Research Findings

**Research ID**: R08  
**Status**: Complete  
**Last Updated**: 2025-12-28

---

## Executive Summary

Recommend building the REST API using Gin (MIT, net/http-based) and streaming progress via Server-Sent Events (SSE). Keep the API as an optional frontend to the Go core to preserve the constitution’s minimal dependency guarantees. Use short-lived JWT Bearer tokens (HMAC-SHA256) for local deployments, with path-based versioning `/api/v1`.

---

## Framework Evaluation

### stdlib net/http

- Pros: Zero deps, Go team maintained, stable; full control.  
- Cons: More boilerplate, manual routing/middleware.

### gin

- Pros: Popular & active, rich middleware ecosystem, good docs, net/http-compatible.  
- Cons: Slight learning curve vs stdlib.

### echo

- Pros: Minimalist and fast, clear API.  
- Cons: Smaller ecosystem vs Gin.

### fiber

- Pros: Very fast, Express-inspired API.  
- Cons: Built on `fasthttp` (non-stdlib), compatibility trade-offs (HTTP/2, tooling).

### Comparison

| Aspect | stdlib | gin | echo | fiber |
|--------|--------|-----|------|-------|
| License | BSD | MIT | MIT | MIT |
| Ecosystem | Low | High | Medium | Medium |
| Middleware | Manual | Rich | Moderate | Rich |
| Performance | Good | Very good | Very good | Excellent |
| Compat. (net/http) | Native | Yes | Yes | No (fasthttp) |

Verdict: Gin offers the best balance of DX, ecosystem, and compatibility while keeping the API optional.

---

## Real-Time Updates

### Server-Sent Events (SSE)

- One-way event stream over HTTP; proxy-friendly; simple to implement.  
- Ideal for pushing progress updates to clients.

### WebSocket

- Bidirectional; useful for interactive features.  
- Higher complexity; may hit proxy/firewall issues.

### Recommendation

Use SSE for progress streaming now; add WebSocket later only if bidirectional control is required.

---

## Authentication

### JWT Approach

- Use HMAC-SHA256 signed Bearer tokens with short TTL; rotate keys via config.  
- For local single-user deployments, support a static API key fallback.  
- Endpoint protection via `Authorization: Bearer <token>`.

---

## API Versioning

### Path Versioning

- `/api/v1/...` for clarity and cache-friendliness.

### Header Versioning

- Optional `Accept-Version` header for advanced clients.

### Recommendation

Primary: Path-based versioning; optionally accept header for future flexibility.

---

## API Design (Draft)

### Key Endpoints

- `POST /api/v1/downloads`: enqueue a download.  
- `GET /api/v1/downloads`: list downloads with states.  
- `GET /api/v1/downloads/{id}`: inspect one download.  
- `DELETE /api/v1/downloads/{id}`: remove/cancel.  
- `GET /api/v1/events`: SSE stream of progress/events.

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-25 | Created document | - |
| 2025-12-28 | Completed research; framework + SSE recommendations | Agent |
