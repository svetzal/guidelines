Here's the plan I've created. It's written to `apps/web/REFACTORING_PLAN.md` and follows these key principles:

## 8-Step Refactoring Plan

**Steps 1-3: Build the safety net (tests first)**
1. **Add test infrastructure** — DataCase, factory fixtures, API auth helpers. Without these, we can't write controller tests.
2. **Write ActorController tests** — the simplest entity, establishes the test pattern for all controllers.
3. **Write Goal/Interaction/Journey controller tests** — complete coverage before touching production code.

**Steps 4-7: Extract and consolidate (safe refactoring)**
4. **Extract `EptWeb.ApiHelpers`** — the 5 identical private helpers (`maybe_put`, `merge_meta`, `format_errors`, `maybe_add_opt`, `get_actor_id`) move to one module.
5. **Extract `EptWeb.EntitySerializer`** — the 4 `serialize_*` functions move to one module, initially preserving the N+1 query pattern.
6. **Fix N+1 queries** — preload associations in the Screenplay context so serializers become pure functions (no `Repo.get` calls).
7. **Unify GraphLive** — replace GraphLive's duplicate serializers with the shared EntitySerializer.

**Step 8: Quality gates** — format, test coverage, Credo strict, security audits.

Each step is independently shippable and the system works correctly after every commit. Tests come first so refactoring is always protected.
