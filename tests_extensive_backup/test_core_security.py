"""
Tests for Core Security Module
"""

import pytest
from src.core.security import SecureRandom


class TestSecureRandom:
    """Test SecureRandom functionality"""

    def test_choice_basic(self):
        """Test basic choice functionality"""
        sequence = [1, 2, 3, 4, 5]
        result = SecureRandom.choice(sequence)
        assert result in sequence

    def test_choice_string_sequence(self):
        """Test choice with string sequence"""
        sequence = "abcdef"
        result = SecureRandom.choice(sequence)
        assert result in sequence

    def test_choice_single_element(self):
        """Test choice with single element"""
        sequence = [42]
        result = SecureRandom.choice(sequence)
        assert result == 42

    def test_choice_empty_sequence_raises_error(self):
        """Test choice with empty sequence raises error"""
        with pytest.raises(ValueError, match="Cannot choose from empty sequence"):
            SecureRandom.choice([])

    def test_randint_basic(self):
        """Test basic randint functionality"""
        result = SecureRandom.randint(1, 10)
        assert 1 <= result <= 10
        assert isinstance(result, int)

    def test_randint_same_values(self):
        """Test randint with same min and max"""
        result = SecureRandom.randint(5, 5)
        assert result == 5

    def test_randint_negative_range(self):
        """Test randint with negative values"""
        result = SecureRandom.randint(-10, -1)
        assert -10 <= result <= -1

    def test_randint_zero_range(self):
        """Test randint including zero"""
        result = SecureRandom.randint(-5, 5)
        assert -5 <= result <= 5

    def test_randint_large_range(self):
        """Test randint with large range"""
        result = SecureRandom.randint(1, 1000000)
        assert 1 <= result <= 1000000

    def test_random_float_basic(self):
        """Test basic random float functionality"""
        result = SecureRandom.random_float()
        assert 0.0 <= result <= 1.0
        assert isinstance(result, float)

    def test_random_float_multiple_calls(self):
        """Test multiple random float calls produce different values"""
        results = [SecureRandom.random_float() for _ in range(10)]
        # Very unlikely all results are the same
        assert len(set(results)) > 1

    def test_random_delay_basic(self):
        """Test random delay functionality"""
        min_delay = 1
        max_delay = 5
        result = SecureRandom.random_delay(min_delay, max_delay)
        assert min_delay <= result <= max_delay
        assert isinstance(result, int)

    def test_random_delay_same_values(self):
        """Test random delay with same min and max"""
        delay = 2
        result = SecureRandom.random_delay(delay, delay)
        assert result == delay

    def test_random_delay_integer_input(self):
        """Test random delay with integer input"""
        result = SecureRandom.random_delay(1, 3)
        assert 1 <= result <= 3
        assert isinstance(result, int)

    def test_random_delay_large_range(self):
        """Test random delay with large range"""
        result = SecureRandom.random_delay(1, 100)
        assert 1 <= result <= 100

    def test_random_delay_precision(self):
        """Test random delay error handling"""
        with pytest.raises(ValueError):
            SecureRandom.random_delay(5, 1)  # min > max should raise error

    def test_consistency_across_calls(self):
        """Test that multiple calls produce reasonable distribution"""
        # Test choice consistency
        choices = [SecureRandom.choice([1, 2, 3, 4, 5]) for _ in range(100)]
        unique_choices = set(choices)
        assert len(unique_choices) > 1  # Should get variety

        # Test randint consistency  
        randints = [SecureRandom.randint(1, 10) for _ in range(100)]
        unique_randints = set(randints)
        assert len(unique_randints) > 1  # Should get variety

        # Test random float consistency
        floats = [SecureRandom.random_float() for _ in range(100)]
        unique_floats = set(floats)
        assert len(unique_floats) > 50  # Should get lots of variety

    def test_security_properties(self):
        """Test security properties of random generation"""
        # Test that we don't get predictable patterns
        sequence1 = [SecureRandom.randint(1, 100) for _ in range(20)]
        sequence2 = [SecureRandom.randint(1, 100) for _ in range(20)]
        
        # Sequences should be different (extremely unlikely to be identical)
        assert sequence1 != sequence2

        # Test float sequences are different
        float_seq1 = [SecureRandom.random_float() for _ in range(10)]
        float_seq2 = [SecureRandom.random_float() for _ in range(10)]
        assert float_seq1 != float_seq2

    def test_edge_cases(self):
        """Test edge cases for random functions"""
        # Test with very small ranges
        result = SecureRandom.random_float(0.0001, 0.0002)
        assert 0.0001 <= result <= 0.0002

        # Test with very large numbers
        result = SecureRandom.randint(1000000, 1000001)
        assert result in [1000000, 1000001]

        # Test choice with complex objects
        objects = [{"a": 1}, {"b": 2}, {"c": 3}]
        result = SecureRandom.choice(objects)
        assert result in objects

    def test_uniform_method(self):
        """Test uniform method"""
        result = SecureRandom.uniform(1.5, 2.5)
        assert 1.5 <= result <= 2.5
        assert isinstance(result, float)

    def test_shuffle_method(self):
        """Test shuffle method"""
        original = [1, 2, 3, 4, 5]
        to_shuffle = original.copy()
        SecureRandom.shuffle(to_shuffle)
        
        # Should contain same elements
        assert set(to_shuffle) == set(original)
        # Length should be same
        assert len(to_shuffle) == len(original)