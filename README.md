# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game's purpose:** This project is a Streamlit number-guessing game where the player tries to identify a secret number. The game provides high/low hints, tracks attempts, and maintains a score.

- [x] **Bugs found:** During testing, I found several issues. Easy mode could generate a secret number outside its displayed 1–20 range, blank or invalid guesses could affect attempts and history, and the high/low hint messages were reversed.

- [x] **Fixes applied:** I refactored `check_guess()` from `app.py` into `logic_utils.py` and corrected the high/low hint logic. A guess that is too high now tells the player to go lower, while a guess that is too low tells the player to go higher. I also added pytest verification for the corrected behavior.

## 🎮 Demo Walkthrough

1. The user starts the Streamlit game and selects a difficulty.
2. The game displays the allowed number range and available attempts.
3. The user enters a numerical guess.
4. If the guess is greater than the secret number, the game returns **"Too High"** and tells the user **"Go LOWER!"**
5. If the guess is less than the secret number, the game returns **"Too Low"** and tells the user **"Go HIGHER!"**
6. If the guess matches the secret number, the game returns **"Win"** and displays **"🎉 Correct!"**
7. The score and game state update based on the result of the guess.
8. The game ends when the player wins or runs out of attempts.

```text
$ python -m pytest
============================= test session starts ==============================
collected 3 items

tests/test_game_logic.py ...                                      [100%]

============================== 3 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
