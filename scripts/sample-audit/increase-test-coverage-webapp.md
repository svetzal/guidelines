## Assessment: Most Violated Principle

**The principle `apps/web` most violates is: Tests Are the Executable Spec.**

### The Evidence

All 134 existing tests pass, but the project achieves only **31.58% test coverage** against a 90% threshold. The majority of the application's behaviour has no executable specification.

**Modules with 0% test coverage include:**

| Module | Lines | Risk |
|--------|-------|------|
| `EptWeb.GraphLive` | 1,537 | Complex visualization state, PubSub, access control |
| `EptWeb.ProjectsLive` | 676 | Project management, token handling, invitations |
| `Ept.Accounts.UserToken` | — | Security-critical token management |
| `EptWeb.InvitationController` | — | Invitation acceptance flow |
| `EptWeb.UserRegistrationLive` | — | Registration flow |
| `EptWeb.UserSettingsLive` | — | User settings |

**Partially covered, security-critical modules:**
- `Ept.Accounts` — **3.13%** (user management)
- `EptWeb.UserAuth` — **26.67%** (authentication plugs and mount hooks)
- `Ept.Screenplay` — **66.12%** (core business logic context)

### Why This is the Most Critical Violation

The irony is that your *existing* tests are excellent. The API controller tests (92–96% coverage) are exemplary — they cover happy paths, edge cases, 404s, validation failures, and cross-project isolation. They genuinely serve as executable specs. The entity schemas sit at 100%. The recently extracted `EntitySerializer` and `ApiHelpers` are well-covered.

But this quality makes the gap starker. The team clearly knows how to write great tests — the discipline simply hasn't been extended to the LiveViews, authentication, and accounts layers. This matters more than any other principle violation because:

1. **It's a risk multiplier.** Without tests, you can't safely refactor, which means other principle violations (duplication, unclear intent) become permanently frozen in place.
2. **Security exposure.** Authentication and authorization code at 3–27% coverage means the most sensitive parts of the application have the least specification.
3. **Invisible breakage.** The recent (and good!) duplication-removal refactoring in `EntitySerializer` and `ApiHelpers` could have silently broken LiveView behaviour — and you'd have no way to know.

### How to Correct It

**Phased approach, highest-risk modules first:**

**Phase 1 — Security foundation** (~2 weeks, targets ~45% coverage)
- Complete `Ept.Accounts` tests (user creation, token generation/verification, scope handling)
- Complete `EptWeb.UserAuth` tests (all plugs, all `on_mount` callbacks, edge cases)
- Test `Ept.Accounts.UserToken` (generation, verification, expiry)

**Phase 2 — Core business logic** (~2 weeks, targets ~65% coverage)
- Bring `Ept.Screenplay` to 100% (focus on sharing, invitations, journey step management — the branches currently uncovered)
- Test PubSub broadcast behaviour

**Phase 3 — LiveView critical paths** (~3 weeks, targets ~80% coverage)
- `ProjectsLive`: mount, project CRUD, token creation/download, invitation sending, member management
- `GraphLive`: mount with access control (owner vs viewer vs denied), entity selection, URL parameter handling, view switching
- Follow the pattern your controller tests already establish — adapt it for `Phoenix.LiveViewTest`

**Phase 4 — Long tail** (~2 weeks, targets ~85%+ coverage)
- `Ept.Emails`, `InvitationController`, registration/settings LiveViews
- Empty-state and error-state rendering

**Tactical note:** The coverage threshold is currently set at 90% but failing silently. Either lower it to reality (e.g. 50%) and ratchet up with each phase, or wire it into CI to block merges. A threshold that fails but is ignored is worse than no threshold — it teaches the team to ignore quality signals.
