#!/usr/bin/env python3
"""
Phase 3 — Content Pipeline
============================
Reads DSASpreadSheetPython.xlsx + Python source files.
Generates MDX content files for Astro Content Collections.

Usage:
    python scripts/pipeline.py

Output:
    site/src/content/problems/  — one .mdx per problem (169 files)
    site/src/content/topics/    — one .mdx per topic  (17 files)
"""

import ast
import json
import re
import sys
import textwrap
from collections import defaultdict
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed.  Run:  pip install openpyxl")
    sys.exit(1)

# ─── Paths ───────────────────────────────────────────────────────────────────
REPO_ROOT    = Path(__file__).resolve().parent.parent
SRC_DIR      = REPO_ROOT / "src"
XLSX_PATH    = REPO_ROOT / "DSASpreadSheetPython.xlsx"
CONTENT_DIR  = REPO_ROOT / "site" / "src" / "content"
PROBLEMS_DIR = CONTENT_DIR / "problems"
TOPICS_DIR   = CONTENT_DIR / "topics"
DATA_DIR     = Path(__file__).resolve().parent / "data"
META_FILE    = DATA_DIR / "problems_metadata.json"

# ─── Topic mappings ──────────────────────────────────────────────────────────
TOPIC_DIR_MAP: dict[str, str] = {
    "Array":                "array",
    "Binary":               "binary",
    "Binary Search":        "binary_search",
    "Binary Search Tree":   "binary_search_tree",
    "Binary Tree":          "binary_tree",
    "Dynamic Programming":  "dynamic_programming",
    "Graph":                "graph",
    "Hash Table":           "hash_table",
    "Heap":                 "heap",
    "Linked List":          "linked_list",
    "Math":                 "math",
    "Matrix":               "matrix",
    "Queue":                "queue",
    "Recursion":            "recursion",
    "Stack":                "stack",
    "String":               "string",
    "Trie":                 "trie",
}

TOPIC_SLUG_MAP: dict[str, str] = {
    k: v.replace("_", "-") for k, v in TOPIC_DIR_MAP.items()
}

TOPIC_META: dict[str, dict] = {
    "Array":                {"icon": "▤", "order": 1,  "desc": "Sliding window, two pointers, intervals, prefix sums, and in-place operations."},
    "Graph":                {"icon": "◎", "order": 2,  "desc": "BFS, DFS, topological sort, union-find, and shortest path algorithms."},
    "Binary Tree":          {"icon": "◈", "order": 3,  "desc": "Traversals, path sums, LCA, construction, serialization, and tree properties."},
    "Stack":                {"icon": "⊟", "order": 4,  "desc": "Monotonic stack, expression evaluation, parentheses, and histograms."},
    "String":               {"icon": "❝", "order": 5,  "desc": "Sliding window, anagrams, palindromes, encoding, and character frequency."},
    "Linked List":          {"icon": "⊶", "order": 6,  "desc": "Reversal, cycle detection, merge, reordering, and fast-slow pointers."},
    "Dynamic Programming":  {"icon": "⊞", "order": 7,  "desc": "Knapsack, LCS, LIS, grid DP, and optimal substructure transitions."},
    "Heap":                 {"icon": "⊠", "order": 8,  "desc": "Min/max heaps, k-way merge, median tracking, and top-k problems."},
    "Binary Search":        {"icon": "⊡", "order": 9,  "desc": "Search templates, rotated arrays, boundary conditions, and answer-space search."},
    "Binary":               {"icon": "⊕", "order": 10, "desc": "Bit manipulation, XOR tricks, masks, and bitwise counting."},
    "Recursion":            {"icon": "↺", "order": 11, "desc": "Backtracking, permutations, subsets, N-Queens, and constraint satisfaction."},
    "Binary Search Tree":   {"icon": "⊿", "order": 12, "desc": "Validation, in-order successor, LCA, kth smallest, and BST properties."},
    "Math":                 {"icon": "∑", "order": 13, "desc": "Digit manipulation, exponentiation, modular arithmetic, and numerical tricks."},
    "Matrix":               {"icon": "◫", "order": 14, "desc": "Spiral traversal, rotation, DP on grid, and constraint-based puzzles."},
    "Trie":                 {"icon": "⊳", "order": 15, "desc": "Prefix tree construction, word search, autocomplete, and design problems."},
    "Hash Table":           {"icon": "≡", "order": 16, "desc": "Lookup tables, frequency maps, grouping, and O(1) average-case operations."},
    "Queue":                {"icon": "→", "order": 17, "desc": "Design problems, BFS layers, and streaming data structures."},
}

TOPIC_PATTERNS: dict[str, list[str]] = {
    "Array":                ["Sliding Window", "Two Pointers", "Prefix Sum", "Interval Merging", "Greedy"],
    "Graph":                ["BFS", "DFS", "Topological Sort", "Union Find", "Shortest Path"],
    "Binary Tree":          ["DFS", "BFS Level Order", "Post-order", "LCA", "Serialization"],
    "Stack":                ["Monotonic Stack", "Stack Evaluation", "Next Greater Element"],
    "String":               ["Sliding Window", "Two Pointers", "Frequency Count", "Palindrome"],
    "Linked List":          ["Fast and Slow Pointers", "Reversal", "Merge", "Cycle Detection"],
    "Dynamic Programming":  ["1D DP", "2D DP", "Knapsack", "Prefix DP", "Decision DP"],
    "Heap":                 ["Min Heap", "Max Heap", "Two Heaps", "K-way Merge"],
    "Binary Search":        ["Left Boundary", "Right Boundary", "Answer Space", "Pivot Finding"],
    "Binary":               ["XOR Trick", "Bit Masking", "Brian Kernighan", "Bit Shift"],
    "Recursion":            ["Backtracking", "DFS", "Pruning", "State Space Search"],
    "Binary Search Tree":   ["In-order Traversal", "BST Property", "LCA"],
    "Math":                 ["Digit Manipulation", "Fast Exponentiation", "Overflow Check"],
    "Matrix":               ["DFS on Grid", "BFS on Grid", "DP on Grid", "Simulation"],
    "Trie":                 ["Prefix Tree", "DFS with Wildcard", "Word Insertion"],
    "Hash Table":           ["Frequency Count", "Complement Lookup", "Grouping"],
    "Queue":                ["Circular Buffer", "Sliding Window"],
}


# ─── Utilities ───────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s\-]", "", s)
    s = re.sub(r"[\s\-]+", "-", s.strip())
    return s


def yaml_str(val: str) -> str:
    """Wrap value in YAML double-quotes with proper escaping."""
    return '"' + val.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    return "[" + ", ".join(f'"{i}"' for i in items) + "]"


def escape_mdx_prose(text: str) -> str:
    """Escape MDX special characters in prose content (not in code fences)."""
    text = text.replace("{", "\\{").replace("}", "\\}")
    # Escape < so MDX doesn't try to parse comparison operators as JSX tags
    text = text.replace("<", "\\<")
    return text


# ─── Step 1: Parse spreadsheet ───────────────────────────────────────────────

def parse_xlsx() -> list[dict]:
    """Read DSASpreadSheetPython.xlsx → list of problem records."""
    print(f"📊 Reading spreadsheet: {XLSX_PATH.name}")
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TIHB169Python"]

    records = []
    for row in ws.iter_rows(min_row=2, max_row=170):
        if not row[0].value:
            continue

        topic     = row[1].value
        difficulty = row[3].value
        prob_cell = row[4]
        comm_cell = row[6]

        title  = prob_cell.value or ""
        lc_url = prob_cell.hyperlink.target if prob_cell.hyperlink else ""
        gh_url = comm_cell.hyperlink.target if comm_cell.hyperlink else ""

        # Extract relative file path from GitHub blob URL
        file_path = None
        if gh_url:
            m = re.search(r"/blob/master/(src/[^?#]+\.py)", gh_url)
            if m:
                file_path = REPO_ROOT / m.group(1)

        records.append({
            "title":     title,
            "topic":     topic,
            "topicSlug": TOPIC_SLUG_MAP.get(topic, slugify(topic)),
            "difficulty": difficulty,
            "lcUrl":     lc_url,
            "ghUrl":     gh_url,
            "slug":      slugify(title),
            "filePath":  file_path,
        })

    print(f"   → {len(records)} problems loaded")
    return records


# ─── Step 2: Parse Python source ─────────────────────────────────────────────

def get_module_docstring(source: str) -> str | None:
    """Extract module-level docstring using AST."""
    try:
        tree = ast.parse(source)
        return ast.get_docstring(tree)
    except SyntaxError:
        return None


def strip_module_docstring(source: str) -> str:
    """Return Python source with the top-level docstring removed."""
    try:
        tree = ast.parse(source)
        if (
            tree.body
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
            and isinstance(tree.body[0].value.value, str)
        ):
            end_line = tree.body[0].end_lineno
            lines = source.splitlines()
            code = "\n".join(lines[end_line:]).strip()
            return code
    except SyntaxError:
        pass
    return source.strip()


def parse_docstring_sections(doc: str) -> dict[str, str]:
    """
    Segment a docstring into: statement, examples, constraints.
    Handles both structured ("Problem Statement:", "Example N:", "Constraints:")
    and unstructured formats.
    """
    if not doc:
        return {"statement": "", "examples": "", "constraints": ""}

    doc = doc.strip()

    # Detect structured format
    is_structured = bool(re.search(
        r"(Problem Statement:|Example \d+:|Constraints:)", doc, re.IGNORECASE
    ))

    if is_structured:
        HEADER_RE = re.compile(
            r"^(Problem Statement|Example\s*\d*|Constraints|Notes?)\s*:?",
            re.IGNORECASE | re.MULTILINE,
        )
        # Split on headers
        parts = HEADER_RE.split(doc)
        # parts alternates: [pre, header, body, header, body, ...]
        # Simpler: find positions
        statement_parts, example_parts, constraint_parts = [], [], []

        tokens = re.split(r"\n(?=(Problem Statement:|Example \d*:?|Constraints:|Notes?:))", doc, flags=re.IGNORECASE)
        for token in tokens:
            t = token.strip()
            if not t:
                continue
            t_lo = t.lower()
            if t_lo.startswith("problem statement:"):
                body = re.sub(r"^problem statement:\s*", "", t, flags=re.IGNORECASE).strip()
                statement_parts.append(body)
            elif re.match(r"example\s*\d*\s*:?", t_lo):
                example_parts.append(t)
            elif re.match(r"constraints?\s*:?", t_lo):
                body = re.sub(r"^constraints?\s*:\s*", "", t, flags=re.IGNORECASE).strip()
                constraint_parts.append(body)
            elif re.match(r"notes?\s*:?", t_lo):
                body = re.sub(r"^notes?\s*:\s*", "", t, flags=re.IGNORECASE).strip()
                constraint_parts.append(body)
            else:
                if not statement_parts:
                    statement_parts.append(t)

        return {
            "statement":   "\n\n".join(statement_parts).strip(),
            "examples":    "\n\n".join(example_parts).strip(),
            "constraints": "\n".join(constraint_parts).strip(),
        }

    # Unstructured: try to find "Example" then "Constraints" sections
    ex_pat  = re.compile(r"\n\s*(?=(?:Example|For example|Input\s*:|Sample input))", re.IGNORECASE)
    con_pat = re.compile(r"\n\s*(?=(?:Constraints?\s*:|Notes?\s*:|Note\s*\d+))", re.IGNORECASE)

    ex_m  = ex_pat.search(doc)
    con_m = con_pat.search(doc)

    if ex_m:
        statement = doc[:ex_m.start()].strip()
        if con_m and con_m.start() > ex_m.start():
            examples    = doc[ex_m.start():con_m.start()].strip()
            constraints = doc[con_m.start():].strip()
        else:
            examples    = doc[ex_m.start():].strip()
            constraints = ""
    elif con_m:
        statement   = doc[:con_m.start()].strip()
        examples    = ""
        constraints = doc[con_m.start():].strip()
    else:
        statement   = doc.strip()
        examples    = ""
        constraints = ""

    return {"statement": statement, "examples": examples, "constraints": constraints}


# ─── Step 3: Build MDX ───────────────────────────────────────────────────────

def build_frontmatter(p: dict, sections: dict, meta: dict) -> str:
    tags     = meta.get("tags",     [])
    patterns = meta.get("patterns", [])
    time_c   = meta.get("timeComplexity",  "")
    space_c  = meta.get("spaceComplexity", "")
    is_prem  = meta.get("isPremium", False)
    similar  = meta.get("similarProblems", [])

    has_stmt = bool(sections.get("statement"))
    has_con  = bool(sections.get("constraints"))
    has_ex   = bool(sections.get("examples"))

    lines = [
        "---",
        f'title: {yaml_str(p["title"])}',
        f'problemSlug: {yaml_str(p["slug"])}',
        f'topic: {yaml_str(p["topic"])}',
        f'topicSlug: {yaml_str(p["topicSlug"])}',
        f'difficulty: {yaml_str(p["difficulty"])}',
        f'leetcodeUrl: {yaml_str(p["lcUrl"])}',
        f'githubUrl: {yaml_str(p["ghUrl"])}',
        f'tags: {yaml_list(tags)}',
        f'patterns: {yaml_list(patterns)}',
        f'timeComplexity: {yaml_str(time_c)}',
        f'spaceComplexity: {yaml_str(space_c)}',
        f'hasProblemStatement: {"true" if has_stmt else "false"}',
        f'hasConstraints: {"true" if has_con else "false"}',
        f'hasExamples: {"true" if has_ex else "false"}',
        f'isPremium: {"true" if is_prem else "false"}',
        f'similarProblems: {yaml_list(similar)}',
        "---",
    ]
    return "\n".join(lines)


def build_body(p: dict, sections: dict, source_code: str, meta: dict) -> str:
    parts: list[str] = []

    # ── Problem Statement ─────────────────────────────────
    if sections.get("statement"):
        parts.append("## Problem Statement\n")
        parts.append(escape_mdx_prose(sections["statement"]))
    else:
        parts.append("## Problem Statement\n")
        parts.append(
            f"> Problem statement not in source file. "
            f"[View on LeetCode →]({p['lcUrl']})"
        )

    # ── Examples ─────────────────────────────────────────
    if sections.get("examples"):
        parts.append("\n\n## Examples\n")
        parts.append(escape_mdx_prose(sections["examples"]))

    # ── Constraints ───────────────────────────────────────
    if sections.get("constraints"):
        parts.append("\n\n## Constraints\n")
        parts.append(escape_mdx_prose(sections["constraints"]))

    # ── Python Solution ───────────────────────────────────
    parts.append("\n\n## Solution\n")
    # Safe inside triple-backtick fence — no escaping needed for {}
    safe_code = source_code.replace("```", "\\`\\`\\`")
    parts.append(f"```python\n{safe_code}\n```")

    # ── Complexity ────────────────────────────────────────
    time_c  = meta.get("timeComplexity",  "")
    space_c = meta.get("spaceComplexity", "")
    if time_c or space_c:
        parts.append("\n\n## Complexity\n")
        if time_c:
            parts.append(f"- **Time**: `{time_c}`")
        if space_c:
            parts.append(f"- **Space**: `{space_c}`")

    # ── Similar Problems ──────────────────────────────────
    similar = meta.get("similarProblems", [])
    if similar:
        parts.append("\n\n## Similar Problems\n")
        base = "/TechInterviewHandbookDSA169"
        for s in similar:
            parts.append(f"- [{s.replace('-', ' ').title()}]({base}/problems/{s})")

    return "\n".join(parts) + "\n"


def build_problem_mdx(p: dict, sections: dict, meta: dict, source_code: str) -> str:
    fm   = build_frontmatter(p, sections, meta)
    body = build_body(p, sections, source_code, meta)
    return f"{fm}\n\n{body}"


# ─── Step 4: Build topic MDX ─────────────────────────────────────────────────

def build_topic_mdx(topic_name: str, counts: dict) -> str:
    slug     = TOPIC_SLUG_MAP.get(topic_name, slugify(topic_name))
    tm       = TOPIC_META.get(topic_name, {})
    icon     = tm.get("icon", "◉")
    order    = tm.get("order", 99)
    desc     = tm.get("desc", f"Python solutions for {topic_name} problems.")
    patterns = TOPIC_PATTERNS.get(topic_name, [])

    total  = counts.get("total", 0)
    easy   = counts.get("Easy", 0)
    medium = counts.get("Medium", 0)
    hard   = counts.get("Hard", 0)

    fm_lines = [
        "---",
        f'title: {yaml_str(topic_name)}',
        f'slug: {yaml_str(slug)}',
        f'description: {yaml_str(desc)}',
        f'icon: {yaml_str(icon)}',
        f'problemCount: {total}',
        f'easyCount: {easy}',
        f'mediumCount: {medium}',
        f'hardCount: {hard}',
        f'patterns: {yaml_list(patterns)}',
        f'order: {order}',
        "---",
    ]

    body = f"{desc}\n"
    return "\n".join(fm_lines) + "\n\n" + body


# ─── Main pipeline ───────────────────────────────────────────────────────────

def run():
    print("\n🚀 DSA Python — Content Pipeline (Phase 3)\n" + "─" * 50)

    # Load enrichment metadata
    enrichment: dict[str, dict] = {}
    if META_FILE.exists():
        enrichment = json.loads(META_FILE.read_text(encoding="utf-8"))
        print(f"📋 Enrichment metadata loaded: {len(enrichment)} entries")
    else:
        print(f"⚠️  No metadata file found at {META_FILE}. Continuing without enrichment.")

    # Ensure output directories exist
    PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)

    # Parse spreadsheet
    problems = parse_xlsx()

    # Track stats
    counts_ok      = 0
    counts_no_file = 0
    counts_no_doc  = 0
    topic_counts: dict[str, dict] = defaultdict(lambda: {"total": 0, "Easy": 0, "Medium": 0, "Hard": 0})
    topic_patterns_agg: dict[str, set] = defaultdict(set)

    print(f"\n📝 Generating problem MDX files...")

    for p in problems:
        slug  = p["slug"]
        topic = p["topic"]
        diff  = p["difficulty"]

        # Update topic stats
        topic_counts[topic]["total"]  += 1
        topic_counts[topic][diff]     += 1

        meta = enrichment.get(slug, {})

        # Aggregate patterns per topic
        for pat in meta.get("patterns", []):
            topic_patterns_agg[topic].add(pat)

        # Read source file
        source_code  = ""
        sections     = {"statement": "", "examples": "", "constraints": ""}
        file_ok      = False

        if p["filePath"] and Path(p["filePath"]).exists():
            file_ok  = True
            raw      = Path(p["filePath"]).read_text(encoding="utf-8")
            docstring = get_module_docstring(raw)

            if docstring:
                sections = parse_docstring_sections(docstring)
                counts_no_doc += 0  # has doc
            else:
                counts_no_doc += 1

            source_code = strip_module_docstring(raw)
        else:
            counts_no_file += 1
            print(f"   ⚠️  File not found: {p.get('filePath', 'N/A')}  ({p['title']})")

        # Generate MDX
        mdx_content = build_problem_mdx(p, sections, meta, source_code)

        # Write file — name: {topicSlug}--{problemSlug}.mdx
        filename = f"{p['topicSlug']}--{slug}.mdx"
        out_path = PROBLEMS_DIR / filename
        out_path.write_text(mdx_content, encoding="utf-8")
        counts_ok += 1

    print(f"   ✅ {counts_ok} problem MDX files written")
    if counts_no_file:
        print(f"   ⚠️  {counts_no_file} source files not found")
    if counts_no_doc:
        print(f"   📭 {counts_no_doc} problems have no docstring (statement shown as LC link)")

    # Generate topic MDX files
    print(f"\n📁 Generating topic MDX files...")
    topics_written = 0
    for topic_name, counts in topic_counts.items():
        mdx = build_topic_mdx(topic_name, counts)
        slug = TOPIC_SLUG_MAP.get(topic_name, slugify(topic_name))
        out_path = TOPICS_DIR / f"{slug}.mdx"
        out_path.write_text(mdx, encoding="utf-8")
        topics_written += 1
        print(f"   → {slug}.mdx  ({counts['total']} problems: {counts['Easy']}E / {counts['Medium']}M / {counts['Hard']}H)")

    print(f"   ✅ {topics_written} topic MDX files written")

    # Remove placeholder .gitkeep if present
    for keep in [PROBLEMS_DIR / ".gitkeep", TOPICS_DIR / ".gitkeep"]:
        if keep.exists():
            keep.unlink()

    # Summary
    print(f"""
{'─' * 50}
✅ Pipeline complete

   Problems:  {counts_ok} MDX files → site/src/content/problems/
   Topics:    {topics_written} MDX files → site/src/content/topics/

Next: Run  cd site && npm run build  to verify the Astro build.
{'─' * 50}
""")


if __name__ == "__main__":
    run()
