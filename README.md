# jolla-note-cli

A very small Jolla Note app command line interface

## Usage

Use `note --help` to get the newest usage help

```
Usage:
    note [options] [-]
    note [options] <file>
    note --delete=<number>

Options:
    -i, --index=<number>    note index
    -d, --delete=<number>   delete note(s) of this index
    -c, --color=<color>     note color
    -l, --list              list all notes
```

## Install

Open your jolla terminate app and run as super user

```bash
pip install git+git://github.com/TylerTemp/jolla-note-cli.git
```

## License

MIT License