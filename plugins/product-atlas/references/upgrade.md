# Upgrade an existing project

Version 2 uses topic-based intent, unresolved questions only, `history/`, and
`documentation/`. The command is now `/product-atlas:generate-documentation`.
These steps apply only to projects created with version 1.

1. Read the old settings and all registry records before changing them.
2. Record the old paths and preserve a recoverable snapshot of the project data.
3. Change `schema_version` to `2`.
4. Rename the `generation` setting to `history` and the `wiki` setting to `documentation`.
5. Move those directories to the new names when their destination paths are free.
6. Run preflight against the updated settings.
7. Group existing intent statements into topic files using the registry rules.
8. Transform saved question answers into the appropriate intent sections.
9. Record old IDs and their new topic locations in `history/changes/`.
10. Repair references and delete answered or superseded question files.
11. Keep unresolved questions and give them the version 2 fields.
12. Review current sources for differences that version 1 left outside the queue.
13. Regenerate the documentation with the new command.

Check path containment before moving directories. Never overwrite a populated
destination. Keep explicit external locations unless the user requests a move.
You can rename a setting key without changing its custom path value. Record that
choice so later runs use the same location.

An old intent record is source material for curation, not a reason to keep one
file per statement. Preserve its meaning, scope, attribution, and evidence.
After saving the topic and history, remove the replaced record. Retain only
current intent in `intent/` and unresolved questions in `questions/`.

Known differences still need alignment questions, even when version 1 marked
the policy question answered. Missing evidence also needs a question. Do not
report alignment merely because migration removed all answered records.

Keep the previous generated output until replacement succeeds. Do not treat
old generated pages or the migration snapshot as evidence. If a step fails,
retain the data needed to resume or restore it and report the incomplete upgrade.
