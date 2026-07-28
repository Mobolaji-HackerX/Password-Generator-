"""Unit tests for the password generator."""

import string
import pytest
from password_generator import PasswordGenerator, estimate_strength


class TestPasswordGenerator:
    def test_default_length(self):
        gen = PasswordGenerator()
        passwords = gen.generate()
        assert len(passwords[0]) == 16

    def test_custom_length(self):
        gen = PasswordGenerator(length=32)
        passwords = gen.generate()
        assert len(passwords[0]) == 32

    def test_multiple_passwords(self):
        gen = PasswordGenerator()
        passwords = gen.generate(count=5)
        assert len(passwords) == 5
        assert len(set(passwords)) == 5  # All unique

    def test_lowercase_only(self):
        gen = PasswordGenerator(
            length=20,
            use_uppercase=False,
            use_digits=False,
            use_symbols=False,
        )
        pwd = gen.generate()[0]
        assert all(c in string.ascii_lowercase for c in pwd)

    def test_uppercase_only(self):
        gen = PasswordGenerator(
            length=20,
            use_lowercase=False,
            use_digits=False,
            use_symbols=False,
        )
        pwd = gen.generate()[0]
        assert all(c in string.ascii_uppercase for c in pwd)

    def test_digits_only(self):
        gen = PasswordGenerator(
            length=20,
            use_lowercase=False,
            use_uppercase=False,
            use_symbols=False,
        )
        pwd = gen.generate()[0]
        assert all(c in string.digits for c in pwd)

    def test_symbols_only(self):
        gen = PasswordGenerator(
            length=20,
            use_lowercase=False,
            use_uppercase=False,
            use_digits=False,
        )
        pwd = gen.generate()[0]
        assert all(c in PasswordGenerator.SYMBOLS for c in pwd)

    def test_ensure_all_types(self):
        gen = PasswordGenerator(length=10, ensure_all_types=True)
        pwd = gen.generate()[0]
        assert any(c.islower() for c in pwd)
        assert any(c.isupper() for c in pwd)
        assert any(c.isdigit() for c in pwd)
        assert any(c in PasswordGenerator.SYMBOLS for c in pwd)

    def test_exclude_ambiguous(self):
        gen = PasswordGenerator(
            length=100,
            exclude_ambiguous=True,
        )
        pwd = gen.generate()[0]
        for char in PasswordGenerator.AMBIGUOUS:
            assert char not in pwd

    def test_empty_pool_raises(self):
        with pytest.raises(ValueError):
            PasswordGenerator(
                use_lowercase=False,
                use_uppercase=False,
                use_digits=False,
                use_symbols=False,
            )

    def test_too_short_for_types(self):
        with pytest.raises(ValueError):
            gen = PasswordGenerator(length=2, ensure_all_types=True)
            gen.generate()


class TestStrengthEstimator:
    def test_weak_password(self):
        result = estimate_strength("abc")
        assert result["rating"] == "weak"

    def test_strong_password(self):
        result = estimate_strength("K9#mPx$vL2@nQfR5")
        assert result["rating"] == "strong"
        assert result["length"] == 16
        assert result["variety"] == 4

    def test_entropy_calculation(self):
        result = estimate_strength("a" * 20)
        assert result["entropy"] > 0
        assert result["has_lower"]
        assert not result["has_upper"]
