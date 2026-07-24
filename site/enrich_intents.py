#!/usr/bin/env python3
"""Classify ecosystem intent records and connect them to generalized intents.

The source records predate the graph schema. This deterministic editorial pass
adds a category, topical tags, and a `specializes` relationship while preserving
all substantive record content and code examples.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTENTS = ROOT / "intents"
CENTRAL = INTENTS / "craftsperson"

# Ordered from narrowest to broadest. The first matching rule supplies the
# generalized intent. Exact slug matches are handled before these rules.
PARENT_RULES: list[tuple[str, str]] = [
    (r"\b(logicless|logic-free).*\bgateway|\bgateway.*\b(logicless|logic-free)", "do-not-unit-test-logicless-gateways"),
    (r"\b(mock|mocking|test double|test-double|fake).*\b(gateway|boundary|interface)|\bowned boundaries\b", "mock-only-owned-boundaries"),
    (r"\b(red.green|tdd|test.driven|green steps|green baseline)\b", "develop-behavior-red-green-refactor"),
    (r"\b(coverage|simplecov|llvm.cov|critical business paths)\b", "use-coverage-as-a-risk-signal"),
    (r"\b(edge cases?|edge and error|error paths?|failure paths?|property tests?|critical flows?|algorithmic invariants?)\b", "cover-edge-cases-and-failure-paths"),
    (r"\b(test layer|test pyramid|integration test|end.to.end|capybara|ui test|instrumented test)\b", "use-purpose-specific-test-layers"),
    (r"\b(readable test|test specification|specs with|test names|organize tests|co.locate specs)\b", "make-tests-readable-specifications"),
    (r"\b(test behavior|test observable|public behavior|behavior not implementation|specify every)\b", "test-observable-behavior"),
    (r"\b(passing test|test suite|green rspec|green ci|prioritize.*tests|gate on.*tests)\b", "require-passing-tests-before-completion"),
    (r"\b(format|formatter|gofmt|rustfmt|ktlint|swiftformat|prettier)\b", "require-canonical-formatting"),
    (r"\b(lint|warnings?|static analy|compiler.aware diagnostics|compiler warnings|typecheck|clippy|credo|ruff|rubocop|detekt|clj.kondo|eastwood|dialyzer|spotbugs|nullaway|threadsanitizer|sanitizer|miri)\b", "resolve-static-analysis-findings"),
    (r"\b(quality gate|quality toolchain|mandatory gate|ci before|ci for pull|remediate quality)\b", "honor-the-project-quality-gate"),
    (r"\b(self.review|verification|verify|report verification)\b", "verify-before-declaring-completion"),
    (r"\b(public api.*doc|document public|public function doc|doxygen|yard|docfx|rustdoc|generated api doc)\b", "document-public-contracts"),
    (r"\b(comment|rationale in|why not what)\b", "use-comments-to-preserve-rationale"),
    (r"\b(document|documentation|readme|doc example)\b", "keep-documentation-aligned"),
    (r"\b(vulnerab|security review gate|security analysis|cargo audit|cargo deny|bundler.audit|dependency risk|gem audit)\b", "audit-dependency-risk"),
    (r"\b(lockfile|lock file|pin.*depend|dependency version|workspace depend|reproducible depend)\b", "make-dependency-resolution-reproducible"),
    (r"\b(minimize.*depend|dependency surface|production dependencies|select maintained|dependency lifecycle|staleness)\b", "minimize-dependency-surface"),
    (r"\b(review.*psychological|psychological safety|review with humility|acknowledge good|reinforce exemplary)\b", "review-with-psychological-safety"),
    (r"\b(actionable.*review|review.*actionable|review feedback|technical debt actionable|connect feedback)\b", "make-review-feedback-actionable"),
    (r"\b(clarify|ambiguous requirement|ambiguous business|assess problem intent)\b", "clarify-ambiguous-intent-before-implementation"),
    (r"\b(escalat|negotiate.*exception|high.impact conflict|uncertain.*decision|tradeoff)\b", "escalate-consequential-tradeoffs"),
    (r"\b(gateway.*external|external.*gateway|isolate external interaction|gateway protocol)\b", "put-gateways-at-external-boundaries"),
    (r"\b(keep gateways? logic|logic.free gateway|logicless gateway adapter)\b", "keep-gateways-logic-free"),
    (r"\b(functional core|imperative shell|side.effect boundar|domain core pure|confine side effects)\b", "isolate-functional-core-from-effects"),
    (r"\b(authentication|authorization|csrf|xss|secret|unsafe decod|untrusted data|security control|strong parameter)\b", "enforce-security-at-trust-boundaries"),
    (r"\b(validate.*boundary|validation at|trust boundary|untrusted input)\b", "validate-untrusted-input-at-boundaries"),
    (r"\b(transaction|database|persist|query|n\\+1|data integrity|upsert|multi.step write|migration safety|uniqueness)\b", "protect-persistent-data-integrity"),
    (r"\b(resource lifetime|resource cleanup|ownership|owned resource|context manager|raii|close|dispos|qobject lifetime)\b", "manage-resource-lifetimes-explicitly"),
    (r"\b(backpressure|bound.*concurr|bounded.*parallel|bounded memory|large data|stream large|concurrent enumeration|queue bound|restart loop|overprocessing)\b", "bound-concurrent-work"),
    (r"\b(async|asynchronous|coroutine|goroutine|concurr|thread|task|supervis|genserver|actor|process resource|lifecycle|cancellation|signal delivery|subprocess lifetime)\b", "structure-concurrent-lifetimes"),
    (r"\b(error context|exception context|source chain|causal chain|aggregate errors)\b", "preserve-error-context"),
    (r"\b(recoverable (error|failure)|domain error|returned errors?|expected failures?|result type|exceptional failure|throws? for|bang function|catch.*exceptions?|filesystem failure|http failure|exit status)\b", "model-recoverable-errors-explicitly"),
    (r"\b(invalid.*state|state validity|absence|absent values?|optional|variant|sealed|enum|data model|identifiers? at compile time|type.safe|unknown (values?|inputs?)|narrow unknown|explicit.*contract|contract.*explicit|value semantics)\b", "make-invalid-states-explicit"),
    (r"\b(benchmark|profil|measure before|performance sensitive|optimization)\b", "optimize-from-measurement"),
    (r"\b(branch|commit|version control change|main.based|pull requests? focused|reviewable)\b", "write-descriptive-commit-messages"),
    (r"\b(small.*increment|single.reason increment|independently shippable|focused change|change review focused)\b", "deliver-small-independent-increments"),
    (r"\b(build config|build surface|cmake|gradle|package distribution|release runtime|app entrypoint|build target)\b", "make-build-configuration-explicit"),
    (r"\b(uv|uvx|cargo|mix (project|task|release|deps)|swiftpm|bun|npm|pnpm|leiningen|deps.edn|project tool|toolchain)\b", "standardize-project-tooling"),
    (r"\b(baseline|compatib|target framework|deployment target|language edition|runtime version|pin.*runtime|pin.*otp|cpp standard)\b", "preserve-supported-platform-baselines"),
    (r"\b(refactor|behavior preservation)\b", "preserve-behavior-during-refactoring"),
    (r"\b(composition over|compose over|inheritance)\b", "prefer-composition-over-inheritance"),
    (r"\b(single source|knowledge duplication|eliminate.*duplication|centralize.*decision)\b", "single-source-each-decision"),
    (r"\b(cohes|focused|single responsibility|one coherent|module files navigable|namespace purpose|structural entit)\b", "keep-code-units-cohesive"),
    (r"\b(delay abstraction|meaningful abstraction|premature abstraction|functions before macros)\b", "delay-abstraction-until-evidence"),
    (r"\b(speculative|yagni)\b", "avoid-speculative-capability"),
    (r"\b(simple design|simplest sufficient|minimize design entit)\b", "apply-simple-design-priorities"),
    (r"\b(readab|explicit.*clever|intention.revealing|human reader)\b", "optimize-code-for-human-readers"),
    (r"\b(idiom|native strengths?|language strengths?|modern (python|csharp|c\\+\\+|kotlin|swift|typescript|ruby|go|elixir)|current .* practices)\b", "use-language-and-ecosystem-idioms"),
    (r"\b(immutable|value semantics|const.correct|declarative|pattern matching|comprehension|enumerable|iteration|data structures?|record shapes?|closure bindings?|predicates?|guards?|result contracts?)\b", "use-language-and-ecosystem-idioms"),
    (r"\b(interface.*contract|protocol|trait|generic abstraction)\b", "prefer-composition-over-inheritance"),
    (r"\b(macro|metaprogram|reflection|template|dangerous cast|implicit conversion)\b", "delay-abstraction-until-evidence"),
]

TOOL_PATTERNS: list[tuple[str, str]] = [
    (r"\buvx?\b", "uv"),
    (r"\bruff\b", "ruff"),
    (r"\bpytest\b", "pytest"),
    (r"\bpydantic\b", "pydantic"),
    (r"\bcargo\b", "cargo"),
    (r"\bclippy\b", "clippy"),
    (r"\brustfmt\b", "rustfmt"),
    (r"\bcriterion\b", "criterion"),
    (r"\bcredo\b", "credo"),
    (r"\bdialyzer\b", "dialyzer"),
    (r"\bmix\b", "mix"),
    (r"\bphoenix\b|\bliveview\b", "phoenix"),
    (r"\becto\b", "ecto"),
    (r"\brspec\b", "rspec"),
    (r"\brubocop\b", "rubocop"),
    (r"\bcapybara\b", "capybara"),
    (r"\bsimplecov\b", "simplecov"),
    (r"\bgradle\b", "gradle"),
    (r"\bdetekt\b", "detekt"),
    (r"\bktlint\b", "ktlint"),
    (r"\bdocfx\b", "docfx"),
    (r"\bcmake\b", "cmake"),
    (r"\bqt\b|\bqobject\b|\bqthread\b", "qt"),
    (r"\bgolangci\b", "golangci-lint"),
    (r"\bclj.kondo\b", "clj-kondo"),
    (r"\bkaocha\b", "kaocha"),
    (r"\bleiningen\b", "leiningen"),
    (r"\bbun\b", "bun"),
    (r"\btypescript\b", "typescript"),
    (r"\bswiftlint\b", "swiftlint"),
    (r"\bswiftformat\b", "swiftformat"),
]

TOPIC_PATTERNS: list[tuple[str, str]] = [
    (r"\basync|concurr|thread|task|process|actor|supervis", "concurrency"),
    (r"\bsecurity|csrf|xss|auth|vulnerab|secret", "security"),
    (r"\btest|spec|coverage|mock", "testing"),
    (r"\bdoc|comment|readme", "documentation"),
    (r"\bdepend|package|gem|module", "dependencies"),
    (r"\bformat", "formatting"),
    (r"\blint|warning|static analy", "static-analysis"),
    (r"\bperformance|benchmark|profil|allocation|cache", "performance"),
    (r"\bdatabase|transaction|query|ecto|migration", "persistence"),
    (r"\berror|exception|failure", "error-handling"),
    (r"\bbuild|release|deploy|ci\b", "build-and-delivery"),
]


def collection_tag(collection: str) -> list[str]:
    return [part for part in collection.removesuffix("-craftsperson").split("-") if part]


def central_metadata() -> tuple[dict[str, str], dict[str, list[str]]]:
    categories: dict[str, str] = {}
    tags: dict[str, list[str]] = {}
    for path in CENTRAL.glob("*.toml"):
        with path.open("rb") as handle:
            record = tomllib.load(handle)
        categories[path.stem] = record["category"]
        tags[path.stem] = record.get("tags", [])
    return categories, tags


def choose_parent(slug: str, title: str, context: str, parents: set[str]) -> str:
    if slug in parents:
        return slug
    # Prefer the record's own label. Broader claim text is useful when labels
    # use ecosystem vocabulary, but it often mentions secondary concerns too.
    for text in (title, context):
        for pattern, parent in PARENT_RULES:
            if re.search(pattern, text):
                return parent
    return "use-language-and-ecosystem-idioms"


def classify(path: Path, categories: dict[str, str], parent_tags: dict[str, list[str]]) -> tuple[str, list[str], str]:
    with path.open("rb") as handle:
        record = tomllib.load(handle)
    # Include the behavioral claim, not only its label. Ecosystems often name
    # the same elemental practice very differently (for example "join child
    # jobs" versus "structure task lifetimes").
    title = f"{path.stem} {record['title']}".lower().replace("-", " ")
    context = " ".join(
        str(record.get(field, ""))
        for field in ("title", "capability", "threat", "strategy")
    ).lower().replace("-", " ")
    parent = choose_parent(path.stem, title, context, set(categories))
    tags = collection_tag(path.parent.name)
    for pattern, tag in TOOL_PATTERNS:
        if re.search(pattern, title) and tag not in tags:
            tags.append(tag)
    for pattern, tag in TOPIC_PATTERNS:
        if re.search(pattern, context) and tag not in tags:
            tags.append(tag)
    for tag in parent_tags[parent]:
        if tag not in tags and len(tags) < 6:
            tags.append(tag)
    return categories[parent], tags, parent


def render_block(category: str, tags: list[str], parent: str) -> str:
    rendered_tags = ", ".join(f'"{tag}"' for tag in tags)
    return (
        f'category = "{category}"\n'
        f"tags = [{rendered_tags}]\n"
        "relations = [\n"
        f'  {{ type = "specializes", target = "craftsperson/{parent}" }},\n'
        "]\n"
    )


def enrich(path: Path, block: str, check: bool) -> bool:
    original = path.read_text()
    title_match = re.search(r"(?m)^title = .+$", original)
    status_match = re.search(r"(?m)^status = ", original)
    if not title_match or not status_match or title_match.end() > status_match.start():
        raise ValueError(f"unexpected record header in {path}")

    prefix = original[: title_match.end()] + "\n"
    header_tail = original[title_match.end() + 1 : status_match.start()]
    # Classification is the only supported content between title and status.
    if header_tail.strip() and not header_tail.lstrip().startswith(("category =", "tags =", "relations =")):
        raise ValueError(f"unrecognized content between title and status in {path}")
    updated = prefix + block + original[status_match.start() :]
    if updated == original:
        return False
    if not check:
        path.write_text(updated)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report whether enrichment would change files")
    args = parser.parse_args()
    categories, parent_tags = central_metadata()
    changed = 0
    for collection in sorted(INTENTS.glob("*-craftsperson")):
        for path in sorted(collection.glob("*.toml")):
            category, tags, parent = classify(path, categories, parent_tags)
            changed += enrich(path, render_block(category, tags, parent), args.check)
    mode = "would update" if args.check else "updated"
    print(f"{mode} {changed} intent records")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
