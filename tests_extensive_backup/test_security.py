"""
Tests for Security utilities
"""

import pytest
from unittest.mock import patch

from src.core.security import SecureRandom


class TestSecureRandom:
    """Test SecureRandom class"""

    def test_choice_with_valid_sequence(self):
        """Test choosing from a valid sequence"""
        sequence = ["a", "b", "c", "d"]
        result = SecureRandom.choice(sequence)
        assert result in sequence

    def test_choice_with_empty_sequence(self):
        """Test choosing from empty sequence raises ValueError"""
        with pytest.raises(ValueError, match="Cannot choose from empty sequence"):
            SecureRandom.choice([])

    def test_choice_with_single_element(self):
        """Test choosing from single element sequence"""
        sequence = ["only_element"]
        result = SecureRandom.choice(sequence)
        assert result == "only_element"

    def test_randint_valid_range(self):
        """Test random integer generation with valid range"""
        min_val, max_val = 1, 10
        result = SecureRandom.randint(min_val, max_val)
        assert min_val <= result <= max_val

    def test_randint_same_values(self):
        """Test random integer generation when min equals max"""
        value = 5
        result = SecureRandom.randint(value, value)
        assert result == value

    def test_randint_invalid_range(self):
        """Test random integer generation with invalid range"""
        with pytest.raises(ValueError, match="min_value must be <= max_value"):
            SecureRandom.randint(10, 5)

    def test_randint_negative_values(self):
        """Test random integer generation with negative values"""
        min_val, max_val = -10, -1
        result = SecureRandom.randint(min_val, max_val)
        assert min_val <= result <= max_val

    def test_randint_zero_range(self):
        """Test random integer generation including zero"""
        min_val, max_val = -5, 5
        result = SecureRandom.randint(min_val, max_val)
        assert min_val <= result <= max_val

    def test_random_float_basic(self):
        """Test random float generation"""
        result = SecureRandom.random_float()
        assert 0.0 <= result < 1.0

    def test_random_float_with_range(self):
        """Test random float generation with custom range"""
        min_val, max_val = 2.5, 7.5
        result = SecureRandom.random_float(min_val, max_val)
        assert min_val <= result <= max_val

    def test_random_float_invalid_range(self):
        """Test random float generation with invalid range"""
        with pytest.raises(ValueError, match="min_value must be <= max_value"):
            SecureRandom.random_float(10.0, 5.0)

    def test_random_delay_basic(self):
        """Test random delay generation"""
        min_seconds, max_seconds = 1, 5
        result = SecureRandom.random_delay(min_seconds, max_seconds)
        assert min_seconds <= result <= max_seconds

    def test_random_delay_invalid_range(self):
        """Test random delay with invalid range"""
        with pytest.raises(ValueError, match="min_seconds must be <= max_seconds"):
            SecureRandom.random_delay(10, 5)

    def test_random_delay_zero_range(self):
        """Test random delay with zero range"""
        seconds = 3
        result = SecureRandom.random_delay(seconds, seconds)
        assert result == seconds

    @patch('secrets.choice')
    def test_choice_uses_secrets(self, mock_choice):
        """Test that choice uses secrets.choice"""
        mock_choice.return_value = "mocked"
        sequence = ["a", "b", "c"]
        
        result = SecureRandom.choice(sequence)
        
        assert result == "mocked"
        mock_choice.assert_called_once_with(sequence)

    @patch('secrets.randbelow')
    def test_randint_uses_secrets(self, mock_randbelow):
        """Test that randint uses secrets.randbelow"""
        mock_randbelow.return_value = 3  # secrets.randbelow returns 0-based
        
        result = SecureRandom.randint(5, 9)  # range: 5 values (5,6,7,8,9)
        
        assert result == 8  # 5 + 3
        mock_randbelow.assert_called_once_with(5)  # range size

    def test_choice_type_preservation(self):
        """Test that choice preserves element types"""
        int_sequence = [1, 2, 3, 4, 5]
        int_result = SecureRandom.choice(int_sequence)
        assert isinstance(int_result, int)
        assert int_result in int_sequence

        str_sequence = ["hello", "world", "test"]
        str_result = SecureRandom.choice(str_sequence)
        assert isinstance(str_result, str)
        assert str_result in str_sequence

    def test_randint_large_range(self):
        """Test random integer generation with large range"""
        min_val, max_val = 1, 1000000
        result = SecureRandom.randint(min_val, max_val)
        assert min_val <= result <= max_val