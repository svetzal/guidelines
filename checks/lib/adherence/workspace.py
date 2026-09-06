"""A finished workspace, partitioned into the modules the checks read."""

from .predicates import collect, collect_rust


class Workspace:
    """A finished workspace, partitioned into production and test modules.

    The partition is per module for Python and per module *and item* for Rust,
    where `#[cfg(test)]` puts unit tests inside the file they exercise. Rust
    checks therefore work from `modules` and ask each item about its own scope,
    rather than trusting a directory split that does not exist there.
    """

    def __init__(self, root, language="python", rustfacts=None):
        self.root = root
        self.language = language
        if language == "rust":
            self.modules = collect_rust(root, rustfacts)
            self.production = [module for module in self.modules if module.is_source]
            self.tests = [module for module in self.modules if module.is_test]
        else:
            self.modules = collect(root)
            self.production = [module for module in self.modules if not module.is_test]
            self.tests = [module for module in self.modules if module.is_test]

    def inventory(self):
        return {
            "parse_errors": [module.parse_error for module in self.modules if module.parse_error],
            "production_modules": sorted(module.relative for module in self.production),
            "test_modules": sorted(module.relative for module in self.tests),
        }
