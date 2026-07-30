# {{project}}

C++20 LeetCode challenge: `{{problem}}`.

## Layout

- `include/{{problem}}.hpp` — implement `solve()` reading `std::cin`, writing `std::cout` (rebound to fast in-memory streams by the runner; output is compared byte for byte, no trimming).
- `test/*.in` / `test/*.out` — input/output pairs, baked into one ctest binary each.
- `test/local/` — extra pairs that run locally only (skipped in CI).

## Build & test

```sh
cmake --preset debug          # clang, ASan+UBSan, max diagnostics
cmake --build --preset debug -j
ctest --preset debug

cmake --preset release        # clang, -O3 -march=native -flto
cmake --build --preset release -j
ctest --preset release
```

## Lint

```sh
cmake --build --preset debug --target format-check  # clang-format-20, report only
cmake --build --preset debug --target tidy-check    # clang-tidy-20, report only
```

## Hooks

```sh
python3 hook.py   # installs pre-push hook: format-check + tidy-check must pass
```
