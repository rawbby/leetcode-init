# leetcode-init

Scaffolds a minimal C++20 LeetCode challenge repo: header-only problem, ctest runner
with input/output pairs baked in as raw-string macros, clang presets (ASan/UBSan debug,
fast release), clang-format/clang-tidy targets, pre-push hook, and a lean GitHub Actions CI.

## Install

```sh
pip install git+https://github.com/<you>/leetcode-init
```

## Use

```sh
leetcode-init [directory]
```

Answer the prompts (problem name, project name, author, optional GitHub repo creation —
token from `GITHUB_TOKEN`/`GH_TOKEN` or entered interactively, skippable).

Non-interactive when all values are given as flags:

```sh
leetcode-init two_sum --problem two_sum --project two_sum --author "Jane Doe" --no-github
leetcode-init two_sum --problem two_sum --project two_sum --author "Jane Doe" --github --public  # needs GITHUB_TOKEN/GH_TOKEN
```

## Test

```sh
python -m unittest discover tests   # generates a project, builds it, runs its ctest suite
```

## Generated workflow

- Implement `solve()` in `include/<problem>.hpp`.
- Add `test/<case>.in` + `test/<case>.out` pairs (or `test/local/` for CI-skipped cases).
- `cmake --preset debug && cmake --build --preset debug -j && ctest --preset debug`
- `python3 hook.py` installs a pre-push hook enforcing clang-format/clang-tidy.
