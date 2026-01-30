The plan is ready for your review. Here's the summary:

**6 incremental commits, each independently shippable:**

1. **Add EntitySerializer unit tests** — safety net before changes
2. **Migrate EntitySerializer to string keys + ISO 8601** — aligns with GraphLive's format; safe because Jason encodes both key types identically
3. **Replace GraphLive's duplicate serializers** — delete ~73 lines, call EntitySerializer instead
4. **Add ApiHelpers unit tests** — safety net before expansion
5. **Extract controller helpers into ApiHelpers** — move 5 duplicated private functions (`get_actor_id`, `maybe_add_opt`, `get_goal_id`, `get_goal_ids`, `get_interaction_ids`) from 3 controllers
6. **(Optional) Extract find-or-404 pattern** — reduce 16 repeated case expressions; lower priority, can defer

Steps 1-5 deliver the highest value by eliminating the two worst duplication tiers. Step 6 is a nice-to-have cleanup.
