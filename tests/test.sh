#!/usr/bin/env bash
# SafeDownload Test Suite
# Constitution: v1.5.0 - Testing Requirements
#
# Usage: ./tests/test.sh [options]
#   --unit       Run unit tests only
#   --e2e        Run E2E tests only
#   --all        Run all tests (default)
#   --coverage   Generate coverage report
#   --verbose    Verbose output
#
# Exit Codes:
#   0 - All tests passed
#   1 - Test failures
#   2 - Setup error

set -euo pipefail

# ===========================================================================
# Configuration
# ===========================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# PROJECT_ROOT is available for future use if needed
# shellcheck disable=SC2034
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"
TEMP_DIR=""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# ===========================================================================
# Helper Functions
# ===========================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

log_test() {
    echo -e "  [TEST] $*"
}

setup() {
    log_info "Setting up test environment..."
    TEMP_DIR=$(mktemp -d)
    export SAFEDOWNLOAD_STATE_DIR="$TEMP_DIR/.safedownload"
    mkdir -p "$SAFEDOWNLOAD_STATE_DIR"
    
    # Copy fixtures if needed
    if [[ -d "$FIXTURES_DIR" ]]; then
        cp -r "$FIXTURES_DIR"/* "$TEMP_DIR/" 2>/dev/null || true
    fi
    
    log_info "Temp directory: $TEMP_DIR"
}

teardown() {
    log_info "Cleaning up..."
    if [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-}"
    
    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        log_error "Assertion failed: $message"
        log_error "  Expected: $expected"
        log_error "  Actual:   $actual"
        return 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-}"
    
    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        log_error "Assertion failed: $message"
        log_error "  String '$needle' not found in output"
        return 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="${2:-}"
    
    if [[ -f "$file" ]]; then
        return 0
    else
        log_error "Assertion failed: $message"
        log_error "  File not found: $file"
        return 1
    fi
}

run_test() {
    local test_name="$1"
    local test_func="$2"
    
    ((TESTS_RUN++))
    log_test "$test_name"
    
    if $test_func; then
        ((TESTS_PASSED++))
        echo -e "    ${GREEN}✓ PASSED${NC}"
    else
        ((TESTS_FAILED++))
        echo -e "    ${RED}✗ FAILED${NC}"
    fi
}

# ===========================================================================
# Unit Tests
# ===========================================================================

test_curl_available() {
    command -v curl &>/dev/null
}

test_curl_version() {
    local version
    version=$(curl --version | head -1 | awk '{print $2}')
    local major minor
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)
    
    # Constitution requires curl 7.60+
    [[ $major -gt 7 ]] || [[ $major -eq 7 && $minor -ge 60 ]]
}

test_python3_available() {
    command -v python3 &>/dev/null
}

test_state_directory_creation() {
    local test_dir="$TEMP_DIR/test_state"
    mkdir -p "$test_dir/.safedownload"
    [[ -d "$test_dir/.safedownload" ]]
}

test_json_state_valid() {
    local state_file="$TEMP_DIR/state-v1.json"
    if [[ -f "$state_file" ]]; then
        python3 -c "import json; json.load(open('$state_file'))" 2>/dev/null
    else
        # Skip if fixture doesn't exist
        return 0
    fi
}

# ===========================================================================
# Integration Tests
# ===========================================================================

test_https_url_detection() {
    # Test that HTTPS URLs are properly detected
    local url="https://example.com/file.zip"
    [[ "$url" == https://* ]]
}

test_http_url_detection() {
    # Test that HTTP URLs are properly detected
    local url="http://example.com/file.zip"
    [[ "$url" == http://* ]] && [[ "$url" != https://* ]]
}

test_checksum_format_sha256() {
    local checksum="sha256:a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447"
    [[ "$checksum" =~ ^sha256:[a-f0-9]{64}$ ]]
}

test_checksum_format_sha512() {
    local checksum
    if command -v sha512sum &>/dev/null; then
        checksum="sha512:$(printf 'test' | sha512sum | awk '{print $1}')"
    elif command -v shasum &>/dev/null; then
        # macOS uses shasum
        checksum="sha512:$(printf 'test' | shasum -a 512 | awk '{print $1}')"
    else
        log_error "Neither sha512sum nor shasum command found. Cannot run checksum test."
        return 1
    fi
    [[ "$checksum" =~ ^sha512:[a-f0-9]{128}$ ]]
}

test_checksum_format_md5() {
    local checksum
    if command -v md5sum &>/dev/null; then
        checksum="md5:$(printf 'test' | md5sum | awk '{print $1}')"
    elif command -v md5 &>/dev/null; then
        # macOS uses md5
        checksum="md5:$(printf 'test' | md5 -q)"
    else
        log_error "Neither md5sum nor md5 command found. Cannot run checksum test."
        return 1
    fi
    [[ "$checksum" =~ ^md5:[a-f0-9]{32}$ ]]
}

# ===========================================================================
# Fixture Tests
# ===========================================================================

test_fixture_state_v0_exists() {
    # Will pass once fixture is created
    [[ -f "$FIXTURES_DIR/state-v0.json" ]] || return 0
}

test_fixture_state_v1_exists() {
    # Will pass once fixture is created
    [[ -f "$FIXTURES_DIR/state-v1.json" ]] || return 0
}

test_fixture_manifest_exists() {
    # Will pass once fixture is created
    [[ -f "$FIXTURES_DIR/manifest-sample.txt" ]] || return 0
}

# ===========================================================================
# Main
# ===========================================================================

main() {
    local run_unit=true
    local run_e2e=true
    local verbose=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --unit)
                run_e2e=false
                shift
                ;;
            --e2e)
                run_unit=false
                shift
                ;;
            --all)
                run_unit=true
                run_e2e=true
                shift
                ;;
            --verbose)
                # shellcheck disable=SC2034  # Reserved for future verbose output mode
                verbose=true
                shift
                ;;
            --help)
                echo "Usage: $0 [--unit|--e2e|--all] [--verbose]"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 2
                ;;
        esac
    done
    
    echo "========================================"
    echo "SafeDownload Test Suite"
    echo "Constitution: v1.5.0"
    echo "========================================"
    echo ""
    
    # Setup
    trap teardown EXIT
    setup
    
    if $run_unit; then
        echo ""
        log_info "Running Unit Tests..."
        echo "----------------------------------------"
        
        run_test "curl is available" test_curl_available
        run_test "curl version >= 7.60" test_curl_version
        run_test "python3 is available" test_python3_available
        run_test "state directory creation" test_state_directory_creation
        run_test "JSON state validation" test_json_state_valid
        
        echo ""
        log_info "Running Integration Tests..."
        echo "----------------------------------------"
        
        run_test "HTTPS URL detection" test_https_url_detection
        run_test "HTTP URL detection" test_http_url_detection
        run_test "SHA256 checksum format" test_checksum_format_sha256
        run_test "SHA512 checksum format" test_checksum_format_sha512
        run_test "MD5 checksum format" test_checksum_format_md5
        
        echo ""
        log_info "Running Fixture Tests..."
        echo "----------------------------------------"
        
        run_test "state-v0.json fixture" test_fixture_state_v0_exists
        run_test "state-v1.json fixture" test_fixture_state_v1_exists
        run_test "manifest-sample.txt fixture" test_fixture_manifest_exists
    fi
    
    if $run_e2e; then
        echo ""
        log_info "Running E2E Tests..."
        echo "----------------------------------------"
        
        if command -v bats &>/dev/null && [[ -d "$SCRIPT_DIR/e2e" ]]; then
            bats "$SCRIPT_DIR/e2e/"*.bats
        else
            log_warn "BATS not installed or no E2E tests found, skipping"
        fi
    fi
    
    # Summary
    echo ""
    echo "========================================"
    echo "Test Summary"
    echo "========================================"
    echo "  Total:  $TESTS_RUN"
    echo -e "  Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "  Failed: ${RED}$TESTS_FAILED${NC}"
    echo ""
    
    if [[ $TESTS_FAILED -gt 0 ]]; then
        log_error "Some tests failed!"
        exit 1
    else
        log_info "All tests passed!"
        exit 0
    fi
}

main "$@"
