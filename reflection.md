# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  At first it looked all good until we started noticing the bugs.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  1.There was no consistency among the number of attempts left. 
    For example: If left side bar shows 8 attempts left, the main screen shows 7 attempts left but in reality we are only getting 6 attempts.
  2. The range of the level is not working properly, easy mode has range till 20 but the game goes till 100 irrespective of the range.
  3. Developer debug info shows the answer beforehand.
  4. New game is not allowing us to play a new game until we refresh the whole page.
  5. Hint is wrong.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  A:We have used claude code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  A: We tried to understand why the ranges are not working in the game and AI suggeted us to change the parameters in the line 136 and the ranges strted working whenever we click "NewGame".
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  A: For the range bug we got an solution but whenever we change the difficulty it 's not resetting the range automatically, we have to press newgame before we start.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
A: I have ran the pytest to see all the bugs are fixed or not and then I have run the streamlit and checked them manually to confirm the changes.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
A: The range bug seemed a bigger bug as it is not following the standard rule of the game, so I ran pytest to find easy,medium and hard ranges. Then I have played the games across all 3 difficulties to check whether the bug is resolved or not.
- Did AI help you design or understand any tests? How?
A: Yes, it showed why the bug is forming, and explained how we can changes and showed me the changes, so that I have understood why is it heppening and fixed the bug as well.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  A: Every time you click a button in Streamlit, the whole script reruns from the top. So `random.randint()` was getting called again on every click, giving a brand new secret each time. It wasn't saving the number anywhere between reruns.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  A: Imagine every time you press a button, your browser refreshes the whole page and forgets everything. That's basically what Streamlit does — it reruns the entire script. Session state is like a little notepad that survives those reruns, so you can write something on it and it'll still be there after the next refresh.

- What change did you make that finally gave the game a stable secret number?
  A: We stored the secret inside `st.session_state` using `if "secret" not in st.session_state`. That way it only gets created once on the very first load and never touched again unless the player starts a new game or switches difficulty.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  A: Writing pytest cases right after fixing a bug. Before this I would just manually test and move on, but having tests meant I could catch when fixing one thing accidentally broke something else. I want to keep doing that going forward.

- What is one thing you would do differently next time you work with AI on a coding task?
  A: I'd review the diff more carefully before accepting every change. A couple of times the AI fixed the right bug but I didn't fully understand why until later. Next time I want to actually read through what changed and make sure I can explain it myself.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  A: I used to think if the AI wrote it, it probably works. Now I know AI code can have bugs just like anyone else's code — it just hides them better because it looks clean and confident. You still have to test it and think critically about what it's actually doing.
