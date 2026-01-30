## Assessment: Most Violated Principle

After a thorough exploration of the `apps/web` Phoenix codebase, the most violated principle is:

### **Simple Design: No Knowledge Duplication**

The codebase has a systematic pattern of duplicating the same business logic — specifically entity serialization — across **six separate locations**. This isn't coincidental similarity that might diverge; it's the *same decision* expressed repeatedly.

---

### Where the duplication lives

**Four API controllers** each contain identical private helper functions:

- `maybe_put/3` — conditionally adding keys to maps
- `merge_meta/3` — merging/removing metadata keys
- `format_errors/1` — traversing changeset errors
- `maybe_add_opt/3` — conditionally building keyword lists

These are copy-pasted verbatim across `ActorController`, `GoalController`, `InteractionController`, and `JourneyController`.

**Then**, `GraphLive` duplicates all four `serialize_*` functions from the controllers — the same database-to-wire transformation logic, reimplemented in the LiveView layer.

---

### Why this is the worst violation

1. **Maintenance landmine**: A change to how entities are serialized requires edits in 6+ files. Miss one, and you have inconsistent API responses.
2. **N+1 queries baked in**: Each serialization function does individual `Repo.get` calls to resolve foreign keys (e.g., `actor_id → actor.external_id`). This pattern is duplicated everywhere, meaning fixing it requires touching every copy.
3. **No tests as a safety net**: The test suite has ~5 tests covering error pages only. Zero API controller tests, zero LiveView tests. Refactoring without tests is dangerous.
4. **Credo confirms**: 15 refactoring opportunities, cyclomatic complexity up to 29 (threshold: 9), nesting depth up to 4 (threshold: 2) — all concentrated in these duplicated serialization functions.

---

### How to correct it

**Step 1: Write tests first** (you can't safely refactor without them)
- Add controller tests for each API endpoint covering CRUD operations
- These tests become the executable spec that protects the refactoring

**Step 2: Extract a shared serialization module**

```elixir
defmodule EptWeb.EntitySerializer do
  @moduledoc "Pure functions for converting Screenplay entities to API representations."

  def serialize_actor(actor) do ... end
  def serialize_goal(goal) do ... end
  def serialize_interaction(interaction) do ... end
  def serialize_journey(journey) do ... end
end
```

This is a *functional core* — pure functions with no side effects, trivially testable in isolation.

**Step 3: Extract shared controller helpers**

```elixir
defmodule EptWeb.ApiHelpers do
  def maybe_put(map, _key, nil), do: map
  def maybe_put(map, key, value), do: Map.put(map, key, value)

  def format_errors(changeset) do ... end
  def merge_meta(existing, add, remove) do ... end
end
```

**Step 4: Fix N+1 queries with preloading**

Move association resolution out of serialization and into the context layer:

```elixir
# In Ept.Screenplay context
def list_goals(project_id) do
  Goal
  |> where(project_id: ^project_id)
  |> preload(:actor)  # Eager load, not N+1
  |> Repo.all()
end
```

Then serializers receive fully-loaded structs and remain pure.

**Step 5: Use the shared module everywhere**

Both API controllers and `GraphLive` import from `EntitySerializer`, eliminating all duplication.

---

### Why *this* principle over others?

The project also violates "Tests Are the Executable Spec" (almost no tests) and has documentation gaps. But the duplication is the **root cause** of the project's fragility — it's what makes the missing tests so dangerous, and what makes every future change risky. Fix the duplication first, and the codebase becomes dramatically easier to test and maintain.
