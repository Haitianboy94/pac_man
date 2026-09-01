# Project analysis and technical choices

The game uses a small scene state machine so menu, gameplay, and end screens
remain independently testable. `GameState` owns score, lives, level, timers,
and cheat flags across scene transitions. The assigned maze package is wrapped
by `src/maze_generator.py`, keeping vendor-specific details outside entities.

Pygame sprites and groups provide rendering and collision integration. A
min-heap maintains the top ten scores efficiently, while JSON keeps the saved
format inspectable and portable.
