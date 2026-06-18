# Coding Prep — Dated Schedule (full-time)

**Situation:** Android + behavioral already passed. **Only two coding rounds left.**
**Rounds:** **Round 1 — Mon Jun 29** · **Round 2 — Wed Jul 1.** Vacation Jul 4–9 (after both, irrelevant).
**Capacity:** full-time, but cap effective work at **~5–6 focused hours/day.** Past that, reps degrade and the taper erodes. More hours ≠ more readiness.

---

## Rules that don't bend

1. **Quality over volume.** 3–4 problems *interview-style* (out loud, clarify → brute force → optimize → dry-run → complexity) beat 8 grinded silently.
2. **20-minute rule.** Stuck 20 min with no progress → read solution, understand, close it, re-implement from scratch.
3. **No code execution from Jun 23 on.** Plain text editor for all mocks — no run button, no autocomplete. Dry-run by hand.
4. **Log the redo list as you go.** Any problem failed / over target / fumbled → `python3 redo.py add <id> "<name>" --pattern P --reason fail|slow|fumble --target N`. The redo list *is* the plan for Jun 27–28.
5. **Protect the taper (Jun 28).** Cramming the eve of Round 1 has negative return.
6. **Time targets:** Easy ≤ 15 min, Medium ≤ 25–30 min. Over target = redo list, even if solved.

---

## The schedule

### Thu Jun 18 — Two pointers / sliding window / binary search (~5 hrs)
Finish Day-2 content. (3Sum ✓, Sort Colors in progress.)
- Remaining: **Longest Repeating Char Replacement (424, M)** · sliding window, **Search in Rotated Sorted Array (33, M)**, **Koko Eating Bananas (875, M)** · binary-search-on-answer (the variant Google loves), **Single Element in Sorted Array (540, M)** if time.
- End: log anything over target.

### Fri Jun 19 — Graphs I: BFS/DFS ⚠️ weak (~5.5 hrs)
- **Templates from memory, blank file (45 min):** iterative BFS (`ArrayDeque`), recursive DFS, iterative DFS w/ explicit stack, grid traversal w/ `directions`.
- **Problems:** Number of Islands (200), Pacific Atlantic (417), Perfect Squares (279) · BFS, + one matrix: Rotate Image (48) or Spiral Matrix (54). **Word Ladder (127, H) → read-and-understand only.**
- Per problem say out loud *why* BFS vs DFS.

### Sat Jun 20 — Graphs II: topo / union-find / Dijkstra ⚠️ weak (~5.5 hrs)
- **Templates from memory:** Kahn's (BFS topo), union-find (path compression + union by rank), Dijkstra (`PriorityQueue`).
- **Problems:** Course Schedule (207), Course Schedule II (210), Number of Provinces (547), Evaluate Division (399). **Longest Increasing Path in Matrix (329, H) → read-and-understand if tight.**
- Recognition drill: "dependency/ordering?" → topo. "same group?" → union-find.

### Sun Jun 21 — Backtracking I ⚠️ weak (~5 hrs)
- **The one template (45 min):** `choose → recurse → unchoose`. Derive subsets / permutations / combination-sum from the single skeleton.
- **Problems:** Subsets (78), Subsets II (90) · the `i > start && nums[i]==nums[i-1]` dup-skip, Permutations (46), Combination Sum (39), Generate Parentheses (22).
- Per problem, state the decision tree out loud: choice / prune / record.

### Mon Jun 22 — Backtracking II + trees ⚠️ weak (~5.5 hrs)
- **Backtracking:** Word Search (79) · grid backtracking, Palindrome Partitioning (131), Letter Combinations (17), Target Sum (494).
- **Trees:** warmups Invert (226) / Balanced (110) / Max Depth (104), then the trap — Diameter (543) · return-value-vs-accumulate, Kth Smallest BST (230) · inorder, **Max Path Sum (124, H)** · same trap, harder.
- Lock the "return value vs side-effect accumulation" articulation.

### Tue Jun 23 — Mock 1 + Linked List templates (~5.5 hrs)
- **Mock 1 (90 min):** two 45-min sessions, plain editor, **one graph + one backtracking** (your weak areas), unseen problems from the Google clusters. Run with the mock-interviewer prompt.
- **Scorecard:** clarified first? brute force stated? narrated throughout? dry-ran before "done"? complexity unprompted? finished in time?
- **Review (60 min):** every "no" → one sentence on the trigger. Failures/slow → redo list.
- **Linked List templates (remaining time):** reverse (`prev/curr/next`), dummy head, fast/slow, merge two sorted.

### Wed Jun 24 — Linked Lists 🆕 (~5.5 hrs)
Biggest gap in v1, 14 problems in the Google cluster. Pointer work is muscle memory — lock the templates and the family is fast.
- **Core:** Reverse (206), Merge Two Sorted (21), Cycle (141) · Floyd, Remove Nth From End (19), Reorder List (143), Cycle II (142), Add Two Numbers (2), Copy List w/ Random Pointer (138), Reverse Linked List II (92).
- **If time:** Swap Nodes in Pairs (24), Sort List (148). **k-Group (25, H) → read-and-understand.**
- Recurring bugs to watch: losing `next` before rewiring, fast/slow off-by-one, forgetting the dummy head.
- **Bridge:** tomorrow's LRU is hashmap + hand-rolled doubly-linked list — today is the prerequisite.

### Thu Jun 25 — DP + Greedy (~5.5 hrs)
- **1D:** Climbing Stairs (70) warmup, House Robber (198 + 213), Coin Change (322), LIS (300), Max Subarray (53) · Kadane, Word Break (139).
- **2D:** Unique Paths (62), Longest Palindromic Substring (5) · expand-around-center. **Edit Distance (72, M) → read-and-understand if tight.**
- **Greedy:** Jump Game (55 + 45), Gas Station (134), Best Time to Buy/Sell II (122).
- Per DP problem, say out loud: **state / transition / base case.**

### Fri Jun 26 — Mock 2 + Design/LRU + heaps/intervals/stacks (~6 hrs, dense)
- **Mock 2 (90 min):** two 45-min problems, plain editor, **random topics** across the whole space. Patches → redo list.
- **Design/LRU (priority):** **LRU Cache (146) — build it COLD**, no peeking; Insert Delete GetRandom O(1) (380); Logger Rate Limiter (359).
- **Heaps:** Kth Largest (215), Top K Frequent (347). **Find Median from Data Stream (295, H) → read-and-understand.**
- **Intervals:** Merge (56), Insert (57), Meeting Rooms II (253).
- **Stacks:** Valid Parens (20) warmup, Decode String (394), Remove K Digits (402). **Largest Rectangle (84, H) → read-and-understand.**
- If fading, lean on the read-and-understand valves. LRU cold is the one non-negotiable.

### Sat Jun 27 — Mock 3 dress rehearsal + redo burn-down (~5 hrs, taper begins)
- **Mock 3 (2 hrs):** simulate the real loop — two back-to-back 45-min rounds, 10-min break, quiet room, plain editor, no notes, random topics (linked lists / design now fair game).
- **Redo burn-down (90 min):** re-solve the redo list **from scratch**, no peeking. A problem leaves the list only when solved within target, narrated, clean dry-run. **Rebuild LRU cold if it's still on the list.**
- **Light Strings/Math-bit pass (remaining, low priority — not weak areas):** atoi (8), Single Number (136) · XOR, Pow(x,n) (50), Reverse Integer (7) · overflow. Internalize the overflow traps once.
- Start winding down. Total ~5 hrs, not 6.

### Sun Jun 28 — TAPER EVE 🛑 (~3 hrs, deliberately light — PROTECT THIS)
- **Template speed-run from memory (~60 min):** BFS, DFS, topo, union-find, Dijkstra, backtracking skeleton, binary search, sliding window, **linked-list reverse + fast/slow, LRU shape.**
- Clear any redo survivors.
- **One optional short mock — easy problem only**, to feel fast. Skip it if you're sharp.
- **No new material after midday.** Eat normal, sleep 8 hrs. Cramming here costs more than it returns.

### Mon Jun 29 — ROUND 1 🎯
- Morning: **one easy warm-up** to feel fast (not to learn). Skim Kotlin toolbelt + template list. Nothing new.
- Interview. Narrate, clarify first, brute force → optimize, dry-run, state complexity. No silent punts.

### Tue Jun 30 — BETWEEN ROUNDS (feather-light)
- You're maintaining, not building. **Do not cram.**
- Optional: one easy warm-up, skim weak-area templates (graphs/backtracking), glance the redo list. Mostly rest.

### Wed Jul 1 — ROUND 2 🎯
- Same morning routine as Jun 29: one easy warm-up, skim templates, nothing new.
- Interview. Then you're done — vacation earned.

---

## Per-problem protocol (paste at the top of every session)

- [ ] Restate the prompt in one sentence. 2–3 clarifying questions out loud (empty input? duplicates? negatives? size bounds → complexity budget?).
- [ ] State brute force + its complexity *before* optimizing.
- [ ] Name the pattern out loud ("BFS on an implicit graph because…").
- [ ] Code. Talk while coding. No silent stretch > 30 sec.
- [ ] Dry-run one normal + one edge case *before* declaring done.
- [ ] State final time + space complexity.

---

## Trims / read-and-understand (release valves — don't grind these)
Word Ladder (127) · Longest Increasing Path (329) · Edit Distance (72) · Find Median from Data Stream (295) · Largest Rectangle (84) · Reverse Nodes in k-Group (25) · Median of Two Sorted Arrays (4). Strings + Math/bit are low-priority tails, not weak areas — fit them in, don't protect them.

## If a day blows past budget
Drop a read-and-understand problem. **Do not** silently extend into the next day — that's how tapers collapse.
