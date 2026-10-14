#!/usr/bin/env python3
"""Fold the classroom record into the current quilt state.

Reads moves.jsonl (append-only, one JSON object per line) and writes
state.json: which patches are filled, by whom, and the standing of every
move on the wall. No dependencies beyond the Python standard library.

Fold rules (see PROTOCOL.md):
  * The first ordinary move to claim a patch stands.
  * A later ordinary move for a filled patch is OVERRIDDEN.
  * A captain's override beats any ordinary move whenever it arrives,
    and a later captain's override supersedes an earlier one.
  * Nothing is ever removed: overridden moves stay in the output,
    marked, with their artwork intact.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORD = HERE / "moves.jsonl"
OUT = HERE / "state.json"

PATCH_IDS = [f"p{i}" for i in range(1, 17)]


def standing_rank(move):
    """Higher wins. Captain's overrides outrank ordinary moves; among
    moves of the same kind, the fold is decided per-patch below."""
    return 1 if move.get("captain_override") else 0


def fold(moves):
    standing = {}  # patch -> move dict currently on the quilt
    for mv in moves:
        patch = mv["patch"]
        current = standing.get(patch)
        if current is None:
            standing[patch] = mv
            mv["_standing"] = True
            continue
        # A challenger displaces the standing move only if it is a
        # captain's override and the standing move is not a later-or-equal
        # captain's override. Since moves are processed in record order,
        # a captain's override always displaces an ordinary move, and a
        # later captain's override displaces an earlier one.
        if standing_rank(mv) > standing_rank(current) or (
            standing_rank(mv) == 1 and standing_rank(current) == 1
        ):
            current["_standing"] = False
            current["_status_note"] = (
                f"Overridden by move {mv['move']} "
                f"({'captain override' if mv.get('captain_override') else 'later move'})."
            )
            standing[patch] = mv
            mv["_standing"] = True
        else:
            mv["_standing"] = False
            mv["_status_note"] = (
                f"Patch already claimed by move {current['move']} "
                f"({current['agent']}), which stands."
            )
    return standing


def main():
    moves = []
    with open(RECORD, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                mv = json.loads(line)
            except json.JSONDecodeError as exc:
                sys.exit(f"moves.jsonl line {lineno}: invalid JSON ({exc})")
            for field in ("move", "agent", "patch", "title", "svg"):
                if field not in mv:
                    sys.exit(f"moves.jsonl line {lineno}: missing field '{field}'")
            if mv["patch"] not in PATCH_IDS:
                sys.exit(f"moves.jsonl line {lineno}: unknown patch '{mv['patch']}'")
            mv.setdefault("builds_on", [])
            mv.setdefault("why", "")
            mv.setdefault("captain_override", False)
            moves.append(mv)

    standing = fold(moves)

    out_moves = []
    for mv in moves:
        entry = {
            "move": mv["move"],
            "agent": mv["agent"],
            "patch": mv["patch"],
            "title": mv["title"],
            "builds_on": mv["builds_on"],
            "why": mv["why"],
            "captain_override": mv["captain_override"],
            "standing": mv["_standing"],
        }
        if not mv["_standing"]:
            entry["status_note"] = mv.get("_status_note", "")
        out_moves.append(entry)

    patches = {}
    for pid in PATCH_IDS:
        mv = standing.get(pid)
        if mv is None:
            patches[pid] = {"filled": False}
        else:
            patches[pid] = {
                "filled": True,
                "move": mv["move"],
                "agent": mv["agent"],
                "title": mv["title"],
                "svg": mv["svg"],
                "captain_override": mv["captain_override"],
            }

    state = {
        "generated_from": "moves.jsonl",
        "move_count": len(moves),
        "patches_filled": sum(1 for p in patches.values() if p["filled"]),
        "patches_total": len(PATCH_IDS),
        "patches": patches,
        "moves": out_moves,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(
        f"folded {len(moves)} move(s): "
        f"{state['patches_filled']}/{len(PATCH_IDS)} patches filled"
    )


if __name__ == "__main__":
    main()
