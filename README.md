# PseudoBusy

### What
PseudoBusy is a script to make your terminal look busy.
It finds random interesting files on your computer and prints them out letter by letter, with varying speed, IDE-like highlighting, and random mistakes.

Works nicely as a noninvasive, nonintensive, screen saver.

### Install
```
python setup.py install
```

### Run
```
python pseudobusy.py
```
If installed:
```
pseudobusy
```

### Stop
<kbd>ctrl</kbd> + <kbd>c</kbd>

### Command-line options

Options | Descriptions
------- | ------------
`-h` or `--help` | show help message
`--version`      | show current version
`-v` or `--verbose` | print debug info (0-3) (default: 1)
`-s` or `--typing-speed-override` | overrides the default typing speed
`-r` or `--reject-first` | checks/rejects invalid files before starting

### Extras
If running in a tmux session, there is a 25% chance each time a file is read that an alternate character set will be used.

### Issues

- [x] Works on Linux completely

- [x] Works on OSX completely

- [ ] Windows not supported

