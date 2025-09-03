"""
Security utilities for cryptographically secure operations
"""

import secrets
from collections.abc import Sequence
from typing import Any


class SecureRandom:
    """Cryptographically secure random number generator"""

    @staticmethod
    def choice(sequence: Sequence[Any]) -> Any:
        """Securely choose a random element from a non-empty sequence"""
        if not sequence:
            raise ValueError("Cannot choose from empty sequence")
        return secrets.choice(sequence)

    @staticmethod
    def randint(min_value: int, max_value: int) -> int:
        """Return a random integer N such that min_value <= N <= max_value"""
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")

        # Use secrets.randbelow for secure random generation
        range_size = max_value - min_value + 1
        return min_value + secrets.randbelow(range_size)

    @staticmethod
    def uniform(min_value: float, max_value: float) -> float:
        """Return a random floating point number N such that min_value <= N <= max_value"""
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")

        # Generate secure random bytes and convert to float in range [0, 1)
        random_bytes = secrets.randbits(32)
        random_float = random_bytes / (2**32)

        # Scale to desired range
        return min_value + random_float * (max_value - min_value)

    @staticmethod
    def shuffle(sequence: list) -> None:
        """Shuffle the sequence in place using cryptographically secure random"""
        # Fisher-Yates shuffle with secure random
        for i in range(len(sequence) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            sequence[i], sequence[j] = sequence[j], sequence[i]
