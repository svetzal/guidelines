# Contract testing across repositories

Both sides of a changed boundary must verify the same identifiable, versioned
executable contract set. This rule applies to APIs, messages and shared file
formats. Reuse the project's existing contract mechanism.

Consumer tests express required requests, responses and behavior.
Provider verification checks the implementation against those contracts.
Include relevant errors, optional fields and supported old and new versions.
Derive test doubles from the verified contracts.
Independent mocks or matching schemas alone do not prove compatible behavior.

Run verification in each repository's required gates.
Record the contract version or hash, tested commits and results for both sides.
If a side has no verification evidence, record the missing work.
Keep changes within the repositories authorized for the task.

A boundary conformance check remains useful when a gateway wrapper has no logic.
The guidance against unit tests of logicless wrappers does not remove this check.
Integration checks test wiring and the user's full journey.
Contract verification proves compatibility only for the cases and versions it covers.

Each craftsperson agent contains this rule so its installed file remains portable.
Foundry initiatives repeat a short reminder during coordination and member work.
