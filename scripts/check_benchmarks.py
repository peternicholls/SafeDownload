#!/usr/bin/env python3
"""
Benchmark Performance Gate Checker

Parses Go benchmark output and enforces constitution performance requirements.
Part of CI/CD pipeline for SafeDownload.

Constitution Requirements (Principle III - Resumable):
- TUI startup: <500ms (target: <200ms)
- List operation: <100ms
- Checksum verification: Parallelized

Usage:
    go test -bench=. -benchmem ./... | python3 scripts/check_benchmarks.py
    python3 scripts/check_benchmarks.py benchmark_results.txt
"""

import re
import sys
import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class BenchmarkResult:
    """Parsed benchmark result from Go test output."""
    name: str
    iterations: int
    ns_per_op: float
    bytes_per_op: Optional[int] = None
    allocs_per_op: Optional[int] = None

    @property
    def ms_per_op(self) -> float:
        """Convert nanoseconds to milliseconds."""
        return self.ns_per_op / 1_000_000

    @property
    def us_per_op(self) -> float:
        """Convert nanoseconds to microseconds."""
        return self.ns_per_op / 1_000


# Constitution-mandated performance gates
PERFORMANCE_GATES: Dict[str, Dict[str, Any]] = {
    # TUI startup must be under 500ms (target 200ms)
    "BenchmarkTUIStartup": {
        "max_ms": 500,
        "target_ms": 200,
        "description": "TUI startup time (Constitution Principle III)",
    },
    # List operation must be under 100ms
    "BenchmarkListDownloads": {
        "max_ms": 100,
        "target_ms": 50,
        "description": "List downloads operation",
    },
    "BenchmarkQueueList": {
        "max_ms": 100,
        "target_ms": 50,
        "description": "Queue list operation",
    },
    # State operations should be fast
    "BenchmarkStateLoad": {
        "max_ms": 50,
        "target_ms": 20,
        "description": "State file loading",
    },
    "BenchmarkStateSave": {
        "max_ms": 100,
        "target_ms": 50,
        "description": "State file saving",
    },
    # Checksum operations (should leverage parallelization)
    "BenchmarkChecksumSHA256": {
        "max_ms": 1000,  # Per 10MB
        "target_ms": 500,
        "description": "SHA256 checksum (per 10MB)",
    },
    "BenchmarkChecksumMD5": {
        "max_ms": 500,  # Per 10MB
        "target_ms": 250,
        "description": "MD5 checksum (per 10MB)",
    },
}

# Pattern to match Go benchmark output
# Example: BenchmarkTUIStartup-8    1000    150000 ns/op    1024 B/op    10 allocs/op
BENCHMARK_PATTERN = re.compile(
    r"^(Benchmark\w+)(?:-\d+)?\s+"  # Benchmark name (with optional CPU count)
    r"(\d+)\s+"                      # Iterations
    r"([\d.]+)\s+ns/op"              # Nanoseconds per operation
    r"(?:\s+(\d+)\s+B/op)?"          # Optional: bytes per operation
    r"(?:\s+(\d+)\s+allocs/op)?",    # Optional: allocations per operation
    re.MULTILINE
)


def parse_benchmark_output(content: str) -> List[BenchmarkResult]:
    """Parse Go benchmark output into structured results."""
    results = []

    for match in BENCHMARK_PATTERN.finditer(content):
        name = match.group(1)
        iterations = int(match.group(2))
        ns_per_op = float(match.group(3))
        bytes_per_op = int(match.group(4)) if match.group(4) else None
        allocs_per_op = int(match.group(5)) if match.group(5) else None

        results.append(BenchmarkResult(
            name=name,
            iterations=iterations,
            ns_per_op=ns_per_op,
            bytes_per_op=bytes_per_op,
            allocs_per_op=allocs_per_op,
        ))

    return results


def check_gates(results: List[BenchmarkResult]) -> Dict[str, Any]:
    """Check benchmark results against performance gates."""
    report = {
        "passed": True,
        "total_benchmarks": len(results),
        "gated_benchmarks": 0,
        "gates_passed": 0,
        "gates_failed": 0,
        "targets_met": 0,
        "results": [],
    }

    for result in results:
        gate = PERFORMANCE_GATES.get(result.name)

        if gate:
            report["gated_benchmarks"] += 1
            gate_passed = result.ms_per_op <= gate["max_ms"]
            target_met = result.ms_per_op <= gate["target_ms"]

            if gate_passed:
                report["gates_passed"] += 1
            else:
                report["gates_failed"] += 1
                report["passed"] = False

            if target_met:
                report["targets_met"] += 1

            status = "✅ PASS" if gate_passed else "❌ FAIL"
            target_status = "🎯 TARGET" if target_met else ""

            report["results"].append({
                "name": result.name,
                "description": gate["description"],
                "actual_ms": round(result.ms_per_op, 2),
                "max_ms": gate["max_ms"],
                "target_ms": gate["target_ms"],
                "gate_passed": gate_passed,
                "target_met": target_met,
                "iterations": result.iterations,
                "bytes_per_op": result.bytes_per_op,
                "allocs_per_op": result.allocs_per_op,
            })
        else:
            # Track ungated benchmarks for informational purposes
            report["results"].append({
                "name": result.name,
                "description": "No gate defined",
                "actual_ms": round(result.ms_per_op, 2),
                "gate_passed": None,
                "target_met": None,
                "iterations": result.iterations,
                "bytes_per_op": result.bytes_per_op,
                "allocs_per_op": result.allocs_per_op,
            })

    return report


def print_report(report: Dict[str, Any], output_format: str = "text") -> None:
    """Print benchmark report in specified format."""
    if output_format == "json":
        print(json.dumps(report, indent=2))
        return

    # Text format
    print("\n" + "=" * 60)
    print("SAFEDOWNLOAD BENCHMARK PERFORMANCE REPORT")
    print("=" * 60)
    print(f"\nTotal benchmarks: {report['total_benchmarks']}")
    print(f"Gated benchmarks: {report['gated_benchmarks']}")
    print(f"Gates passed: {report['gates_passed']}/{report['gated_benchmarks']}")
    print(f"Targets met: {report['targets_met']}/{report['gated_benchmarks']}")
    print()

    # Print gated results first
    print("-" * 60)
    print("GATED BENCHMARKS")
    print("-" * 60)

    for result in report["results"]:
        if result.get("gate_passed") is not None:
            status = "✅ PASS" if result["gate_passed"] else "❌ FAIL"
            target_status = " 🎯" if result.get("target_met") else ""
            print(f"\n{status}{target_status} {result['name']}")
            print(f"   {result['description']}")
            print(f"   Actual: {result['actual_ms']:.2f}ms | Max: {result['max_ms']}ms | Target: {result['target_ms']}ms")
            if result.get("bytes_per_op"):
                print(f"   Memory: {result['bytes_per_op']} B/op, {result.get('allocs_per_op', 0)} allocs/op")

    # Print ungated results
    ungated = [r for r in report["results"] if r.get("gate_passed") is None]
    if ungated:
        print("\n" + "-" * 60)
        print("OTHER BENCHMARKS (no gate)")
        print("-" * 60)
        for result in ungated:
            print(f"\n   {result['name']}: {result['actual_ms']:.2f}ms")

    # Final summary
    print("\n" + "=" * 60)
    if report["passed"]:
        print("✅ ALL PERFORMANCE GATES PASSED")
    else:
        print("❌ PERFORMANCE GATES FAILED")
        print("\nFailed gates:")
        for result in report["results"]:
            if result.get("gate_passed") is False:
                print(f"  - {result['name']}: {result['actual_ms']:.2f}ms > {result['max_ms']}ms")
    print("=" * 60 + "\n")


def main() -> int:
    """Main entry point."""
    # Parse arguments
    output_format = "text"
    input_file = None

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg in ("--json", "-j"):
            output_format = "json"
        elif arg in ("--help", "-h"):
            print(__doc__)
            return 0
        elif not arg.startswith("-"):
            input_file = arg

    # Read input
    if input_file:
        try:
            with open(input_file, "r") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            return 1
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Reading from stdin... (Ctrl+D to end)")
        content = sys.stdin.read()

    if not content.strip():
        print("Error: No benchmark data provided", file=sys.stderr)
        print("Usage: go test -bench=. ./... | python3 scripts/check_benchmarks.py", file=sys.stderr)
        return 1

    # Parse and check
    results = parse_benchmark_output(content)

    if not results:
        print("Warning: No benchmark results found in input", file=sys.stderr)
        print("Expected format: BenchmarkName-N    iterations    ns/op", file=sys.stderr)
        return 1

    report = check_gates(results)
    print_report(report, output_format)

    # Exit with error if gates failed
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
