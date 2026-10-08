#!/usr/bin/env python3
"""
Revise AI images after user dissatisfaction or a change request.

Flow (two models, one job each):
  1. GEMINI_REVISION_MODEL (default gemini-3.8-flash, text-only) rewrites the
     manifest prompt so it carries the user's feedback while keeping the deck's
     rendering / palette / text-policy / composition constraints.
  2. The normal image_gen.py manifest run re-renders the item with the drawing
     model (Gemini backend default: gemini-nano-banana-2.1).

The old prompt is kept in `prompt_history`; the item goes back to `Pending`.
First-time generation never uses this script — call image_gen.py directly.

Usage:
  python3 image_revise.py <image_prompts.json> --file cover.png --feedback "더 몰입감 있게"
  python3 image_revise.py <image_prompts.json> --file a.png --file b.png --feedback "..." [--no-render]
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402

configure_utf8_stdio()

DEFAULT_REVISION_MODEL = "gemini-3.8-flash"

REWRITE_INSTRUCTION = """You rewrite prompts for an AI image model used in a presentation deck.
Rewrite the ORIGINAL PROMPT so the new image satisfies the USER FEEDBACK.
Keep, unchanged in spirit: the rendering style sentence, the palette/HEX guidance,
the calm-zone / composition requirement for slide text, the aspect intent, and every
safety or "NO text / no logos" clause. Change subject matter, mood, framing or detail
only as far as the feedback asks. The feedback may be Korean; write the prompt in English.
Return ONLY the new prompt text — no preface, no quotes, no markdown."""


def _load_env() -> None:
    # image_gen.py의 .env 탐색 규칙을 그대로 재사용한다
    import image_gen
    image_gen._load_image_env_file()


def rewrite_prompt(original: str, feedback: str, purpose: str, model: str) -> str:
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY not set (.env or environment).")
    base_url = os.environ.get("GEMINI_BASE_URL")
    client = (genai.Client(api_key=api_key, http_options={"base_url": base_url})
              if base_url else genai.Client(api_key=api_key))
    contents = (f"{REWRITE_INSTRUCTION}\n\nIMAGE PURPOSE: {purpose}\n\n"
                f"ORIGINAL PROMPT:\n{original}\n\nUSER FEEDBACK:\n{feedback}")
    resp = client.models.generate_content(
        model=model, contents=[contents],
        config=types.GenerateContentConfig(response_modalities=["TEXT"]))
    text = (resp.text or "").strip()
    if len(text) < 40:
        raise RuntimeError(f"Revision model returned an unusable prompt: {text!r}")
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("manifest", help="Path to images/image_prompts.json")
    ap.add_argument("--file", action="append", required=True,
                    help="Manifest item filename to revise (repeatable)")
    ap.add_argument("--feedback", required=True, help="User's dissatisfaction / change request")
    ap.add_argument("--revision-model", default=None,
                    help=f"Prompt-rewriting model (default env GEMINI_REVISION_MODEL or {DEFAULT_REVISION_MODEL})")
    ap.add_argument("--no-render", action="store_true", help="Rewrite prompts only; skip image_gen.py")
    args = ap.parse_args()

    _load_env()
    model = args.revision_model or os.environ.get("GEMINI_REVISION_MODEL") or DEFAULT_REVISION_MODEL
    manifest_path = Path(args.manifest)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_name = {it["filename"]: it for it in data["items"]}
    missing = [f for f in args.file if f not in by_name]
    if missing:
        raise SystemExit(f"Not in manifest: {missing}")

    for name in args.file:
        item = by_name[name]
        print(f"[Revise] {name} — rewriting prompt with {model}")
        new_prompt = rewrite_prompt(item["prompt"], args.feedback, item.get("purpose", ""), model)
        item.setdefault("prompt_history", []).append({
            "prompt": item["prompt"],
            "replaced_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "feedback": args.feedback,
            "revision_model": model,
        })
        item["prompt"] = new_prompt
        item["status"] = "Pending"
        item.pop("last_error", None)
        print(f"  new prompt: {new_prompt[:160]}{'...' if len(new_prompt) > 160 else ''}")

    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.no_render:
        return
    cmd = [sys.executable, str(_SCRIPTS_DIR / "image_gen.py"), "--manifest", str(manifest_path),
           "--output", str(manifest_path.parent)]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
