# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
### Bug 1: Secret number can be outside the selected difficulty range

**Input/Trigger:** Select Easy difficulty and start a game.

**Expected Behavior:** Easy mode displays a valid range of 1 to 20, so the secret number should also be between 1 and 20.

**Actual Behavior:** The Developer Debug Info showed the secret number as 72 even though Easy mode displayed a range of 1 to 20. This makes the game impossible to solve using valid guesses.

**Suspected Code Location:** The bug is likely related to the secret-number generation or difficulty configuration in `app.py` or `logic_utils.py`.


### Bug 2: Blank guesses are added to history and affect attempts

**Input/Trigger:** Leave the guess input empty and click "Submit Guess."

**Expected Behavior:** The application should display an error asking the user to enter a guess without recording the blank input or consuming an attempt.

**Actual Behavior:** The application displays "Enter a guess.", but empty strings (`""`) are still added to the History. Repeated blank submissions also affect the game's attempt state.

**Suspected Code Location:** The guess submission/validation logic in `app.py`, especially where history and attempts are updated before validating the input.


### Bug 3: Numbers outside the allowed range are accepted

**Input/Trigger:** On Easy mode (range 1 to 20), enter a number far outside the range, such as `454534`.

**Expected Behavior:** The game should reject the number and tell the user that the guess must be between 1 and 20. An invalid out-of-range guess should not produce a hint or count as a valid guess.

**Actual Behavior:** The game accepts `454534`, processes it as a guess, and displays a hint such as "Go HIGHER!" even though the number is far outside the Easy difficulty range.

**Suspected Code Location:** Input validation and hint logic in `app.py` and/or `logic_utils.py`.

### Bug Reproduction Logs

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
| --- | --- | --- | --- | --- |
| Easy mode with a new game | Secret should be between 1 and 20 | Developer Debug Info showed secret as 72 | No console error; Secret: 72 | `app.py` / `logic_utils.py`, secret generation |
| Blank input (`""`) | Show validation message without recording guess or consuming attempt | "Enter a guess." appears, but `""` is added to History and attempts are affected | No console error | `app.py`, guess submission and validation |
| `454534` on Easy mode | Reject guess because valid range is 1–20 | Guess is accepted and a hint such as "Go HIGHER!" is displayed | No console error; game eventually reports out of attempts | `app.py` / `logic_utils.py`, range validation and hint logic |

---

## 2. How did you use AI as a teammate?

I used ChatGPT as an AI teammate to help investigate the bugs, reason about the code, plan the refactoring, and design tests. I also attempted to use the AI coding assistant inside VS Code with `app.py` and `logic_utils.py` attached, but it repeatedly returned "Language model unavailable," so I could not rely on it to apply edits directly.

One AI suggestion that was correct was to investigate the `check_guess()` function for the reversed high/low hints and refactor that logic into `logic_utils.py`. After reviewing the code myself, I confirmed that a guess greater than the secret returned "Too High" but incorrectly told the player to "Go HIGHER!" I changed the hint to "Go LOWER!" and similarly corrected the "Too Low" hint. I verified the result using pytest, and all three tests passed.

I did not accept the initial testing approach as written when the tests compared the entire return value of `check_guess()` to a single string such as `"Too High"`. The function actually returns a tuple containing both the outcome and the hint message. I changed the tests to unpack `outcome, message` and verify both values separately. This was a better match for the function's actual interface, and `python -m pytest` then reported 3 passing tests.

---

## 3. Debugging and testing your fixes

- I decided a bug was fixed only after checking both the code behavior and an automated test. I did not assume that a change was correct just because the code looked reasonable.

For the high/low hint bug, I tested `check_guess(60, 50)` and verified that it returned `"Too High"` with `"Go LOWER!"`. I also tested `check_guess(40, 50)` and verified that it returned `"Too Low"` with `"Go HIGHER!"`. A winning guess of 50 against a secret of 50 was also tested. Running `python -m pytest` produced 3 passed tests.

AI helped me think about what each test should verify, but I still had to inspect the pytest failures myself. The first version of the tests failed because `check_guess()` returns a tuple instead of only an outcome string. I corrected the tests to verify both the outcome and message, then reran pytest to confirm the result.


---

## 4. What did you learn about Streamlit and state?

I learned that Streamlit reruns the Python script from top to bottom whenever the user interacts with the app. Because of this, normal variables may be recreated during a rerun, while `st.session_state` can preserve important game information such as the secret number, attempts, score, status, and history between interactions.

I would explain session state as a persistent storage area for values that need to survive Streamlit reruns. This project showed me that state also needs to be updated in the correct order. For example, changing the attempt counter before validating a guess can create incorrect behavior even though the state itself persists correctly.

## 5. Looking ahead: your developer habits

One habit I want to reuse is reproducing a bug with a specific input before changing the code, then writing a focused test for the expected behavior. This made it much easier to tell whether my change actually repaired the problem instead of creating another issue.

When working with AI on future coding tasks, I would give it one specific bug at a time and provide the relevant files and observed behavior. I would also verify every suggestion with the source code and tests instead of accepting generated code immediately. This project reinforced the importance of keeping a human in the loop when using AI for debugging.
