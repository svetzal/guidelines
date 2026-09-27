# Product contexts

These are source-navigation hints verified when skill version 1.0.0 was written.
Read current code, charter and et records; do not treat these hints as release
status. Each repository and skill installation must remain usable independently.

## Bedrock

Read `CHARTER.md`, `docs/README.md`,
`docs/customer-business-intent.md` and
`docs/design-system/agent-guide.md` for work affecting the modelling language.
The application is under `apps/bedrock`. Existing presentation lives in
`lib/bedrock_web/components/` and `lib/bedrock_web/live/` beneath that application;
its theme and layout sources include `assets/css/app.css` and `assets/css/site.css`.
Preserve Bedrock's own tokens and public/account/workshop distinctions.

Run et at the Bedrock root. A known discovery example is
`field_service_owner` → `own_business_system` → `explore_before_adopting`.
Look it up before use. Keep Bedrock's actual product model separate from the
portable models it constructs for customers.

The owner wants to describe work, try a change and understand what was built.
Compose conversation, bounded intent, working preview and evidence without
repeating the whole specification in chat. Keep proposed, agreed, queued,
verified, accepted and published states distinct. An owner confirmation, successful
test or preview does not silently authorize publication.

Owner-facing language should reflect their business expertise. Infrastructure
and implementation details belong where they explain a choice or failure, not
in every routine action. Retain tenant scope, passwordless access and existing
construction/adoption boundaries. Run `mix precommit` inside `apps/bedrock` for
implementation changes.

## Roost

Read `CHARTER.md`, `docs/product.md`, `docs/contract-v1.md` and the relevant operator
runbook. Domain code is `lib/hosting`; console source is `lib/hosting_web`, including
`console_html.ex`, `environment_html.ex` and `beam_html.ex`. Current presentation
uses `priv/static/console.css`, with ink, muted, paper, line, green and lime roles.
Start from those roles and Roost's layout; inspect them before proposing changes.
Do not assume LiveView or Bedrock's Tailwind build is present on a console page.

Run et from the Roost root with its own configuration. Known customer Goals are
`bring_my_app_online` and `keep_my_app_available`; these are lookup hints, not
permission to invent a customer portal. Inspect all states: default listings can
hide already-created records. A verified
operator trace is `administrator` → `operate_customer_services_safely` →
`inspect_customer_inventory`, `recognize_service_trouble`,
`restore_customer_service` and `trace_hosting_actions`. Re-read these before use.
At skill creation neither product had recorded Journeys; Roost's et charter was
empty while its local charter was populated. Report remaining gaps precisely.
Do not route operator work through Bedrock's tracker or substitute the Customer
actor for the Administrator merely because a default listing omits it.

An operator needs system identity, placement, shared dependencies, dated health,
operation progress and uncertainty in one coherent workspace. Technical identifiers
can be decision-critical here. Group them and reveal deeper evidence progressively;
do not hide necessary source SHAs, observation times or recovery context as clutter.

Keep reseller, tenant and system identities distinct. Distinguish observed systems
from managed systems; inventory does not grant restart or deployment authority.
Accepted operation intent, execution, verification and uncertain outcomes are
separate states. Never turn a stale observation into a green success badge or add
a command merely because a generic inspector has an action slot.

Keep `Hosting` and OTP `:hosting`, scoped client identity, Canadian residency,
durable commands and recovery safeguards. Work in Roost's authoritative repository,
not Bedrock's `vendor/roost`. Run root `mix precommit` for implementation changes
and relevant host tests when changing operational code.
