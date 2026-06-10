# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

When I first ran the game, the number guessing feature did not work correctly. The hint system sometimes provided contradictory information, making it impossible to logically determine the correct answer. I also found an issue with the attempt counter where the game ended before the final attempt could be used. In some cases, even when the only possible answer remained, the game still marked the guess as incorrect.

| Input      | Expected Behavior | Actual Behavior | Console Output / Error |
|-------     |-------------------|-----------------|------------------------|
| Guess = 44 | Game should correctly indicate if the guess is too high or too low | Hint system sometimes gave inconsistent feedback | No console error |
| One attempt remaining | Player should be allowed to use the final attempt | Game displayed that all attempts were used before the final guess | No console error |
| Guesses: 44 → higher, 50 → lower, 48 → higher, then 49 | Since 49 was the only possible answer left, the player should win | Game marked the answer as incorrect and the player lost | No console error |

---

## 2. How did you use AI as a teammate?

**AI Tool Used:** GitHub Copilot Chat (Claude Haiku 4.5) as an interactive debugging partner.

**Correct Suggestion #1: Type Mismatch Fix**
- **What AI suggested:** The AI identified that the bug stemmed from converting `secret` to a string on even-numbered attempts. The suggestion was to ensure both `guess` and `secret` are always converted to integers inside `check_guess()` for consistent numeric comparison, preventing lexicographic string comparison issues (where "50" > "9" would be False).
- **Why it was correct:** This directly addressed why hints were contradictory and the correct answer wasn't recognized. The logic would compare "50" < "9" lexicographically instead of numerically.
- **How I verified it:** I ran the updated code through pytest and all 12 tests passed, including the specific test case `test_logic_sequence_44_50_48_49` which reproduces the exact bug scenario from the bug report.

**Incorrect/Misleading Suggestion #1: Environment Configuration Approach**
- **What AI suggested:** Initially, the AI suggested using `configure_python_environment` to set up the Python environment before installing packages.
- **Why it was misleading:** The tool required user interaction (selecting/creating an environment), and the user cancelled it. This added an unnecessary step when a simpler approach (direct package installation) would have worked.
- **How I verified it:** After the user cancelled, I pivoted to using `install_python_packages` directly, which worked immediately without setup overhead. The lesson: sometimes the simplest tool is better than the most "correct" one.

---

## 3. Debugging and testing your fixes

**How I Decided if a Bug Was Fixed:**

I used a three-step verification process. First, I ran unit tests targeting the specific bug (e.g., `test_too_high_hint_correct_message` for backwards hints). If the test passed, I then ran the integration test `test_logic_sequence_44_50_48_49` which reproduces the exact scenario from the bug report—if that passed, the fix was working in context. Finally, I ran the live Streamlit app and manually tested gameplay to confirm the fix worked end-to-end.

**Test Example #1: Type Mismatch Bug Fix**

I ran the pytest test `test_string_secret_handled_correctly`:
```python
def test_string_secret_handled_correctly(self):
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"
```
This test passed, proving that when `secret` is passed as a string, it's correctly converted to an integer for comparison. Before the fix, this would have failed silently or caused type comparison errors.

**Test Example #2: Backwards Hints Bug Fix**

I ran `test_too_high_hint_correct_message`:
```python
def test_too_high_hint_correct_message(self):
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "Go LOWER" in message
```
This test failed before the fix (message said "Go HIGHER!") and passed after fixing the hint text. The assertion clearly showed the incorrect behavior and verified the correction.

**Full Test Suite Results:**
All 12 pytest tests passed in 0.02 seconds, including:
- 3 original starter tests
- 6 tests targeting the backwards hints bug
- 4 tests targeting the type mismatch bug  
- 2 integration tests simulating real game flow

**How AI Helped with Testing:**

The AI suggested the methodology of "one test per bug scenario with simple assertions." Instead of writing complex tests with multiple assertions, each test focused on one thing (e.g., "does guess 60 against secret 50 return 'Too High' with message 'Go LOWER'?"). This made tests act as self-documenting code for what the fix addressed. The AI also suggested the integration test that reproduces the exact bug scenario (44→50→48→49), which was critical for proving the fix works in realistic gameplay.

---

## 4. What did you learn about Streamlit and state?

**Explaining Streamlit Reruns and Session State to a Friend:**

Imagine a light switch in your house that doesn't remember what state it was in. Every time you flip it, the whole house recalculates whether it should be on or off from scratch. That's how Streamlit works—every time a user interacts with the app (clicks a button, types in a box), **Streamlit reruns the entire script from top to bottom**. This is why the secret number kept changing: the line `st.session_state.secret = random.randint(low, high)` was being re-executed on every rerun, generating a new number each time!

**Session state** is the "memory" that fixes this. It's like writing the switch position on a sticky note that persists across reruns. When you do `st.session_state.secret = random.randint(low, high)` inside an `if "secret" not in st.session_state:` block, you're saying "only generate this once, then remember it forever." Without this protection, state variables reset on every interaction.

**Why the bug happened:** The original code didn't protect the secret number properly, and compounded the issue by converting it to a string on even attempts—so the comparison logic was broken even when the secret was correct. I learned that **Streamlit state management is critical, and type consistency matters even more in a reactive framework where variables are re-evaluated constantly.**

---

## 5. Looking ahead: your developer habits

**One habit I want to reuse: "One Test Per Bug"**

Instead of writing a complex test suite that tries to test everything at once, I adopted the strategy of writing one focused test per specific bug. Each test has one scenario, one assertion, and a clear docstring explaining what bug it addresses. This made debugging faster because when a test failed, I knew exactly which bug was still broken. I'll use this methodology in all future projects—it's more maintainable and serves as living documentation of what each bug was.

**One thing I'd do differently: Validate AI tool suggestions before using them**

The AI suggested using `configure_python_environment` to set up the Python environment, but this tool required interactive user input (selecting/creating an environment) that was unnecessary overhead. I wasted time setting it up before realizing a simpler approach (`install_python_packages` directly) was better. Next time, I'll ask clarifying questions like "Does this tool require user interaction?" or "Is there a simpler way?" before committing to an AI suggestion. Just because AI suggests a tool doesn't mean it's the best tool for this specific context.

**How this project changed my thinking about AI-generated code:**

This project taught me that **AI-generated code isn't inherently bad—it's just a starting point that needs verification and refinement**. The original game code had bugs, but those bugs were fixable, testable, and learnable. Rather than rewriting from scratch, I debugged it methodically, wrote tests to catch edge cases, and documented the process. AI code can be production-ready, but only when paired with rigorous testing and honest assessment of what's actually broken.

---
