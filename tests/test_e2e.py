import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd=None, env=None):
    subprocess.run(args, cwd=cwd, env=env, check=True)


class EndToEndTest(unittest.TestCase):
    def test_generate_build_and_run_tests(self):
        env = {
            **os.environ,
            "PYTHONPATH": str(ROOT / "src"),
            "GIT_AUTHOR_NAME": "ci",
            "GIT_AUTHOR_EMAIL": "ci@local",
            "GIT_COMMITTER_NAME": "ci",
            "GIT_COMMITTER_EMAIL": "ci@local",
        }
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "two_sum"
            run(
                sys.executable, "-m", "leetcode_init.main", str(dest),
                "--problem", "two_sum", "--project", "two_sum",
                "--author", "ci", "--no-github",
                env=env,
            )
            self.assertTrue((dest / ".git").is_dir())
            self.assertTrue((dest / ".git" / "hooks" / "pre-push").is_file())
            self.assertTrue((dest / "include" / "two_sum.hpp").is_file())
            self.assertTrue((dest / ".gitignore").is_file())
            run("cmake", "--preset", "debug", cwd=dest)
            run("cmake", "--build", "--preset", "debug", "-j", cwd=dest)
            run("ctest", "--preset", "debug", cwd=dest)


if __name__ == "__main__":
    unittest.main()
