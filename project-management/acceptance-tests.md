# Acceptance test plan

- [x] `make lint` passes flake8 and mypy.
- [x] `make test` passes configuration and highscore validation tests (the two
  legacy expectations for eleven entries must be updated to the required top ten).
- [ ] Start, play, pause, resume, lose, and save a score manually.
- [ ] Clear ten levels and verify the victory/name-entry flow.
- [ ] Exercise every cheat from the pause menu.
- [ ] Launch the clean PyInstaller build without the development environment.
- [ ] Start with malformed config/highscore files and verify a clean message.
