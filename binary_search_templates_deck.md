# Binary Search Templates Deck

**How to use (same as the graph deck):**
1. **Cold retype.** Close this file, type each skeleton from a blank doc, timed. Reading isn't repping.
2. **Predict before you run.** Write the expected output on the reference array first. A wrong template (esp. `mid` or the bounds) announces itself when the prediction misses.
3. **State complexity out loud.** Every template, every time.
4. **Wobble-driven.** Rep Templates 1, 3, 4 daily until automatic; Template 2 (rotated) every few days. Once `mid` is reflex, drop the daily frequency — don't let the warm-up bloat.

---

## ⚠️ The pitfalls that bit you (read first, every time)

1. **`mid = lo + (hi - lo) / 2`.** The midpoint is an *index anchored to `lo`*. `(hi - lo) / 2` alone is an *offset* — only correct when `lo == 0`, which is why it broke the moment `lo` moved on #33. Not `(hi - lo + 1) / 2`, not `(lo + hi) / 2` (overflow at scale). Memorize the one form.
2. **Pair the loop condition to the update, or infinite-loop:**
   - `while (lo <= hi)` ↔ `lo = mid + 1` / `hi = mid - 1` (closed interval, return `lo`)
   - `while (lo < hi)` ↔ `hi = mid` (half-open) — needs `lo = mid + 1` on the other branch or it spins
   - **Pick the `lo <= hi` style and use it everywhere** — it's the one you already drilled, and all four templates below use it.
3. **Overflow.** `piles.sum()` on an `IntArray` returns `Int` and overflows (~10¹³). Widen: `sumOf { it.toLong() }`. Same for any sum/product of two large Ints.
4. **No early `return` in a boundary search.** Exact-match search returns the instant it hits the target. Boundary search (Templates 3–4) must run to collapse — a `mid` that works might not be the *smallest* one. Return `lo` at the end.

---

## Reference array (for predictions)

```
nums = [1, 3, 5, 7, 9]      // indices 0..4
```

---

## 1. Exact match — sorted array

*"Find target in a sorted array, return its index or -1."*

```kotlin
fun search(nums: IntArray, target: Int): Int {
    var lo = 0
    var hi = nums.size - 1
    while (lo <= hi) {
        val mid = lo + (hi - lo) / 2
        when {
            nums[mid] == target -> return mid       // early return is OK here
            nums[mid] < target  -> lo = mid + 1
            else                -> hi = mid - 1
        }
    }
    return -1
}
```

**Predict:** target `7` → `3`; target `4` → `-1`.
**Complexity:** O(log n) time, O(1) space.

---

## 2. Exact match — ROTATED sorted array (#33, your redo)

*"Sorted array rotated at an unknown pivot, distinct values, find target."*

```kotlin
fun searchRotated(nums: IntArray, target: Int): Int {
    var lo = 0
    var hi = nums.size - 1
    while (lo <= hi) {
        val mid = lo + (hi - lo) / 2
        when {
            nums[mid] == target -> return mid
            nums[lo] <= nums[mid] -> {                          // LEFT half [lo..mid] is sorted
                if (target >= nums[lo] && target < nums[mid]) hi = mid - 1
                else lo = mid + 1
            }
            else -> {                                           // RIGHT half [mid..hi] is sorted
                if (target > nums[mid] && target <= nums[hi]) lo = mid + 1
                else hi = mid - 1
            }
        }
    }
    return -1
}
```

**The whole trick:** find which half is sorted by comparing `nums[lo]` to `nums[mid]`, then check whether `target` falls **inside that sorted half's range**. *Never* compare `target` to `nums[mid]` for direction — that's plain binary search and it fails on rotation. (This is exactly where attempt 1 went.)
**Predict** on `[4,5,6,7,0,1,2,3]`: target `0` → `4`; target `3` → `7`; target `8` → `-1`.
**Complexity:** O(log n) time, O(1) space.

---

## 3. Boundary / first-true (the workhorse)

*"Smallest index/value where a monotonic predicate flips false→true." Lower-bound, insertion point, "first element ≥ target", "smallest X that works."*

```kotlin
// pred is monotonic over [lo, hi]: false … false true … true
// returns the smallest value where pred is true; (hi + 1) if never true
fun firstTrue(lo0: Int, hi0: Int, pred: (Int) -> Boolean): Int {
    var lo = lo0
    var hi = hi0
    while (lo <= hi) {
        val mid = lo + (hi - lo) / 2
        if (pred(mid)) hi = mid - 1      // works → answer is mid or further left, keep looking
        else           lo = mid + 1      // fails → answer is strictly right of mid
    }
    return lo                            // first value where pred is true; NO early return
}
```

**Watch:** the only difference from Template 1 is *no early return* and the predicate (not equality) picks the direction. `lo` converges onto the boundary — that's why you return `lo`.
**Predict:** `firstTrue(0, 4) { nums[it] >= 5 }` → `2`; `{ nums[it] >= 6 }` → `3`; `{ nums[it] >= 10 }` → `5` (none, past the end).
**Complexity:** O(log n × cost of `pred`).

---

## 4. Binary search on the ANSWER (#875 Koko, your redo)

*Same skeleton as Template 3 — but you search a **value range**, not an array, with a `feasible()` you write.*

```kotlin
fun minFeasible(piles: IntArray, h: Int): Int {
    val lo = maxOf(1L, piles.sumOf { it.toLong() } / h)   // valid lower bound, clamp ≥ 1
    val hi = piles.max().toLong()                          // a value that always works

    fun feasible(k: Long): Boolean {                       // monotonic: once true, stays true as k grows
        var hours = 0L
        for (p in piles) hours += (p + k - 1) / k          // integer ceil(p/k); needs k ≥ 1
        return hours <= h
    }

    var l = lo
    var r = hi
    while (l <= r) {
        val mid = l + (r - l) / 2
        if (feasible(mid)) r = mid - 1
        else               l = mid + 1
    }
    return l.toInt()
}
```

**Recognition cues — the "name it in 5 sec" part:**
- "**minimum** speed / capacity / size / divisor such that [constraint] holds"
- the answer is a **number in a range**, and *"does value V work?"* is **monotonic** (true for all V above some threshold)
- the range is huge (~10⁹) so you can't scan it linearly

**Traps (all from your Koko run):** `sum()` overflows `Int` → `sumOf { it.toLong() }`; integer ceil `(p + k - 1) / k` divides by zero if `k == 0` → clamp `lo ≥ 1`; floating-point `ceil(p.toDouble()/k)` works but reads as a smell — use the integer form.
**Complexity:** O(n · log(range)) — `n` for `feasible`, log over the **value space** (not the array — say `log(max)`, not `log n`).

---

## Recognition drill — name the template in 5 seconds

Read one, say T1 / T2 / T3 / T4, verify. Shuffle each pass.

1. Find target in a sorted array. → **T1**
2. Min eating speed to finish in H hours. → **T4**
3. Find target in a rotated sorted array. → **T2**
4. First index where `nums[i] >= target` (insertion point). → **T3**
5. Smallest divisor so the sum stays under a limit. → **T4**
6. Least capacity to ship all packages in D days. → **T4**
7. Find first and last position of a target. → **T3** (run it twice: first-true, then last-true)
8. Smallest number of days to make M bouquets. → **T4**
9. Search a value in a sorted array, return insertion point if absent. → **T3**
10. Min speed / max value / smallest X subject to a monotonic check. → **T4**

> The tell for T4: the answer is a *number you'd otherwise guess-and-check*, and checking one guess is monotonic. T3 and T4 are the **same skeleton**; T4 just searches a value range with a hand-written `feasible()`.

---

## Warmup routine (~5 min)

1. **Cold-type T1, T3, T4** from a blank file (T2 every few days). Typo-free is the bar; `mid` must be automatic.
2. **Predict** each on the reference array before running.
3. **State complexity out loud** — and for T4, say `log(value range)`, not `log n`.
4. Any template where `mid` or the bounds wobbled → it's tomorrow's warm-up, alone.
