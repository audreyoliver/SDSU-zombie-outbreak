# Team B: The Antidote 🧪

### Mission briefing

Not every chemist drank the coffee. A few survivors in the Chemistry building have been working nonstop, and they've cooked up an antidote they call **Decaf-X**.

One dose turns a zombie back into a regular human. Even better, cured people are **immune for good**. Apparently you can only get turned by bad coffee once.

Your plan: **track down zombies and cure them.** Every faculty member you cure is one less zombie biting students *and* one more human survivor.

The catch: Decaf-X takes time to make and deliver. Your squads can only cure so many zombies per hour, and meanwhile the zombies keep making new zombies.

### What your response squads do

Each response squad is an **antidote team** that mixes Decaf-X, tracks down zombies, and doses them. One team can cure about **120 zombies per hour**. With all 4 squads, that's **480 per hour**.

Cures slow down when **hardly any zombies are left**, because they get hard to find.

### Your model: three boxes

| Box | Meaning | At 7:30 p.m. |
| --- | --- | --- |
| **S** | Humans who could still get bitten | 40,000 |
| **I** | Zombies | 2,000 |
| **R** | Cured humans, immune for good | 0 |

$$S \;\xrightarrow{\text{bitten}}\; I \;\xrightarrow{\text{cured}}\; R$$

This is the same S → I → R flow from the SIR lesson! The only difference is how zombies leave I. Instead of the usual $\gamma I$, they're removed at a fixed number per hour, set by your antidote supply.

### The equations

Bites per hour:

$$B=\beta\,\frac{S\,I}{42000}$$

Cures per hour are your full capacity, unless there aren't enough zombies left to fill it:

$$C=\min\left(c,\;\frac{I}{\tau}\right),\qquad c = 120r$$

- $c$ is how many cures your teams can deliver per hour.
- $I/\tau$: you can't cure zombies that don't exist. With $\tau = 1$ hour (leave it fixed), cures slow down smoothly as zombies run out.

The rates of change:

$$\frac{dS}{dt}=-B,\qquad\frac{dI}{dt}=B-C,\qquad\frac{dR}{dt}=C$$

Look at $dI/dt$. The zombie count grows when bites outpace cures and shrinks when cures outpace bites. That tug-of-war decides everything.

### Who survives?

**Survivors = S(24) + R(24)**: humans who were never bitten *plus* everyone you cured. Cured faculty and staff count too, so divide by **42,000** (everyone on campus) to get your survival percentage.

### Think about it before you run

- With no prevention, zombies bite about 667 students per hour at 7:30 p.m. (you calculated this for the baseline!). Even with all 4 squads curing, you max out at 480 per hour. What could prevention do to that 667?
- Why do cured faculty count as survivors here, while captured zombies don't count for Team C?
- Check: why does S + I + R always equal 42,000?

## Your budget: 4 Survival Squads

Campus leadership has rounded up **4 Survival Squads** of student volunteers for your team. That's your whole budget. You have to decide where each squad goes **before 7:30 p.m.** Once the outbreak starts, nobody can be reassigned. (Phones are down, and nobody wants to cross campus at midnight to deliver a message.)

Each squad gets one of two jobs:

- **🛡️ Prevention squads** sweep campus with megaphones and group chats. They lock doors, set up buddy systems, and teach everyone the golden rule: *never go to office hours alone.* Prevention works the same way for every team: it makes every zombie less effective by lowering **β**, the infection rate.
- **🎯 Response squads** work on your team's mission (see your mission briefing above).

If you put **p** squads on prevention, you have **r = 4 − p** left for response.

### What prevention actually buys you

The formula is β = 0.12 + 0.23 × (0.30)^p per hour. You don't need to memorize it. This table shows what it means:

| Prevention squads (p) | Response squads (r) | β (per hour) | One zombie bites someone about every… |
| --- | --- | --- | --- |
| 0 | 4 | 0.350 | 2.9 hours |
| 1 | 3 | 0.189 | 5.3 hours |
| 2 | 2 | 0.141 | 7.1 hours |
| 3 | 1 | 0.126 | 7.9 hours |
| 4 | 0 | 0.122 | 8.2 hours |

(The last column is 1/β. It assumes the zombie is surrounded by humans, which is true at the start.)

Notice the pattern. The **first** prevention squad makes a huge difference, and each extra squad helps less and less. This is called **diminishing returns**. Even with all 4 squads on prevention, zombies still spread, because you can't lock *every* door. So the real question is this: **when does one more prevention squad stop being worth it, compared with sending it on your mission?**

*All of these numbers are invented game rules, not real emergency science.*

## Your task: test every plan

There are only five possible plans, so you can test **all** of them. That makes this an optimization problem you can solve completely!

**Use the code boxes in your team's notebook to run your model and generate your results.** They're already written, so you don't have to code anything. You only change one number:

| Code box | What it does | Do you change anything? |
| --- | --- | --- |
| 1. Setup | Loads the math tools | No |
| 2. Model equations | Your team's equations from above, written in code | No |
| 3. Parameters | Sets the starting numbers and runs the simulation | **Yes: `prevention_points`** |
| 4. Visualize | Draws the graph of humans and zombies over 24 hours | No |
| 5. Results | Prints your number of survivors | No, but read your answer here! |
| 6. Your answers | A text box for your results table and answers | **Yes: double-click it to type** |

1. Click into box 1 and press **Shift + Enter**. Do the same for box 2. You only need to run these once.
2. In box 3, find the line `prevention_points = 2` between the rows of `#` signs (under `CHANGE THIS ONE NUMBER`) and change the 2 to a **0**. Leave `nighttime_bonus = False` alone for now. (`response_points` updates automatically: whatever squads aren't on prevention go on your mission.)
3. Run boxes 3, 4, and 5 in order. Box 5 prints **Human survivors at rescue** and the **Survivor percentage**. Write both in the table below, and look at your graph.
4. Go back to box 3, change `prevention_points` to **1**, and rerun boxes 3, 4, and 5. Repeat for **2**, **3**, and **4**.

*Tip:* If anything looks strange or you get an error, use **Kernel → Restart & Run All** (Jupyter) or **Runtime → Run all** (Google Colab) to start fresh.

| Prevention squads (p) | Response squads (r) | Human survivors at rescue | Survival % |
| --- | --- | --- | --- |
| 0 | 4 | | |
| 1 | 3 | | |
| 2 | 2 | | |
| 3 | 1 | | |
| 4 | 0 | | |

### Report back to campus leadership

Be ready to tell everyone:

- Your **best plan**: how many squads on prevention, and how many on your mission?
- **Why** it works. Point to something on your graph.
- One way our model is **unrealistic**, and how you might improve it.

When your table is full, tell the host your best plan. Then head to the end of your notebook, where there's a 🛑 STOP sign. Don't go past it until the host says so!

---

# 🛑 STOP HERE

**Don't go past this point yet!** First finish your normal-night table and tell the host your best plan. Wait here until the host announces breaking news.

---

# 🌙 BREAKING NEWS: The Night Twist

### 9:58 p.m. — Urgent update from the Chemistry department

*"We made a mistake in our analysis. The cold brew's caffeine peaks overnight. From **10 p.m. to 4 a.m.**, the zombies will be wide awake, jittery, and **twice as aggressive**. Repeat: twice as aggressive. Get ready."*

Zombies are **night owls**. Between 10 p.m. and 4 a.m., β (the infection rate) **doubles**. That window opens only **2.5 hours** after the outbreak, while the horde is still growing. After 4 a.m., everything goes back to normal.

Your squads are already deployed, so you can't change tonight's plan. But campus leadership wants to know: **if you had known about this at 7:30 p.m., would you have assigned your squads differently?**

## Test the night twist

The last code box in your notebook is a complete copy of your model with **night-owl zombies switched on**. You don't need to change anything above it.

1. In that box, set `prevention_points = 0` and press **Shift + Enter**.
2. Record the survivors in the table below.
3. Repeat for 1, 2, 3, and 4.

The gray band on the graph marks the night-owl hours. Watch what happens to the zombie curve inside it.

## Night-twist results

| Prevention squads (p) | Response squads (r) | Survivors: normal night (copy from before) | Survivors: night-owl zombies |
| --- | --- | --- | --- |
| 0 | 4 | | |
| 1 | 3 | | |
| 2 | 2 | | |
| 3 | 1 | | |
| 4 | 0 | | |

## Report back

- Did your **best plan** change? If so, why?
- Which plan got hurt the **most** by the twist? Use your graph to explain.
- Why does it matter that the dangerous hours come so **early** in the outbreak? What if they came at the very end instead?
