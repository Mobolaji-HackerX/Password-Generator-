# 🔐 Password Generator

A secure, customizable command-line password generator built with Python. Generate strong passwords with full control over length, character types, and ambiguity exclusion.

## Features

- ✅ **Secure generation** — Uses Python's `secrets` module (cryptographically strong randomness)
- ✅ **Customizable length** — Any length you need
- ✅ **Character type toggles** — Include/exclude uppercase, lowercase, digits, symbols
- ✅ **Ambiguous character exclusion** — Optionally remove `0`, `O`, `1`, `l`, `I`
- ✅ **Strength estimation** — Entropy calculation and visual strength meter
- ✅ **Clipboard copy** — One-click copy to clipboard (cross-platform)
- ✅ **Batch generation** — Generate multiple passwords at once
- ✅ **Save to file** — Export passwords to a text file
- ✅ **Interactive mode** — Guided prompts for beginners
- ✅ **CLI mode** — Fast, scriptable command-line usage

## Installation

```bash
# Clone the repo
git clone https://github.com/Mobolaji-HackerX/Password-Generator.git
cd Password-Generator

# No dependencies required for basic usage!
# Optional: install pyperclip for better clipboard support on Linux
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended for first use)

```bash
python password_generator.py
```

You'll be guided through options step by step.

### CLI Mode

```bash
# Generate a 20-character password
python password_generator.py -l 20

# Generate 5 passwords, 32 characters each
python password_generator.py -l 32 -n 5

# No symbols, exclude ambiguous characters, copy to clipboard
python password_generator.py -l 16 --no-symbols --exclude-ambiguous --copy

# Save to file
python password_generator.py -l 24 -n 10 --save passwords.txt
```

### Options

| Flag | Description |
|------|-------------|
| `-l, --length` | Password length (default: 16) |
| `-n, --count` | Number of passwords to generate (default: 1) |
| `--no-upper` | Exclude uppercase letters |
| `--no-lower` | Exclude lowercase letters |
| `--no-digits` | Exclude digits |
| `--no-symbols` | Exclude special characters |
| `--exclude-ambiguous` | Remove `0`, `O`, `1`, `l`, `I` |
| `--copy` | Copy the first password to clipboard |
| `--save FILE` | Save passwords to a file |
| `-i, --interactive` | Launch interactive mode |

## Example Output

```
$ python password_generator.py -l 20

k9#mPx$vL2@nQfR5wZt!

Strength: GOOD (~93.3 bits)
```

## Project Structure

```
password-generator/
├── password_generator.py    # Main script
├── tests/
│   └── test_generator.py    # Unit tests
├── requirements.txt         # Optional dependencies
├── .gitignore
└── README.md
```

## Running Tests

```bash
python -m pytest tests/
```

## Why `secrets` instead of `random`?

This generator uses Python's [`secrets`](https://docs.python.org/3/library/secrets.html) module, which is designed for cryptography and security. The standard `random` module is **not** suitable for password generation.

## License

MIT
