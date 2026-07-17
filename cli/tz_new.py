#!/usr/bin/env python3
"""tz-new — scaffold a project from tz-forge composable modules.

Usage:
  tz-new <kind> <name> [--assistant=PROFILE] [--skills=a,b] [--create-github]
  tz-new --list
  tz-new --list-kinds

Examples:
  python cli/tz_new.py rust-lib demo-crate --assistant=fractal-swarm
  python cli/tz_new.py rust-lib /tmp/demo --assistant=humans-only
  python cli/tz_new.py python-mcp mysvc --assistant=solo-ai --skills=commit-prep,pr-review
  python cli/tz_new.py ml-rust-crate trit-demo --assistant=fractal-swarm --create-github
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # minimal fallback without PyYAML
    yaml = None  # type: ignore


ASSISTANT_PROFILES = (
    "humans-only",
    "solo-ai",
    "solo-ai-rich",
    "fractal-swarm",
)

# Module install rules used when catalog install keys are incomplete
MODULE_INSTALL: dict[str, dict[str, Any]] = {
    "fleet": {
        "copy_tree": [
            (".github", ".github"),
            ("scripts", "scripts"),
            ("docs/FLEET_STANDARDS.md", "docs/FLEET_STANDARDS.md"),
        ],
    },
    "license-mit": {
        "files": [
            ("LICENSE", "LICENSE"),
            ("REUSE.toml", "REUSE.toml"),
        ],
    },
    "pre-commit": {
        "files": [(".pre-commit-config.yaml", ".pre-commit-config.yaml")],
    },
    "local-ci-rust": {
        "files": [("check.sh", "scripts/check.sh")],
        "chmod_x": ["scripts/check.sh"],
    },
    "local-ci-python": {
        "files": [("check.sh", "scripts/check.sh")],
        "chmod_x": ["scripts/check.sh"],
    },
    "rust-cargo-deny": {
        "files": [("deny.toml", "deny.toml")],
    },
    "rust-toolchain": {
        "files": [("rust-toolchain.toml", "rust-toolchain.toml")],
    },
    "dependabot-cargo": {
        "copy_tree": [(".github", ".github")],
    },
    "dependabot-python": {
        "copy_tree": [(".github", ".github")],
    },
    "gitleaks-config": {
        "files": [(".gitleaks.toml", ".gitleaks.toml")],
    },
    "gitignore-rust": {
        "append_files": [("gitignore-rust", ".gitignore")],
    },
    "gitignore-python": {
        "append_files": [("gitignore-python", ".gitignore")],
    },
    "gitignore-ml": {
        "append_files": [("gitignore-ml", ".gitignore")],
    },
    "devcontainer-rust": {
        "files": [("devcontainer.json", ".devcontainer/devcontainer.json")],
    },
    "devcontainer-python": {
        "files": [("devcontainer.json", ".devcontainer/devcontainer.json")],
    },
    "agents-md-lite": {
        "templates": [("AGENTS.md.tmpl", "AGENTS.md")],
    },
    "agents-md-fractal": {
        "templates": [("AGENTS.md.tmpl", "AGENTS.md")],
    },
    "claude-md-lite": {
        "templates": [("CLAUDE.md.tmpl", "CLAUDE.md")],
    },
    "skills-generic": {
        "copy_tree": [(".", "skills")],
    },
    "skills-ml": {
        "copy_tree": [(".", "skills")],
    },
    "kickoffs": {
        "files": [("README.md", ".claude/kickoffs/README.md")],
    },
    "model-policy": {
        "files": [("model-policy.md", "docs/MODEL_POLICY.md")],
    },
    "harness-min": {
        "files": [("COMPOSE.md", "docs/compose/agent-harness.md")],
    },
    "cabal-profile": {
        "files": [("COMPOSE.md", "docs/compose/cabal-devmelopner.md")],
    },
    "security-mcp-opt": {
        "files": [("COMPOSE.md", "docs/compose/security-mcp.md")],
    },
}

MODULE_PATHS: dict[str, str] = {
    "fleet": "modules/fleet",
    "license-mit": "modules/license/mit",
    "pre-commit": "modules/pre-commit",
    "local-ci-rust": "modules/local-ci/rust",
    "local-ci-python": "modules/local-ci/python",
    "rust-cargo-deny": "modules/rust/cargo-deny",
    "rust-toolchain": "modules/rust/toolchain",
    "dependabot-cargo": "modules/gha/dependabot-cargo",
    "dependabot-python": "modules/gha/dependabot-python",
    "gitleaks-config": "modules/gha/gitleaks-config",
    "gitignore-rust": "modules/git",
    "gitignore-python": "modules/git",
    "gitignore-ml": "modules/git",
    "devcontainer-rust": "modules/devcontainer/rust",
    "devcontainer-python": "modules/devcontainer/python-uv",
    "agents-md-lite": "modules/agents/agents-md-lite",
    "agents-md-fractal": "modules/agents/agents-md-fractal",
    "claude-md-lite": "modules/agents/claude-md-lite",
    "skills-generic": "modules/agents/skills-generic",
    "skills-ml": "modules/agents/skills-ml",
    "kickoffs": "modules/agents/kickoffs",
    "model-policy": "modules/agents",
    "harness-min": "modules/agents/harness-min",
    "cabal-profile": "modules/agents/cabal-profile",
    "security-mcp-opt": "modules/agents/security-mcp-opt",
}

# Skills available under modules/agents/skills-*
KNOWN_SKILLS: dict[str, str] = {
    "commit-prep": "modules/agents/skills-generic/commit-prep",
    "pr-review": "modules/agents/skills-generic/pr-review",
    "fleet-gap": "modules/agents/skills-generic/fleet-gap",
    "unsafe-review": "modules/agents/skills-generic/unsafe-review",
    "cargo-check": "modules/agents/skills-generic/cargo-check",
    "hf-model-card": "modules/agents/skills-ml/hf-model-card",
    "train-smoke": "modules/agents/skills-ml/train-smoke",
}

GENERIC_SKILL_IDS = [
    "commit-prep",
    "pr-review",
    "fleet-gap",
    "unsafe-review",
    "cargo-check",
]
ML_SKILL_IDS = ["hf-model-card", "train-smoke"]


def forge_root() -> Path:
    env = os.environ.get("TZ_FORGE_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent


def project_snake(name: str) -> str:
    """Normalize project name to a Python/Rust-ish identifier."""
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if not s:
        s = "project"
    if s[0].isdigit():
        s = f"p_{s}"
    return s


def load_kind(root: Path, kind: str) -> dict[str, Any]:
    path = root / "project-kinds" / f"{kind}.yaml"
    if not path.is_file():
        known = sorted(p.stem for p in (root / "project-kinds").glob("*.yaml"))
        raise SystemExit(f"unknown kind {kind!r}; known: {', '.join(known)}")
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            raise SystemExit(f"invalid kind file: {path}")
        return data
    return _parse_kind_yaml(text)


def _parse_kind_yaml(text: str) -> dict[str, Any]:
    """Minimal parser for project-kinds/*.yaml without PyYAML."""
    data: dict[str, Any] = {"modules": {}, "assistant_profiles": {}}
    section: str | None = None
    sub: str | None = None
    always: list[str] = []
    profiles: dict[str, list[str]] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if not line.startswith(" ") and line.endswith(":"):
            section = stripped[:-1].strip()
            sub = None
            continue
        if section is None and ":" in stripped and not stripped.endswith(":"):
            k, v = stripped.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
            continue
        if not line.startswith(" "):
            if ":" in stripped and not stripped.endswith(":"):
                k, v = stripped.split(":", 1)
                data[k.strip()] = v.strip().strip("\"'")
            continue
        s = line.strip()
        if section == "modules":
            if s == "always:":
                sub = "always"
                continue
            if s.startswith("- ") and sub == "always":
                always.append(s[2:].strip())
        elif section == "assistant_profiles":
            if s.endswith(":") and not s.startswith("-"):
                sub = s[:-1].strip()
                profiles.setdefault(sub, [])
                continue
            if s.startswith("- ") and sub:
                profiles[sub].append(s[2:].strip())
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line or line.startswith(" "):
            continue
        if ":" in line and not line.endswith(":"):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
    data["modules"] = {"always": always}
    data["assistant_profiles"] = profiles
    return data


def list_kinds(root: Path) -> list[tuple[str, str, str]]:
    """Return (id, default_assistant, description) for each kind."""
    out: list[tuple[str, str, str]] = []
    for p in sorted((root / "project-kinds").glob("*.yaml")):
        kd = load_kind(root, p.stem)
        out.append(
            (
                p.stem,
                str(kd.get("default_assistant") or "solo-ai"),
                str(kd.get("description") or ""),
            )
        )
    return out


def resolve_modules(kind_data: dict[str, Any], assistant: str) -> list[str]:
    mods = kind_data.get("modules") or {}
    always = list(mods.get("always") or [])
    profiles = kind_data.get("assistant_profiles") or {}
    if assistant not in ASSISTANT_PROFILES:
        raise SystemExit(
            f"unknown assistant {assistant!r}; choose from {', '.join(ASSISTANT_PROFILES)}"
        )
    extra = list(profiles.get(assistant) or [])
    seen: set[str] = set()
    out: list[str] = []
    for m in always + extra:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def render_template(text: str, variables: dict[str, str]) -> str:
    out = text
    for key, val in variables.items():
        out = out.replace("{{" + key + "}}", val)
    return out


def append_text(dest: Path, text: str) -> None:
    ensure_parent(dest)
    existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    chunk = text if text.endswith("\n") else text + "\n"
    if existing and not existing.endswith("\n"):
        existing += "\n"
    # avoid exact duplicate appends
    if chunk.strip() and chunk.strip() in existing:
        return
    dest.write_text(existing + chunk, encoding="utf-8")


def copy_module(
    root: Path,
    dest: Path,
    module_id: str,
    variables: dict[str, str],
) -> None:
    if module_id == "skeleton":
        return  # handled separately
    rel = MODULE_PATHS.get(module_id)
    if not rel:
        print(f"warn: unknown module id {module_id!r}, skip", file=sys.stderr)
        return
    src_base = root / rel
    if not src_base.exists():
        print(f"warn: missing module path {src_base}, skip", file=sys.stderr)
        return
    rules = MODULE_INSTALL.get(module_id, {})

    for src_rel, dst_rel in rules.get("copy_tree", []):
        s = src_base / src_rel if src_rel != "." else src_base
        d = dest / dst_rel
        if s.is_file():
            ensure_parent(d)
            shutil.copy2(s, d)
        elif s.is_dir():
            for p in s.rglob("*"):
                if not p.is_file():
                    continue
                rel_p = p.relative_to(s)
                # drop root-level README.md from skill packs (module docs only)
                if module_id.startswith("skills-") and rel_p.name == "README.md" and len(rel_p.parts) == 1:
                    continue
                target = d / rel_p
                if p.name.endswith(".tmpl"):
                    target = d / Path(*rel_p.parts[:-1]) / p.name[: -len(".tmpl")]
                ensure_parent(target)
                try:
                    text = p.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    shutil.copy2(p, target)
                    continue
                if "{{" in text or p.name.endswith(".tmpl"):
                    target.write_text(render_template(text, variables), encoding="utf-8")
                else:
                    shutil.copy2(p, target)
        else:
            print(f"warn: missing {s}", file=sys.stderr)

    for src_rel, dst_rel in rules.get("files", []):
        s = src_base / src_rel
        d = dest / dst_rel
        if not s.is_file():
            print(f"warn: missing {s}", file=sys.stderr)
            continue
        ensure_parent(d)
        shutil.copy2(s, d)

    for src_rel, dst_rel in rules.get("append_files", []):
        s = src_base / src_rel
        d = dest / dst_rel
        if not s.is_file():
            print(f"warn: missing {s}", file=sys.stderr)
            continue
        append_text(d, s.read_text(encoding="utf-8"))

    for src_rel, dst_rel in rules.get("templates", []):
        s = src_base / src_rel
        d = dest / dst_rel
        if not s.is_file():
            print(f"warn: missing template {s}", file=sys.stderr)
            continue
        ensure_parent(d)
        text = render_template(s.read_text(encoding="utf-8"), variables)
        d.write_text(text, encoding="utf-8")

    for rel_path in rules.get("chmod_x", []):
        p = dest / rel_path
        if p.is_file():
            p.chmod(p.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_skeleton(
    root: Path,
    dest: Path,
    kind: str,
    kind_data: dict[str, Any],
    variables: dict[str, str],
) -> None:
    """Copy kind skeleton and rewrite {{project}} / PROJECT package dirs."""
    skel_rel = kind_data.get("skeleton") or f"modules/skeletons/{kind}"
    src = root / skel_rel
    if not src.is_dir():
        print(f"warn: no skeleton at {src}", file=sys.stderr)
        return

    snake = variables["project_snake"]

    for p in src.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(src)
        parts = list(rel.parts)
        # Rename placeholder package dirs
        parts = ["src" if x == "src" else snake if x == "PROJECT" else x for x in parts]
        # Also rewrite path segments that are literally PROJECT
        out_rel = Path(*parts) if parts else Path(".")
        name = out_rel.name
        is_tmpl = name.endswith(".tmpl")
        if is_tmpl:
            out_rel = out_rel.with_name(name[: -len(".tmpl")])
        # README.skeleton.md → only used if no README yet; write as hint file skip if README exists
        if name == "README.skeleton.md":
            out_rel = out_rel.with_name("README.skeleton.md")

        target = dest / out_rel
        ensure_parent(target)
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            shutil.copy2(p, target)
            continue
        rendered = render_template(text, variables)
        if name == "README.skeleton.md":
            # Prefer skeleton README content only when README not already written
            readme = dest / "README.md"
            if not readme.exists():
                readme.write_text(rendered, encoding="utf-8")
            else:
                # keep as extra compose note
                target.write_text(rendered, encoding="utf-8")
            continue
        target.write_text(rendered, encoding="utf-8")
        if name.endswith(".sh") or p.name.endswith(".sh"):
            target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_extra_skills(
    root: Path,
    dest: Path,
    skill_ids: list[str],
    variables: dict[str, str],
) -> list[str]:
    """Install selected skills under dest/skills/<id>/."""
    installed: list[str] = []
    for sid in skill_ids:
        rel = KNOWN_SKILLS.get(sid)
        if not rel:
            print(f"warn: unknown skill {sid!r}, skip", file=sys.stderr)
            continue
        src = root / rel
        if not src.is_dir():
            print(f"warn: missing skill path {src}, skip", file=sys.stderr)
            continue
        d = dest / "skills" / sid
        if d.exists():
            installed.append(sid)
            continue
        shutil.copytree(src, d)
        for p in d.rglob("*"):
            if p.is_file():
                try:
                    text = p.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                if "{{" in text:
                    p.write_text(render_template(text, variables), encoding="utf-8")
        installed.append(sid)
    return installed


def skills_from_modules(modules: list[str]) -> list[str]:
    skills: list[str] = []
    if "skills-generic" in modules:
        skills.extend(GENERIC_SKILL_IDS)
    if "skills-ml" in modules:
        skills.extend(ML_SKILL_IDS)
    # dedupe preserve order
    seen: set[str] = set()
    out: list[str] = []
    for s in skills:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def write_tz_forge_yaml(
    dest: Path,
    kind: str,
    name: str,
    assistant: str,
    modules: list[str],
    skills: list[str],
) -> None:
    tools = {
        "claude": assistant != "humans-only",
        "agents_md": assistant != "humans-only",
        "skills": skills,
        "cursor": False,
        "copilot_instructions": False,
        "tero": assistant == "fractal-swarm",
        "harness": "harness-min" in modules or assistant == "fractal-swarm",
        "cabal": "cabal-profile" in modules or assistant == "fractal-swarm",
    }
    # harness/cabal true only if module installed for accuracy
    tools["harness"] = "harness-min" in modules
    tools["cabal"] = "cabal-profile" in modules
    doc = {
        "kind": kind,
        "name": name,
        "assistant": {
            "profile": assistant,
            "tools": tools,
        },
        "modules": {m: {"version": "1"} for m in modules if m != "skeleton"},
        "options": {
            "default_branch": "main",
            "use_dev_branch": True,
        },
    }
    path = dest / ".tz-forge.yaml"
    if yaml is not None:
        path.write_text(
            yaml.safe_dump(doc, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )
        return
    lines = [
        f"kind: {kind}",
        f"name: {name}",
        "assistant:",
        f"  profile: {assistant}",
        "  tools:",
        f"    claude: {'true' if tools['claude'] else 'false'}",
        f"    agents_md: {'true' if tools['agents_md'] else 'false'}",
        "    skills:",
    ]
    if skills:
        for s in skills:
            lines.append(f"      - {s}")
    else:
        lines.append("      []")
    lines += [
        "    cursor: false",
        "    copilot_instructions: false",
        f"    tero: {'true' if tools['tero'] else 'false'}",
        f"    harness: {'true' if tools['harness'] else 'false'}",
        f"    cabal: {'true' if tools['cabal'] else 'false'}",
        "modules:",
    ]
    for m in modules:
        if m == "skeleton":
            continue
        lines.append(f'  {m}: {{ version: "1" }}')
    lines += [
        "options:",
        "  default_branch: main",
        "  use_dev_branch: true",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_minimal_readme(dest: Path, name: str, kind: str, assistant: str) -> None:
    readme = dest / "README.md"
    if readme.exists():
        return
    badges = f"""<!-- FLEET-BADGES:BEGIN -->
[![CI](https://github.com/tzervas/{name}/actions/workflows/fleet-ci.yml/badge.svg?branch=main)](https://github.com/tzervas/{name}/actions/workflows/fleet-ci.yml?query=branch%3Amain)
[![Security](https://github.com/tzervas/{name}/actions/workflows/fleet-security.yml/badge.svg?branch=main)](https://github.com/tzervas/{name}/actions/workflows/fleet-security.yml?query=branch%3Amain)
<!-- FLEET-BADGES:END -->
"""
    readme.write_text(
        f"""# {name}

{badges}
Scaffolded by [tz-forge](https://github.com/tzervas/tz-forge) (`tz-new`).

- **kind:** `{kind}`
- **assistant profile:** `{assistant}`

## Local gate

```bash
./scripts/check.sh   # when installed for this kind
```

## License

MIT — Copyright 2026 Tyler Zervas
""",
        encoding="utf-8",
    )


def create_github_repo(dest: Path, name: str, public: bool = True) -> None:
    """Optionally create GitHub repo via gh and set remote."""
    if shutil.which("gh") is None:
        raise SystemExit("--create-github requires GitHub CLI (`gh`) installed and authenticated")
    visibility = "--public" if public else "--private"
    # init git if needed
    if not (dest / ".git").exists():
        subprocess.run(["git", "init", "-b", "main"], cwd=dest, check=True)
        subprocess.run(["git", "add", "-A"], cwd=dest, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"chore: scaffold {name} via tz-forge"],
            cwd=dest,
            check=True,
        )
    cmd = [
        "gh",
        "repo",
        "create",
        f"tzervas/{name}",
        visibility,
        "--source",
        str(dest),
        "--remote",
        "origin",
        "--description",
        f"Scaffolded by tz-forge ({name})",
        "--push",
    ]
    print(f"running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"github: https://github.com/tzervas/{name}")


def scaffold(
    kind: str,
    name_or_path: str,
    assistant: str,
    extra_skills: list[str] | None = None,
    create_github: bool = False,
) -> Path:
    root = forge_root()
    kind_data = load_kind(root, kind)
    if assistant is None:
        assistant = kind_data.get("default_assistant") or "solo-ai"

    dest = Path(name_or_path).expanduser()
    if not dest.is_absolute() and "/" not in name_or_path and "\\" not in name_or_path:
        dest = Path.cwd() / name_or_path
    dest = dest.resolve()
    name = dest.name

    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"destination not empty: {dest}")
    dest.mkdir(parents=True, exist_ok=True)

    modules = resolve_modules(kind_data, assistant)
    snake = project_snake(name)
    variables = {
        "project": name,
        "project_snake": snake,
        "description": str(
            kind_data.get("description")
            or f"{name} ({kind}) scaffolded by tz-forge"
        ),
        "kind": kind,
    }

    for mid in modules:
        if mid == "skeleton":
            continue
        copy_module(root, dest, mid, variables)

    if "skeleton" in modules or kind_data.get("skeleton"):
        install_skeleton(root, dest, kind, kind_data, variables)

    # skills from modules + optional --skills=
    skills = skills_from_modules(modules)
    if extra_skills:
        more = install_extra_skills(root, dest, extra_skills, variables)
        for s in more:
            if s not in skills:
                skills.append(s)

    write_tz_forge_yaml(dest, kind, name, assistant, modules, skills)
    write_minimal_readme(dest, name, kind, assistant)

    print(f"created {dest}")
    print(f"  kind:      {kind}")
    print(f"  assistant: {assistant}")
    print(f"  modules:   {', '.join(m for m in modules if m != 'skeleton')}")
    if skills:
        print(f"  skills:    {', '.join(skills)}")

    if create_github:
        create_github_repo(dest, name)

    return dest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tz-new",
        description="Scaffold a project from tz-forge modules",
    )
    parser.add_argument(
        "kind",
        nargs="?",
        default=None,
        help="project kind (see --list)",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="project name or destination path",
    )
    parser.add_argument(
        "--assistant",
        default=None,
        help="humans-only | solo-ai | solo-ai-rich | fractal-swarm",
    )
    parser.add_argument(
        "--skills",
        default=None,
        help="comma-separated skill ids to install (e.g. commit-prep,pr-review,train-smoke)",
    )
    parser.add_argument(
        "--create-github",
        action="store_true",
        help="create GitHub repo via `gh repo create` and push",
    )
    parser.add_argument(
        "--list",
        "--list-kinds",
        dest="list_kinds",
        action="store_true",
        help="list project kinds and exit",
    )
    args = parser.parse_args(argv)

    root = forge_root()
    if args.list_kinds:
        rows = list_kinds(root)
        width = max((len(r[0]) for r in rows), default=8)
        for kid, default_a, desc in rows:
            print(f"{kid.ljust(width)}  default={default_a:14}  {desc}")
        return 0

    if not args.kind or not args.name:
        parser.error("kind and name are required (or use --list)")

    assistant = args.assistant
    if assistant is None:
        kd = load_kind(root, args.kind)
        assistant = kd.get("default_assistant") or "solo-ai"
    if assistant not in ASSISTANT_PROFILES:
        raise SystemExit(
            f"invalid --assistant={assistant!r}; "
            f"choose from {', '.join(ASSISTANT_PROFILES)}"
        )

    extra: list[str] = []
    if args.skills:
        extra = [s.strip() for s in args.skills.split(",") if s.strip()]

    scaffold(
        args.kind,
        args.name,
        assistant,
        extra_skills=extra or None,
        create_github=args.create_github,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
