"""Minimal train smoke for {{project}}.

Does not download large models by default — validates imports only.
"""

from __future__ import annotations


def main() -> None:
    try:
        import transformers  # noqa: F401
        import datasets  # noqa: F401
    except ImportError as exc:
        raise SystemExit(f"missing dep: {exc}") from exc
    print("train-smoke: imports ok ({{project}})")


if __name__ == "__main__":
    main()
