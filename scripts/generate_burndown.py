#!/usr/bin/env python3
"""
Sprint Burndown Chart Generator

Generates burndown charts from sprint YAML files for SafeDownload project.
Outputs SVG charts and Markdown tables for sprint tracking.

Usage:
    python3 scripts/generate_burndown.py dev/sprints/sprint-01.yaml
    python3 scripts/generate_burndown.py --all  # Process all sprints
    python3 scripts/generate_burndown.py --output-dir docs/charts sprint-01.yaml
"""

import os
import sys
import yaml
import argparse
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class Task:
    """Represents a sprint task."""
    id: str
    title: str
    status: str
    story_points: int = 1
    completed_date: Optional[str] = None

    @property
    def is_complete(self) -> bool:
        return self.status.lower() in ("done", "complete", "completed")


@dataclass
class Sprint:
    """Represents a sprint with tasks and timeline."""
    id: str
    name: str
    start_date: datetime
    end_date: datetime
    goals: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    @property
    def total_points(self) -> int:
        return sum(t.story_points for t in self.tasks)

    @property
    def completed_points(self) -> int:
        return sum(t.story_points for t in self.tasks if t.is_complete)

    @property
    def remaining_points(self) -> int:
        return self.total_points - self.completed_points

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

    @property
    def progress_percent(self) -> float:
        if self.total_points == 0:
            return 0.0
        return (self.completed_points / self.total_points) * 100


def parse_sprint_yaml(filepath: str) -> Sprint:
    """Parse a sprint YAML file into a Sprint object."""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    # Parse dates
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")

    # Parse tasks
    tasks = []
    for task_data in data.get("tasks", []):
        task = Task(
            id=task_data.get("id", ""),
            title=task_data.get("title", ""),
            status=task_data.get("status", "pending"),
            story_points=task_data.get("story_points", 1),
            completed_date=task_data.get("completed_date"),
        )
        tasks.append(task)

    return Sprint(
        id=data.get("id", Path(filepath).stem),
        name=data.get("name", "Unknown Sprint"),
        start_date=start_date,
        end_date=end_date,
        goals=data.get("goals", []),
        tasks=tasks,
    )


def calculate_ideal_burndown(sprint: Sprint) -> List[Dict[str, Any]]:
    """Calculate ideal (linear) burndown line."""
    points = []
    total = sprint.total_points
    days = sprint.duration_days

    for day in range(days + 1):
        date = sprint.start_date + timedelta(days=day)
        remaining = total - (total * day / days) if days > 0 else 0
        points.append({
            "day": day,
            "date": date.strftime("%Y-%m-%d"),
            "remaining": round(remaining, 1),
        })

    return points


def calculate_actual_burndown(sprint: Sprint) -> List[Dict[str, Any]]:
    """Calculate actual burndown based on task completion dates."""
    points = []
    remaining = sprint.total_points

    # Group completed tasks by date
    completions_by_date: Dict[str, int] = {}
    for task in sprint.tasks:
        if task.is_complete and task.completed_date:
            date = task.completed_date
            completions_by_date[date] = completions_by_date.get(date, 0) + task.story_points

    # Build actual burndown
    for day in range(sprint.duration_days + 1):
        date = sprint.start_date + timedelta(days=day)
        date_str = date.strftime("%Y-%m-%d")

        # Subtract completed points for this date
        if date_str in completions_by_date:
            remaining -= completions_by_date[date_str]

        points.append({
            "day": day,
            "date": date_str,
            "remaining": max(0, remaining),
        })

    return points


def generate_svg_chart(sprint: Sprint, ideal: List[Dict], actual: List[Dict]) -> str:
    """Generate SVG burndown chart."""
    # Chart dimensions
    width = 600
    height = 400
    margin = {"top": 40, "right": 40, "bottom": 60, "left": 60}
    chart_width = width - margin["left"] - margin["right"]
    chart_height = height - margin["top"] - margin["bottom"]

    # Scale factors
    max_points = sprint.total_points
    max_days = sprint.duration_days
    x_scale = chart_width / max_days if max_days > 0 else 0
    y_scale = chart_height / max_points if max_points > 0 else 0

    # Generate ideal line path
    ideal_path = "M " + " L ".join(
        f"{margin['left'] + p['day'] * x_scale},{margin['top'] + (max_points - p['remaining']) * y_scale}"
        for p in ideal
    )

    # Generate actual line path (only up to current data)
    today = datetime.now().strftime("%Y-%m-%d")
    actual_filtered = [p for p in actual if p["date"] <= today]
    actual_path = ""
    if actual_filtered:
        actual_path = "M " + " L ".join(
            f"{margin['left'] + p['day'] * x_scale},{margin['top'] + (max_points - p['remaining']) * y_scale}"
            for p in actual_filtered
        )

    # Generate x-axis labels (every other day for readability)
    x_labels = ""
    for i, p in enumerate(ideal):
        if i % 2 == 0 or i == len(ideal) - 1:
            x = margin["left"] + p["day"] * x_scale
            y = height - margin["bottom"] + 20
            date_short = datetime.strptime(p["date"], "%Y-%m-%d").strftime("%m/%d")
            x_labels += f'<text x="{x}" y="{y}" text-anchor="middle" font-size="10">{date_short}</text>\n'

    # Generate y-axis labels
    y_labels = ""
    step = max(1, max_points // 5)
    for points in range(0, max_points + 1, step):
        x = margin["left"] - 10
        y = margin["top"] + (max_points - points) * y_scale + 4
        y_labels += f'<text x="{x}" y="{y}" text-anchor="end" font-size="10">{points}</text>\n'

    # Generate grid lines
    grid_lines = ""
    for points in range(0, max_points + 1, step):
        y = margin["top"] + (max_points - points) * y_scale
        grid_lines += f'<line x1="{margin["left"]}" y1="{y}" x2="{width - margin["right"]}" y2="{y}" stroke="#e0e0e0" stroke-width="1"/>\n'

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; }}
    .axis-label {{ font-family: Arial, sans-serif; font-size: 12px; }}
    .legend {{ font-family: Arial, sans-serif; font-size: 11px; }}
    text {{ font-family: Arial, sans-serif; }}
  </style>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="white"/>

  <!-- Title -->
  <text x="{width/2}" y="25" text-anchor="middle" class="title">{sprint.name} - Burndown Chart</text>

  <!-- Grid -->
  {grid_lines}

  <!-- Axes -->
  <line x1="{margin['left']}" y1="{margin['top']}" x2="{margin['left']}" y2="{height - margin['bottom']}" stroke="black" stroke-width="2"/>
  <line x1="{margin['left']}" y1="{height - margin['bottom']}" x2="{width - margin['right']}" y2="{height - margin['bottom']}" stroke="black" stroke-width="2"/>

  <!-- Axis Labels -->
  <text x="{width/2}" y="{height - 10}" text-anchor="middle" class="axis-label">Days</text>
  <text x="15" y="{height/2}" text-anchor="middle" transform="rotate(-90, 15, {height/2})" class="axis-label">Story Points Remaining</text>

  <!-- X-axis tick labels -->
  {x_labels}

  <!-- Y-axis tick labels -->
  {y_labels}

  <!-- Ideal Burndown Line -->
  <path d="{ideal_path}" fill="none" stroke="#2196F3" stroke-width="2" stroke-dasharray="5,5"/>

  <!-- Actual Burndown Line -->
  {f'<path d="{actual_path}" fill="none" stroke="#4CAF50" stroke-width="3"/>' if actual_path else ''}

  <!-- Legend -->
  <line x1="{width - 150}" y1="55" x2="{width - 120}" y2="55" stroke="#2196F3" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="{width - 115}" y="58" class="legend">Ideal</text>

  <line x1="{width - 150}" y1="75" x2="{width - 120}" y2="75" stroke="#4CAF50" stroke-width="3"/>
  <text x="{width - 115}" y="78" class="legend">Actual</text>

  <!-- Progress indicator -->
  <text x="{width - 150}" y="100" class="legend">Progress: {sprint.progress_percent:.0f}%</text>
  <text x="{width - 150}" y="115" class="legend">{sprint.completed_points}/{sprint.total_points} points</text>
</svg>'''

    return svg


def generate_markdown_table(sprint: Sprint) -> str:
    """Generate Markdown table with sprint status."""
    lines = [
        f"## {sprint.name} Status",
        "",
        f"**Sprint Period**: {sprint.start_date.strftime('%Y-%m-%d')} to {sprint.end_date.strftime('%Y-%m-%d')}",
        f"**Progress**: {sprint.completed_points}/{sprint.total_points} points ({sprint.progress_percent:.0f}%)",
        "",
        "### Goals",
        "",
    ]

    for goal in sprint.goals:
        lines.append(f"- {goal}")

    lines.extend([
        "",
        "### Tasks",
        "",
        "| ID | Task | Status | Points |",
        "|:---|:-----|:-------|-------:|",
    ])

    for task in sprint.tasks:
        status_emoji = "✅" if task.is_complete else "⏳" if task.status == "in-progress" else "📋"
        lines.append(f"| {task.id} | {task.title} | {status_emoji} {task.status} | {task.story_points} |")

    lines.extend([
        "",
        "### Burndown Data",
        "",
        "| Day | Date | Ideal | Actual |",
        "|----:|:-----|------:|-------:|",
    ])

    ideal = calculate_ideal_burndown(sprint)
    actual = calculate_actual_burndown(sprint)
    today = datetime.now().strftime("%Y-%m-%d")

    for i, p in enumerate(ideal):
        actual_val = actual[i]["remaining"] if i < len(actual) and actual[i]["date"] <= today else "-"
        lines.append(f"| {p['day']} | {p['date']} | {p['remaining']:.1f} | {actual_val} |")

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate burndown charts from sprint YAML files"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Sprint YAML files to process",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all sprint files in dev/sprints/",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="docs/charts",
        help="Output directory for generated files (default: docs/charts)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["svg", "md", "both"],
        default="both",
        help="Output format (default: both)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of files",
    )

    args = parser.parse_args()

    # Find files to process
    files = []
    if args.all:
        sprints_dir = Path("dev/sprints")
        if sprints_dir.exists():
            files = list(sprints_dir.glob("sprint-*.yaml"))
        else:
            print(f"Error: Directory not found: {sprints_dir}", file=sys.stderr)
            return 1
    else:
        files = [Path(f) for f in args.files]

    if not files:
        print("Error: No sprint files specified. Use --all or provide file paths.", file=sys.stderr)
        return 1

    # Create output directory
    if not args.stdout:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file
    for filepath in files:
        if not filepath.exists():
            print(f"Warning: File not found: {filepath}", file=sys.stderr)
            continue

        try:
            sprint = parse_sprint_yaml(str(filepath))
            ideal = calculate_ideal_burndown(sprint)
            actual = calculate_actual_burndown(sprint)

            if args.stdout:
                if args.format in ("svg", "both"):
                    print(generate_svg_chart(sprint, ideal, actual))
                if args.format in ("md", "both"):
                    print(generate_markdown_table(sprint))
            else:
                base_name = filepath.stem

                if args.format in ("svg", "both"):
                    svg_path = output_dir / f"{base_name}-burndown.svg"
                    svg_path.write_text(generate_svg_chart(sprint, ideal, actual))
                    print(f"Generated: {svg_path}")

                if args.format in ("md", "both"):
                    md_path = output_dir / f"{base_name}-status.md"
                    md_path.write_text(generate_markdown_table(sprint))
                    print(f"Generated: {md_path}")

        except Exception as e:
            print(f"Error processing {filepath}: {e}", file=sys.stderr)
            continue

    return 0


if __name__ == "__main__":
    sys.exit(main())
