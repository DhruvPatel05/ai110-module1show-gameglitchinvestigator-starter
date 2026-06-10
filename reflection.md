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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
