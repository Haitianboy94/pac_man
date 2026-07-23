# Pacman Project — Feature List & Task Breakdown

This breaks the spec into individually assignable tasks. Tasks are grouped by
subsystem, with rough dependencies and effort noted. A suggested 2-person split
is proposed at the end, but tasks are modular enough to rearrange.

Legend: **[S]** small, **[M]** medium, **[L]** large · Dependencies in *(depends on: ...)*

---

## 1. Project Setup & Tooling

- [ ] **1.1** [S] Initialize repo structure, `.gitignore`, virtualenv/uv setup
- [ ] **1.2** [S] Write `Makefile` with `install`, `run`, `debug`, `clean`, `lint`, `lint-strict`
- [ ] **1.3** [S] Configure flake8 + mypy (strict-compatible config files)
- [ ] **1.4** [M] Set up base package structure (modules for config, game, entities, UI, highscore)
- [ ] **1.5** [S] Set up pytest/unittest skeleton (not graded, but useful for both devs)

---

## 2. Configuration System

- [ ] **2.1** [M] JSON-with-comments parser (strip `#` lines, optionally `//` and `/* */`)
- [ ] **2.2** [M] Config schema/dataclass or Pydantic-style model with defaults for all keys (`highscore_filename`, `level`, `width`, `height`, `lives`, `pacgum`, `points_per_pacgum`, `points_per_super_pacgum`, `points_per_ghost`, `seed`, `level_max_time`)
- [ ] **2.3** [M] Validation & clamping logic: invalid/missing values → safe defaults + log message, unknown keys ignored, never crash
- [ ] **2.4** [S] CLI entrypoint: `python3 pac-man.py config.json`, exactly one arg, clean error on missing/invalid file (no traceback)
- [ ] **2.5** [S] Unit tests for config parsing edge cases (missing keys, bad types, malformed JSON, comments)

---

## 3. Maze Generator Integration

- [ ] **3.1** [M] Study assigned "A-Maze-ing" package's public interface/API
- [ ] **3.2** [M] Build adapter/loader that converts their maze output into your internal maze representation (walls/corridors grid)
- [ ] **3.3** [S] Call generator with `PERFECT=False`, fixed `seed` for level 1, random seed for subsequent levels
- [ ] **3.4** [S] Error handling if generator raises/fails — clean fallback or message, no crash
- [ ] **3.5** [S] Unit test / manual test harness that renders raw generator output before UI exists (helps unblock rendering work early)

---

## 4. Core Game Entities & Logic

- [ ] **4.1** [M] Player entity: position, direction, movement through corridors only, collision with walls
- [ ] **4.2** [S] Input handling: arrow keys / WASD
- [ ] **4.3** [M] Pacgum placement (most corridors) + consumption logic (+X score)
- [ ] **4.4** [M] Super-pacgum placement (4 corners) + consumption logic (+Y score, triggers ghost-edible state)
- [ ] **4.5** [L] Ghost entity base class: position, corner spawn, movement through corridors
- [ ] **4.6** [L] Ghost "chase" behavior when not edible (define & implement algorithm — distance-based or similar)
- [ ] **4.7** [M] Ghost "flee" behavior when edible
- [ ] **4.8** [M] Ghost eaten logic: +Z score, respawn to corner after delay (5–10s)
- [ ] **4.9** [M] Player-ghost collision: lose life (unless edible-ghost-eaten case), respawn player at center
- [ ] **4.10** [S] Lives system: start at 3, decrement on hit, game over at 0
- [ ] **4.11** [S] Win condition per level (all pacgums eaten) / win condition for game (all levels done)
- [ ] **4.12** [M] Level timer: countdown, define behavior on timeout (restart level / end game / etc.)
- [ ] **4.13** [S] Score tracking: persists across levels/lives, never decreases
- [ ] **4.14** [M] Level progression manager: advance level, regenerate maze, carry over score/lives, at least 10 levels
- [ ] **4.15** [S] Pause/resume state handling (game logic side, distinct from UI pause menu)

---

## 5. Highscore System

- [ ] **5.1** [M] Persistent storage design (JSON file), load-on-start / save-on-end
- [ ] **5.2** [S] File error handling: missing file, corrupted/invalid format → safe fallback, no crash
- [ ] **5.3** [S] Name validation: max 10 chars, alphanumeric + spaces only
- [ ] **5.4** [S] Score validation: non-negative integers
- [ ] **5.5** [S] Maintain top 10 list, sorted, insert new scores correctly
- [ ] **5.6** [S] Expose data for main menu display and name-entry flow

---

## 6. User Interface (Graphics Library — pygame/MLX/etc.)

- [x] **6.1** [M] Rendering setup: window init, game loop/render loop, frame timing
- [x] **6.2** [M] Maze rendering (walls, corridors) from internal maze representation
- [x] **6.3** [S] Player sprite/rendering + animation (optional: mouth open/close)

- [ ] **6.4** [S] Ghost sprite/rendering (normal vs. edible visual state)
- [x] **6.5** [S] Pacgum / super-pacgum rendering
- [x] **6.6** [M] Main Menu screen: Start Game, View Highscores, Instructions, Exit
- [ ] **6.7** [M] In-game HUD: score, lives, level, remaining time (always visible)
- [x] **6.8** [M] Pause Menu: Resume, Return to Main Menu
- [ ] **6.9** [M] Game Over screen: final score + name entry for highscore
- [ ] **6.10** [M] Victory screen: final score + congratulatory message + name entry
- [ ] **6.11** [S] Instructions screen (controls/rules)
- [ ] **6.12** [S] Highscore display screen/panel (top 10, names + scores)
- [x] **6.13** [S] Input handling glue: keyboard events → menu navigation / pause toggle

---

## 7. Cheat Mode

- [ ] **7.1** [S] Toggle mechanism (e.g. keybind) to activate/deactivate cheat mode
- [ ] **7.2** [S] Invincibility (no life lost on ghost contact)
- [ ] **7.3** [S] Level skip (instantly complete current level)
- [ ] **7.4** [S] Ghost freeze (ghosts stop moving)
- [ ] **7.5** [S] Extra lives (add lives on demand)
- [ ] **7.6** [S] Increased player speed
- [ ] **7.7** [S] Optional: on-screen indicator that cheat mode is active (helps reviewer confirm it's working)

---

## 8. Packaging & Deployment

- [ ] **8.1** [M] Choose platform (Steam or Itch.io), set up unlisted/private build
- [ ] **8.2** [M] Packaging script/spec (e.g., PyInstaller or platform-specific build tool) — must live at repo root
- [ ] **8.3** [S] In-package instructions (controls, options, configuration) bundled with the build
- [ ] **8.4** [S] Verify packaged build launches standalone (no dev environment dependencies)
- [ ] **8.5** [S] Document/test the "regenerate package" process, since it may be requested live during review

---

## 9. Documentation

- [ ] **9.1** [S] README skeleton: first italic line with logins, Description, Instructions
- [ ] **9.2** [M] README: Resources section (references + AI usage disclosure — what was used for what)
- [ ] **9.3** [M] README: Configuration section (keys, defaults, format)
- [ ] **9.4** [M] README: Highscore section (design + rationale)
- [ ] **9.5** [M] README: Maze Generation section (how the assigned package is integrated)
- [ ] **9.6** [M] README: Implementation section (technical summary)
- [ ] **9.7** [M] README: General Software Architecture section (modules/classes/relationships, maybe a diagram)
- [ ] **9.8** [S] README: Project Management section + link to management subdirectory

---

## 10. Project Management Artifacts

- [ ] **10.1** [M] Create `project-management/` subdirectory
- [ ] **10.2** [M] Project timeline (Gantt/Kanban board or equivalent)
- [ ] **10.3** [S] Progress tracking log (actual vs. planned)
- [ ] **10.4** [M] Project analysis & key technical choices writeup
- [ ] **10.5** [M] Risk analysis & mitigation notes
- [ ] **10.6** [S] Team organization notes (who did what, decision process)
- [ ] **10.7** [M] Acceptance test plan (features tested, bugs found/fixed log)
- [ ] **10.8** [S] Summary of blocking points/conflicts encountered

---

## 11. Testing & QA

- [ ] **11.1** [M] Unit tests: config parsing, highscore persistence, scoring logic
- [ ] **11.2** [M] Manual test pass: full game loop (menu → play → win/lose → highscore → menu)
- [ ] **11.3** [S] Manual test pass: all cheat mode features
- [ ] **11.4** [S] Stress test: faulty config files, missing maze package, corrupted highscore file — confirm no tracebacks anywhere
- [ ] **11.5** [S] Playtest at least 10 levels end-to-end for balance/timing issues

---

## Suggested 2-Person Split

The natural fault line is **game engine/logic** vs. **presentation/infra**, since they can be developed in parallel against a shared interface (e.g. agree early on the `Maze`, `GameState`, and `Config` data shapes).

**Person A — Core Gameplay & Systems**
- Sections 3 (Maze integration), 4 (Core entities/logic), 7 (Cheat mode), part of 11 (gameplay testing)

**Person B — Interface, Config & Delivery**
- Sections 2 (Config), 5 (Highscore), 6 (UI/menus/HUD), 8 (Packaging), part of 11 (robustness testing)

**Shared / either person, ideally together early on:**
- Section 1 (project setup) — do this first, together, to agree on structure
- Section 9 (README) — split by section based on who built what
- Section 10 (Project management docs) — ongoing, shared responsibility throughout

**Suggested sequencing:**
1. Both: agree on data models (Config, Maze representation, GameState) — a short design session before splitting off
2. Parallel work on Sections 2–3 (Person B / Person A) since these unblock everything else
3. Parallel work on Section 4 (Person A) and Section 6 skeleton (Person B) once data models are stable
4. Integrate early and often — the ghost/player/maze logic (A) and the renderer (B) need to sync on coordinate systems and timing
5. Sections 5, 7, 8 can slot in once the core loop works
6. Documentation (9, 10) throughout, not just at the end
