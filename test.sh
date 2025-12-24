#!/usr/bin/env bash
#
# Test script for SafeDownload and the legacy Resumable Download Manager
#

set -euo pipefail

echo "=== SafeDownload - Test Suite ==="
echo

# ============================================================================
# Test Legacy download.sh
# ============================================================================

echo "--- Testing Legacy download.sh ---"
echo

# Test 1: Help message
echo "Test 1: Verify legacy help message displays correctly"
if ./download.sh --help | grep -q "Usage:"; then
    echo "✓ Help message works"
else
    echo "✗ Help message failed"
    exit 1
fi
echo

# Test 2: URL validation (missing URL)
echo "Test 2: Verify error handling for missing URL"
if ./download.sh 2>&1 | grep -q "Usage:"; then
    echo "✓ Missing URL handling works"
else
    echo "✗ Missing URL handling failed"
    exit 1
fi
echo

# Test 3: Filename extraction
echo "Test 3: Test filename extraction from URL"
if grep -q "get_filename_from_url" download.sh; then
    echo "✓ Filename extraction function exists"
else
    echo "✗ Filename extraction function missing"
    exit 1
fi
echo

# Test 4: Check dependencies
echo "Test 4: Verify curl is available"
if command -v curl &> /dev/null; then
    echo "✓ curl is installed"
else
    echo "✗ curl is not installed"
    exit 1
fi
echo

echo "Test 5: Verify bash syntax for download.sh"
if bash -n download.sh; then
    echo "✓ Bash syntax is valid"
else
    echo "✗ Bash syntax is invalid"
    exit 1
fi
echo

# Test 6: Check for required functions
echo "Test 6: Verify all required functions exist in download.sh"
required_functions=(
    "print_info"
    "print_success"
    "print_warning"
    "print_error"
    "usage"
    "get_filename_from_url"
    "format_bytes"
    "get_file_size"
    "check_curl_support"
    "check_resume_support"
    "get_remote_size"
    "download_file"
    "main"
)

all_functions_exist=true
for func in "${required_functions[@]}"; do
    if grep -E "^${func}\(\)|^function ${func}" download.sh > /dev/null 2>&1; then
        echo "  ✓ Function $func exists"
    else
        echo "  ✗ Function $func missing"
        all_functions_exist=false
    fi
done

if [ "$all_functions_exist" = true ]; then
    echo "✓ All required functions exist"
else
    echo "✗ Some required functions are missing"
    exit 1
fi
echo

# Test 7: Check for proper error handling
echo "Test 7: Verify error handling patterns exist"
if grep -q "set -euo pipefail" download.sh; then
    echo "✓ Strict error handling is enabled"
else
    echo "✗ Strict error handling is not enabled"
    exit 1
fi
echo

# ============================================================================
# Test safedownload CLI
# ============================================================================

echo "--- Testing SafeDownload CLI ---"
echo

# Test 8: Help message
echo "Test 8: Verify safedownload help message"
if ./safedownload --help | grep -q "SafeDownload"; then
    echo "✓ SafeDownload help works"
else
    echo "✗ SafeDownload help failed"
    exit 1
fi
echo

# Test 9: Version
echo "Test 9: Verify safedownload version"
if ./safedownload --version | grep -q "SafeDownload v"; then
    echo "✓ Version command works"
else
    echo "✗ Version command failed"
    exit 1
fi
echo

# Test 10: Bash syntax
echo "Test 10: Verify bash syntax for safedownload"
if bash -n safedownload; then
    echo "✓ Bash syntax is valid"
else
    echo "✗ Bash syntax is invalid"
    exit 1
fi
echo

# Test 11: Status command
echo "Test 11: Verify status command"
# Strip all ANSI escape codes (comprehensive pattern)
strip_ansi() {
    sed 's/\x1b\[[0-9;?]*[a-zA-Z]//g; s/\x1b\].*\x07//g; s/\x1b[^[]*//g'
}
if ./safedownload --status 2>&1 | strip_ansi | grep -q "SafeDownload Status\|No downloads"; then
    echo "✓ Status command works"
else
    echo "✗ Status command failed"
    exit 1
fi
echo

# Test 12: List command
echo "Test 12: Verify list command"
# This should return successfully even with no downloads
if ./safedownload --list 2>/dev/null; then
    echo "✓ List command works"
else
    echo "✗ List command failed"
    exit 1
fi
echo

# Test 13: Check for state management functions
echo "Test 13: Verify state management functions exist"
state_functions=(
    "read_state"
    "write_state"
    "add_download"
    "update_download_state"
    "get_download"
    "list_downloads"
    "remove_download"
)

all_state_funcs=true
for func in "${state_functions[@]}"; do
    if grep -E "^${func}\(\)|^function ${func}" safedownload > /dev/null 2>&1; then
        echo "  ✓ Function $func exists"
    else
        echo "  ✗ Function $func missing"
        all_state_funcs=false
    fi
done

if [ "$all_state_funcs" = true ]; then
    echo "✓ All state management functions exist"
else
    echo "✗ Some state management functions are missing"
    exit 1
fi
echo

# Test 14: Check for SHA verification function
echo "Test 14: Verify SHA verification function exists"
if grep -q "verify_sha" safedownload; then
    echo "✓ SHA verification function exists"
else
    echo "✗ SHA verification function missing"
    exit 1
fi
echo

# Test 15: Check for TUI functions
echo "Test 15: Verify TUI functions exist"
tui_functions=(
    "init_tui"
    "cleanup_tui"
    "draw_tui_layout"
    "run_tui"
    "process_tui_command"
)

all_tui_funcs=true
for func in "${tui_functions[@]}"; do
    if grep -E "^${func}\(\)|^function ${func}" safedownload > /dev/null 2>&1; then
        echo "  ✓ Function $func exists"
    else
        echo "  ✗ Function $func missing"
        all_tui_funcs=false
    fi
done

if [ "$all_tui_funcs" = true ]; then
    echo "✓ All TUI functions exist"
else
    echo "✗ Some TUI functions are missing"
    exit 1
fi
echo

# Test 16: Check for parallel download functions
echo "Test 16: Verify parallel download functions exist"
if grep -q "process_queue" safedownload && grep -q "count_active_downloads" safedownload; then
    echo "✓ Parallel download functions exist"
else
    echo "✗ Parallel download functions missing"
    exit 1
fi
echo

# Test 17: Check for manifest support
echo "Test 17: Verify manifest support exists"
if grep -q "parse_manifest" safedownload; then
    echo "✓ Manifest support exists"
else
    echo "✗ Manifest support missing"
    exit 1
fi
echo

# Test 18: Verify python3 is available (required for state management)
echo "Test 18: Verify python3 is available"
if command -v python3 &> /dev/null; then
    echo "✓ python3 is installed"
else
    echo "✗ python3 is not installed (required for safedownload)"
    exit 1
fi
echo

# Test 19: Verify install.sh syntax
echo "Test 19: Verify install.sh syntax"
if bash -n install.sh; then
    echo "✓ Install script syntax is valid"
else
    echo "✗ Install script syntax is invalid"
    exit 1
fi
echo

echo "=== All Tests Passed! ==="
echo
echo "Note: Full integration tests require network access and actual file downloads."
echo "The basic functionality and structure have been verified."
