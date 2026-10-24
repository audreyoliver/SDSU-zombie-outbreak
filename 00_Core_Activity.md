# SDSU: Can you survive?!?!

> **No coding experience needed.** Everything you need is already written. When you get to the computer part, you'll press **Shift + Enter** to run each box from top to bottom and change two numbers. This activity is about thinking like a mathematician, not a programmer.

## 1. Form groups and hear the story

Work in groups of 2–4 with one laptop between you.

### 🧟 Incident Report: Tonight, 6:00 p.m.

It started with the coffee.

This afternoon, a mysterious shipment of "limited-edition midterm-grading cold brew" turned up in every faculty and staff break room on campus. No return address. The label just read: *"Stay up forever."*

By 3:00, professors were grading at superhuman speed. By 5:00, they had stopped blinking. Right now, all **2,000 faculty and staff** are sitting very, very still at their desks, staring at the wall.

The Chemistry department (the few chemists who skipped the coffee) has run the numbers on the brew. Their verdict: **at exactly 7:30 p.m. tonight, every faculty and staff member who drank it will turn into a zombie.** They'll be slow, relentless, and they'll still hold office hours.

Here's the good news: none of the **40,000 students** drank the coffee (it was faculty-only, and honestly, that's the first perk that ever worked in your favor). Every student on campus is still human.

Your phone buzzes with an emergency alert:

> **SDSU ALERT:** Faculty/staff outbreak expected at **7:30 P.M.** Outside rescue teams will reach campus at **7:30 P.M. TOMORROW**. Survive 24 hours. Stay away from break rooms.

**You have about 90 minutes.** Your group has just been named the **Campus Survival Math Team**. Before 7:30, campus leadership (the parts that aren't about to become zombies) needs you to predict how the outbreak will spread and decide how to spend a small budget of resources to save as many students as you can. When the clock hits 7:30, your plan is locked in. ⏰

Three plans are on the table, and each team will investigate one:

- **Team A: The Fortress.** Barricade the GMCS building (Geology, Mathematics & Computer Science) and screen students in as fast as you safely can. Mathematicians have known all along that it's the safest building on campus.
- **Team B: The Antidote.** The Chemistry department thinks it can reverse the cold brew. Cured faculty go back to being human, and they're immune for good.
- **Team C: The Resistance.** Organize the students and fight back. The more students left standing, the stronger the resistance.

Before choosing a plan, though, you need to understand what happens if **nobody does anything**. That's what mathematicians call a **baseline**.

*Everything here (the population, the rates, the coffee) is fictional and just for the game. These are not real SDSU numbers or real emergency advice.*

## 2. Mini lesson: how mathematicians model an outbreak

### The big idea: sort everyone into boxes

Tracking 42,000 people one by one would be a nightmare. Mathematicians do something simpler: they sort everyone into a few **compartments** (boxes) and keep track of **how many people are in each box** and **how fast people move between boxes**.

The most famous version is the **SIR model**, published in 1927 by William Kermack and Anderson McKendrick. Versions of it are still used today to study flu, measles, COVID-19, and (apparently) zombies.

| Box | Stands for | In our story |
|---|---|---|
| **S** | **S**usceptible | Humans who could still get bitten |
| **I** | **I**nfectious | Active zombies who can bite people |
| **R** | **R**emoved | People who can no longer spread or catch the infection |

People flow in one direction:

$$S \;\xrightarrow{\text{bitten}}\; I \;\xrightarrow{\text{removed}}\; R$$

In a real disease, "removed" usually means someone recovered and is now immune. In our zombie scenarios, what "removed" means depends on your team's plan: sheltered, cured, or… taken out of the game. So you'll have to think carefully about who counts as a **survivor**.

### Rates of change: the "speedometer" of the outbreak

We write $t$ for the number of **hours since the outbreak**. So $t=0$ is 7:30 p.m. tonight, when the faculty turn, and $t=24$ is 7:30 p.m. tomorrow, when rescue arrives. (Quick check: what time is $t=2.5$? What about $t=16.5$?)

The symbol $\dfrac{dS}{dt}$ (say "dee S dee t") is a **rate of change**: how fast the number of susceptible humans is changing at a given moment, in **people per hour**. It's like a car's speedometer. It doesn't tell you where you are, only how fast you're moving right now.

- If $\dfrac{dS}{dt} = -500$, humans are being lost at 500 per hour *at that moment*.
- A negative rate means the box is shrinking, and a positive rate means it's growing.

### Where the infection formula comes from

How fast do zombies make new zombies? Picture campus as a big crowd where everyone mixes randomly:

1. Each zombie lunges at people at a steady pace. We call that pace **β** ("beta"), measured **per hour**.
2. Not everyone a zombie reaches can be infected. Some of them are already zombies! The fraction who are still human is $\dfrac{S}{N}$, where $N$ is the total population.
3. So each zombie creates about $\beta \cdot \dfrac{S}{N}$ new zombies per hour.
4. Multiply by the number of zombies, $I$, to get the total:

$$\text{new infections per hour} = \beta \, \frac{S \, I}{N}$$

Notice this needs **both** humans and zombies. If either $S$ or $I$ is zero, nobody gets infected. More zombies means faster spread, and so do more humans to find.

Removal works more simply: each zombie leaves the infectious box at rate **γ** ("gamma") per hour, so $\gamma I$ zombies are removed each hour. (A handy fact: $1/\gamma$ is roughly the average number of hours a zombie stays active.)

### The SIR equations

Put those flows together and you get three equations, one for each box:

$$\frac{dS}{dt}=-\beta\frac{SI}{N},\qquad
\frac{dI}{dt}=\beta\frac{SI}{N}-\gamma I,\qquad
\frac{dR}{dt}=\gamma I.$$

Read them like a bank account: **what flows in minus what flows out.**

- **S** only loses people (to infection).
- **I** gains people from infection and loses them to removal.
- **R** only gains people (from removal).

These are **differential equations**: equations about rates of change. You won't solve them by hand. The computer will chop the 24 hours into tiny slices and add up the changes very precisely. Because the model tracks *averages*, it sometimes reports decimals like 188.04 people. Think of that as "about 188."

### Bonus idea: R₀, the "zombie reproduction number"

Epidemiologists love a number called **R₀** ("R-naught"). It's the average number of people one zombie infects when almost everyone is still human. In the SIR model, $R_0 = \beta/\gamma$. If $R_0 > 1$, the outbreak grows. If $R_0 < 1$, it fizzles out. Keep this in mind when your team decides how to spend its budget: anything that lowers β or removes zombies faster pushes R₀ down.

## 3. Discuss: what does our model need?

Talk these through as a group. There are no wrong answers yet.

1. Which boxes (compartments) do we need, and what does each one mean in our story?
2. How many people start in each box at 7:30 p.m. (t = 0)? What is the total, $N$?
3. What events move people from one box to another?
4. What are we assuming? (Does everyone mix with everyone? Can zombies turn back into humans? Does anyone leave campus?)
5. When rescue arrives at 7:30 p.m. tomorrow, who counts as a **human survivor**?

## 4. Build the simplest apocalypse first

Let's start with the worst case, where **nobody fights back**. No fortress, no antidote, no resistance. Zombies are never removed, so set $\gamma = 0$.

Use these starting values:

| Quantity | Value | Meaning |
|---|---|---|
| $S(0)$ | 40,000 | Students, all human at 7:30 p.m. |
| $I(0)$ | 2,000 | Faculty/staff zombies at 7:30 p.m. |
| $R(0)$ | 0 | Nobody removed yet |
| $N$ | 42,000 | Total population |
| $\beta$ | 0.35 per hour | How aggressively zombies spread the infection |

Because $\gamma = 0$, the R box never fills up. Mathematicians call this the **SI model**, a special case of SIR.

Work through these with pencil and paper (a calculator helps):

1. Rewrite the three SIR equations with $\gamma = 0$. Which terms disappear?
2. Plug in the 7:30 p.m. starting values. How fast is each box changing at that moment, in people per hour?
3. Add your three equations together. What do you get, and why does that mean the total population never changes?
4. **Sketch** what you think $S(t)$, $I(t)$, and $R(t)$ look like from 7:30 p.m. tonight to 7:30 p.m. tomorrow. When do you think the zombies spread fastest? Does anyone survive?
5. *Optional challenge:* Estimate the situation at 8:30 p.m. Take each rate from question 2, multiply by 1 hour, and add it to the starting count. (This shortcut is called **Euler's method**. It assumes the rate stays fixed for the whole hour. Does it really?)

*Curious about code?* There's an empty box at the bottom of the notebook if you'd like to try typing your starting values. It's completely optional. The full working model will be handed out next.

## 5. Reveal: what actually happens?

Wait for the host to release **01_Baseline_Answer.ipynb**. Open it and click into the first gray box. Press **Shift + Enter** to run it and keep pressing until you reach the bottom. You'll see the computer's solution and a graph.

Talk it over:

- How close was your sketch to the real curves?
- How many students are still human when rescue arrives?
- When are zombies being created fastest?
- Compare the computer's 8:30 p.m. numbers with your Euler estimate. Why are they different? (Hint: did the rate really stay fixed for the whole hour?)

## 6. Choose your plan and save the campus

Now the host will hand your team its mission: **A (Fortress)**, **B (Antidote)**, or **C (Resistance)**.

Every team gets **4 Survival Squads** of student volunteers. That's your whole budget. Each squad gets one of two jobs:

- **🛡️ Prevention:** sweep campus with megaphones, lock doors, and set up buddy systems. This makes every zombie less effective (it lowers β). It works the same way for every team.
- **🎯 Response:** work on your team's mission: screening students into the Fortress, delivering antidote, or leading the Resistance.

You have to assign your squads by 7:30 p.m., and they stay put until rescue. In your notebook you only change **one number**, `prevention_points` (how many squads go to prevention), then rerun. Try all five splits (0, 1, 2, 3, or 4) and record how many humans survive each time. Which plan saves the most students, and *why*? Use your graphs to explain. Your team brief explains exactly what each kind of squad does.

When your table is full, report your best plan to the host. Then stay alert. The night is young, and nobody knows *everything* about that cold brew yet… 🌙

## Optional warm-up: the leaked security log

A campus security camera recorded a *different*, practice outbreak, one with randomness built in. The hour-by-hour counts are in **synthetic_baseline_log.csv**. If you finish early:

- Check that every row adds up to 42,000 people.
- Use the new infections in each row to rebuild the next row.

This log comes from a random, hour-by-hour simulation, so it won't exactly match the computer's smooth solution. Don't use it to restart or tune your team's scenario. Every mission begins fresh at 7:30 p.m. with the original numbers.
