#!/usr/bin/env python3
"""
Add detailed explanations to all problem MDX files.
This script reads each problem file, analyzes the solution code,
and adds a comprehensive explanation section.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


# Explanation templates for common patterns
EXPLANATIONS = {
    "two-sum": """
## Explanation

### Approach: Hash Map for Complement Lookup

The key insight is to use a hash map (dictionary) to store numbers we've seen along with their indices. As we iterate through the array, for each number we check if its complement (target - current number) already exists in our hash map.

**Think of it like this:** Imagine you're at a party looking for someone whose age, when added to yours, equals a specific number. Instead of asking everyone repeatedly, you write down each person's age as you meet them. When you meet someone new, you quickly check your notes to see if you've already met their "complement."

### Step-by-Step Walkthrough

Let's trace through Example 1: `nums = [2,7,11,15]`, `target = 9`

1. **Initialize:** Create empty dictionary `d = {}`

2. **i=0, num=2:**
   - Check if `9 - 2 = 7` is in `d`? No
   - Store: `d[2] = 0` → `d = {2: 0}`

3. **i=1, num=7:**
   - Check if `9 - 7 = 2` is in `d`? **Yes!**
   - Return `[d[2], 1]` = `[0, 1]` ✓

### Code Breakdown

```python
d = {}  # Maps number → index
```
We use a dictionary to achieve O(1) lookup time for complements.

```python
for i, num in enumerate(nums):
```
Iterate through array with both index and value.

```python
if target - num in d:
    return [d[target - num], i]
```
**The core logic:** If the complement exists in our map, we've found our pair! Return the stored index of the complement and the current index.

```python
d[num] = i
```
If no match yet, store this number's index for future lookups.

### Why This Works

- **Time Efficiency:** Each element is visited once, and hash map operations (insert/lookup) are O(1)
- **Space Trade-off:** We use extra space to store up to n elements, but gain significant speed
- **Single Pass:** Unlike the brute force O(n²) approach of checking all pairs, we solve it in one pass
""",

    "3sum": """
## Explanation

### Approach: Sorting + Two Pointers

The strategy is to convert the 3Sum problem into multiple 2Sum problems. We sort the array first, then for each element, we use two pointers to find pairs that sum to the negative of that element.

**Analogy:** Imagine arranging numbers in a line from smallest to largest. You pick one number and use two people (pointers) starting from opposite ends to find two numbers that, together with your picked number, sum to zero.

### Step-by-Step Walkthrough

Let's trace through Example 1: `nums = [-1,0,1,2,-1,-4]`

1. **Sort:** `nums = [-4,-1,-1,0,1,2]`

2. **i=0, nums[i]=-4:**
   - left=1, right=5
   - Need: -4 + nums[left] + nums[right] = 0
   - Try: -4 + (-1) + 2 = -3 (too small, left++)
   - Try: -4 + (-1) + 2 = -3 (too small, left++)
   - Try: -4 + 0 + 2 = -2 (too small, left++)
   - Try: -4 + 1 + 2 = -1 (too small, left++)
   - left >= right, no solution with -4

3. **i=1, nums[i]=-1:**
   - left=2, right=5
   - Try: -1 + (-1) + 2 = 0 ✓ Found: `[-1,-1,2]`
   - Skip duplicates, move both pointers
   - left=3, right=4
   - Try: -1 + 0 + 1 = 0 ✓ Found: `[-1,0,1]`

4. **i=2, nums[i]=-1:** Skip (duplicate of previous)

5. Continue for remaining elements...

### Code Breakdown

```python
nums.sort()
```
**Critical first step:** Sorting enables two-pointer technique and makes duplicate handling easier.

```python
if i > 0 and nums[i] == nums[i - 1]:
    continue
```
**Duplicate prevention:** Skip if current number equals previous to avoid duplicate triplets.

```python
left, right = i + 1, len(nums) - 1
```
**Two-pointer setup:** Search space is everything after current element.

```python
total = nums[i] + nums[left] + nums[right]
if total < 0:
    left += 1  # Need larger sum
elif total > 0:
    right -= 1  # Need smaller sum
```
**Core logic:** Since array is sorted, we can intelligently move pointers based on whether sum is too small or too large.

```python
while left < right and nums[left] == nums[left + 1]:
    left += 1
while left < right and nums[right] == nums[right - 1]:
    right -= 1
```
**Skip duplicates:** After finding a valid triplet, skip all duplicate values to avoid duplicate results.

### Why This Works

- **Sorting benefit:** Enables two-pointer technique and O(1) duplicate detection
- **Time complexity:** O(n²) - outer loop O(n) × inner two-pointer O(n)
- **Space efficiency:** O(1) extra space (excluding output array)
- **Completeness:** The two-pointer approach guarantees we check all valid combinations
""",

    "binary-tree-level-order-traversal": """
## Explanation

### Approach: Breadth-First Search (BFS) with Queue

Level order traversal means visiting all nodes at depth 0, then all nodes at depth 1, then depth 2, and so on. BFS is the natural choice because it explores nodes level by level.

**Analogy:** Imagine a family tree where you want to list all people generation by generation. You'd first list the grandparent, then all their children, then all grandchildren, etc. That's exactly what level order traversal does!

### Step-by-Step Walkthrough

Let's trace through Example 1: `root = [3,9,20,null,null,15,7]`

```
      3
     / \\
    9   20
       /  \\
      15   7
```

1. **Initialize:**
   - `result = []`
   - `queue = deque([3])`

2. **Level 0 (queue has 1 node):**
   - `level = []`
   - Process node 3: `level = [3]`, add children 9, 20 to queue
   - `result = [[3]]`
   - `queue = deque([9, 20])`

3. **Level 1 (queue has 2 nodes):**
   - `level = []`
   - Process node 9: `level = [9]`, no children
   - Process node 20: `level = [9, 20]`, add children 15, 7 to queue
   - `result = [[3], [9, 20]]`
   - `queue = deque([15, 7])`

4. **Level 2 (queue has 2 nodes):**
   - `level = []`
   - Process node 15: `level = [15]`, no children
   - Process node 7: `level = [15, 7]`, no children
   - `result = [[3], [9, 20], [15, 7]]`
   - `queue = deque([])` (empty)

5. **Done!** Return `[[3], [9, 20], [15, 7]]`

### Code Breakdown

```python
if not root:
    return []
```
**Edge case:** Handle empty tree immediately.

```python
queue = deque([root])
```
**Queue initialization:** Use `deque` for O(1) append and popleft operations. Start with root node.

```python
while queue:
```
**Main loop:** Continue until queue is empty (all nodes processed).

```python
level = []
for _ in range(len(queue)):
```
**Key technique:** Capture the current queue size before the loop. This tells us exactly how many nodes are at the current level. We process exactly that many nodes before moving to the next level.

```python
node = queue.popleft()
level.append(node.val)
```
**Process node:** Remove from front of queue (FIFO) and add its value to current level.

```python
if node.left:
    queue.append(node.left)
if node.right:
    queue.append(node.right)
```
**Add children:** Enqueue children for processing in the next level. Left before right maintains left-to-right order.

```python
result.append(level)
```
**Complete level:** After processing all nodes at current level, add the level list to result.

### Why This Works

- **Queue property:** FIFO (First In, First Out) naturally processes nodes level by level
- **Level separation:** By capturing `len(queue)` before inner loop, we know exactly which nodes belong to current level
- **Time complexity:** O(n) - visit each node exactly once
- **Space complexity:** O(n) - queue can hold up to n/2 nodes at the last level (complete binary tree)
"""
}


def get_problem_slug(filepath: Path) -> str:
    """Extract problem slug from filename."""
    filename = filepath.stem  # e.g., 'array--two-sum'
    parts = filename.split('--')
    if len(parts) == 2:
        return parts[1]
    return filename


def read_mdx_file(filepath: Path) -> Tuple[str, str, str]:
    """
    Read MDX file and split into frontmatter, content before solution, and content after solution.
    Returns: (frontmatter, before_solution, after_solution)
    """
    content = filepath.read_text(encoding='utf-8')
    
    # Split frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content, "", ""
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Find the ## Solution section
    solution_match = re.search(r'\n## Solution\n', body)
    if not solution_match:
        return f"---{frontmatter}---", body, ""
    
    before_solution = body[:solution_match.end()]
    after_solution = body[solution_match.end():]
    
    return f"---{frontmatter}---", before_solution, after_solution


def has_explanation_section(content: str) -> bool:
    """Check if the file already has an explanation section."""
    return '## Explanation' in content


def analyze_code_structure(code: str) -> Dict[str, any]:
    """Analyze code to extract key information."""
    analysis = {
        'has_sorting': 'sort' in code.lower(),
        'has_queue': 'deque' in code or 'Queue' in code,
        'has_stack': 'stack' in code.lower() or (code.count('.append(') > 0 and code.count('.pop()') > 0),
        'has_hashmap': bool(re.search(r'\{.*:.*\}|dict\(|defaultdict|Counter', code)),
        'has_two_pointers': 'left' in code and 'right' in code,
        'has_dp': 'dp' in code.lower() or bool(re.search(r'\[.*\]\s*\*\s*\d', code)),
        'has_recursion': 'def ' in code and code.count('def ') > 1,
        'has_dfs': 'dfs' in code.lower(),
        'has_bfs': 'bfs' in code.lower() or 'deque' in code,
        'has_binary_search': 'binary' in code.lower() or ('left' in code and 'right' in code and 'mid' in code),
        'has_sliding_window': 'window' in code.lower() or ('left' in code and 'right' in code and 'for' in code),
        'has_set': 'set(' in code or 'set()' in code,
        'has_heap': 'heapq' in code or 'heap' in code.lower(),
        'has_trie': 'Trie' in code or 'children' in code,
        'uses_enumerate': 'enumerate(' in code,
        'has_while_loop': 'while ' in code,
        'has_for_loop': 'for ' in code,
    }
    return analysis


def generate_generic_explanation(problem_slug: str, code: str, problem_title: str = "") -> str:
    """Generate a comprehensive explanation based on code analysis."""
    
    # Check if we have a specific template
    if problem_slug in EXPLANATIONS:
        return EXPLANATIONS[problem_slug]
    
    analysis = analyze_code_structure(code)
    
    explanation = "\n## Explanation\n\n"
    explanation += "### Approach\n\n"
    
    # Build approach description based on detected patterns
    approach_parts = []
    
    if analysis['has_bfs'] and analysis['has_queue']:
        approach_parts.append("This solution uses **Breadth-First Search (BFS)** with a queue to explore nodes level by level")
    elif analysis['has_dfs'] or analysis['has_recursion']:
        approach_parts.append("This solution uses **Depth-First Search (DFS)** to explore all possible paths")
    
    if analysis['has_dp']:
        approach_parts.append("It employs **Dynamic Programming** to build up the solution by solving smaller subproblems")
    
    if analysis['has_two_pointers']:
        approach_parts.append("It uses the **Two Pointers** technique to efficiently search through the data")
    
    if analysis['has_binary_search']:
        approach_parts.append("It applies **Binary Search** to find the target in logarithmic time")
    
    if analysis['has_hashmap']:
        approach_parts.append("It leverages a **Hash Map** for O(1) lookups and efficient tracking")
    
    if analysis['has_set']:
        approach_parts.append("It uses a **Set** for fast membership testing and duplicate detection")
    
    if analysis['has_heap']:
        approach_parts.append("It utilizes a **Heap** to efficiently maintain ordered elements")
    
    if analysis['has_sorting']:
        approach_parts.append("The algorithm starts by **sorting** the input to enable more efficient processing")
    
    if analysis['has_sliding_window']:
        approach_parts.append("It employs a **Sliding Window** to track a contiguous subset of elements")
    
    if approach_parts:
        explanation += ". ".join(approach_parts) + ".\n\n"
    else:
        explanation += "This solution implements an efficient algorithm to solve the problem systematically.\n\n"
    
    # Add intuition section
    explanation += "### Intuition\n\n"
    
    if analysis['has_hashmap'] and analysis['uses_enumerate']:
        explanation += "The key insight is to trade space for time. By storing elements in a hash map as we iterate, we can check for required values in constant time rather than repeatedly scanning the array.\n\n"
    elif analysis['has_two_pointers'] and analysis['has_sorting']:
        explanation += "After sorting, we can use two pointers moving from opposite ends. This allows us to adjust our search based on whether the current sum is too large or too small, eliminating many unnecessary comparisons.\n\n"
    elif analysis['has_dp']:
        explanation += "The problem exhibits optimal substructure - the solution to a larger problem can be built from solutions to smaller subproblems. By storing these intermediate results, we avoid redundant calculations.\n\n"
    elif analysis['has_bfs']:
        explanation += "BFS guarantees we explore nodes in order of their distance from the start. This is perfect for finding shortest paths or processing elements level by level.\n\n"
    elif analysis['has_binary_search']:
        explanation += "By maintaining a sorted search space, we can eliminate half of the remaining candidates with each comparison, leading to logarithmic time complexity.\n\n"
    else:
        explanation += "The solution breaks down the problem into manageable steps, processing elements systematically to build the final answer.\n\n"
    
    # Add algorithm walkthrough
    explanation += "### Algorithm\n\n"
    
    # Extract key steps from code
    lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
    
    step_num = 1
    for line in lines:
        if 'def ' in line and '(' in line:
            continue
        elif line.startswith('if ') and 'not' in line and 'return' in lines[lines.index(line) + 1] if lines.index(line) + 1 < len(lines) else False:
            explanation += f"{step_num}. **Handle edge cases**: Check for empty or invalid input\n"
            step_num += 1
        elif '.sort()' in line or 'sorted(' in line:
            explanation += f"{step_num}. **Sort the input**: Arrange elements in ascending order\n"
            step_num += 1
        elif 'deque([' in line or 'queue = ' in line:
            explanation += f"{step_num}. **Initialize queue**: Start with the root/initial elements\n"
            step_num += 1
        elif re.match(r'^(result|res|ans|output)\s*=\s*\[\]', line):
            explanation += f"{step_num}. **Initialize result container**: Create list to store the answer\n"
            step_num += 1
        elif 'for ' in line and 'range' in line:
            explanation += f"{step_num}. **Iterate through elements**: Process each element systematically\n"
            step_num += 1
            break
        elif 'while ' in line:
            explanation += f"{step_num}. **Main loop**: Continue until condition is met\n"
            step_num += 1
            break
    
    if analysis['has_two_pointers']:
        explanation += f"{step_num}. **Move pointers**: Adjust left/right pointers based on current sum\n"
        step_num += 1
    
    if analysis['has_hashmap']:
        explanation += f"{step_num}. **Update hash map**: Store elements for future lookups\n"
        step_num += 1
    
    explanation += f"{step_num}. **Return result**: Output the computed answer\n\n"
    
    # Add complexity analysis explanation
    explanation += "### Why This Works\n\n"
    
    complexity_points = []
    
    if analysis['has_hashmap']:
        complexity_points.append("**Hash map efficiency**: O(1) average-case lookups dramatically reduce time complexity")
    
    if analysis['has_two_pointers']:
        complexity_points.append("**Two pointers optimization**: Eliminates need for nested loops by intelligently moving pointers")
    
    if analysis['has_sorting']:
        complexity_points.append("**Sorting benefit**: Enables binary search, two pointers, and easy duplicate handling")
    
    if analysis['has_dp']:
        complexity_points.append("**Memoization**: Stores subproblem solutions to avoid redundant calculations")
    
    if analysis['has_bfs']:
        complexity_points.append("**Level-order processing**: Guarantees shortest path and systematic exploration")
    
    if analysis['has_binary_search']:
        complexity_points.append("**Logarithmic search**: Halves search space with each iteration")
    
    if not complexity_points:
        complexity_points.append("**Systematic approach**: Processes elements in a logical order to build the solution")
    
    for point in complexity_points:
        explanation += f"- {point}\n"
    
    explanation += "- **Correctness**: The algorithm handles all edge cases and produces the expected output\n"
    explanation += "- **Efficiency**: Optimized for both time and space constraints\n"
    
    return explanation


def add_explanation_to_file(filepath: Path, dry_run: bool = False) -> bool:
    """Add explanation section to a problem file."""
    try:
        # Read file
        frontmatter, before_solution, after_solution = read_mdx_file(filepath)
        
        # Check if explanation already exists
        if has_explanation_section(before_solution + after_solution):
            print(f"  ⏭️  Already has explanation: {filepath.name}")
            return False
        
        # Extract code from solution section
        code_match = re.search(r'```python\n(.*?)\n```', after_solution, re.DOTALL)
        if not code_match:
            print(f"  ⚠️  No Python code found: {filepath.name}")
            return False
        
        code = code_match.group(1)
        problem_slug = get_problem_slug(filepath)
        
        # Generate explanation
        explanation = generate_generic_explanation(problem_slug, code)
        
        # Find where to insert (after the code block, before ## Complexity)
        complexity_match = re.search(r'\n## Complexity\n', after_solution)
        if complexity_match:
            insert_pos = complexity_match.start()
            new_after = after_solution[:insert_pos] + explanation + "\n" + after_solution[insert_pos:]
        else:
            # If no complexity section, add at the end
            new_after = after_solution.rstrip() + "\n" + explanation + "\n"
        
        # Reconstruct file
        new_content = frontmatter + before_solution + new_after
        
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  ✅ Added explanation: {filepath.name}")
        else:
            print(f"  🔍 Would add explanation: {filepath.name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {filepath.name}: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Add explanations to problem MDX files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--file', type=str, help='Process a single file')
    args = parser.parse_args()
    
    problems_dir = Path(__file__).parent.parent / 'site' / 'src' / 'content' / 'problems'
    
    if args.file:
        filepath = problems_dir / args.file
        if filepath.exists():
            add_explanation_to_file(filepath, args.dry_run)
        else:
            print(f"File not found: {filepath}")
        return
    
    # Process all files
    mdx_files = sorted(problems_dir.glob('*.mdx'))
    print(f"\nProcessing {len(mdx_files)} problem files...\n")
    
    added = 0
    skipped = 0
    errors = 0
    
    for filepath in mdx_files:
        result = add_explanation_to_file(filepath, args.dry_run)
        if result:
            added += 1
        elif result is False:
            skipped += 1
        else:
            errors += 1
    
    print(f"\n{'DRY RUN - ' if args.dry_run else ''}Summary:")
    print(f"  ✅ Added: {added}")
    print(f"  ⏭️  Skipped: {skipped}")
    print(f"  ❌ Errors: {errors}")
    print(f"  📊 Total: {len(mdx_files)}")


if __name__ == '__main__':
    main()
