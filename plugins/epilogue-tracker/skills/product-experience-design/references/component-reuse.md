# Borrowing the customer catalogue

The source library is the stock customer system's executable catalogue, currently
in `system-template` beside Bedrock and Roost in the umbrella workspace. Its role
is reusable capability and presentation, not a runtime dependency of management.

Inspect these source paths when the checkout is available:

| Source relative to system-template | Use |
| --- | --- |
| `CATALOGUE.md` | Behaviour and accessibility contracts |
| `lib/shop_web/components/workbench.ex` | Reusable presentation controls and patterns |
| `lib/shop_web/components/core_components.ex` | Native form and control conventions |
| `lib/shop/catalogue/components.ex` | Component dependencies and usage |
| `lib/shop/catalogue/domain.ex`, `model.ex` | Domain bindings and conceptual relationships |
| `lib/shop_web/live/catalogue/` | Working examples and compositions |
| `assets/css/workbench.css` | Semantic roles, density, focus and layout conventions |
| `priv/catalogue/` | Versioned domain and composition declarations |
| `test/shop_web/live/catalogue_live_test.exs` | Behavioural examples and semantics |

Use the repository map if the checkout is elsewhere. When it is absent, use a
verified source checkout or supplied artifact if available. Continue target-product
analysis, but report library reuse as unverified until its source is inspected.
A screenshot or this skill's descriptions are not a substitute for the code.

## Reuse choices

Start with the receiving product's existing components. Compare their contracts
with the catalogue before deciding to retain, adapt or replace them. Reuse suitable
pure presentation code under the local namespace, along with relevant behaviour
and accessibility checks. Record the source commit and adaptations in the local
component documentation. Preserve source attribution and applicable licensing.

Map semantic roles rather than pasting global CSS. For example, a selected row,
muted supporting text, warning, danger action and focus ring each need a local
token. Preserve each product's brand and task layout. Check contrast after mapping;
the catalogue's colours are not a guarantee for a different palette.

Keep business contexts, permissions, queries and fixtures out of presentation
components. Porting a table does not port inventory semantics or Shop's data.
Do not import Shop modules into either product, or Bedrock modules into Roost.
Never edit Bedrock's vendored Roost copy.

If repeated use justifies a shared dependency, propose a separately versioned,
platform-neutral presentation package with an ADR and explicit contracts. Do not
add a package or extraction project incidentally to a UI task. A documented local
adaptation is an acceptable starting point and remains independently releasable.

## Starter compositions

- **Table + inspector:** compare records while retaining selected context.
- **Record + inspector:** complete a bounded action beside its consequences.
- **Task + evidence:** act while seeing the facts and completion conditions.
- **Schedule + agenda:** manage time windows with conflicts and zone meaning.
- **History + filters:** inspect dated facts, corrections and freshness.
- **Public enquiry + staff follow-up:** demonstrate a handoff across authority.

Choose from the task, not the number of fields in an entity. Add a pattern when
existing ones cannot express the work, and state the missing responsibility.

## Useful component conventions

Tables have semantic captions and headings, accurate `aria-sort`, stable row
identity and named keyboard selection controls. Whole-row pointer selection must
not swallow nested actions. Search and pagination operate over the declared data
scope; preserve selected context when it leaves the current result page.

Controls align in height, spacing and focus treatment. Icons support named actions;
icon-only controls still need accessible names. Status uses words as well as
colour. Forms retain invalid input, associate errors and focus a useful recovery
target. Inspector content follows a logical reading order at narrow widths.
