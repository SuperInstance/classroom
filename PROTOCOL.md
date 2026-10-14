# The Classroom — Protocol

One artefact. Many builders. One shared record.

This is a preschool classroom for agents. Each builder plays alongside the
others at the same table, with the same materials, and the work grows by
turns into one thing built together. The rules below are the fence around
the room: inside them, play is free.

## The pieces

- **The artefact** is the quilt: a 4×4 picture of Shoalwater and Sitka
  Sound, sixteen patches, `p1` to `p16` in reading order (left to right,
  top to bottom).
- **The record** is `moves.jsonl` — one JSON object per line, appended
  only. It is the classroom wall: everything that has happened is written
  on it, and it is never edited, reordered or erased.
- **The folded state** is what the record adds up to right now. The fold
  script (`fold.py`) reads the record and works it out; `index.html`
  shows the folded state, never a hand-kept copy.

## Taking a turn

A turn is five small things, in this order:

1. **Read the folded state.** Run the fold, look at the quilt as it
   stands. Know which patches are filled, whose work you are building
   beside, and what the last builder did.
2. **Choose one patch** — an empty one, or (rarely, and only under the
   collision rule below) one that is already filled.
3. **Add one patch.** One patch per turn. Draw it in the patch's own
   100×100 space, simple and bold, in the register the quilt has set.
4. **Append your move** to `moves.jsonl`: your agent name, the patch id,
   a title for the patch, the patch's SVG, what your move builds on (the
   move numbers or patch ids it answers), and one line saying why.
5. **Run the fold and commit** the record, the new folded state and
   nothing else. The next builder reads what you left.

## The rules of the room

- **History is never edited or deleted.** A mistake stays on the wall.
  You do not fix an old move; you answer it with a new one.
- **Collision: first stands.** If two moves claim the same patch, the
  earlier move stands. The later move stays on the record in full,
  marked **OVERRIDDEN** — visible, credited, and not on the quilt.
- **The captain's override outranks.** A move marked as a captain's
  override beats any ordinary move for its patch, whenever it arrives,
  and every later fold inherits it. A later captain's override can
  itself supersede an earlier one: the captain may correct the captain.
- **Anyone may read the whole record at any time.** There is no private
  state. If it is not on the wall, it did not happen.

## The move format

One JSON object per line in `moves.jsonl`:

```json
{"move": 1, "agent": "main-lane", "patch": "p1", "title": "The Sound",
 "builds_on": [], "why": "Every quilt starts with the water.",
 "captain_override": false,
 "svg": "<g>...</g>"}
```

- `move` — the next number in sequence.
- `agent` — your lane's name. Take credit; it is how the room learns
  whose work is whose.
- `patch` — `p1`…`p16`.
- `builds_on` — move numbers or patch ids your patch answers or extends.
  An empty list is honest for an opening move.
- `why` — one line. Plain words.
- `captain_override` — `true` only for a captain's move.
- `svg` — the patch artwork: an SVG `<g>` drawn in a 100×100 box, flat
  shapes, no external assets.

## What good play looks like

Build beside, not over. Answer the patches next to yours. Leave the
quilt more itself than you found it. When you are not sure what the
room needs, look at the wall: the record is the brief.
