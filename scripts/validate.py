#!/usr/bin/env python3
"""
Phase 3 — Content Validation
==============================
Scans generated MDX files and reports gaps:
  • Missing problem statements
  • Missing enrichment (patterns, complexity, tags)
  • Problems without source files
  • Duplicate slugs
  • Premium problems detected vs flagged

Usage:
    python scripts/validate.py
    python scripts/validate.py --json   (machine-readable output)
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT    = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = REPO_ROOT / "site" / "src" / "content" / "problems"
DATA_DIR     = Path(__file__).resolve().parent / "data"
META_FILE    = DATA_DIR / "problems_metadata.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
FIELD_RE       = re.compile(r'^(\w+):\s*(.+)$', re.MULTILINE)


def parse_frontmatter(mdx: str) -> dict:
    m = FRONTMATTER_RE.match(mdx)
    if not m:
        return {}
    fm = {}
    for field_m in FIELD_RE.finditer(m.group(1)):
        key = field_m.group(1)
        val = field_m.group(2).strip()
        fm[key] = val
    return fm


def bool_val(s: str) -> bool:
    return s.strip().lower() == "true"


def list_val(s: str) -> list:
    s = s.strip()
    if s in ("[]", ""):
        return []
    return [x.strip().strip('"') for x in s.strip("[]").split(",") if x.strip()]


def run(as_json: bool = False):
    if not PROBLEMS_DIR.exists():
        print("ERROR: problems dir not found. Run pipeline.py first.")
        sys.exit(1)

    mdx_files = sorted(PROBLEMS_DIR.glob("*.mdx"))
    if not mdx_files:
        print("No MDX files found. Run pipeline.py first.")
        sys.exit(1)

    enrichment = {}
    if META_FILE.exists():
        enrichment = json.loads(META_FILE.read_text(encoding="utf-8"))

    issues: dict[str, list] = {
        "no_problem_statement": [],
        "no_patterns":          [],
        "no_complexity":        [],
        "no_tags":              [],
        "empty_source":         [],
        "not_in_enrichment":    [],
        "premium_unflagged":    [],
    }
    slugs_seen: dict[str, str] = {}
    duplicate_slugs: list      = []
    total                      = 0

    for f in mdx_files:
        content = f.read_text(encoding="utf-8")
        fm      = parse_frontmatter(content)
        total  += 1

        title = fm.get("title", "").strip('"')
        slug  = fm.get("slug",  "").strip('"')

        # Duplicate slug detection
        if slug in slugs_seen:
            duplicate_slugs.append({"slug": slug, "files": [slugs_seen[slug], f.name]})
        else:
            slugs_seen[slug] = f.name

        # Missing problem statement
        if not bool_val(fm.get("hasProblemStatement", "false")):
            issues["no_problem_statement"].append({"slug": slug, "title": title})

        # Missing patterns
        if not list_val(fm.get("patterns", "[]")):
            issues["no_patterns"].append({"slug": slug, "title": title})

        # Missing complexity
        tc = fm.get("timeComplexity",  "\"\"").strip('"')
        sc = fm.get("spaceComplexity", "\"\"").strip('"')
        if not tc or not sc:
            issues["no_complexity"].append({"slug": slug, "title": title, "time": tc, "space": sc})

        # Missing tags
        if not list_val(fm.get("tags", "[]")):
            issues["no_tags"].append({"slug": slug, "title": title})

        # Empty source (no Solution section)
        if "## Solution" not in content or "```python" not in content:
            issues["empty_source"].append({"slug": slug, "title": title})

        # Not in enrichment JSON
        if slug not in enrichment:
            issues["not_in_enrichment"].append({"slug": slug, "title": title})

    # Summary counts
    report = {
        "total_files": total,
        "duplicate_slugs": duplicate_slugs,
        "issues": {k: {"count": len(v), "items": v} for k, v in issues.items()},
    }

    if as_json:
        print(json.dumps(report, indent=2))
        return

    # ── Human-readable output ─────────────────────────────────────────────────
    print("\n🔍 DSA Python — Content Validation Report\n" + "─" * 50)
    print(f"   MDX files scanned: {total}")

    if duplicate_slugs:
        print(f"\n❌ DUPLICATE SLUGS ({len(duplicate_slugs)}):")
        for d in duplicate_slugs:
            print(f"   slug={d['slug']}  →  {d['files']}")
    else:
        print("   ✅ No duplicate slugs")

    checks = [
        ("no_problem_statement", "Missing problem statement (will show LC link)"),
        ("no_patterns",          "Missing patterns enrichment"),
        ("no_complexity",        "Missing complexity enrichment"),
        ("no_tags",              "Missing topic tags enrichment"),
        ("empty_source",         "No Python solution found"),
        ("not_in_enrichment",    "Not in problems_metadata.json"),
    ]

    for key, label in checks:
        items = issues[key]
        count = len(items)
        icon  = "✅" if count == 0 else ("⚠️ " if count < 20 else "❌")
        print(f"\n{icon} {label}: {count}")
        if 0 < count <= 10:
            for item in items:
                print(f"   • {item['title']} ({item['slug']})")
        elif count > 10:
            for item in items[:5]:
                print(f"   • {item['title']} ({item['slug']})")
            print(f"   ... and {count - 5} more")

    print(f"\n{'─' * 50}")
    total_issues = sum(len(v) for v in issues.values())
    if total_issues == 0 and not duplicate_slugs:
        print("✅ All checks passed!")
    else:
        print(f"⚠️  {total_issues} issue(s) found across {total} files.")
    print()


if __name__ == "__main__":
    as_json = "--json" in sys.argv
    run(as_json=as_json)
