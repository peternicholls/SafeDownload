# Tests Directory

This directory contains all test suites for SafeDownload.

**Constitution**: v1.5.0 - Testing Requirements

## Directory Structure

```
tests/
├── README.md           # This file
├── test.sh             # Main test runner
├── unit/               # Unit tests (60% of total)
│   └── (Go tests when v1.0.0)
├── integration/        # Integration tests (30% of total)
│   └── (Go tests when v1.0.0)
├── e2e/                # End-to-end tests (10% of total)
│   └── cli_test.bats   # CLI behavior tests
├── security/           # Security-focused tests
├── accessibility/      # Accessibility tests
├── performance/        # Benchmark tests
└── fixtures/           # Test data
    ├── state-v0.json   # v0.x state file sample
    ├── state-v1.json   # v1.0.0 state file sample
    └── manifest-sample.txt  # Sample manifest file
```

## Running Tests

### All Tests
```bash
./tests/test.sh
```

### Unit Tests Only
```bash
./tests/test.sh --unit
```

### E2E Tests Only
```bash
./tests/test.sh --e2e
# Or directly with BATS:
bats tests/e2e/
```

### Go Tests (v1.0.0+)
```bash
# All tests
go test ./...

# With coverage
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out

# With race detection
go test -race ./...

# Benchmarks
go test -bench=. ./...
```

## Coverage Requirements

Per Constitution v1.5.0:

| Code Type | Minimum Coverage |
|-----------|------------------|
| Go code (v1.x+) | ≥80% line coverage |
| Bash code (v0.x) | ≥60% function coverage |
| Public APIs | 100% documentation |

## Test Categories

### Unit Tests (60%)
- Fast (<5s total)
- No external dependencies (use mocks)
- Test individual functions/methods

### Integration Tests (30%)
- Component interactions
- May use filesystem
- Mock network calls

### E2E Tests (10%)
- Full CLI workflows
- Real binary execution
- Constitution compliance verification

### Security Tests
- HTTPS enforcement (Principle X)
- Credential leak prevention (Principle IX, X)
- TLS verification

### Accessibility Tests
- High-contrast mode (Principle XI)
- Colorblind-safe indicators
- Screen reader compatibility

### Performance Tests
- TUI startup <500ms
- Queue list <100ms
- Add download <100ms

## Adding Tests

### For Bash (v0.x)
Add test functions to `test.sh`:
```bash
test_my_feature() {
    # Test implementation
    [[ "$result" == "expected" ]]
}

# In main, add:
run_test "My feature description" test_my_feature
```

### For BATS E2E
Add to `e2e/cli_test.bats`:
```bash
@test "CLI: My feature description" {
    run "$SAFEDOWNLOAD" my-command
    [ "$status" -eq 0 ]
    [[ "$output" =~ "expected" ]]
}
```

### For Go (v1.0.0+)
Create `*_test.go` files:
```go
func TestMyFeature(t *testing.T) {
    // Test implementation
    assert.Equal(t, expected, actual)
}
```

## Fixtures

Test fixtures are in `fixtures/`:

- **state-v0.json**: Sample v0.x state file for migration testing
- **state-v1.json**: Sample v1.0.0 state file with all fields
- **manifest-sample.txt**: Sample manifest with various URL formats

## CI Integration

Tests run automatically via GitHub Actions on:
- Push to `main`
- Pull requests to `main`

See `.github/workflows/test.yml` for configuration.
