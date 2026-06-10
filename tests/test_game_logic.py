import pytest
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ==================== EXISTING TESTS ====================
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# ==================== BUG FIX TESTS ====================
# FIX: Comprehensive test suite created with AI to target specific bugs
# AI methodology: One test per bug scenario, simple assertions, clear docs
# Each test reproduces the exact error condition and verifies the fix

# Tests targeting Bug #2: Backwards Hints
class TestBackwardsHintsBug:
    """Tests for the backwards hints bug fix.
    
    FIXME: Logic breaks here - hint messages were backwards
    Original: "Too High" → "Go HIGHER!" (wrong direction)
    Fixed: "Too High" → "Go LOWER!" (correct direction)
    """
    
    def test_too_high_hint_correct_message(self):
        """Verify 'Too High' returns 'Go LOWER!' not 'Go HIGHER!'"""
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"
        assert "Go LOWER" in message, f"Expected 'Go LOWER' in message, got: {message}"
        assert "Go HIGHER" not in message, "Should not say 'Go HIGHER' when guess is too high"
    
    def test_too_low_hint_correct_message(self):
        """Verify 'Too Low' returns 'Go HIGHER!' not 'Go LOWER!'"""
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"
        assert "Go HIGHER" in message, f"Expected 'Go HIGHER' in message, got: {message}"
        assert "Go LOWER" not in message, "Should not say 'Go LOWER' when guess is too low"
    
    def test_hint_consistency_across_ranges(self):
        """Verify hints are consistent for different number ranges"""
        # Test at different magnitudes
        test_cases = [
            (100, 50, "Too High", "Go LOWER"),  # High guess, high secret
            (1, 50, "Too Low", "Go HIGHER"),    # Low guess, high secret
            (99, 1, "Too High", "Go LOWER"),    # Very high guess
            (2, 100, "Too Low", "Go HIGHER"),   # Very low guess
        ]
        
        for guess, secret, expected_outcome, expected_msg in test_cases:
            outcome, message = check_guess(guess, secret)
            assert outcome == expected_outcome
            assert expected_msg in message, f"Failed for guess={guess}, secret={secret}"


# Tests targeting Bug #1: Type Mismatch
# AI identified: secret converted to string on even attempts caused
# lexicographic comparison ("50" > "9" is False) instead of numeric
class TestTypeMismatchBug:
    """Tests for the type mismatch bug fix.
    
    FIXME: Logic breaks here - secret type mismatch bug
    Original: secret converted to str on even attempts, causing comparison failures
    Fixed: ensure both guess and secret are converted to int consistently
    """
    
    def test_string_secret_handled_correctly(self):
        """Verify that string secrets are converted to int for comparison"""
        # This simulates the edge case where secret might be passed as string
        outcome, message = check_guess(50, "50")
        assert outcome == "Win"
    
    def test_string_secret_too_high(self):
        """Verify comparison works when secret is string"""
        outcome, message = check_guess(60, "50")
        assert outcome == "Too High"
        assert "Go LOWER" in message
    
    def test_string_secret_too_low(self):
        """Verify comparison works when secret is string"""
        outcome, message = check_guess(40, "50")
        assert outcome == "Too Low"
        assert "Go HIGHER" in message
    
    def test_integer_consistency(self):
        """Verify that int(string) comparison doesn't use lexicographic ordering"""
        # This would fail with string comparison: "50" > "9" is False
        # But should work with int comparison: 50 > 9 is True
        outcome_high, _ = check_guess(50, "9")
        outcome_low, _ = check_guess(9, "50")
        
        assert outcome_high == "Too High"  # 50 > 9 correctly identified
        assert outcome_low == "Too Low"    # 9 < 50 correctly identified


# ==================== INTEGRATION TESTS ====================
# FIX: Integration tests verify bugs are fixed in real game flow
# Reproduces exact error scenarios from bug report (e.g., 44→50→48→49)
class TestGameFlowWithBugFixes:
    """Integration tests simulating actual game flow with fixed logic"""
    
    def test_logic_sequence_44_50_48_49(self):
        """Reproduce bug scenario: 44→"Higher", 50→"Lower", 48→"Higher", then 49
        
        Expected: After hints, 49 should be recognized as correct
        Bug: Game marked 49 as incorrect due to type/hint issues
        """
        secret = 49
        
        # Guess 44 - should get "Too Low" / "Go Higher"
        outcome, msg = check_guess(44, secret)
        assert outcome == "Too Low"
        assert "Go HIGHER" in msg
        
        # Guess 50 - should get "Too High" / "Go Lower"
        outcome, msg = check_guess(50, secret)
        assert outcome == "Too High"
        assert "Go LOWER" in msg
        
        # Guess 48 - should get "Too Low" / "Go Higher"
        outcome, msg = check_guess(48, secret)
        assert outcome == "Too Low"
        assert "Go HIGHER" in msg
        
        # Guess 49 - should WIN (only remaining possibility)
        outcome, msg = check_guess(49, secret)
        assert outcome == "Win", "Player should win when guessing the correct number"
    
    def test_contradictory_hints_resolved(self):
        """Verify that contradictory hint scenarios are fixed
        
        Before fix: Player might get conflicting guidance
        After fix: Guidance should always point toward correct answer
        """
        secret = 50
        
        # Series of hints that should logically narrow down answer
        hints = [
            (60, "Too High", "Go LOWER"),   # Too high, go lower
            (40, "Too Low", "Go HIGHER"),   # Too low, go higher
            (55, "Too High", "Go LOWER"),   # Too high, go lower
            (45, "Too Low", "Go HIGHER"),   # Too low, go higher
            (50, "Win", "Correct"),         # Should win on 50
        ]
        
        for guess, expected_outcome, expected_hint_word in hints:
            outcome, msg = check_guess(guess, secret)
            assert outcome == expected_outcome
            assert expected_hint_word in msg or "Correct" in msg
