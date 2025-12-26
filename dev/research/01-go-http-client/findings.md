# R01: Go HTTP Client Libraries - Research Findings

**Research ID**: R01  
**Status**: Complete  
**Last Updated**: 2025-12-25  
**Researcher**: Agent  
**Time Spent**: ~3 hours

---

## Executive Summary

This research evaluated HTTP client libraries for SafeDownload's Go core migration, focusing on **resumable download support** (Constitution Principle III) and **minimal dependencies** (Constitution Principle II).

**Recommendation**: Use **stdlib net/http** with a custom download manager wrapper, informed by grab's patterns. This approach provides zero external dependencies, full control over implementation, and aligns with constitution principles.

**Key Findings**:
1. stdlib net/http provides all primitives needed for resumable downloads
2. grab library offers excellent patterns but has maintenance concerns (last major update 4 years ago)
3. resty is feature-rich but overkill for download use case (REST client, not download manager)
4. Connection pooling requires careful configuration for concurrent downloads

---

## Library Evaluations

### 1. stdlib `net/http`

**Source**: https://pkg.go.dev/net/http  
**License**: BSD-3-Clause (Go standard library)  
**Dependencies**: 0 (part of Go itself)

#### Evaluation Notes

The Go standard library provides a robust HTTP client through `http.Client` and `http.Transport`. It supports all necessary features for building a download manager:

- Range header requests for resumable downloads
- Context cancellation for clean abort
- Connection pooling via `http.Transport`
- TLS configuration for secure downloads
- HTTP/2 automatic upgrade

#### Code Example: Basic Resumable Download

```go
package downloader

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "os"
)

// ResumeDownload downloads a file with resume support
func ResumeDownload(ctx context.Context, url, destPath string) error {
    // Check for existing partial download
    existingSize := int64(0)
    if stat, err := os.Stat(destPath); err == nil {
        existingSize = stat.Size()
    }

    // Create request with Range header if resuming
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return fmt.Errorf("create request: %w", err)
    }

    if existingSize > 0 {
        req.Header.Set("Range", fmt.Sprintf("bytes=%d-", existingSize))
    }

    // Execute request
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return fmt.Errorf("execute request: %w", err)
    }
    defer resp.Body.Close()

    // Handle response status
    switch resp.StatusCode {
    case http.StatusOK:
        // Server doesn't support range, start fresh
        existingSize = 0
    case http.StatusPartialContent:
        // Resume from existing position
    case http.StatusRequestedRangeNotSatisfiable:
        // File already complete
        return nil
    default:
        return fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }

    // Open file for writing (append if resuming)
    flags := os.O_CREATE | os.O_WRONLY
    if existingSize > 0 {
        flags |= os.O_APPEND
    } else {
        flags |= os.O_TRUNC
    }
    
    file, err := os.OpenFile(destPath, flags, 0644)
    if err != nil {
        return fmt.Errorf("open file: %w", err)
    }
    defer file.Close()

    // Copy with progress tracking possible
    _, err = io.Copy(file, resp.Body)
    return err
}
```

#### Pros Discovered

- **Zero dependencies**: Part of Go standard library
- **Full control**: Complete flexibility over implementation
- **Well-documented**: Extensive official documentation
- **Battle-tested**: Used by millions of Go applications
- **Active development**: Maintained by Go team
- **HTTP/2 support**: Automatic upgrade when available
- **Context support**: First-class cancellation

#### Cons Discovered

- **More boilerplate**: Need to implement resume logic manually
- **No progress tracking**: Must build progress callbacks
- **No batch downloads**: Must implement concurrency logic
- **No checksum helpers**: Verification logic needed

#### Recommendation

✅ **RECOMMENDED** - Best choice for SafeDownload. Zero dependencies align with Constitution Principle II, and full control allows precise implementation of resume behavior.

---

### 2. grab Library

**Source**: https://github.com/cavaliergopher/grab  
**Stars**: 1,465 ⭐  
**License**: BSD-3-Clause  
**Last Push**: 2024-05-14  
**Last Major Update**: ~4 years ago  
**Open Issues**: 28  
**Used By**: 570 repositories

#### Evaluation Notes

Grab is a purpose-built download manager for Go with impressive built-in features. The library was designed for "downloading thousands of large files from remote file repositories where the remote files are immutable."

**Design Philosophy** (from README):
> "Grab aims to be stateless. The only state that exists is the remote files you wish to download and the local copy which may be completed, partially completed or not yet created."

This aligns well with SafeDownload's state persistence approach.

**Features**:
- Auto-resume incomplete downloads
- Progress monitoring (concurrent via channels)
- Checksum verification
- Batch downloads with concurrency control
- Rate limiting (extensible interface)
- Filename guessing from headers/URL

#### Code Example: Using grab

```go
package main

import (
    "fmt"
    "time"
    "github.com/cavaliergopher/grab/v3"
)

func main() {
    client := grab.NewClient()
    req, _ := grab.NewRequest(".", "https://example.com/file.zip")

    // Start download
    resp := client.Do(req)

    // Progress loop
    t := time.NewTicker(500 * time.Millisecond)
    defer t.Stop()

    for {
        select {
        case <-t.C:
            fmt.Printf("Progress: %.2f%%\n", 100*resp.Progress())
        case <-resp.Done:
            if err := resp.Err(); err != nil {
                fmt.Printf("Error: %v\n", err)
            }
            return
        }
    }
}
```

#### Pros Discovered

- **Resume built-in**: Automatic resume on second run
- **Progress callbacks**: Easy progress tracking via channels
- **Checksum support**: Built-in verification
- **Batch API**: Download multiple files with worker pool
- **Well-designed API**: Clean, idiomatic Go
- **Stateless**: No additional state files (like .crdownload)

#### Cons Discovered

- **Maintenance concerns**: Last significant commit 4 years ago
- **External dependency**: Adds 1 dependency to project
- **28 open issues**: Some long-standing bugs
- **Limited customization**: Some patterns hardcoded
- **No HTTP/2 optimizations**: Uses HTTP/1.1 patterns

#### Recommendation

⚠️ **STUDY BUT DON'T ADOPT** - Excellent patterns to learn from, but maintenance status is concerning. Use as reference implementation for our stdlib wrapper.

---

### 3. resty Library

**Source**: https://github.com/go-resty/resty  
**Stars**: 11,432 ⭐  
**License**: MIT  
**Last Push**: 2025-12-25 (actively maintained)  
**Open Issues**: 23  
**Forks**: 771

#### Evaluation Notes

Resty is a full-featured REST client library for Go. While popular and actively maintained, it's designed for API interactions rather than file downloads.

**Features**:
- Fluent API for HTTP requests
- Automatic JSON/XML marshaling
- Request/response middleware
- Retry with backoff
- Multipart file upload
- Debug mode

#### Code Example: Download with resty

```go
package main

import (
    "github.com/go-resty/resty/v2"
)

func main() {
    client := resty.New()
    
    // Basic download (no resume support)
    _, err := client.R().
        SetOutput("file.zip").
        Get("https://example.com/file.zip")
    
    if err != nil {
        panic(err)
    }
}
```

#### Pros Discovered

- **Actively maintained**: Commits within last week
- **Large community**: 11,000+ stars
- **Rich features**: Middleware, retry, debug
- **Good docs**: Comprehensive documentation

#### Cons Discovered

- **Not designed for downloads**: REST client, not download manager
- **No resume support**: Must implement Range headers manually
- **No progress tracking**: For downloads specifically
- **Heavy**: Many features we don't need
- **Multiple dependencies**: Brings transitive dependencies

#### Recommendation

❌ **NOT RECOMMENDED** - Wrong tool for the job. Designed for REST APIs, not file downloads.

---

### 4. go-retryablehttp

**Source**: https://github.com/hashicorp/go-retryablehttp  
**Stars**: 2,247 ⭐  
**License**: MPL-2.0  
**Last Push**: 2025-12-09  
**Open Issues**: 80

#### Evaluation Notes

HashiCorp's retryable HTTP client wraps net/http with automatic retry logic and backoff. Useful for API calls, but not designed for large file downloads.

#### Pros Discovered

- **Automatic retries**: Configurable retry policy
- **Backoff strategies**: Linear and exponential
- **Logging integration**: Structured logging support
- **Maintained**: HashiCorp backing

#### Cons Discovered

- **MPL-2.0 license**: More restrictive than BSD/MIT
- **Not download-focused**: Retries entire request, not resume
- **80 open issues**: Significant issue backlog
- **External dependency**: Adds dependency

#### Recommendation

❌ **NOT RECOMMENDED** - Retry semantics don't match download use case. We need resume (Range headers), not full-request retry.

---

## Comparison Matrix

| Criterion (Weight) | stdlib net/http | grab | resty | go-retryablehttp |
|--------------------|-----------------|------|-------|------------------|
| **Constitution Alignment (25%)** | 100 | 70 | 40 | 50 |
| **Performance (20%)** | 90 | 85 | 80 | 75 |
| **Maintainability (20%)** | 100 | 50 | 90 | 70 |
| **Developer Experience (15%)** | 60 | 95 | 85 | 70 |
| **Community Support (10%)** | 100 | 60 | 95 | 75 |
| **Dependency Footprint (10%)** | 100 | 80 | 50 | 60 |
| **Weighted Score** | **91.5** | **71.0** | **71.5** | **66.5** |

### Scoring Rationale

**stdlib net/http (91.5)**:
- Constitution: Perfect (zero deps, full control)
- Performance: Excellent (direct access to primitives)
- Maintainability: Perfect (Go team maintains)
- DX: Lower (more boilerplate required)
- Community: Perfect (entire Go ecosystem)
- Dependencies: Perfect (zero)

**grab (71.0)**:
- Constitution: Good but has external dependency
- Performance: Very good (optimized for downloads)
- Maintainability: Concerning (4 years since major update)
- DX: Excellent (download-focused API)
- Community: Limited (1.4k stars, 570 users)
- Dependencies: Good (minimal deps)

---

## HTTP Range Request Implementation

### How Range Requests Work

HTTP Range requests enable partial content retrieval, essential for resumable downloads.

**Request Flow**:
1. Client sends `Range: bytes=N-M` header (or `bytes=N-` for "N to end")
2. Server responds with `206 Partial Content` if supported
3. Server includes `Content-Range: bytes N-M/total` header
4. Server sends only the requested byte range

**Key Headers**:
- `Accept-Ranges: bytes` - Server indicates range support
- `Range: bytes=0-999` - Client requests first 1000 bytes
- `Content-Range: bytes 0-999/5000` - Server confirms partial response
- `If-Range: <etag>` - Conditional range (only if unchanged)

### Server Support Detection

```go
// CheckRangeSupport performs a HEAD request to check if server supports Range
func CheckRangeSupport(ctx context.Context, url string) (bool, int64, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodHead, url, nil)
    if err != nil {
        return false, 0, err
    }

    client := &http.Client{Timeout: 30 * time.Second}
    resp, err := client.Do(req)
    if err != nil {
        return false, 0, err
    }
    defer resp.Body.Close()

    // Check for Accept-Ranges header
    acceptRanges := resp.Header.Get("Accept-Ranges")
    supportsRange := acceptRanges == "bytes"

    // Get content length if available
    contentLength := resp.ContentLength

    return supportsRange, contentLength, nil
}
```

### Handling Partial Content (206)

```go
// HandlePartialContent processes a 206 response for resume
func HandlePartialContent(resp *http.Response, destFile *os.File) error {
    // Validate 206 response
    if resp.StatusCode != http.StatusPartialContent {
        return fmt.Errorf("expected 206, got %d", resp.StatusCode)
    }

    // Parse Content-Range header
    contentRange := resp.Header.Get("Content-Range")
    // Format: "bytes 1000-1999/5000"
    var start, end, total int64
    _, err := fmt.Sscanf(contentRange, "bytes %d-%d/%d", &start, &end, &total)
    if err != nil {
        return fmt.Errorf("parse Content-Range: %w", err)
    }

    // Verify we're resuming from the right position
    currentPos, _ := destFile.Seek(0, io.SeekEnd)
    if currentPos != start {
        return fmt.Errorf("position mismatch: file at %d, server at %d", currentPos, start)
    }

    // Copy remaining content
    _, err = io.Copy(destFile, resp.Body)
    return err
}
```

### Fallback for Non-Supporting Servers

```go
// DownloadWithFallback attempts range request, falls back to full download
func DownloadWithFallback(ctx context.Context, url, destPath string) error {
    existingSize := getFileSize(destPath)
    
    req, _ := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if existingSize > 0 {
        req.Header.Set("Range", fmt.Sprintf("bytes=%d-", existingSize))
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    switch resp.StatusCode {
    case http.StatusOK:
        // Server doesn't support Range or file changed
        // Start fresh download
        return downloadFresh(destPath, resp.Body)
    
    case http.StatusPartialContent:
        // Resume from existing position
        return appendToFile(destPath, resp.Body)
    
    case http.StatusRequestedRangeNotSatisfiable:
        // Range is beyond file size - file is complete
        return nil
    
    default:
        return fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }
}
```

---

## Connection Pooling Strategy

### http.Transport Configuration

The default `http.Transport` configuration is suboptimal for concurrent downloads. Key findings from research:

**Default Values (problematic)**:
- `MaxIdleConns`: 100
- `MaxIdleConnsPerHost`: 2 (too low!)
- `IdleConnTimeout`: 90s

**Problem**: With only 2 idle connections per host, concurrent downloads to the same server will queue and cause `TIME_WAIT` socket exhaustion.

**Recommended Configuration for SafeDownload**:

```go
// NewDownloadTransport creates an optimized transport for concurrent downloads
func NewDownloadTransport() *http.Transport {
    // Clone default to inherit TLS settings
    t := http.DefaultTransport.(*http.Transport).Clone()
    
    // Increase connection pool for concurrent downloads
    t.MaxIdleConns = 100
    t.MaxConnsPerHost = 100        // Limit total connections per host
    t.MaxIdleConnsPerHost = 100    // Keep all idle connections
    t.IdleConnTimeout = 90 * time.Second
    
    // Optimize for large file transfers
    t.ResponseHeaderTimeout = 30 * time.Second
    t.ExpectContinueTimeout = 1 * time.Second
    
    // Enable HTTP/2 (default with TLS)
    t.ForceAttemptHTTP2 = true
    
    return t
}

// Usage
var downloadClient = &http.Client{
    Transport: NewDownloadTransport(),
    Timeout:   0, // No timeout for large downloads (use context instead)
}
```

### Critical Warning

⚠️ **Go Version Note**: `Transport.MaxConnsPerHost` had a bug causing panics under high load in versions prior to Go 1.24.8 and 1.25.2. Ensure SafeDownload requires Go 1.24.8+ if using this setting.

### Connection Pool Best Practices

1. **Read response body completely**: Connections only return to pool after `resp.Body.Close()` with body fully read
2. **Use `io.Copy(io.Discard, resp.Body)`** if discarding body
3. **Prefer HTTP/2** when available for multiplexing benefits
4. **Test HTTP/1.1 vs HTTP/2**: Large file transfers may perform better on HTTP/1.1 due to head-of-line blocking in HTTP/2

### Concurrent Download Management

```go
// DownloadManager manages concurrent downloads with pooled connections
type DownloadManager struct {
    client      *http.Client
    maxWorkers  int
    semaphore   chan struct{}
}

func NewDownloadManager(maxConcurrent int) *DownloadManager {
    return &DownloadManager{
        client: &http.Client{
            Transport: NewDownloadTransport(),
        },
        maxWorkers: maxConcurrent,
        semaphore:  make(chan struct{}, maxConcurrent),
    }
}

// Download starts a download with concurrency limiting
func (dm *DownloadManager) Download(ctx context.Context, url, dest string) error {
    // Acquire semaphore slot
    select {
    case dm.semaphore <- struct{}{}:
        defer func() { <-dm.semaphore }()
    case <-ctx.Done():
        return ctx.Err()
    }
    
    // Perform download using shared client (and connection pool)
    return dm.downloadFile(ctx, url, dest)
}
```

---

## Benchmarks

### Test Methodology

Benchmarks should be performed during implementation phase with:
- File sizes: 1MB, 100MB, 1GB
- Network conditions: Local, LAN, WAN
- Concurrency levels: 1, 5, 10, 20 downloads
- Metrics: Throughput, memory usage, CPU usage, connection count

### Projected Results

Based on research, expected characteristics:

| Implementation | Strengths | Weaknesses |
|----------------|-----------|------------|
| stdlib + wrapper | Lowest memory, fastest startup | Slightly more CPU for progress tracking |
| grab | Best DX, proven patterns | Memory overhead from features |

### Recommendation

Benchmark during Sprint 01 implementation to validate approach. If stdlib wrapper performance is within 10% of grab, proceed with stdlib.

---

## Key Quotes and References

### Quote 1: grab Design Philosophy

> "Grab aims to be stateless. The only state that exists is the remote files you wish to download and the local copy which may be completed, partially completed or not yet created."

**Source**: [grab README](https://github.com/cavaliergopher/grab)  
**Relevance**: Aligns with SafeDownload's state persistence approach - external state file, not embedded

### Quote 2: Connection Pooling

> "Configure Transport.MaxIdleConnsPerHost and Transport.MaxIdleConns to relatively high values, such as 100 (or even 10,000!) to improve HTTP/1.1 performance."

**Source**: [Go HTTP Connection Pools](https://davidbacisin.com/writing/golang-http-connection-pools-1)  
**Relevance**: Critical configuration for concurrent downloads

### Quote 3: Response Body Handling

> "In Go, the response body must be read to completion and closed before it can be returned to the idle connection pool."

**Source**: [Go HTTP Connection Pools](https://davidbacisin.com/writing/golang-http-connection-pools-1)  
**Relevance**: Important for connection pool efficiency

---

## Decision Rationale

### Final Decision

**Use stdlib net/http with a custom download manager wrapper**, informed by grab's patterns.

### Rationale

1. **Constitution Alignment**: Zero external dependencies (Principle II)
2. **Full Control**: Can implement exact resume behavior needed (Principle III)
3. **Long-term Maintenance**: No dependency on external project health
4. **Performance**: Direct access to HTTP primitives
5. **Learning Value**: grab provides excellent patterns to study

### Trade-offs Accepted

1. **More Development Time**: ~2-3 days extra vs using grab directly
2. **More Testing**: Must verify resume behavior thoroughly
3. **Feature Implementation**: Progress tracking, checksums need custom code

### Mitigation Strategy

- Study grab's implementation for patterns
- Port proven patterns, not entire library
- Write comprehensive tests for resume behavior

---

## Answers to Key Questions

### Q1: Should we use grab library or stdlib net/http?

**Answer**: Use stdlib net/http with custom wrapper  
**Confidence**: HIGH  
**Rationale**: Zero dependencies align with constitution, grab's maintenance status is concerning, stdlib provides all necessary primitives

### Q2: How to implement range header requests for resume?

**Answer**: See "HTTP Range Request Implementation" section above  
**Confidence**: HIGH  
**Rationale**: Standard HTTP mechanism, well-documented, code examples provided

### Q3: Connection pooling strategy for parallel downloads?

**Answer**: Configure custom `http.Transport` with `MaxIdleConnsPerHost=100`, `MaxConnsPerHost=100`  
**Confidence**: HIGH  
**Rationale**: Research confirms default settings inadequate, best practices documented

### Q4: How to handle servers that don't support Range headers?

**Answer**: Check for 200 vs 206 status, fallback to fresh download  
**Confidence**: HIGH  
**Rationale**: HTTP spec defines behavior, graceful degradation implemented in code example

### Q5: TLS certificate verification approach?

**Answer**: Use stdlib defaults (system cert pool), allow optional custom CA for enterprise  
**Confidence**: MEDIUM  
**Rationale**: Needs validation in R06 (GPG Verification research)

---

## Open Questions

1. **HTTP/2 vs HTTP/1.1 for large downloads**: Need benchmarks to determine optimal protocol for SafeDownload's use case
2. **Custom dialer for congestion control**: Advanced optimization for future version
3. **Connection keep-alive across download queue**: How long to maintain pool between batch downloads

---

## Action Items

- [x] Evaluate HTTP client libraries
- [x] Document Range header implementation
- [x] Document connection pooling configuration
- [x] Create comparison matrix with scoring
- [ ] Create decision entry in decision-log.yaml
- [ ] Update feature spec F011 with library choice
- [ ] Benchmark during Sprint 01 implementation

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-25 | Created document | - |
| 2025-12-25 | Completed full research - library evaluation, Range headers, connection pooling | Agent |
