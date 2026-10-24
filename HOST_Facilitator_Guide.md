# Host guide: SDSU, Can you survive?!?!

This is a club event for students with no coding experience. Students reason about the math, and the notebooks do all the computing. Everything here is fictional: the population, rates, and capacities are game rules, not SDSU statistics or emergency guidance.

## Story at a glance

- **6:00 p.m. (event start):** All 2,000 faculty/staff drank a mysterious "midterm-grading cold brew." Chemistry predicts they will turn into zombies at **7:30 p.m.** The 40,000 students did not drink it.
- **The countdown:** The roughly 90-minute activity *is* the countdown. Teams must lock in a plan before 7:30 p.m.
- **Rescue:** 7:30 p.m. tomorrow, 24 hours after the outbreak. The model clock t counts hours since 7:30 p.m. (t=0 → 7:30 p.m., t=2.5 → 10 p.m., t=8.5 → 4 a.m., t=16.5 → noon, t=24 → rescue).
- **Teams:** A, The Fortress (barricade GMCS); B, The Antidote (Decaf-X cure); C, The Resistance (students capture zombies and lock them in a parking-structure basement).
- **Plot twist:** "Night-owl zombies" are twice as aggressive from 10 p.m. to 4 a.m.

## Schedule (about 90 minutes)

1. Form teams of 2–4 with one laptop each (5 minutes).
2. Read the story aloud (dramatic delivery encouraged) (5).
3. SIR mini lesson from the core handout: compartments, rates of change, where βSI/N comes from, R₀ (15).
4. Discussion questions: boxes, starting values, assumptions, who counts as a survivor (5).
5. The simplest apocalypse: with gamma=0, teams rewrite the equations, compute the 7:30 p.m. rates, sketch the curves, and optionally do one Euler step to 8:30 p.m. (15).
6. Release 01_Baseline_Answer.ipynb, run it together, and compare it with the sketches and the Euler estimate (5).
7. Hand out team briefs and notebooks. Teams test all five squad assignments for a normal night, fill in their table, and tell you their best plan. Students should stop at the 🛑 STOP sign at the end of the notebook (25).
8. Once every team has reported, announce the breaking news (the “9:58 p.m. update from Chemistry”). Teams scroll past the 🛑 STOP sign at the end of their notebook, read the night twist, run the night-twist code box for all five plans, and report whether their best plan changed (15).

## Key numbers for the baseline (no response)

Rates at 7:30 p.m.: dS/dt=-666.666667, dI/dt=666.666667, dR/dt=0 people/hour. One Euler step to 8:30 p.m. gives S=39,333.333333 and I=2,666.666667. The exact solution differs because S and I change continuously during the hour. The baseline leaves approximately 188.04 uninfected humans at rescue.

## The budget: 4 Survival Squads

Each team has 4 Survival Squads (in the code, `prevention_points` = p and `response_points` = r = 4 − p). Squads are whole numbers, assigned before the outbreak, and fixed for all 24 hours, so there are exactly five plans.

| Squad type | What it does in the story | What it does in the model |
| --- | --- | --- |
| Prevention (all teams) | Megaphones, locked doors, buddy systems | beta_day = 0.12 + 0.23 × 0.30^p (0.350, 0.189, 0.141, 0.126, 0.122): diminishing returns |
| Response, Team A | Screening checkpoint at a GMCS door | Admissions up to 125r students/hour (max 500), shelter capacity 10,000 |
| Response, Team B | Antidote team delivering Decaf-X | Cures up to 120r zombies/hour |
| Response, Team C | Trains and leads student fighters | Captures = 0.005r × S per hour, so capture power shrinks as students are bitten |

Testing all five plans is a complete search of this choice set. It does not consider changing squad assignments over time. There is no target percentage; the goal is to maximize human survivors at rescue.

## Survivor definitions

| Team | Survivors | Percentage out of |
| --- | --- | --- |
| A: The Fortress | S + H (outside humans + sheltered) | 40,000 |
| B: The Antidote | S + R (never bitten + cured faculty/staff) | 42,000 |
| C: The Resistance | S only (captured zombies are still zombies) | 40,000 |

Don't compare raw scores across teams; each scenario has different rules. Reward correct interpretation, testing all five plans, and clear explanations of the tradeoffs.

## Answer tables

HOST_Results.csv contains full precision. Decimal values are model averages (for example, a tiny decimal I is not literally a fraction of a zombie).

### Team A: The Fortress

| Prevention squads | Response squads | Normal night survivors | Night-owl survivors |
| --- | --- | --- | --- |
| 0 | 4 | 9,222 | 6,371 |
| 1 | 3 | 14,747 | 10,000 |
| 2 | 2 | 20,785 | 13,925 |
| 3 | 1 | 22,268 | 15,134 |
| 4 | 0 | 21,745 | 14,310 |

Best normal night: 3 prevention, 1 response squads; 22,268 survivors (55.7%).

Best night-owl: 3 prevention, 1 response squads; 15,134 survivors (37.8%).

### Team B: The Antidote

| Prevention squads | Response squads | Normal night survivors | Night-owl survivors |
| --- | --- | --- | --- |
| 0 | 4 | 13,580 | 11,707 |
| 1 | 3 | 41,998 | 20,044 |
| 2 | 2 | 37,926 | 25,173 |
| 3 | 1 | 29,435 | 20,430 |
| 4 | 0 | 21,745 | 14,310 |

Best normal night: 1 prevention, 3 response squads; 41,998 survivors (100.0%).

Best night-owl: 2 prevention, 2 response squads; 25,173 survivors (59.9%).

### Team C: The Resistance

| Prevention squads | Response squads | Normal night survivors | Night-owl survivors |
| --- | --- | --- | --- |
| 0 | 4 | 37,506 | 1,287 |
| 1 | 3 | 38,880 | 38,049 |
| 2 | 2 | 38,660 | 35,257 |
| 3 | 1 | 31,348 | 21,026 |
| 4 | 0 | 21,745 | 14,310 |

Best normal night: 1 prevention, 3 response squads; 38,880 survivors (97.2%).

Best night-owl: 1 prevention, 3 response squads; 38,049 survivors (95.1%).

## Talking points for the reports

- **Diminishing returns:** The first prevention squad cuts β almost in half; later squads help far less. Where does each team's best plan stop adding prevention?
- **The twist changes things:** Compare each team's best plan with and without night-owl zombies. Because the 10 p.m.–4 a.m. window starts only 2.5 hours after the outbreak, it hits while the horde is still growing. Look for plans whose survivors collapse under the twist and plans whose best choice shifts.
- **Survivor definitions matter:** Why do cured faculty count for Team B but captured zombies don't count for Team C?
- **Model limitations:** Everyone mixes randomly, nobody leaves campus, fighting causes no injuries, the shelter never fails, and squads can't be reassigned.

## Modeling notes (for the host)

- Infection and responses are simultaneous continuous flows, solved with SciPy's odeint. Capacities are rates in people/hour.
- A fixed-rate flow can't continue once its source box is empty, so each response uses a fixed response_time τ = 1 hour as a per-person upper limit. This makes flows taper smoothly instead of driving populations negative. Keep τ fixed.
  - A: admissions = min(v, (K−H)/τ, S/τ), with negative inputs clipped to zero. GMCS never exceeds 10,000 and approaches capacity gradually.
  - B: cures = min(c, I/τ). Full capacity while zombies are plentiful, tapering when few remain.
  - C: captures = min(aS, I/τ).
- N stays at the reference value 42,000. S+I+H, S+I+R, or S+I+D always totals 42,000. Sheltered, cured, and captured people don't transmit. There is no reinfection, no new arrivals, no fighting casualties, and no shelter breaches. Zero response squads means no team response.
- The night-owl twist doubles β for 2.5 ≤ t < 8.5 only. Output is every 0.1 hour; odeint uses finer internal steps (hmax = 0.05) so it can't skip the switch, and every result was checked against an independent solve split at t=2.5 and t=8.5.
- The printed peak is the largest sampled zombie count within the 24 hours, not necessarily the all-time peak. Peak times are read from the time array, not the array index.

## Practical tips for a no-coding audience

- Students change only one number, `prevention_points`: in the main settings box for the normal night, and in the night-twist box at the end for the twist. If something breaks, use **Kernel → Restart & Run All** (Jupyter) or **Runtime → Run all** (Google Colab).
- Laptops need Python with NumPy, SciPy, and Matplotlib. Test before the event. Google Colab has all three built in and runs the .ipynb files in a browser, which avoids installation problems.
- Team A has the most complex equation (a three-way min). Consider giving it to a team that enjoys a puzzle.
- One laptop per team is enough. Have one person drive while the others record results and read the graph.

## Files

- 00_Core_Activity (.md/.ipynb): story, SIR lesson, discussion, baseline exercise. Hand out at the start.
- 01_Baseline_Answer (.py/.ipynb): release after step 5.
- Group_A/B/C_Brief.md and Group_A/B/C (.py/.ipynb): one set per team. Each notebook opens with its brief. The normal-night experiment comes first; the night twist sits after a 🛑 STOP sign at the end, with its own code box.
- synthetic_baseline_log.csv: optional early-finisher warm-up ("leaked security log"). It is a random hourly simulation (beta=0.35, no removal, random.Random(340), Bernoulli infections with start-of-hour probability beta*I/42000), not the ODE trajectory. No fitting needed.
- HOST_*: this guide, full results, and preview plots. Keep them away from students.
- refresh_ode_models.py: regenerates the scripts, notebooks, briefs, previews, results, this guide, and the zip. It keeps any existing 00_Core_Activity files and the practice log.
