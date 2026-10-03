
## 2026-10-03 — Deterministic hashing for rollout bucketing

**Problem:** how do you decide if a given user falls in the X% of
users who should see a flag?

**Naive approach (rejected):** `random.random() < rollout_percentage / 100`
evaluated on every call to `/evaluate`. This is wrong, not just
unpolished — it means the same user can get a different answer on two
consecutive page loads, since each call draws a fresh random number.
That breaks the actual point of a feature flag: a consistent
experience per user.

**Chosen approach:** hash `f"{user_id}:{flag_key}"` with a stable hash
function (`hashlib.md5`/`sha256`), take the result modulo 100, and
compare against `rollout_percentage`. The same user + same flag always
hashes to the same bucket, so repeated calls are consistent, while
different users are spread roughly evenly across the 0–99 range. No
state needs to be stored to guarantee the consistency — it falls out
of the hash being deterministic.

**Verified:** `test_evaluate_consistent_across_repeated_calls` asserts
the same user_id returns the same result across 10 calls.