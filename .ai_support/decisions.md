# decisions.md

## 2026-01-10
Fixed PyCharm type inference warning in nested_submodules().
Cause: incorrect assert on subm.path.
Decision: assert on subm instead, cast subm.path to str.
