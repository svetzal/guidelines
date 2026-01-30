## Assessment: Most Violated Principle — **No Knowledge Duplication**

After a thorough review of `apps/web/`, the project most severely violates the principle: **"Avoid multiple spots that must change together for the same reason."**

### The Violation in Three Tiers

**Tier 1 (High Risk) — Serialization exists in two places:**

- `EptWeb.EntitySerializer` — used by API controllers, produces atom-keyed maps with raw Ecto datetimes
- `EptWeb.GraphLive` (private functions around lines 1340–1412) — produces string-keyed maps with ISO 8601 formatted timestamps

Both derive the same fields from the same schemas. When a field is added to any entity, **four locations** must be updated: the schema, the context, `EntitySerializer`, and `GraphLive`'s private serializer. Missing the GraphLive copy will silently break the visualization — and there are no LiveView tests to catch it.

**Tier 2 (Maintenance Burden) — Controller helpers duplicated across files:**

- `get_actor_id/2` — copied identically into 3 controllers
- `maybe_add_opt/3` — copied identically into 3 controllers
- `get_goal_id/2`, `get_goal_ids/2`, `get_interaction_ids/2` — similar patterns duplicated

A bug fix in one copy could easily be missed in the others.

**Tier 3 (Structural) — Every controller action repeats the same find-or-404 pattern verbatim.** Lower risk but obscures the essential differences between controllers.

### How to Correct It

**Step 1 — Unify serialization into `EntitySerializer`.** Make it the single source of truth. Have it produce string-keyed maps with ISO 8601 timestamps (the more portable format). Remove the four private `serialize_*` functions from `GraphLive` and call `EntitySerializer` instead. The API tests should continue to pass since `Jason` serializes both atom-keyed and string-keyed maps to the same JSON output.

**Step 2 — Move shared controller helpers into `EptWeb.ApiHelpers`.** This module already exists and all controllers already `import` it. Move `get_actor_id/2`, `get_goal_id/2`, `get_goal_ids/2`, `get_interaction_ids/2`, and `maybe_add_opt/3` there, then delete the private copies from each controller.

**Step 3 (Optional) — Extract a `with_entity` helper** for the repeated find-or-404 pattern. Lower priority — the current approach is readable even if repetitive.

### Why This Is the Worst Violation

Other principles have gaps (notably test coverage), but knowledge duplication creates **silent, compounding risk**. Every entity schema change is a landmine — developers must remember to update both serialization paths with no compiler warning or test failure to catch a miss. The other gaps (e.g., missing LiveView tests) are additive work; this duplication is a structural defect that makes every future change more error-prone.
