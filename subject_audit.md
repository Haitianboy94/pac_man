# Subject Compliance Audit

The project covers most gameplay requirements, but several mandatory items are missing or currently failing.

## Critical / Likely Evaluation Failures

1. **Mandatory lint fails**
   - `make lint` reports **52 flake8 violations**.
   - `mypy` reports **19 errors** across 11 files.
   - This violates the required flake8 and mypy rules.

2. **Project-management evidence is absent**
   - No dedicated project-management directory exists.
   - `README.md:254-256` links to a placeholder path that does not exist.
   - Missing timeline/progress tracking, risk analysis, team organization, and acceptance test plan.

3. **Highscore corruption can crash with a traceback**
   - `src/config/highscore.py:23-34` lets invalid entries raise `InvalidHighscoreError`.
   - `src/game.py:27` does not catch it.
   - Confirmed: a score file containing `{"Alice": "bad"}` terminates with a traceback.
   - Other file errors such as permissions and invalid encoding are also not handled during load.

4. **Packaged build omits all sounds**
   - `pac-man.spec:8-11` bundles config and sprites, but not `sounds/`.
   - The executable builds, but starting gameplay will fail when `Sounds.start()` loads `sounds/start.wav`.

5. **CLI does not require exactly one argument**
   - `pac-man.py:18-20` silently uses the bundled default when no argument is supplied.
   - The subject explicitly requires exactly one configuration-file argument.

6. **Mandatory debug rule is broken**
   - `Makefile:11` runs:
     ```make
     python -m pdb python pac-man.py config.json
     ```
   - Confirmed result: `Error: python does not exist`.
   - It should pass `pac-man.py` directly to pdb.

## Functional / Specification Gaps

7. **Pause menu has no Resume button**
   - `src/ui/pause_menu.py:26-48` only provides Cheats and Main Menu.
   - Escape resumes gameplay, but the subject explicitly requires a Resume option in the pause menu.

8. **Super-pacgum placement is incorrect for rectangular mazes**
   - `src/entities/maze.py:62-67` mixes row and column dimensions.
   - It also uses inset positions rather than the actual four corner cells.
   - This can produce fewer than four correctly placed super-pacgums when width and height differ.

9. **The `pacgum` configuration value is unused**
   - It is parsed, but gameplay always fills every open cell/corridor independently of `config.pacgum`.
   - The README's description of this setting does not match the implementation.

10. **README does not document configuration defaults**
    - `README.md:95+` lists purposes but not default values, despite the explicit README requirement.
    - It also claims malformed configuration falls back safely, while malformed JSON currently exits.

11. **Highscores with duplicate names are not persisted reliably**
    - `src/config/highscore.py:40-42` converts entries into a dictionary.
    - Multiple scores under the same player name collapse into one, potentially retaining an arbitrary/lower score rather than that player's best.

12. **General initialization errors remain unhandled**
    - `pac-man.py:38-49` can traceback on mixer initialization, display initialization, asset loading, or highscore loading.
    - Only `game.loop()` is wrapped, and only `KeyboardInterrupt` is caught.

13. **Pause does not fully pause timed effects**
    - Timers are updated at `src/scenes/game_scene.py:142-146` before checking pause at lines 155-157.
    - Edible mode and other timer-driven states continue expiring while paused.

14. **No deployment evidence**
    - There is no Steam/Itch.io URL or other evidence of the mandatory public-platform build in the repository/README.

## Tooling / Test Issues

- `make test`: **73 passed, 2 failed**.
- The two failing tests incorrectly expect 11 entries while their names and the subject say Top 10:
  - `tests/test_highscore.py:121`
  - `tests/test_highscore.py:144`
- `flake8` and `mypy` are not declared in `pyproject.toml`, so `make lint` may not work in a clean installation.
- `pyproject.toml` requires Python 3.13 even though the README advertises Python 3.10+. This is not internally consistent.

## Already Covered Well

- External maze package is integrated with `perfect=False`.
- Fixed first-level seed and random subsequent generation are implemented.
- Maze-generation failure has a fallback.
- Ten default levels, scoring, lives, win/loss scenes, HUD, ghost behavior, cheats, menus, and name entry are present.
- README contains the required first line and the main required sections.

## Recommended Priority

Fix lint/mypy, highscore crash handling, packaging sounds, CLI/debug rules, and add the project-management directory before evaluation.
