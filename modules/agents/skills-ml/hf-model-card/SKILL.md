---
name: hf-model-card
description: Draft or refresh a Hugging Face model card (MODEL_CARD.md / README model section). Use when publishing BitNet/trit/HF checkpoints or training runs.
metadata:
  author: tz-forge
  version: "1.0"
  domain: ml
allowed-tools: Bash(git:*) Bash(huggingface-cli:*) Bash(python:*)
---

# HF model card

## When to use

- Publishing a checkpoint to Hugging Face Hub (`tzervas/*`)
- Opening a PR that adds training artifacts
- Operator BitNet / hybrid / trit models needing license + data notes

## Steps

1. Prefer existing `MODEL_CARD.md` or HF YAML front-matter in `README.md`.
2. Fill: architecture, intended use, training data + licenses, eval metrics, limitations.
3. Cite code repo: `https://github.com/tzervas/{{project}}` when known.
4. Never embed secrets, tokens, or private dataset URLs.
5. If card is a stub from tz-forge, expand product-specific sections before upload.

## Checklist

- [ ] License declared (MIT / Apache-2.0 / other)
- [ ] Training data provenance listed
- [ ] Evaluation numbers or "not evaluated" honest note
- [ ] No credentials in card or git history
