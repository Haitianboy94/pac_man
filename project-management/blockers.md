# Blocking points and conflicts

The vendor maze API and the required top-ten highscore behavior were the main
integration constraints. The original test fixtures expected eleven scores;
the implementation follows the specification and retains ten, so those
fixtures need correction rather than a code change.
