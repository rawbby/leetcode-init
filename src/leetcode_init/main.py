import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from getpass import getpass
from importlib import resources
from pathlib import Path

SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")


def run(*args, cwd=None, capture=False):
    return subprocess.run(
        args, cwd=cwd, check=True, text=True, capture_output=capture)


def git_config(key):
    out = subprocess.run(
        ["git", "config", "--get", key],
        capture_output=True, text=True)
    return out.stdout.strip()


def ask(prompt, default="", given=None):
    if given is not None:
        value = given.strip()
    else:
        suffix = f" [{default}]" if default else ""
        value = input(f"{prompt}{suffix}: ").strip() or default
    if not value:
        sys.exit(f"error: {prompt} is required")
    return value


def ask_snake(prompt, default="", given=None):
    value = ask(prompt, default, given)
    if not SNAKE.match(value):
        sys.exit(f"error: '{value}' is not snake_case")
    return value


def render_tree(node, dest, subs):
    for child in node.iterdir():
        name = child.name
        if name == "__pycache__" or name.endswith(".pyc"):
            continue
        if name.startswith("_"):
            name = "." + name[1:]
        elif name == "problem.hpp":
            name = f"{subs['problem']}.hpp"
        target = dest / name
        if child.is_dir():
            target.mkdir()
            render_tree(child, target, subs)
        else:
            text = child.read_text(encoding="utf-8")
            for key, value in subs.items():
                text = text.replace("{{" + key + "}}", value)
            target.write_text(text, encoding="utf-8")


def init_git(dest, project):
    run("git", "init", "-q", "-b", "main", cwd=dest)
    run(sys.executable, "hook.py", cwd=dest)
    run("git", "add", "-A", cwd=dest)
    run("git", "commit", "-q", "-m", f"init: {project}", cwd=dest)


def undo(dest, created_dir, repo):
    if repo is not None:
        try:
            repo.delete()
        except Exception as e:
            print(f"warning: undo failed, delete https://github.com/{repo.full_name} manually: {e}", file=sys.stderr)
    try:
        if created_dir:
            shutil.rmtree(dest)
        elif dest.exists():
            for child in dest.iterdir():
                shutil.rmtree(child) if child.is_dir() else child.unlink()
    except Exception as e:
        print(f"warning: undo failed, remove {dest} manually: {e}", file=sys.stderr)


def create_github_repo(dest, project, github, private, state):
    interactive = github is None
    if interactive:
        github = ask("Create GitHub repository? (y/n)", "y").lower() == "y"
    if not github:
        return
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token and interactive:
        token = getpass("GitHub token (empty to skip): ").strip()
    if not token:
        if interactive:
            print("skipped GitHub repository creation")
            return
        sys.exit("error: --github requires GITHUB_TOKEN or GH_TOKEN")
    from github import Auth, Github

    gh = Github(auth=Auth.Token(token))
    user = gh.get_user()
    if private is None:
        private = ask("Private repository? (y/n)", "n").lower() == "y" if interactive else False
    repo = user.create_repo(f"leetcode_{project}", private=private, description=f"LeetCode: {project}")
    state["repo"] = repo
    push_url = f"https://x-access-token:{token}@github.com/{repo.full_name}.git"
    run("git", "remote", "add", "origin", push_url, cwd=dest)
    run("git", "push", "-q", "--no-verify", "-u", "origin", "main", cwd=dest)
    run("git", "remote", "set-url", "origin", repo.clone_url, cwd=dest)
    print(f"created {repo.html_url}")


def main():
    parser = argparse.ArgumentParser(prog="leetcode-init")
    parser.add_argument("directory", nargs="?")
    parser.add_argument("--problem", help="problem name in snake_case")
    parser.add_argument("--project", help="project name in snake_case")
    parser.add_argument("--author", help="author for the LICENSE")
    github = parser.add_mutually_exclusive_group()
    github.add_argument("--github", dest="github", action="store_true", default=None)
    github.add_argument("--no-github", dest="github", action="store_false")
    visibility = parser.add_mutually_exclusive_group()
    visibility.add_argument("--private", dest="private", action="store_true", default=None)
    visibility.add_argument("--public", dest="private", action="store_false")
    args = parser.parse_args()

    if args.github and not (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")):
        sys.exit("error: --github requires GITHUB_TOKEN or GH_TOKEN")
    dir_name = Path(args.directory).name if args.directory else ""
    problem = ask_snake("Problem name (snake_case)", dir_name if SNAKE.match(dir_name) else "two_sum", args.problem)
    dest = Path(args.directory or problem).resolve()
    if dest.exists() and any(dest.iterdir()):
        sys.exit(f"error: {dest} is not empty")
    default_project = dest.name if SNAKE.match(dest.name) else problem
    project = ask_snake("Project name", default_project, args.project)
    author = ask("Author", git_config("user.name"), args.author)

    subs = {
        "project": project,
        "problem": problem,
        "author": author,
        "year": str(date.today().year),
    }
    created_dir = not dest.exists()
    state = {"repo": None}
    try:
        dest.mkdir(parents=True, exist_ok=True)
        render_tree(resources.files("leetcode_init") / "templates", dest, subs)
        init_git(dest, project)
        create_github_repo(dest, project, args.github, args.private, state)
    except BaseException:
        undo(dest, created_dir, state["repo"])
        raise
    print(f"ready: {dest}")


if __name__ == "__main__":
    main()
