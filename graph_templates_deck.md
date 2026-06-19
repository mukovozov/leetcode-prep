# Graph Traversal Templates Deck

**How to use this (same as the primitive deck):**
1. **Cold retype.** Close this file, open a blank doc, type each skeleton from memory, timed. The blank-doc retype is the whole point — reading isn't repping.
2. **Predict before you run.** Before executing, write the expected output on the reference graph/grid. A wrong template announces itself when the prediction misses. *Predicting is non-negotiable — it's the step that catches the `removeFirst`/`removeLast` class of bug.*
3. **State complexity out loud.** Every template, every time. Say it before you call yourself done.
4. **Living page.** When a problem exposes a variant not here (multi-source BFS, topo sort, union-find, Dijkstra), add a row.

> Note: these are the cleaned canonical versions — `intArrayOf` not `arrayOf` (boxing), `!visited[..]` not `== false`. Rep these, not the rougher drafts.

---

## Reference graph (for the three traversal orders)

```
1 → [2, 3]
2 → [4]
3 → [4, 5]
4 → []
5 → []
```

Starting from node `1`, the three traversals produce **three different orders**:

| Traversal | Order | Why |
|---|---|---|
| **BFS** (FIFO, `removeFirst`) | `1 2 3 4 5` | level by level — all of node 1's neighbors before their children |
| **Iterative DFS** (LIFO, `removeLast`) | `1 3 5 4 2` | depth-first, but stack pops neighbors back-to-front → 3-branch first |
| **Recursive DFS** | `1 2 4 3 5` | depth-first, neighbors front-to-back → dive 1→2→4 before sibling 3 |

**The one-line distinctions to lock:**
- `removeFirst` = **BFS**. `removeLast` = **iterative DFS**. One method call is the entire difference.
- **DFS visits children before siblings. BFS visits all siblings (the full level) before any children.**
- Diagnostic on this graph: *does 4 come before or after 3?* Before → depth-first. After → breadth-first.

---

## 1. BFS — adjacency list

*Shortest path in unweighted graph, level-order, "fewest steps."*

```kotlin
fun bfs(adj: Map<Int, List<Int>>, start: Int): List<Int> {
    val traversal = mutableListOf<Int>()
    val queue = ArrayDeque<Int>()
    val visited = mutableSetOf<Int>()

    queue.addLast(start)
    visited.add(start)                       // mark on ENQUEUE
    while (queue.isNotEmpty()) {
        val current = queue.removeFirst()    // FIFO → BFS
        traversal.add(current)
        for (n in adj[current] ?: emptyList()) {
            if (n !in visited) {
                visited.add(n)               // mark on enqueue, not on dequeue
                queue.addLast(n)
            }
        }
    }
    return traversal                         // 1 2 3 4 5
}
```

**Watch:** mark visited *when you enqueue*, not when you dequeue — otherwise a node can be queued twice. `removeFirst` is the whole reason this is BFS.
**Complexity:** O(V + E) time, O(V) space.

---

## 2. Iterative DFS — adjacency list

*Same skeleton as BFS — only `removeLast` instead of `removeFirst`.*

```kotlin
fun dfsIterative(adj: Map<Int, List<Int>>, start: Int): List<Int> {
    val traversal = mutableListOf<Int>()
    val stack = ArrayDeque<Int>()
    val visited = mutableSetOf<Int>()

    stack.addLast(start)
    visited.add(start)
    while (stack.isNotEmpty()) {
        val current = stack.removeLast()     // LIFO → DFS  (only change from BFS)
        traversal.add(current)
        for (n in adj[current] ?: emptyList()) {
            if (n !in visited) {
                visited.add(n)
                stack.addLast(n)
            }
        }
    }
    return traversal                         // 1 3 5 4 2
}
```

**Watch:** this does NOT produce the same order as recursive DFS — the stack pops neighbors in reverse. Fine for reachability/visitation (most problems); matters only when order is load-bearing.
**Complexity:** O(V + E) time, O(V) space.

---

## 3. Recursive DFS — adjacency list (the default)

*Backtracking, tree post-order, "compute something on the way back up." Default to this unless depth could blow the stack (~10⁵+ on a chain-shaped graph → mention the iterative rewrite).*

```kotlin
fun dfsRecursive(adj: Map<Int, List<Int>>, start: Int): List<Int> {
    val traversal = mutableListOf<Int>()
    val visited = mutableSetOf<Int>()
    recurse(adj, start, visited, traversal)
    return traversal                         // 1 2 4 3 5
}

private fun recurse(
    adj: Map<Int, List<Int>>, current: Int,
    visited: MutableSet<Int>, traversal: MutableList<Int>,
) {
    if (current in visited) return           // base-case guard at entry
    visited.add(current)
    traversal.add(current)
    for (n in adj[current] ?: emptyList()) {
        recurse(adj, n, visited, traversal)
    }
}
```

**Watch:** visited-check at the *top* of the call (single source of truth). The call stack is your stack — clean, but deep chains can `StackOverflowError`.
**Complexity:** O(V + E) time, O(V) space (+ recursion depth on the call stack).

---

## 4. BFS — grid (implicit graph)

*Number of Islands, Max Area, Rotting Oranges (multi-source), Pacific Atlantic, shortest path on a grid.*

```kotlin
fun bfsGrid(grid: List<IntArray>, sr: Int, sc: Int): List<Pair<Int, Int>> {
    val rows = grid.size
    val cols = grid[0].size
    val dirs = arrayOf(
        intArrayOf(0, 1), intArrayOf(0, -1),
        intArrayOf(1, 0), intArrayOf(-1, 0),
    )

    val traversal = mutableListOf<Pair<Int, Int>>()
    val queue = ArrayDeque<Pair<Int, Int>>()
    val visited = Array(rows) { BooleanArray(cols) }

    queue.addLast(sr to sc)
    visited[sr][sc] = true
    while (queue.isNotEmpty()) {
        val (r, c) = queue.removeFirst()
        traversal.add(r to c)
        for (d in dirs) {
            val nr = r + d[0]
            val nc = c + d[1]
            if (nr in 0 until rows && nc in 0 until cols && !visited[nr][nc]) {
                visited[nr][nc] = true
                queue.addLast(nr to nc)
            }
        }
    }
    return traversal
}
```

**The grid traps (these bite everyone):**
1. **No `adj` map** — a grid is an *implicit* graph. Neighbors are *computed* from `(r,c) + direction`, not looked up. The `dirs` array IS the adjacency function.
2. **Bounds check BEFORE indexing.** `nr in 0 until rows && nc in 0 until cols` must come before `grid[nr][nc]` / `visited[nr][nc]`. `&&` short-circuits left-to-right, so order is load-bearing — bounds first.
3. **All four directions.** Drop one and traversal silently breaks.
4. **`visited` = `BooleanArray` grid**, not `Set<Pair>` — pairs box and hash; the boolean grid is O(1).
5. **BFS visit order depends on `dirs` order.** Cosmetic for island-counting; real for multi-source BFS / shortest-path tie-breaking.

**Reference grid** `[[5,6],[7,8]]` from `(0,0)` with dirs right,left,down,up → visits values `5 6 7 8` (right enqueues before down).
**Complexity:** O(rows · cols) time and space.

---

## 5. DFS — grid (recursive)

*Same as grid BFS minus the queue. Number of Islands is usually written this way — shortest, fewest moving parts.*

```kotlin
fun dfsGrid(grid: List<IntArray>, r: Int, c: Int, visited: Array<BooleanArray>) {
    val rows = grid.size
    val cols = grid[0].size
    if (r !in 0 until rows || c !in 0 until cols || visited[r][c]) return   // guard at entry
    visited[r][c] = true
    // process (r, c) here

    val dirs = arrayOf(
        intArrayOf(0, 1), intArrayOf(0, -1),
        intArrayOf(1, 0), intArrayOf(-1, 0),
    )
    for (d in dirs) dfsGrid(grid, r + d[0], c + d[1], visited)
}
```

**Watch:** push the bounds + visited check to the *top* of the call (mirrors recursive adj DFS) — let invalid cells early-return instead of checking before each recursive call. Cleaner than guarding at the call site.
**Complexity:** O(rows · cols) time and space.

---

## Warmup routine (~10 min)

1. **Predict the three orders** on the reference graph from node 1 — BFS, iterative DFS, recursive DFS — *before* looking. (`1 2 3 4 5` / `1 3 5 4 2` / `1 2 4 3 5`.)
2. **Cold-type all five skeletons** from a blank file, timed. Typo-free is the bar.
3. **State complexity out loud** as you finish each.
4. Any skeleton that wobbled → it's tomorrow's warmup, alone.

**Next variants to add when you hit them:** Kahn's topo sort (BFS over in-degrees), union-find (path compression + union by rank), Dijkstra (`PriorityQueue`). Those are Day-4 — leave room.
