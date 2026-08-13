# Pac-Man

## Run from source

Install the dependencies and start the game:

```sh
make install
make run
```

## Build an executable

PyInstaller is included in the development dependencies. Build the game with:

```sh
make package
```

The executable is created at `dist/pac-man` (`dist/pac-man.exe` on Windows).
It includes the default `config.json` and all sprite assets, so it can be moved
and run on its own:

```sh
./dist/pac-man
```

You can optionally provide a custom configuration file:

```sh
./dist/pac-man path/to/config.json
```

PyInstaller builds for the operating system on which it runs. Build separately
on Windows, macOS, or Linux when you need an executable for that platform.
Remove generated packaging files with `make package-clean`.
