#!/usr/bin/env python3
"""
Password Generator CLI
A secure, customizable password generator with strength checking.
"""

import argparse
import random
import string
import sys
import secrets
from typing import Optional


class PasswordGenerator:
    """Secure password generator with configurable options."""

    # Characters that look similar — optionally excluded
    AMBIGUOUS = "0O1lI"

    # Character pools
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"

    def __init__(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
        exclude_ambiguous: bool = False,
        ensure_all_types: bool = True,
    ):
        self.length = length
        self.use_uppercase = use_uppercase
        self.use_lowercase = use_lowercase
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.exclude_ambiguous = exclude_ambiguous
        self.ensure_all_types = ensure_all_types

        self._build_pool()

    def _build_pool(self) -> None:
        """Build the character pool based on selected options."""
        self.pool = ""
        self.pools = []

        if self.use_lowercase:
            chars = self.LOWERCASE
            if self.exclude_ambiguous:
                chars = "".join(c for c in chars if c not in self.AMBIGUOUS)
            self.pool += chars
            self.pools.append(chars)

        if self.use_uppercase:
            chars = self.UPPERCASE
            if self.exclude_ambiguous:
                chars = "".join(c for c in chars if c not in self.AMBIGUOUS)
            self.pool += chars
            self.pools.append(chars)

        if self.use_digits:
            chars = self.DIGITS
            if self.exclude_ambiguous:
                chars = "".join(c for c in chars if c not in self.AMBIGUOUS)
            self.pool += chars
            self.pools.append(chars)

        if self.use_symbols:
            self.pool += self.SYMBOLS
            self.pools.append(self.SYMBOLS)

        if not self.pool:
            raise ValueError("At least one character type must be enabled.")

    def generate(self, count: int = 1) -> list[str]:
        """Generate one or more passwords."""
        passwords = []
        for _ in range(count):
            passwords.append(self._generate_one())
        return passwords

    def _generate_one(self) -> str:
        """Generate a single password."""
        if self.ensure_all_types and len(self.pools) > 1:
            # Ensure at least one character from each selected pool
            password_chars = [secrets.choice(pool) for pool in self.pools]
            remaining = self.length - len(password_chars)
            if remaining < 0:
                raise ValueError(
                    f"Length {self.length} is too short for the required character types."
                )
            password_chars += [secrets.choice(self.pool) for _ in range(remaining)]
            secrets.SystemRandom().shuffle(password_chars)
        else:
            password_chars = [secrets.choice(self.pool) for _ in range(self.length)]

        return "".join(password_chars)


def estimate_strength(password: str) -> dict:
    """Estimate password strength and return metrics."""
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    variety = sum([has_lower, has_upper, has_digit, has_symbol])

    # Entropy estimation (bits)
    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_symbol:
        pool_size += 32

    entropy = length * (pool_size.bit_length() - 1) if pool_size > 0 else 0

    # Strength rating
    if length < 8 or variety < 2:
        rating = "weak"
    elif length < 12 or variety < 3 or entropy < 50:
        rating = "fair"
    elif length < 16 or entropy < 80:
        rating = "good"
    else:
        rating = "strong"

    return {
        "length": length,
        "variety": variety,
        "entropy": round(entropy, 1),
        "rating": rating,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
    }


def strength_bar(rating: str) -> str:
    """Return a visual strength indicator."""
    bars = {
        "weak": "█░░░░",
        "fair": "███░░",
        "good": "████░",
        "strong": "█████",
    }
    return bars.get(rating, "░░░░░")


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard (cross-platform)."""
    try:
        import subprocess

        # Try platform-specific clipboard commands
        if sys.platform == "darwin":  # macOS
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
            return True
        elif sys.platform == "win32":  # Windows
            subprocess.run(["clip"], input=text.encode(), check=True)
            return True
        else:  # Linux
            # Try wl-copy (Wayland) first, then xclip (X11)
            for cmd in [["wl-copy"], ["xclip", "-selection", "clipboard"]]:
                try:
                    proc = subprocess.run(
                        cmd, input=text.encode(), check=True, capture_output=True
                    )
                    return True
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            # Fallback: try pyperclip
            try:
                import pyperclip
                pyperclip.copy(text)
                return True
            except ImportError:
                return False
    except Exception:
        return False


def interactive_mode() -> None:
    """Run the generator in interactive mode."""
    print("\n🔐 Password Generator")
    print("=" * 40)

    try:
        length = int(input("Password length [16]: ") or "16")
    except ValueError:
        length = 16

    use_upper = input("Include uppercase? [Y/n]: ").lower() != "n"
    use_lower = input("Include lowercase? [Y/n]: ").lower() != "n"
    use_digits = input("Include digits? [Y/n]: ").lower() != "n"
    use_symbols = input("Include symbols? [Y/n]: ").lower() != "n"
    exclude_ambig = input("Exclude ambiguous chars (0, O, 1, l)? [y/N]: ").lower() == "y"

    try:
        gen = PasswordGenerator(
            length=length,
            use_uppercase=use_upper,
            use_lowercase=use_lower,
            use_digits=use_digits,
            use_symbols=use_symbols,
            exclude_ambiguous=exclude_ambig,
        )
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        return

    count = input("How many passwords? [1]: ") or "1"
    try:
        count = int(count)
    except ValueError:
        count = 1

    passwords = gen.generate(count)

    print("\n" + "=" * 40)
    for i, pwd in enumerate(passwords, 1):
        strength = estimate_strength(pwd)
        bar = strength_bar(strength["rating"])
        print(f"\n  Password {i}: {pwd}")
        print(f"  Strength: {bar} {strength['rating'].upper()}")
        print(f"  Entropy: ~{strength['entropy']} bits | Length: {strength['length']}")

    if len(passwords) == 1 and copy_to_clipboard(passwords[0]):
        print("\n📋 Copied to clipboard!")

    print()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate secure, customizable passwords.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Interactive mode
  %(prog)s -l 20                    # 20-character password
  %(prog)s -l 32 -n 5               # 5 passwords, 32 chars each
  %(prog)s -l 12 --no-symbols       # No special characters
  %(prog)s --exclude-ambiguous      # Exclude 0, O, 1, l, I
        """,
    )
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length (default: 16)")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of passwords (default: 1)")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--exclude-ambiguous", action="store_true", help="Exclude ambiguous characters (0, O, 1, l, I)")
    parser.add_argument("--no-ensure-types", action="store_true", help="Don't require at least one of each selected type")
    parser.add_argument("--copy", action="store_true", help="Copy first password to clipboard")
    parser.add_argument("--save", metavar="FILE", help="Save passwords to file")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return

    try:
        gen = PasswordGenerator(
            length=args.length,
            use_uppercase=not args.no_upper,
            use_lowercase=not args.no_lower,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous,
            ensure_all_types=not args.no_ensure_types,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    passwords = gen.generate(args.count)

    for i, pwd in enumerate(passwords, 1):
        if args.count > 1:
            print(f"{i}: ", end="")
        print(pwd)

    if passwords:
        strength = estimate_strength(passwords[0])
        if args.count == 1:
            print(f"\nStrength: {strength['rating'].upper()} (~{strength['entropy']} bits)")

        if args.copy:
            if copy_to_clipboard(passwords[0]):
                print("📋 Copied to clipboard")
            else:
                print("⚠️ Could not copy to clipboard", file=sys.stderr)

        if args.save:
            with open(args.save, "w") as f:
                f.write("\n".join(passwords) + "\n")
            print(f"💾 Saved to {args.save}")


if __name__ == "__main__":
    main()
