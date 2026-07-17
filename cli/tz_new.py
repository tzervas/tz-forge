#!/usr/bin/env python3
"""tz-new — scaffold a project from tz-forge composable modules.

Usage:
  tz-new <kind> <name> [--assistant=PROFILE] [--out DIR]

Examples:
  python cli/tz_new.py rust-lib demo-crate --assistant=fractal-swarm
  python cli/tz_new.py rust-lib /tmp/demo --assistant=humans-only
  python cli/tz_new.py python-mcp mysvc --assistant=solo-ai
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
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
    "rust-cargo-deny": {
        "files": [("deny.toml", "deny.toml")],
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
    "kickoffs": {
        "files": [("README.md", ".claude/kickoffs/README.md")],
    },
    "model-policy": {
        # path is modules/agents; file is model-policy.md
        "files": [("model-policy.md", "docs/MODEL_POLICY.md")],
    },
}

MODULE_PATHS: dict[str, str] = {
    "fleet": "modules/fleet",
    "license-mit": "modules/license/mit",
    "pre-commit": "modules/pre-commit",
    "local-ci-rust": "modules/local-ci/rust",
    "rust-cargo-deny": "modules/rust/cargo-deny",
    "agents-md-lite": "modules/agents/agents-md-lite",
    "agents-md-fractal": "modules/agents/agents-md-fractal",
    "claude-md-lite": "modules/agents/claude-md-lite",
    "skills-generic": "modules/agents/skills-generic",
    "kickoffs": "modules/agents/kickoffs",
    "model-policy": "modules/agents",
}


def forge_root() -> Path:
    env = os.environ.get("TZ_FORGE_ROOT")
    if env:
        return Path(env).resolve()
    # cli/tz_new.py → repo root
    return Path(__file__).resolve().parent.parent


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
    # tiny YAML subset parser for our kind files
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
        if not line.startswith(" ") and line.endswith(":"):
            key = line[:-1].strip()
            section = key
            sub = None
            continue
        if section in ("id", "description", "default_assistant") and ":" in line:
            # top-level scalar already handled when section set from previous
            pass
        # top-level scalars
        stripped = line.strip()
        if section is None and ":" in stripped and not stripped.endswith(":"):
            k, v = stripped.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
            continue
        if not line.startswith(" "):
            if ":" in stripped and not stripped.endswith(":"):
                k, v = stripped.split(":", 1)
                data[k.strip()] = v.strip().strip("\"'")
            continue
        indent = len(line) - len(line.lstrip(" "))
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
        elif section in ("id", "description", "default_assistant"):
            pass
        # re-read top keys that appear as "key: value" at indent 0 — handled above
        _ = indent
    # second pass for simple keys
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


def resolve_modules(kind_data: dict[str, Any], assistant: str) -> list[str]:
    mods = kind_data.get("modules") or {}
    always = list(mods.get("always") or [])
    profiles = kind_data.get("assistant_profiles") or {}
    if assistant not in ASSISTANT_PROFILES:
        raise SystemExit(
            f"unknown assistant {assistant!r}; choose from {', '.join(ASSISTANT_PROFILES)}"
        )
    extra = list(profiles.get(assistant) or [])
    # preserve order, dedupe
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


def copy_module(
    root: Path,
    dest: Path,
    module_id: str,
    variables: dict[str, str],
) -> None:
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
            if d.exists():
                # merge copy
                for p in s.rglob("*"):
                    if p.is_file():
                        rel_p = p.relative_to(s)
                        target = d / rel_p
                        ensure_parent(target)
                        shutil.copy2(p, target)
            else:
                shutil.copytree(s, d)
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


def write_tz_forge_yaml(
    dest: Path,
    kind: str,
    name: str,
    assistant: str,
    modules: list[str],
) -> None:
    skills = []
    if "skills-generic" in modules:
        skills = [
            "commit-prep",
            "pr-review",
            "fleet-gap",
            "unsafe-review",
            "cargo-check",
        ]
    tools = {
        "claude": assistant != "humans-only",
        "agents_md": assistant != "humans-only",
        "skills": skills,
        "cursor": False,
        "copilot_instructions": False,
        "tero": assistant == "fractal-swarm",
        "harness": assistant == "fractal-swarm",
        "cabal": assistant == "fractal-swarm",
    }
    # Prefer PyYAML dump; else hand-write
    doc = {
        "kind": kind,
        "name": name,
        "assistant": {
            "profile": assistant,
            "tools": tools,
        },
        "modules": {m: {"version": "1"} for m in modules},
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
        lines.append(f"  {m}: {{ version: \"1\" }}")
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


def scaffold(kind: str, name_or_path: str, assistant: str) -> Path:
    root = forge_root()
    kind_data = load_kind(root, kind)
    if assistant is None:
        assistant = kind_data.get("default_assistant") or "solo-ai"

    # name can be a path: last component is project name
    dest = Path(name_or_path).expanduser()
    if not dest.is_absolute() and "/" not in name_or_path and "\\" not in name_or_path:
        dest = Path.cwd() / name_or_path
    dest = dest.resolve()
    name = dest.name

    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"destination not empty: {dest}")
    dest.mkdir(parents=True, exist_ok=True)

    modules = resolve_modules(kind_data, assistant)
    variables = {
        "project": name,
        "description": kind_data.get("description")
        or f"{name} ({kind}) scaffolded by tz-forge",
        "kind": kind,
    }

    for mid in modules:
        copy_module(root, dest, mid, variables)

    write_tz_forge_yaml(dest, kind, name, assistant, modules)
    write_minimal_readme(dest, name, kind, assistant)

    print(f"created {dest}")
    print(f"  kind:      {kind}")
    print(f"  assistant: {assistant}")
    print(f"  modules:   {', '.join(modules)}")
    return dest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tz-new",
        description="Scaffold a project from tz-forge modules",
    )
    parser.add_argument("kind", help="project kind (rust-lib, python-mcp, agent-swarm)")
    parser.add_argument("name", help="project name or destination path")
    parser.add_argument(
        "--assistant",
        default=None,
        help="humans-only | solo-ai | solo-ai-rich | fractal-swarm",
    )
    parser.add_argument(
        "--list-kinds",
        action="store_true",
        help="list project kinds and exit",
    )
    args = parser.parse_args(argv)

    root = forge_root()
    if args.list_kinds:
        for p in sorted((root / "project-kinds").glob("*.yaml")):
            print(p.stem)
        return 0

    assistant = args.assistant
    if assistant is None:
        # load default from kind
        kd = load_kind(root, args.kind)
        assistant = kd.get("default_assistant") or "solo-ai"
    if assistant not in ASSISTANT_PROFILES:
        raise SystemExit(
            f"invalid --assistant={assistant!r}; "
            f"choose from {', '.join(ASSISTANT_PROFILES)}"
        )

    scaffold(args.kind, args.name, assistant)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
