I now have everything I need. Here is the complete, detailed, step-by-step plan:

---

## Plan: Closing the Test Coverage Gap in `apps/web`

### Overview

The project has 31.58% test coverage against a 90% threshold. The existing tests (API controllers, EntitySerializer, ApiHelpers) are exemplary. The gap is in: Accounts (3.13%), UserAuth (26.67%), Screenplay (66.12%), all LiveViews (0%), InvitationController (0%), Emails (0%), and ApiAuth plug (0%). This plan works highest-risk-first in 14 discrete steps, each producing a passing test suite and a committable increment.

---

### Step 1: Add `log_in_user/1` Test Helper to ConnCase

**Why:** Every LiveView and controller test that touches authenticated routes needs a helper to simulate a logged-in browser session. The existing `setup_api_auth` only handles API Bearer token auth. We need the equivalent for browser session auth.

**File:** `apps/web/test/support/conn_case.ex`

**What to add:**
- A `log_in_user/2` function that:
  1. Calls `Ept.Accounts.generate_user_session_token(user)` to get a session token
  2. Calls `Plug.Test.init_test_session(conn, %{})` then puts `user_token` into the session via `Plug.Conn.put_session(conn, :user_token, token)`
  3. Returns the conn with the session established
- A `setup_browser_auth/1` setup callback that creates a user via `Fixtures.user_fixture()`, creates a project via `Fixtures.project_fixture(user)`, and returns `{:ok, conn: log_in_user(build_conn(), user), user: user, project: project}`
- A `register_and_log_in_user/1` setup callback (alias for clarity)

**Pattern reference:** This is the standard `phx.gen.auth` test helper pattern. Adapt from what `setup_api_auth` already does, but for browser sessions instead of API Bearer tokens.

**Verify:** Run `mix test` — all 134 existing tests should still pass. No new tests yet, just infrastructure.

---

### Step 2: Test `Ept.Accounts` Context (Security-Critical)

**Why:** At 3.13% coverage, the authentication context is the highest-risk untested code. Every user-facing operation depends on it.

**File to create:** `apps/web/test/ept/accounts_test.exs`

**Test module:** `Ept.AccountsTest`, using `Ept.DataCase, async: true`

**Tests to write:**

```
describe "get_user_by_email/1"
  - test "returns user when email exists"
  - test "returns nil when email does not exist"
  - test "returns nil for nil input" (guard clause — won't match binary guard)

describe "get_user_by_email_and_password/2"
  - test "returns user with correct email and password"
  - test "returns nil with correct email but wrong password"
  - test "returns nil with nonexistent email"
  - test "returns nil with nil password" (timing attack protection)

describe "get_user!/1"
  - test "returns user by id"
  - test "raises Ecto.NoResultsError for missing id"

describe "register_user/1"
  - test "creates user with valid attributes"
  - test "hashes the password (not stored in plaintext)"
  - test "returns error changeset with missing email"
  - test "returns error changeset with invalid email format"
  - test "returns error changeset with too-short password"
  - test "returns error changeset with duplicate email"
  - test "stores first_name and last_name"

describe "create_user/1"
  - test "delegates to register_user/1"

describe "change_user_registration/2"
  - test "returns a changeset for the user"
  - test "allows setting email and password"

describe "change_user_email/2"
  - test "returns a changeset for changing email"

describe "change_user_password/2"
  - test "returns a changeset for changing password"
  - test "validates password confirmation"

describe "update_user_password/3"
  - test "updates password with valid current password"
  - test "returns error with invalid current password"
  - test "deletes all user tokens after password change"
  - test "returns error with too-short new password"

describe "generate_user_session_token/1"
  - test "generates a token for the user"

describe "get_user_by_session_token/1"
  - test "returns user for valid token"
  - test "returns nil for invalid token"
  - test "returns nil for expired token" (this requires inserting a token with old timestamp — use Repo.update! to backdate)

describe "delete_user_session_token/1"
  - test "deletes the session token"
  - test "returns :ok even when token doesn't exist"

describe "confirm_user/1"
  - test "confirms user with valid token"
  - test "returns :error with invalid token"
  - test "returns :error with expired token"
  - test "deletes confirm tokens after confirmation"

describe "get_user_by_reset_password_token/1"
  - test "returns user with valid reset token"
  - test "returns nil with invalid token"
  - test "returns nil with expired token"

describe "reset_user_password/2"
  - test "resets password with valid attrs"
  - test "returns error with invalid attrs (too short)"
  - test "deletes all user tokens after reset"
```

**Setup:** Use `import Ept.Fixtures` and create users with `user_fixture/1`. For email token tests, use `Ept.Accounts.UserToken.build_email_token/2` and insert directly via `Repo.insert!/1`.

**Verify:** `mix test test/ept/accounts_test.exs`

---

### Step 3: Test `Ept.Accounts.UserToken` (Security-Critical)

**Why:** Token generation, hashing, and verification is security-critical infrastructure. Incorrect behaviour here means session hijacking or token replay attacks.

**File to create:** `apps/web/test/ept/accounts/user_token_test.exs`

**Test module:** `Ept.Accounts.UserTokenTest`, using `Ept.DataCase, async: true`

**Tests to write:**

```
describe "build_session_token/1"
  - test "returns a token and a UserToken struct"
  - test "token is 32 bytes of random data"
  - test "struct has context 'session' and correct user_id"

describe "verify_session_token_query/1"
  - test "returns {:ok, query} for valid token"
  - test "query finds user when token exists and is not expired"
  - test "query returns nil when token is expired (> 60 days)"
  - test "query returns nil when token doesn't exist"

describe "build_email_token/2"
  - test "returns base64url token and hashed UserToken struct"
  - test "struct stores hashed version (not raw)"
  - test "struct has correct context and sent_to"

describe "verify_email_token_query/2" with "confirm" context
  - test "returns {:ok, query} for valid base64 token"
  - test "returns :error for invalid base64 encoding"
  - test "query finds user when token valid and email unchanged"
  - test "query returns nil when token expired (> 7 days for confirm)"

describe "verify_email_token_query/2" with "reset_password" context
  - test "query returns nil when token expired (> 1 day for reset_password)"
  - test "query finds user when token is fresh"

describe "verify_change_email_token_query/2"
  - test "returns {:ok, query} for valid change: token"
  - test "returns :error for invalid base64 encoding"
  - test "query returns nil when expired (> 7 days)"

describe "by_token_and_context_query/2"
  - test "returns query matching token and context"

describe "by_user_and_contexts_query/2"
  - test "matches all contexts when :all is passed"
  - test "matches only specified contexts when list is passed"
```

**Verify:** `mix test test/ept/accounts/user_token_test.exs`

---

### Step 4: Test `EptWeb.UserAuth` (Security-Critical)

**Why:** At 26.67% coverage, this module guards every authenticated route. It handles login, logout, session management, remember-me cookies, and LiveView mount hooks.

**File to create:** `apps/web/test/ept_web/user_auth_test.exs`

**Test module:** `EptWeb.UserAuthTest`, using `EptWeb.ConnCase, async: true`

**Tests to write:**

```
describe "log_in_user/3"
  - test "stores user token in session"
  - test "redirects to / by default"
  - test "redirects to user_return_to path when set in session"
  - test "clears session on login (fixation protection)"
  - test "writes remember_me cookie when params include remember_me: true"
  - test "does not write remember_me cookie by default"

describe "log_out_user/1"
  - test "deletes user session token from database"
  - test "clears session"
  - test "deletes remember_me cookie"
  - test "redirects to /"
  - test "broadcasts disconnect on live_socket_id" (verify via EptWeb.Endpoint.subscribe)

describe "fetch_current_user/2"
  - test "assigns current_user from session token"
  - test "assigns nil when no session token"
  - test "assigns user from remember_me cookie when no session"
  - test "assigns nil when neither session nor cookie"

describe "on_mount :mount_current_user"
  - test "assigns current_user from session"
  - test "assigns nil when no session token"

describe "on_mount :ensure_authenticated"
  - test "continues when user is authenticated"
  - test "halts and redirects to login when not authenticated"
  - test "puts flash error message when not authenticated"

describe "on_mount :redirect_if_user_is_authenticated"
  - test "redirects to / when user is authenticated"
  - test "continues when not authenticated"

describe "redirect_if_user_is_authenticated/2" (plug)
  - test "redirects when user is assigned"
  - test "passes through when no user"

describe "require_authenticated_user/2" (plug)
  - test "passes through when user is assigned"
  - test "redirects to login when no user"
  - test "stores return_to path for GET requests"
  - test "does not store return_to for non-GET requests"
```

**Important notes:**
- For plug tests, build a conn, set assigns manually, call the plug function, assert on response.
- For `on_mount` tests, use `Phoenix.LiveViewTest` — but these are tricky. An alternative is to test them indirectly via the LiveView mount tests in later steps. If direct testing is too complex, document the decision and cover via integration tests.
- For `fetch_current_user` cookie tests, use `Plug.Test.init_test_session` and `Plug.Conn.put_resp_cookie` with the signed cookie.

**Verify:** `mix test test/ept_web/user_auth_test.exs`

---

### Step 5: Test `EptWeb.Plugs.ApiAuth`

**Why:** This plug protects all API routes. It's currently at 0% coverage and only indirectly tested through the API controller tests.

**File to create:** `apps/web/test/ept_web/plugs/api_auth_test.exs`

**Test module:** `EptWeb.Plugs.ApiAuthTest`, using `EptWeb.ConnCase, async: true`

**Tests to write:**

```
describe "call/2"
  - test "assigns current_project, current_user, and api_token for valid Bearer token"
  - test "returns 401 with error message when no Authorization header"
  - test "returns 401 with error message when Authorization header is malformed"
  - test "returns 401 when Bearer token is invalid/expired"
  - test "halts the connection on authentication failure"
```

**Setup:** Use `Fixtures.user_fixture()`, `Fixtures.project_fixture(user)`, `Fixtures.api_token_fixture(project)` for the happy path. Use `Phoenix.ConnTest.build_conn()` with `Plug.Conn.put_req_header` for setting up the authorization header. Call `EptWeb.Plugs.ApiAuth.call(conn, [])` directly.

**Verify:** `mix test test/ept_web/plugs/api_auth_test.exs`

---

### Step 6: Complete `EptWeb.ApiHelpers` Test Coverage

**Why:** 5 functions are untested: `get_actor_id/2`, `get_goal_id/2`, `get_goal_ids/2`, `get_interaction_ids/2`, `maybe_add_opt/3`. These are used by every API controller.

**File:** `apps/web/test/ept_web/api_helpers_test.exs` (existing file — add new `describe` blocks)

**Tests to add:**

```
describe "get_actor_id/2"
  - test "returns internal UUID when actor external_id exists"
  - test "returns nil when actor external_id doesn't exist"
  - test "returns nil when external_id param is nil"

describe "get_goal_id/2"
  - test "returns internal UUID when goal external_id exists"
  - test "returns nil when goal external_id doesn't exist"
  - test "returns nil when external_id param is nil"

describe "get_goal_ids/2"
  - test "returns list of internal UUIDs for existing goal external_ids"
  - test "filters out non-existent goal external_ids"
  - test "returns empty list when param is nil"

describe "get_interaction_ids/2"
  - test "returns list of internal UUIDs for existing interaction external_ids"
  - test "filters out non-existent interaction external_ids"
  - test "returns empty list when param is nil"

describe "maybe_add_opt/3"
  - test "adds option to keyword list when value is not nil"
  - test "returns original keyword list when value is nil"
```

**Verify:** `mix test test/ept_web/api_helpers_test.exs`

---

### Step 7: Test `Ept.Screenplay` Context — Sharing, Invitations, Members

**Why:** The Screenplay context is at 66.12%. The entity CRUD is well-covered indirectly through API controller tests. The uncovered branches are: project sharing (invitations, members, viewable projects), API tokens, and journey step management.

**File to create:** `apps/web/test/ept/screenplay_test.exs`

**Test module:** `Ept.ScreenplayTest`, using `Ept.DataCase, async: true`

**Tests to write:**

```
describe "list_projects/1"
  - test "returns projects owned by user"
  - test "returns empty list when user has no projects"
  - test "does not return other users' projects"

describe "get_project!/1"
  - test "returns project by id"
  - test "raises for nonexistent id"

describe "get_project_by_slug/2"
  - test "returns project by user_id and slug"
  - test "returns nil when not found"

describe "create_project/1"
  - test "creates project with valid attrs"
  - test "returns error for missing name"

describe "update_project/2"
  - test "updates project name"
  - test "returns error for invalid data"

describe "delete_project/1"
  - test "deletes the project"

describe "change_project/2"
  - test "returns a changeset"

## API Tokens
describe "list_project_api_tokens/1"
  - test "lists tokens for project"
  - test "returns empty list when no tokens"

describe "create_project_api_token/2"
  - test "creates token and returns raw_token"
  - test "raw_token can be used to verify"

describe "verify_api_token/1"
  - test "returns {:ok, token} for valid token with preloaded project and user"
  - test "returns error for invalid token"

describe "delete_api_token/1"
  - test "deletes the token"
  - test "token can no longer verify after deletion"

## Invitations
describe "create_project_invitation/3"
  - test "creates invitation with hashed token"
  - test "returns url_token for the invitation link"
  - test "broadcasts :invitation :created via PubSub"

describe "get_invitation_by_token/1"
  - test "returns {:ok, invitation} for valid, unexpired, unaccepted token"
  - test "returns {:error, :not_found} for invalid token"
  - test "returns {:error, :not_found} for expired invitation"
  - test "returns {:error, :not_found} for already-accepted invitation"

describe "accept_invitation/2"
  - test "marks invitation as accepted and creates project member"
  - test "handles duplicate membership gracefully (on_conflict: :nothing)"
  - test "broadcasts :invitation :updated via PubSub"

describe "list_project_invitations/1"
  - test "lists invitations for project with invited_by preloaded"

## Members
describe "list_project_members/1"
  - test "lists members with user preloaded"
  - test "returns empty list when no members"

describe "user_can_view_project?/2"
  - test "returns true for project owner"
  - test "returns true for project member"
  - test "returns false for unrelated user"

describe "remove_project_member/2"
  - test "removes the member"
  - test "returns :ok even when member doesn't exist"

describe "list_viewable_projects/1"
  - test "includes owned projects with role 'owner'"
  - test "includes shared projects with role from membership"
  - test "deduplicates — owner takes precedence over member"
  - test "sorts by project name"

## Journey step management
describe "update_journey_steps/2"
  - test "replaces journey steps with new interaction_ids"
  - test "maintains position ordering"
  - test "handles empty interaction_ids (clears steps)"

## Bulk loading
describe "load_project_data/1"
  - test "loads project with all entity types and associations"
```

**PubSub testing:** Subscribe to the PubSub topic before calling the function, then assert_receive the broadcast message. Example:
```elixir
Ept.Screenplay.PubSub.subscribe(project.id)
{:ok, _url_token, _invitation} = Screenplay.create_project_invitation(project, user, "test@example.com")
assert_receive {:entity_change, :invitation, :created, _}
```

**Verify:** `mix test test/ept/screenplay_test.exs`

---

### Step 8: Test `Ept.Emails`

**Why:** Simple module (56 lines), easy win, and ensures invitation emails render correctly.

**File to create:** `apps/web/test/ept/emails_test.exs`

**Test module:** `Ept.EmailsTest`, using `ExUnit.Case, async: true` (pure function, no DB needed — but need fixtures, so actually use `Ept.DataCase, async: true`)

**Tests to write:**

```
describe "invitation_email/2"
  - test "sets correct recipient (invitation email)"
  - test "sets correct from address from config"
  - test "includes project name in subject"
  - test "includes accept URL with token in text body"
  - test "includes accept URL with token in HTML body"
  - test "includes inviter name in body when first_name is set"
  - test "includes inviter email in body when first_name is nil"
  - test "includes expiry information"
```

**Setup:** Create a user, project, and invitation fixture. Pass the invitation (with preloaded project and invited_by) and a fake url_token string to `Emails.invitation_email/2`. Assert on the Swoosh.Email struct fields.

**Verify:** `mix test test/ept/emails_test.exs`

---

### Step 9: Test `EptWeb.InvitationController`

**Why:** This is a small (31 lines) but security-relevant controller that handles the POST from InvitationLive's registration form.

**File to create:** `apps/web/test/ept_web/controllers/invitation_controller_test.exs`

**Test module:** `EptWeb.InvitationControllerTest`, using `EptWeb.ConnCase`

**Tests to write:**

```
describe "POST /invitations/:token/accept"
  - test "logs in user and redirects to project when credentials are valid"
  - test "redirects to login with error flash when credentials are invalid"
  - test "redirects to login when user email doesn't exist"
```

**Setup:** Create a user with `user_fixture()`, a project, an invitation. Build a conn (not logged in), POST to the accept path with valid/invalid user credentials. Assert on redirect location and flash messages.

**Note:** The token param in the path doesn't actually get validated in this controller (it's used for routing only). The controller validates via `get_user_by_email_and_password`.

**Verify:** `mix test test/ept_web/controllers/invitation_controller_test.exs`

---

### Step 10: Test `EptWeb.UserRegistrationLive`

**Why:** Registration is the entry point for new users. It's a relatively simple LiveView (105 lines) — good for establishing the LiveView testing pattern before tackling the complex ones.

**File to create:** `apps/web/test/ept_web/live/user_registration_live_test.exs`

**Test module:** `EptWeb.UserRegistrationLiveTest`, using `EptWeb.ConnCase, async: true`

**Import:** `import Phoenix.LiveViewTest`

**Tests to write:**

```
describe "mount" (unauthenticated user)
  - test "renders registration form"
  - test "shows email, first name, last name, and password fields"
  - test "shows link to login page"

describe "mount" (authenticated user)
  - test "redirects to / when already logged in" (use log_in_user helper from Step 1)

describe "validate event"
  - test "validates form on change (shows errors for invalid input)"
  - test "clears errors when input becomes valid"

describe "save event"
  - test "creates user account with valid data" (assert user exists in DB after)
  - test "shows validation errors with invalid data (short password)"
  - test "shows validation errors with duplicate email"
```

**Pattern:** Use `live(conn, ~p"/users/register")` to mount the LiveView. Use `render_change/2` for validation events and `render_submit/2` for save events. Assert on rendered HTML for error messages using `has_element?/2` or string matching.

**Verify:** `mix test test/ept_web/live/user_registration_live_test.exs`

---

### Step 11: Test `EptWeb.UserSettingsLive`

**Why:** Settings handles email change, password change, and profile updates — all security-sensitive operations.

**File to create:** `apps/web/test/ept_web/live/user_settings_live_test.exs`

**Test module:** `EptWeb.UserSettingsLiveTest`, using `EptWeb.ConnCase, async: true`

**Import:** `import Phoenix.LiveViewTest`

**Setup:** Every test needs an authenticated user. Use `setup :register_and_log_in_user` (from Step 1).

**Tests to write:**

```
describe "mount"
  - test "renders settings page with profile, email, and password sections"
  - test "redirects to login when not authenticated" (use bare build_conn())

describe "update profile"
  - test "updates first_name and last_name"
  - test "shows flash on success"
  - test "validates profile fields (too long)"

describe "update email"
  - test "updates email with valid current password"
  - test "shows error with invalid current password"
  - test "validates email format"

describe "update password"
  - test "updates password with valid current password"
  - test "shows error with invalid current password"
  - test "validates new password length"
  - test "shows flash on success"
```

**Verify:** `mix test test/ept_web/live/user_settings_live_test.exs`

---

### Step 12: Test `EptWeb.ProjectsLive`

**Why:** This is the main project management interface (675 lines, 16 event handlers). It handles CRUD, token management, invitation sending, and member management.

**File to create:** `apps/web/test/ept_web/live/projects_live_test.exs`

**Test module:** `EptWeb.ProjectsLiveTest`, using `EptWeb.ConnCase, async: true`

**Import:** `import Phoenix.LiveViewTest`

**Setup:** Use `setup :register_and_log_in_user`

**Tests to write:**

```
describe "mount"
  - test "renders projects list"
  - test "shows 'New Project' button"
  - test "shows owned projects"
  - test "shows shared projects (where user is member)"
  - test "redirects to login when not authenticated"

describe "project CRUD"
  - test "new_project event shows the create form"
  - test "cancel_form event hides the form"
  - test "save_project creates a new project"
  - test "save_project shows validation errors for blank name"
  - test "edit_project event shows edit form with existing data"
  - test "save_project updates an existing project"
  - test "delete_project removes the project"

describe "API token management"
  - test "show_token_form event shows token creation form"
  - test "hide_token_form event hides the form"
  - test "create_token creates a token and shows the download alert"
  - test "dismiss_token hides the token alert"
  - test "delete_token removes the token"

describe "invitation management"
  - test "show_invite_form event shows invitation form"
  - test "hide_invite_form event hides the form"
  - test "send_invitation sends email and shows flash"
  - test "send_invitation shows error for invalid email"

describe "member management"
  - test "remove_member removes a viewer from the project"
```

**Testing approach:** Mount the LiveView with `{:ok, view, _html} = live(conn, ~p"/projects")`. Use `render_click/2` for button events. For forms, use `render_submit/2` with the form data. For token creation, assert the flash message and download alert appear. For invitations, assert the `Swoosh.Adapters.Test` received the email.

**Verify:** `mix test test/ept_web/live/projects_live_test.exs`

---

### Step 13: Test `EptWeb.GraphLive` (Critical Paths Only)

**Why:** GraphLive is the largest module (1,537 lines) with complex state. Full coverage of all 14+ event handlers would be extensive. Focus on the critical paths: access control, mount, view switching, and entity selection.

**File to create:** `apps/web/test/ept_web/live/graph_live_test.exs`

**Test module:** `EptWeb.GraphLiveTest`, using `EptWeb.ConnCase, async: true`

**Import:** `import Phoenix.LiveViewTest`

**Tests to write:**

```
describe "mount — access control"
  - test "renders for project owner"
  - test "renders for project viewer (member)"
  - test "redirects with error for non-member user"
  - test "redirects with error for nonexistent project"
  - test "redirects to login when not authenticated"

describe "mount — initial state"
  - test "sets page title to project name"
  - test "assigns loading: true on initial render"
  - test "shows explore view by default"

describe "handle_params — view switching"
  - test "switches to items view when view=items param"
  - test "defaults to explore view for unknown view param"

describe "handle_event — view controls"
  - test "toggle_goals toggles goal visibility"
  - test "toggle_journeys toggles journey visibility"
  - test "switch_view changes between explore and items"

describe "handle_event — entity selection (items view)"
  - test "items_select_actor sets actor selection and patches URL"
  - test "items_select_goal sets goal selection and patches URL"
  - test "clear_selection resets selection state"

describe "handle_event — entity selection (explore view)"
  - test "select_actor sets selection and patches URL"
  - test "select_goal sets selection and patches URL"
  - test "select_interaction sets selection and patches URL"
  - test "select_journey sets selection and patches URL"
  - test "go_back navigates to parent context"
```

**Setup for each describe block:**
- Owner tests: Use `setup :register_and_log_in_user`, create project owned by user.
- Viewer tests: Create a different project owner, add the logged-in user as member via `Ept.Screenplay.accept_invitation/2` or direct `ProjectMember` insertion.
- Non-member tests: Create project owned by another user, try to access as logged-in user.

**Data setup for selection tests:** Create actors, goals, interactions, journeys in the project before mounting. After mount, send a `:load_data` message (which the LiveView sends to itself on connected mount) and wait for it to process.

**Note:** The D3 graph visualization is JavaScript-side and won't be tested here. Focus on server-side state management, access control, and URL parameter handling.

**Verify:** `mix test test/ept_web/live/graph_live_test.exs`

---

### Step 14: Test `EptWeb.InvitationLive`

**Why:** Handles three states: invalid token, logged-in auto-accept, and registration. Completes the invitation flow coverage.

**File to create:** `apps/web/test/ept_web/live/invitation_live_test.exs`

**Test module:** `EptWeb.InvitationLiveTest`, using `EptWeb.ConnCase, async: true`

**Import:** `import Phoenix.LiveViewTest`

**Tests to write:**

```
describe "mount — invalid token"
  - test "renders error message for invalid token"
  - test "renders error message for expired invitation"
  - test "shows link to login page"

describe "mount — logged in user"
  - test "auto-accepts invitation and redirects to project"
  - test "shows flash with project name"
  - test "redirects to /projects with error if acceptance fails"

describe "mount — not logged in, valid token"
  - test "shows choose mode with login and register options"
  - test "shows project name in invitation message"

describe "choose_register event"
  - test "switches to registration form"

describe "choose_back event"
  - test "returns to choose mode from register mode"

describe "validate_register event"
  - test "validates registration form on change"

describe "register_and_accept event"
  - test "creates user, accepts invitation, triggers form submission"
  - test "shows errors for invalid registration data"
```

**Setup:**
- Invalid token: Use `live(conn, ~p"/invitations/bogus-token")`
- Logged-in: Use `log_in_user` helper, create invitation for the logged-in user's email
- Not logged-in: Use bare `build_conn()`, create invitation, navigate to invitation URL with the raw token

**Verify:** `mix test test/ept_web/live/invitation_live_test.exs`

---

### Step 15: Ratchet Coverage Threshold and Verify

**Why:** The current implicit 90% threshold is aspirational and ignored. After completing Steps 1-14, set a realistic threshold that matches actual coverage and can be enforced in CI.

**Actions:**

1. Run `mix test --cover` from `apps/web/` and record the actual coverage percentage.
2. Add a `test_coverage` configuration to `apps/web/mix.exs` in the `project/0` function:
   ```elixir
   test_coverage: [threshold: <actual_percentage_minus_2>]
   ```
   This sets the threshold just below the achieved coverage so it passes now but catches regressions.
3. Run `mix test --cover` again to confirm it passes the threshold.
4. Run `mix credo --strict` and fix any warnings.
5. Run `mix format` to ensure consistent formatting.

**Expected coverage after all steps:** Based on the module sizes and test coverage:
- Accounts (253 lines): 0% → ~95% = ~240 lines covered
- UserToken (176 lines): 0% → ~90% = ~158 lines covered
- UserAuth (177 lines): 26% → ~85% = ~150 lines covered
- Screenplay (788 lines): 66% → ~85% = ~670 lines covered
- Emails (56 lines): 0% → ~95% = ~53 lines covered
- ApiAuth plug (45 lines): 0% → ~95% = ~43 lines covered
- GraphLive (1,537 lines): 0% → ~40% = ~615 lines (critical paths only)
- ProjectsLive (675 lines): 0% → ~70% = ~473 lines
- InvitationLive (230 lines): 0% → ~80% = ~184 lines
- UserRegistrationLive (105 lines): 0% → ~85% = ~89 lines
- UserSettingsLive (247 lines): 0% → ~75% = ~185 lines
- InvitationController (31 lines): 0% → ~95% = ~29 lines

**Projected total coverage:** ~65-70%, up from 31.58%. Set threshold at 60%.

**Verify:** `mix test --cover` passes the threshold. All 134+ existing tests plus new tests pass.

---

### Execution Notes

**Ordering:** Steps are designed to be executed in sequence. Steps 1 must come first (test infrastructure). Steps 2-5 (security foundation) should come next. Steps 6-8 (business logic) are independent of each other. Steps 9-14 (LiveViews and controllers) depend on the test helpers from Step 1 and the context tests establishing patterns.

**Delegation:** Each step should be delegated to the appropriate craftsperson sub-agent (`elixir-phoenix-craftsperson` for LiveView tests, `elixir-craftsperson` for context and plug tests). Each step produces a independently committable increment.

**Commit strategy:** One commit per step. Each commit message follows the pattern: `Add <module> tests — <coverage area>`. For example: `Add Ept.Accounts tests — user registration, sessions, password reset`.

**Quality gates per step:**
1. `mix test` — all tests pass
2. `mix format` — code is formatted
3. `mix credo --strict` — zero warnings
4. `mix test --cover` — verify coverage is increasing
