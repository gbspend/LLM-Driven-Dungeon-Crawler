# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A 2D turn-based pygame dungeon crawler used as a research prototype. Game mechanics (the state updates for combat, item and enemy spawning, and consumable use) come from LLM calls instead of hand-written rules. This is the codebase for Spendlove & Kline, "An Initial Design for Generative Game Mechanics via LLM Function Emulation" (ICCC 2026).

## Running

```
pip install -r requirements.txt
python AI_rogue_like.py
```

- You need a `secret.py` in the repo root that contains `KEY = "<groq api key>"`. It is gitignored. `api_call.py` imports it at module load, so any module that imports `api_call` fails without it.
- Run from the repo root. Assets (`Book.ttf`, `bg/`, `Entities/`, `*.csv` maps) are loaded by relative path.
- Every LLM prompt and response is logged to `game.log`, which is gitignored. Logging is configured at the top of `AI_rogue_like.py` and must stay above the other imports.
- The repo has no test suite, linter or build step. The experimental harnesses are ad hoc scripts:
  - `events.py`: `first_chain_test`, `first_var_test`, `summon_test`.
  - `combatsim.py`: repeats LLM calls to collect outcome distributions. Much of it is stale. It uses old `Enemy(...)` signatures and the old `DEALT:` string format, and it imports `parse_damage`.
  - `python entities.py` opens a viewer that shows every enemy sprite.

## Architecture

**Main loop and turn logic (`AI_rogue_like.py`).**
- The `__main__` block creates the display, the map, the player and the starting enemies. These are module-level globals such as `player`, `tiles_list`, `tile_size`, `textBox`, `necro` and `goblin`. `Game` methods read them directly, so `Game` only works when the file is run as the script.
- `GameState` (RUN / INV / FIGHT / ITEM / GAMEOVER) drives input handling and which overlay panel is shown.
- Player input goes to `Game.state_update_player(order)`. `order` is a tuple such as `("MOVE", player, dir)`, `("ATK", ...)` or `("ITEM", idx)`, or the string `"SKIP"`. Enemies then move through `state_update_enemy()`.
- The large string-literal `state_update` block is old dead code kept for reference.

**Async LLM calls (`events.py`).**
- LLM calls must not block the pygame loop. They are wrapped in `Task(func, args, postf)` objects and grouped into a `Chain(executor, [tasks], finalf)`.
- Chains are appended to `game.active_chains`. `Game.update()` polls them once per frame.
- **Threading rule:** a task's `func` runs on a worker thread and must only call the LLM and read state, returning a result. `postf` and `finalf` run on the main thread and are the only place game state changes (HP, `enemies`, positions, inventory, `textBox`). Examples: `api_call.start_combat` → `Game.apply_combat`, `api_call.use_item` → `Game.handle_use_item`, `api_call.gen_item` → `Game.apply_loot`.
- A task's `postf` returns a boolean that decides whether the chain continues. When every chain has finished, the state goes back to RUN, which closes the FIGHT or ITEM panel.
- If a worker raises, `Task` logs the error and marks itself and its chain `failed` instead of crashing; `postf`/`finalf` are skipped and `Game.update` sets a fallback panel message.
- `game.enemy_turn` holds off the enemy turn until the player's LLM action has resolved and its result panel has been dismissed. At most one enemy starts a fight per turn.

**LLM layer (`api_call.py`).** All prompts live here. The client is Groq.
- `get_response2` is the current helper. It defaults to `openai/gpt-oss-20b` because Groq retired Llama 3.1. It pulls the first JSON object out of the reply and retries up to 4 times on API errors or unparseable replies. After that it returns `{}` (or `""` when `incl_json=False`, which gives free-text narration), so callers should use `.get()` with defaults or handle the `KeyError`.
- `get_response` is the older helper for plain text, using `llama-3.3-70b-versatile`.
- Most callers also wrap their calls in `try/except` and retry recursively using a `tryc` counter.
- **The current combat pipeline is `start_combat`**, which `Game.start_combat2` runs on a worker thread:
  1. `combat_scenario` writes narration.
  2. `combat_vars_together` maps the narration to a JSON of variable changes (`player_hp`, `enemy_hp`, distances, `enemy_count`, statuses). Missing keys fall back to `COMBAT_DEFAULTS`, and values are normalised (HP tiers uppercased, `enemy_count` clamped to 0–3).
  3. `combat_scenario_redo` rewrites the narration so it matches those effects.
  4. If `enemy_count` > 0, `enemy_generator` creates new enemies and `parse_sprite` asks the LLM to pick sprites for them (falling back to a random sprite if the name doesn't match).
  5. It returns an outcome dict; `Game.apply_combat` then applies knockback through `push`, spawns reinforcements, applies damage and starts the loot chain. Statuses are returned but not applied yet.
- The `combat_state_update_*` functions are the older one-shot design and are mostly unused. Also note that `combat_vars_together` is defined twice in the file, so the second definition is the one that runs.
- Qualitative LLM outputs become numbers in fixed tables. `Game.combat_handler` converts NONE/LOW/MEDIUM/HIGH/FATAL into fractions of max HP. `combat_handler_item` and `heal_handler_item` do the same for items.
- `gen_item` and the `use_item_*` chain handle loot and consumables. Target, stat (`hp` or `description`) and effect are each chosen by a separate LLM call. Effects that are not HP changes go into `current_effects`. `get_desc()` appends those effects to the entity description, so the next prompt sees them. The player's effects are cleared after a single read.

**World and entities.**
- `tiles.py` `TileMap` reads a tile-ID CSV (`test_tile2.csv`) and an object CSV (`objs2.csv`). In the object CSV, a numeric entry is a decoration and `T`/`C` are animated fires, which also block movement.
- Tiles are tuples `(surface, x, y, collides)`. Collision tile IDs are hardcoded in `load_tiles`.
- Positions are in pixels, and one move is `TILE_SIZE` (16).
- `entities.py` loads every PNG in `Entities/` as a 4-frame, 16×16 animation and names it by splitting the CamelCase filename, so `GoblinFighter.png` becomes `"Goblin Fighter"`. The LLM chooses sprites from this list of names.
- `characters.py`: `Character` is the player and holds `weapons` and `items` as `(name, description)` tuples. `Enemy` moves randomly and attacks when orthogonally adjacent. `hp_state` maps HP to HEALTHY/WOUNDED/MAIMED, and these states are passed into prompts.
- `panels.py` holds the FIGHT and ITEM overlays. `text.py` holds the scrolling log `TextBox` and the `Inventory` screen. Layout and color constants are in `consts.py`.
