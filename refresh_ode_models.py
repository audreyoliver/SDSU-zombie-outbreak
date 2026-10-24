"""Create the ODE-format model scripts, notebooks, and host results."""
from pathlib import Path
import contextlib, csv, io, json, zipfile, os

ROOT=Path(__file__).resolve().parent
OUT=ROOT if (ROOT/'00_Core_Activity.md').exists() else ROOT/'SDSU_Zombie_Event'
OUT.mkdir(exist_ok=True)
os.environ.setdefault('MPLBACKEND','Agg')

def section(title):
    return '# ' + '='*78+'\n# '+title+'\n# '+'='*78+'\n'

def make_script(group):
    baseline=group=='BASELINE'
    title='BASIC SIR MODEL: NO RESPONSE' if baseline else f'GROUP {group}: '+{'A':'THE FORTRESS (GMCS SAFE ZONE)','B':'THE ANTIDOTE (CURE WITH IMMUNITY)','C':'THE RESISTANCE (CAPTURE THE ZOMBIES)'}[group]
    setup=section('1. SETUP AND INTRODUCTION')+f'''# {title}
# Outbreak: 7:30 p.m. tonight. Rescue: 7:30 p.m. tomorrow (24 hours).
# Fictional population: 40,000 susceptible students and 2,000 zombies.
# All rates, resources, and GMCS capacity are invented game assumptions.
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

print("Libraries imported successfully!")
'''
    if baseline:
        function='''# S: susceptible humans; I: active zombies; R: removed individuals.
# In this no-response baseline, gamma = 0, so R stays zero.
def sir_model(y, t, N, beta, gamma):
    """Return the rates of change (people/hour) of S, I, and R.

    beta and gamma have units 1/hour; t is hours since the 7:30 p.m. outbreak.
    beta*S/N is the infection rate generated per active zombie.
    beta is not the number infected regardless of susceptibility.
    """
    S, I, R = y
    new_infections = beta * S * I / N
    new_removals = gamma * I
    dS_dt = -new_infections
    dI_dt = new_infections - new_removals
    dR_dt = new_removals
    return dS_dt, dI_dt, dR_dt

print("Basic SIR model function defined.")
'''
    else:
        params={'A':'entry_rate, capacity, response_time','B':'cure_capacity, response_time','C':'fighting_strength, response_time'}[group]
        labels={'A':'S: humans outside; I: active zombies; H: humans safe in GMCS.','B':'S: never-infected humans; I: zombies; R: cured immune humans.','C':'S: uninfected humans; I: active zombies; D: captured zombies (locked away for good).'}[group]
        state={'A':'S, I, H','B':'S, I, R','C':'S, I, D'}[group]
        flow={
          'A':'''    # At most 500/hour; slow near full capacity or when few humans remain.
    admissions = min(entry_rate, max(capacity - H, 0) / response_time,
                     max(S, 0) / response_time)
    dS_dt = -new_infections - admissions
    dI_dt = new_infections
    dH_dt = admissions
    return dS_dt, dI_dt, dH_dt
''',
          'B':'''    # Capacity is fixed, with a one-hour response limit when few zombies remain.
    # Cured people enter R, remain human, and are permanently immune.
    cures = min(cure_capacity, max(I, 0) / response_time)
    dS_dt = -new_infections
    dI_dt = new_infections - cures
    dR_dt = cures
    return dS_dt, dI_dt, dR_dt
''',
          'C':'''    # Fighting capacity falls as uninfected students are lost.
    eliminated = min(fighting_strength * max(S, 0),
                     max(I, 0) / response_time)
    dS_dt = -new_infections
    dI_dt = new_infections - eliminated
    dD_dt = eliminated
    return dS_dt, dI_dt, dD_dt
'''}[group]
        function=f'''# {labels}
def zombie_model(y, t, N, beta_day, nighttime_bonus,
                 {params}):
    """Return compartment rates (people/hour); t is hours since the 7:30 p.m. outbreak.

    response_time = 1 hour provides a maximum per-person transition rate.
    Capped rates slow smoothly in cumulative counts near an empty compartment.
    """
    {state} = y
    beta = beta_day
    if nighttime_bonus and 2.5 <= t < 8.5:
        beta = 2 * beta_day
    new_infections = beta * S * I / N
{flow}
print("Scenario model function defined.")
'''
    settings=section('3. PART 2: SET PARAMETERS AND RUN THE SIMULATION')+'''# --- 3.1 Population, initial conditions, and time units ---
N = 42000
S0, I0 = 40000, 2000
# All times and rates below use HOURS, not days.
'''
    if baseline:
        settings+='''R0 = 0
y0 = S0, I0, R0

# --- 3.2 Baseline transmission and removal rates (1/hour) ---
beta = 0.35
gamma = 0.0                  # No cure, shelter, or fighting yet.
'''
    else:
        settings+='''


######################################################################################################
# --- 3.2 CHANGE THIS ONE NUMBER ---
# You have 4 Survival Squads. How many go to prevention?
prevention_points = 2         # Try 0, 1, 2, 3, and 4.
######################################################################################################
# Don't change anything below this line.


nighttime_bonus = False       # Leave as False for now.
response_points = 4 - prevention_points   # The rest go on your mission.
beta_day = 0.12 + 0.23 * (0.30 ** prevention_points)
response_time = 1.0           # Hours; keep fixed for this activity.
'''
        settings+= {
         'A':'''H0 = 0
y0 = S0, I0, H0
capacity = 10000
entry_rate = 125 * response_points  # Students/hour; maximum 500.
''',
         'B':'''R0 = 0
y0 = S0, I0, R0
cure_capacity = 120 * response_points  # People/hour; constant for this run.
''',
         'C':'''D0 = 0
y0 = S0, I0, D0
fighting_strength = 0.005 * response_points  # Eliminations per human per hour.
'''}[group]
    settings+='''
# --- 3.3 Time grid: 7:30 p.m. to 7:30 p.m. tomorrow, with output every 0.1 hour ---
t = np.linspace(0, 24, 241)

# --- 3.4 Solve the differential equations (supplied code) ---
# odeint chooses internal steps; t controls the returned output times.
# A small maximum internal step resolves the nighttime switches reliably.
print("\\n--- Running the simulation ---")
'''
    if baseline:
        settings+='''solution = odeint(sir_model, y0, t, args=(N, beta, gamma),
                   rtol=1e-8, atol=1e-7, hmax=0.05, mxstep=10000)
S, I, R = solution.T
'''
    else:
        params={'A':'entry_rate, capacity, response_time','B':'cure_capacity, response_time','C':'fighting_strength, response_time'}[group]
        state={'A':'S, I, H','B':'S, I, R','C':'S, I, D'}[group]
        settings+=f'''solution = odeint(zombie_model, y0, t,
                   args=(N, beta_day, nighttime_bonus,
                         {params}),
                   rtol=1e-8, atol=1e-7, hmax=0.05, mxstep=10000)
{state} = solution.T
'''
    settings+='print("--- Simulation complete ---")\n'
    third={'BASELINE':('R','Removed (zero in baseline)'),'A':('H','Humans sheltered in GMCS'),'B':('R','Cured immune humans'),'C':('D','Captured zombies')}[group]
    plotting=section('4. PART 3: VISUALIZE THE OUTBREAK')+f'''plt.figure(figsize=(10, 6))
plt.plot(t, S, color="royalblue", linewidth=2, label="Susceptible humans")
plt.plot(t, I, color="firebrick", linewidth=2, label="Active zombies")
plt.plot(t, {third[0]}, color="seagreen", linewidth=2, label="{third[1]}")
'''
    if not baseline:
        plotting+='''if nighttime_bonus:
    plt.axvspan(2.5, 8.5, color="gray", alpha=0.15, label="Night-owl zombies (10 p.m.-4 a.m.)")
'''
    plotting+=f'''plt.xticks([0, 2.5, 8.5, 16.5, 24], ["7:30 p.m.", "10 p.m.", "4 a.m.", "Noon", "Rescue\\n7:30 p.m."])
plt.xlabel("Time since outbreak began (hours)")
plt.ylabel("Number of people")
plt.title("{title}")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()
'''
    score={'BASELINE':'S[-1]','A':'S[-1] + H[-1]','B':'S[-1] + R[-1]','C':'S[-1]'}[group]
    denom=42000 if group=='B' else 40000
    insights=section('5. PART 4: REPORT YOUR RESULTS')+f'''survivors = {score}
survivor_percent = 100 * survivors / {denom}
peak_index = np.argmax(I)
peak_hour = t[peak_index]      # Use the TIME, not the array index.
print(f"\\nHuman survivors at rescue: {{survivors:,.0f}}")
print(f"Survivor percentage: {{survivor_percent:.1f}}%")
print(f"Active zombies at rescue: {{I[-1]:,.0f}}")
print(f"Peak active zombies WITHIN these 24 hours: {{I[peak_index]:,.0f}}")
print(f"That peak occurs {{peak_hour:.1f}} hours after the 7:30 p.m. outbreak.")
# This is a grid-based peak within the rescue horizon, not an all-time peak.
'''
    if baseline:insights+='''one_hour = np.argmin(np.abs(t - 1))   # t = 1 is 8:30 p.m.
print(f"At 8:30 p.m.: S = {S[one_hour]:,.1f}, I = {I[one_hour]:,.1f}  (compare with your Euler estimate)")
'''
    if group=='A':insights+='print(f"Humans sheltered in GMCS: {H[-1]:,.0f}")\n'
    if group=='B':insights+='print(f"Cured immune humans at rescue: {R[-1]:,.0f}")\n'
    if group=='C':insights+='print(f"Captured zombies (locked away): {D[-1]:,.0f}")\n'
    questions=section('6. YOUR TEAM CHALLENGE')
    if baseline:
        questions+='''# Explain why gamma=0 makes this the SI special case of SIR.
# Check S + I + R = N. Which curve never increases?
# Compare the first-hour Euler estimate with the continuous ODE solution.
# You will next receive your group's response scenario.
'''
    else:
        questions+='''# Run prevention_points = 0, 1, 2, 3, 4 and record all five survivor counts.
# You always have exactly 4 squads. Which split saves the most students?
# Use your graph to explain why, and name one way the model is unrealistic.
# When your table is full, tell the host your best plan, then STOP.
'''
    parts=[setup,section('2. PART 1: DEFINE THE MODEL EQUATIONS')+function,settings,plotting,insights,questions]
    if not baseline:
        body=lambda x:x.split('='*78+'\n',2)[2]
        night=section('7. NIGHT TWIST: NIGHT-OWL ZOMBIES')+'''# Run the boxes above first: this box reuses the model defined there.
'''+body(settings)+'\n'+body(plotting)+'\n'+body(insights)
        night=night.replace('''nighttime_bonus = False       # Leave as False for now.
''','''nighttime_bonus = True        # Night-owl zombies are ON in this box.
''').replace('# --- 3.','# --- 7.').replace(f'plt.title("{title}")',f'plt.title("{title}: NIGHT-OWL ZOMBIES")')
        assert 'nighttime_bonus = True ' in night
        parts.append(night)
    return parts

def md(text):return {'cell_type':'markdown','metadata':{},'source':text.splitlines(True)}
def code(text):return {'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':text.splitlines(True)}
def write_nb(path,cells):
    for i,c in enumerate(cells):c['id']=f'ode-{i}'
    path.write_text(json.dumps({'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'nbformat':4,'nbformat_minor':5},indent=2))

budget=r'''## Your budget: 4 Survival Squads

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

**Use the code boxes below this one to run your model and generate your results.** They're already written, so you don't have to code anything. You only change one number:

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
'''
briefs={
'A':r'''# Team A: The Fortress 🏰

### Mission briefing

The Geology, Mathematics & Computer Science building (GMCS) has thick concrete walls, very few doors, and a math department that has quietly stockpiled snacks for years "just in case." It's the safest building on campus.

Your plan: **barricade GMCS and bring as many students inside as you can.** Once a student is inside, they're safe until rescue arrives at 7:30 p.m. tomorrow.

But there are two problems:

- **Space.** GMCS fits only **10,000** students, a quarter of campus.
- **Screening.** Nobody gets in without a bite check at the door. Let one zombie in and the whole fortress falls.

### What your response squads do

Each response squad runs a **screening checkpoint** at a GMCS door. One checkpoint can check about **125 students per hour**. With all 4 squads on checkpoints, that's **500 students per hour**, the fastest the doors can handle.

Screening slows down in two situations:

- **The building is almost full.** It takes longer to find the last open spaces.
- **Hardly any humans are left outside.** There's almost nobody left in line.

### Your model: three boxes

| Box | Meaning | At 7:30 p.m. |
| --- | --- | --- |
| **S** | Humans still outside | 40,000 |
| **I** | Zombies | 2,000 |
| **H** | Humans safe inside GMCS | 0 |

People move like this:

$$\text{H (safe inside)} \;\xleftarrow{\text{screened in}}\; \text{S (outside)} \;\xrightarrow{\text{bitten}}\; \text{I (zombie)}$$

Students outside are in a race. Every hour, some get screened into GMCS and some get bitten, both at the same time.

### The equations

Bites per hour (the same as in the baseline):

$$B=\beta\,\frac{S\,I}{42000}$$

Admissions per hour are the **smallest** of three limits:

$$A=\min\left(v,\;\frac{10000-H}{\tau},\;\frac{S}{\tau}\right)$$

- $v = 125r$ is how fast your checkpoints can work.
- $(10000-H)/\tau$: you can't admit more people than there are open spaces.
- $S/\tau$: you can't admit more people than are waiting outside.
- $\tau = 1$ hour is a fixed "response time" that makes screening slow down smoothly near those limits. Leave it alone.

The rates of change:

$$\frac{dS}{dt}=-B-A,\qquad\frac{dI}{dt}=B,\qquad\frac{dH}{dt}=A$$

Humans outside are lost in two ways (bitten or sheltered), zombies only increase, and the shelter only fills. Nobody inside GMCS ever gets bitten.

### Who survives?

**Survivors = S(24) + H(24)**: humans still outside *plus* everyone safe inside. Divide by 40,000 to get your survival percentage.

### Think about it before you run

- At 500 students per hour, what's the fastest GMCS could possibly fill up? Is that before or after rescue?
- At most 10,000 of the 40,000 students fit inside. What has to happen for the other 30,000 to survive?
- Check: why does S + I + H always equal 42,000?
''',
'B':r'''# Team B: The Antidote 🧪

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
''',
'C':r'''# Team C: The Resistance ⚔️

### Mission briefing

Forget hiding. The students are fighting back.

The rugby team, the rock-climbing club, ROTC, and one extremely determined chess club have formed **The Resistance**. Armed with pool noodles, rope, and duct tape, they capture zombies and lock them in a parking-structure basement until rescue arrives.

Captured zombies are **out of the game** and can't bite anyone ever again. But they're still zombies, so they don't count as survivors. (The rescue teams can deal with them.)

Here's what makes your plan different: **the Resistance is made of students.** The more students who are still human, the more fighters you have. Every bitten student is one less fighter.

### What your response squads do

Each response squad **trains and leads fighters**, so more squads means every student fighter captures zombies faster. The total capture rate is

$$\text{captures per hour} = 0.005 \times r \times S$$

With all 4 squads and all 40,000 students still human, that's 0.005 × 4 × 40,000 = **800 captures per hour**. If half the students get bitten, capture power drops by half.

Captures also slow down when **hardly any zombies are left** to find.

### Your model: three boxes

| Box | Meaning | At 7:30 p.m. |
| --- | --- | --- |
| **S** | Humans (and potential fighters) | 40,000 |
| **I** | Zombies on the loose | 2,000 |
| **D** | Captured zombies, locked away for good | 0 |

$$S \;\xrightarrow{\text{bitten}}\; I \;\xrightarrow{\text{captured}}\; D$$

### The equations

Bites per hour:

$$B=\beta\,\frac{S\,I}{42000}$$

Captures per hour are your fighting power, unless there aren't enough zombies left:

$$F=\min\left(a\,S,\;\frac{I}{\tau}\right),\qquad a = 0.005r$$

- $aS$: capture power grows with the number of humans.
- $I/\tau$: you can't capture zombies that don't exist. Keep $\tau = 1$ hour fixed.

The rates of change:

$$\frac{dS}{dt}=-B,\qquad\frac{dI}{dt}=B-F,\qquad\frac{dD}{dt}=F$$

The only way to lose humans is by bites. In this model, nobody gets hurt in the fighting itself. (Is that realistic?)

### Who survives?

**Survivors = S(24)**: only humans who were never bitten. Captured zombies don't count. Divide by 40,000 to get your survival percentage.

### Think about it before you run

- With all 4 squads, you start with 800 captures per hour against about 667 bites per hour (with no prevention). Who's winning at 7:30 p.m.? Will it stay that way?
- If half the students get bitten, what happens to your capture power? Why could that spiral out of control?
- Check: why does S + I + D always equal 42,000?
'''}

intro='''# SDSU: Can you survive?!?!

> **How to use this notebook:** Click the first gray code box and press **Shift + Enter**. Keep pressing until you reach the bottom. The last boxes draw your graph and print your survivor count. You don't need to understand every line of code. The only line you ever change is `prevention_points`, framed by rows of `#` signs under `CHANGE THIS ONE NUMBER`.
'''

baseline_note='''
## The baseline: what if nobody does anything?

This is the answer to the "simplest apocalypse" from the core activity: no fortress, no antidote, no resistance. Zombies are never removed (γ = 0). Run every box, then compare with your work:

- How close was your sketch to the computer's curves?
- How many students are still human when rescue arrives at 7:30 p.m. tomorrow?
- When are zombies being created the fastest?
'''


core=r'''# SDSU: survive until rescue

## 1. Form groups and hear the background

Work in groups of 2–4 with one laptop. At 7:30 p.m., the 2,000 faculty/staff in our fictional SDSU population become zombies. None of the 40,000 students is infected yet. Outside rescuers arrive at 7:30 p.m. tomorrow, so your horizon is 24 hours. All population counts, capacities, and rates are fictional game assumptions.

## 2. Mini lesson on SIR

S means susceptible humans; I means infectious active zombies; R means removed from transmission. The standard flow is S → I → R. In ordinary epidemic SIR, R often means recovered immune people. In our scenarios the meaning of removal depends on what the response does, so survivor counts must be defined carefully.

Let t be hours after 7:30 p.m. The standard continuous-time equations are

$$\frac{dS}{dt}=-\beta\frac{SI}{N},\qquad
\frac{dI}{dt}=\beta\frac{SI}{N}-\gamma I,\qquad
\frac{dR}{dt}=\gamma I.$$

These derivatives are rates in people/hour. β and γ have units per hour. Infection depends on both susceptible humans and active zombies. The computer will solve these equations; you do not need an analytic solution or to write a solver. Decimal populations describe approximate average counts.

## 3. Discuss what the basic model needs

1. Which groups do we need, and what do they mean?
2. What should the initial conditions and N be?
3. Which processes move people between compartments?
4. What mixing, infection, and removal assumptions are we making?
5. What should count as a human survivor at rescue?

## 4. Build the simplest apocalypse first

Before shelter, cure, or fighting is introduced, set γ=0. Use S(0)=40,000, I(0)=2,000, R(0)=0, N=42,000, β=0.35 per hour. This is the SI special case of the SIR framework: R remains zero.

1. Simplify the three differential equations with γ=0.
2. Calculate the initial rates dS/dt, dI/dt, dR/dt at 7:30 p.m.
3. Add the three equations. Why does the population stay constant?
4. Sketch the shapes you expect for S(t), I(t), and R(t) before rescue.
5. Optional: estimate the state one hour later by multiplying each initial derivative by one hour and adding it to the initial count. This is a one-step Euler approximation, not the exact ODE answer at t=1.

If you want to start coding, write the three initial values and try expressing your derivatives in a function. The complete model function, odeint call, and plots will be supplied at the answer reveal.

## 5. Compare with the basic-model answer

Wait for the host to release 01_Baseline_Answer.ipynb. Run its cells in order. Which section defines the biology, and which section solves the equations? Why is the peak time found using t[np.argmax(I)] instead of treating the array index as hours? Compare the continuous first-hour result with your optional Euler estimate.

## 6. Move to your scenario

The host will distribute Group A, B, or C. All groups share four Survival Squads, a fixed assignment from 7:30 p.m. to rescue, and the same prevention rule. Test every assignment and explain your best plan. Afterwards repeat with nighttime aggression from 10 p.m. to 4 a.m.

## Optional synthetic-data warm-up

synthetic_baseline_log.csv records six fictional baseline intervals from a separate random hourly practice outbreak, before any response. It uses start-of-hour infection probabilities rather than an exact continuous ODE trajectory. Check each row's population total and reconstruct the next state. Do not treat these integer counts as the exact ODE solution, fit parameters for the main challenge, or restart your scenario at the end of the log. All scenarios begin at 7:30 p.m. from the original initial conditions.
'''
# Keep hand-edited core materials; only write the default version if missing.
if (OUT/'00_Core_Activity.md').exists():
    core=(OUT/'00_Core_Activity.md').read_text()
else:
    (OUT/'00_Core_Activity.md').write_text(core)
if not (OUT/'00_Core_Activity.ipynb').exists():
    write_nb(OUT/'00_Core_Activity.ipynb',[md(core),code('# Optional: try defining your initial conditions and derivatives here.\n# The full answer will be supplied by the host after the group work.\n')])

twist_intro=r'''---

# 🛑 STOP HERE

**Don't go past this point yet!** First finish your normal-night table and tell the host your best plan. Wait here until the host announces breaking news.

---

# 🌙 BREAKING NEWS: The Night Twist

### 9:58 p.m. — Urgent update from the Chemistry department

*"We made a mistake in our analysis. The cold brew's caffeine peaks overnight. From **10 p.m. to 4 a.m.**, the zombies will be wide awake, jittery, and **twice as aggressive**. Repeat: twice as aggressive. Get ready."*

Zombies are **night owls**. Between 10 p.m. and 4 a.m., β (the infection rate) **doubles**. That window opens only **2.5 hours** after the outbreak, while the horde is still growing. After 4 a.m., everything goes back to normal.

Your squads are already deployed, so you can't change tonight's plan. But campus leadership wants to know: **if you had known about this at 7:30 p.m., would you have assigned your squads differently?**

## Test the night twist

The code box below is a complete copy of your model with **night-owl zombies switched on**. You don't need to change anything above it.

1. In the box below, set `prevention_points = 0` and press **Shift + Enter**.
2. Record the survivors in the table under the box.
3. Repeat for 1, 2, 3, and 4.

The gray band on the graph marks the night-owl hours. Watch what happens to the zombie curve inside it.
'''
twist_after=r'''## Night-twist results

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
'''


def answer_box(title,intro,questions,outro=''):
    text=f'## ✏️ {title}\n\n*Double-click this box to type your answers. Press **Shift + Enter** when you\'re done to make it look neat again.*\n\n'+intro
    for i,q in enumerate(questions,1):
        text+=f'**{i}. {q}**\n\n> ✏️ *Your answer:* \n\n'
    return text+outro

results_table="""| Prevention squads (p) | Response squads (r) | Human survivors at rescue | Survival % |
| --- | --- | --- | --- |
| 0 | 4 | | |
| 1 | 3 | | |
| 2 | 2 | | |
| 3 | 1 | | |
| 4 | 0 | | |
"""
team_answers=answer_box('6. Your team\'s answers',
    '### Results: normal night\n\nCopy the survivors and survival % from box 5 for each plan.\n\n'+results_table+'\n### Report back to campus leadership\n\n',
    ['What is your best plan? How many squads go on prevention, and how many on your mission?',
     'Why does it work? Point to something on your graph.',
     'Name one way our model is unrealistic. How might you improve it?'],
    '---\n\nWhen you\'re done, tell the host your best plan. Then scroll down to the 🛑 STOP sign and wait there.\n')
night_answers=answer_box('Night-twist answers',
    '### Results: night twist\n\n| Prevention squads (p) | Response squads (r) | Survivors: normal night (copy from box 6) | Survivors: night-owl zombies |\n| --- | --- | --- | --- |\n| 0 | 4 | | |\n| 1 | 3 | | |\n| 2 | 2 | | |\n| 3 | 1 | | |\n| 4 | 0 | | |\n\n### Report back\n\n',
    ['Did your best plan change? If so, why?',
     'Which plan got hurt the most by the twist? Use your graph to explain.',
     'Why does it matter that the dangerous hours come so early in the outbreak? What if they came at the very end instead?'])
baseline_answers=answer_box('6. Your answers',
    '',
    ['How close was your sketch to the computer\'s curves?',
     'How many students are still human when rescue arrives at 7:30 p.m. tomorrow?',
     'When are zombies being created the fastest? (Box 5 prints the peak time.)',
     'Why does setting γ = 0 turn SIR into the simpler SI model? Which curve never goes up?',
     'Box 5 prints the computer\'s numbers at 8:30 p.m. How do they compare with your Euler estimate, and why are they different?'],
    '---\n\nNext, the host will hand out your team\'s mission!\n')

# Notebook version of the brief: results table and report questions live in box 6 instead.
_a=budget.index('| Prevention squads (p) | Response squads (r) | Human survivors at rescue')
_b=budget.index("Don't go past it until the host says so!\n")+len("Don't go past it until the host says so!\n")
budget_nb=(budget[:_a]+"When all five plans are tested, fill in **box 6** and tell the host your best plan. Then scroll to the 🛑 STOP sign near the end of your notebook. Don't go past it until the host says so!\n"+budget[_b:]).replace(
    'Write both in the table below, and look at your graph.','Write both in the results table in **box 6** (your answers box, just below box 5), and look at your graph.')

scripts={}
verify_scripts={}
for group in ['BASELINE','A','B','C']:
    parts=make_script(group);scripts[group]='\n\n'.join(parts);verify_scripts[group]='\n\n'.join(parts[:6])
    name='01_Baseline_Answer' if group=='BASELINE' else f'Group_{group}'
    (OUT/f'{name}.py').write_text(scripts[group])
    text=intro+baseline_note if group=='BASELINE' else intro+'\n'+briefs[group]+'\n'+budget_nb
    # Box 6 is a Markdown answers box in notebooks; the .py keeps the questions as comments.
    cells=[md(text)]+[code(p) for p in parts[:5]]+[md(baseline_answers if group=='BASELINE' else team_answers)]
    if group!='BASELINE':cells+=[md(twist_intro),code(parts[6]),md(night_answers)]
    write_nb(OUT/f'{name}.ipynb',cells)
    if group!='BASELINE':(OUT/f'Group_{group}_Brief.md').write_text(briefs[group]+'\n'+budget.replace('the code boxes below this one','the code boxes in your team\'s notebook')+'\n'+twist_intro.replace('The code box below','The last code box in your notebook').replace('In the box below','In that box').replace('the table under the box','the table below')+'\n'+twist_after)

# Run the actual delivered scripts and compare every continuous ODE scenario.
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
plt.show=lambda:None
results=[];saved={}
with contextlib.redirect_stdout(io.StringIO()):
    for group in ['BASELINE','A','B','C']:
        for night in ([False] if group=='BASELINE' else [False,True]):
            for p in ([0] if group=='BASELINE' else range(5)):
                text=verify_scripts[group].replace('prevention_points = 2 ',f'prevention_points = {p} ').replace('nighttime_bonus = False ',f'nighttime_bonus = {night} ')
                ns={};exec(text,ns)
                sol=ns['solution'];tt=ns['t']
                assert sol.shape==(241,3) and np.isfinite(sol).all()
                assert np.max(np.abs(sol.sum(axis=1)-42000))<1e-5
                assert sol.min()>-1e-5
                assert np.max(np.diff(ns['S']))<=1e-6
                if group=='A':assert np.max(ns['H'])<=10000+1e-5 and np.max(np.diff(ns['H'])/.1)<=500+1e-4
                if group=='B':assert np.max(np.diff(ns['R'])/.1)<=120*(4-p)+1e-4
                if group=='BASELINE':baseline=ns['survivors']
                else:
                    # Independent segmentation at the night boundaries verifies the switches.
                    args=(42000,ns['beta_day'],False)
                    if group=='A':extra=(ns['entry_rate'],ns['capacity'],ns['response_time'])
                    elif group=='B':extra=(ns['cure_capacity'],ns['response_time'])
                    else:extra=(ns['fighting_strength'],ns['response_time'])
                    y=np.array(ns['y0'],float)
                    for lo,hi,multiplier in [(0,2.5,1),(2.5,8.5,2 if night else 1),(8.5,24,1)]:
                        y=odeint(ns['zombie_model'],y,np.linspace(lo,hi,101),args=(42000,ns['beta_day']*multiplier,False)+extra,rtol=1e-9,atol=1e-8,hmax=.025)[-1]
                    assert np.max(np.abs(y-sol[-1]))<.05
                    results.append([group,night,p,4-p,ns['survivors'],ns['survivor_percent'],ns['S'][-1],ns['I'][-1],sol[-1,2],ns['peak_hour']])
                if group!='BASELINE' and night:
                    # The notebook's separate night-twist cell must reproduce the night result.
                    ns2={};exec(scripts[group].replace('prevention_points = 2 ',f'prevention_points = {p} '),ns2)
                    assert ns2['nighttime_bonus'] is True and abs(ns2['survivors']-ns['survivors'])<1e-6
                if (group=='BASELINE') or (p==2 and not night):saved[group]=ns
                plt.close('all')

buf=io.StringIO();w=csv.writer(buf)
w.writerow(['group','nighttime_bonus','prevention_points','response_points','human_survivors','survivor_percent','S_final','I_final','H_or_R_or_D_final','peak_hour_within_24h']);w.writerows(results)
(OUT/'HOST_Results.csv').write_text(buf.getvalue())

# Host previews: actual plotted data for a sample allocation, one figure per model.
for group,ns in saved.items():
    fig,ax=plt.subplots(figsize=(9,5))
    third={'BASELINE':'R: removed','A':'H: sheltered humans','B':'R: cured immune humans','C':'D: captured zombies'}[group]
    for j,(label,color) in enumerate(zip(['S: susceptible humans','I: active zombies',third],['royalblue','firebrick','seagreen'])):
        ax.plot(ns['t'],ns['solution'][:,j],label=label,color=color,linewidth=2)
    ax.set(xlabel='Hours since 7:30 p.m. outbreak',ylabel='People',title=f'{group}: '+('no response' if group=='BASELINE' else '2 prevention + 2 response; standard'))
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/f'HOST_Preview_{group}.png',dpi=130);plt.close(fig)

team_names={'A':'Team A: The Fortress','B':'Team B: The Antidote','C':'Team C: The Resistance'}
key=''
for group in 'ABC':
    key+=f'\n### {team_names[group]}\n\n| Prevention squads | Response squads | Normal night survivors | Night-owl survivors |\n| --- | --- | --- | --- |\n'
    for p in range(5):
        a=next(r[4] for r in results if r[:3]==[group,False,p]);b=next(r[4] for r in results if r[:3]==[group,True,p])
        key+=f'| {p} | {4-p} | {a:,.0f} | {b:,.0f} |\n'
    for n in (False,True):
        best=max((r for r in results if r[:2]==[group,n]),key=lambda r:r[4])
        key+=f'\nBest {"night-owl" if n else "normal night"}: {best[2]} prevention, {best[3]} response squads; {best[4]:,.0f} survivors ({best[5]:.1f}%).\n'

guide=f'''# Host guide: SDSU, Can you survive?!?!

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

Rates at 7:30 p.m.: dS/dt=-666.666667, dI/dt=666.666667, dR/dt=0 people/hour. One Euler step to 8:30 p.m. gives S=39,333.333333 and I=2,666.666667. The exact solution differs because S and I change continuously during the hour. The baseline leaves approximately {baseline:,.2f} uninfected humans at rescue.

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
{key}
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
'''
(OUT/'HOST_Facilitator_Guide.md').write_text(guide)
(OUT/'README.md').write_text('''# SDSU: Can you survive?!?!

A zombie-apocalypse math event for students with no coding experience. At 6 p.m., students learn that all 2,000 faculty/staff will turn into zombies at 7:30 p.m. after drinking a mysterious cold brew. Teams have the activity's roughly 90 minutes to model the outbreak with SIR-style differential equations and decide how to deploy **4 Survival Squads** to keep the 40,000 students human until rescue at 7:30 p.m. tomorrow.

## How the event runs

1. **00_Core_Activity:** story, SIR mini lesson, discussion, and the "simplest apocalypse" baseline by hand.
2. **01_Baseline_Answer.ipynb:** release after teams finish the baseline.
3. **Team briefs and notebooks:** each team gets one mission:
   - **Team A, The Fortress:** screen students into the GMCS building (10,000 spaces, up to 125 students/hour per squad).
   - **Team B, The Antidote:** cure zombies with Decaf-X (120 cures/hour per squad); cured people are immune and count as survivors.
   - **Team C, The Resistance:** students capture zombies (power = 0.005 × squads × humans still standing).
4. Each team splits its 4 squads between **prevention** (lowers the infection rate for everyone) and **response** (its own mission), tests all five splits, then, after reporting, scrolls past the 🛑 STOP sign to test the **night-owl twist** in its own code box (zombies twice as aggressive from 10 p.m. to 4 a.m.).

Students only change one number in the notebooks. Everything runs on NumPy, SciPy, and Matplotlib (Google Colab works out of the box).

HOST_ files (facilitator guide, answer tables, previews) are for the facilitator only. Run refresh_ode_models.py to regenerate the notebooks, briefs, answers, and zip after editing it.
''')
(OUT/'requirements.txt').write_text('numpy\nscipy\nmatplotlib\n')
(OUT/'refresh_ode_models.py').write_text(Path(__file__).read_text())
# Exclude the obsolete generator so it cannot silently restore the discrete edition.
with zipfile.ZipFile((ROOT if OUT!=ROOT else ROOT.parent)/'SDSU_Zombie_Project.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name!='generate_project.py':z.write(p,arcname='SDSU_Zombie_Event/'+p.name)
print('Verified baseline and all 30 continuous scenarios: conservation, nonnegativity, capacity bounds, and nighttime switch accuracy.')
for g in 'ABC':
    for night in (False,True):
        best=max((r for r in results if r[:2]==[g,night]),key=lambda r:r[4])
        print(g,'night' if night else 'standard','best allocation:',best[2],best[3],'survivors:',round(best[4]))
