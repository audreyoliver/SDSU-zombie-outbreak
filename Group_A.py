# ==============================================================================
# 1. SETUP AND INTRODUCTION
# ==============================================================================
# GROUP A: THE FORTRESS (GMCS SAFE ZONE)
# Outbreak: 7:30 p.m. tonight. Rescue: 7:30 p.m. tomorrow (24 hours).
# Fictional population: 40,000 susceptible students and 2,000 zombies.
# All rates, resources, and GMCS capacity are invented game assumptions.
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

print("Libraries imported successfully!")


# ==============================================================================
# 2. PART 1: DEFINE THE MODEL EQUATIONS
# ==============================================================================
# S: humans outside; I: active zombies; H: humans safe in GMCS.
def zombie_model(y, t, N, beta_day, nighttime_bonus,
                 entry_rate, capacity, response_time):
    """Return compartment rates (people/hour); t is hours since the 7:30 p.m. outbreak.

    response_time = 1 hour provides a maximum per-person transition rate.
    Capped rates slow smoothly in cumulative counts near an empty compartment.
    """
    S, I, H = y
    beta = beta_day
    if nighttime_bonus and 2.5 <= t < 8.5:
        beta = 2 * beta_day
    new_infections = beta * S * I / N
    # At most 500/hour; slow near full capacity or when few humans remain.
    admissions = min(entry_rate, max(capacity - H, 0) / response_time,
                     max(S, 0) / response_time)
    dS_dt = -new_infections - admissions
    dI_dt = new_infections
    dH_dt = admissions
    return dS_dt, dI_dt, dH_dt

print("Scenario model function defined.")


# ==============================================================================
# 3. PART 2: SET PARAMETERS AND RUN THE SIMULATION
# ==============================================================================
# --- 3.1 Population, initial conditions, and time units ---
N = 42000
S0, I0 = 40000, 2000
# All times and rates below use HOURS, not days.



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
H0 = 0
y0 = S0, I0, H0
capacity = 10000
entry_rate = 125 * response_points  # Students/hour; maximum 500.

# --- 3.3 Time grid: 7:30 p.m. to 7:30 p.m. tomorrow, with output every 0.1 hour ---
t = np.linspace(0, 24, 241)

# --- 3.4 Solve the differential equations (supplied code) ---
# odeint chooses internal steps; t controls the returned output times.
# A small maximum internal step resolves the nighttime switches reliably.
print("\n--- Running the simulation ---")
solution = odeint(zombie_model, y0, t,
                   args=(N, beta_day, nighttime_bonus,
                         entry_rate, capacity, response_time),
                   rtol=1e-8, atol=1e-7, hmax=0.05, mxstep=10000)
S, I, H = solution.T
print("--- Simulation complete ---")


# ==============================================================================
# 4. PART 3: VISUALIZE THE OUTBREAK
# ==============================================================================
plt.figure(figsize=(10, 6))
plt.plot(t, S, color="royalblue", linewidth=2, label="Susceptible humans")
plt.plot(t, I, color="firebrick", linewidth=2, label="Active zombies")
plt.plot(t, H, color="seagreen", linewidth=2, label="Humans sheltered in GMCS")
if nighttime_bonus:
    plt.axvspan(2.5, 8.5, color="gray", alpha=0.15, label="Night-owl zombies (10 p.m.-4 a.m.)")
plt.xticks([0, 2.5, 8.5, 16.5, 24], ["7:30 p.m.", "10 p.m.", "4 a.m.", "Noon", "Rescue\n7:30 p.m."])
plt.xlabel("Time since outbreak began (hours)")
plt.ylabel("Number of people")
plt.title("GROUP A: THE FORTRESS (GMCS SAFE ZONE)")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()


# ==============================================================================
# 5. PART 4: REPORT YOUR RESULTS
# ==============================================================================
survivors = S[-1] + H[-1]
survivor_percent = 100 * survivors / 40000
peak_index = np.argmax(I)
peak_hour = t[peak_index]      # Use the TIME, not the array index.
print(f"\nHuman survivors at rescue: {survivors:,.0f}")
print(f"Survivor percentage: {survivor_percent:.1f}%")
print(f"Active zombies at rescue: {I[-1]:,.0f}")
print(f"Peak active zombies WITHIN these 24 hours: {I[peak_index]:,.0f}")
print(f"That peak occurs {peak_hour:.1f} hours after the 7:30 p.m. outbreak.")
# This is a grid-based peak within the rescue horizon, not an all-time peak.
print(f"Humans sheltered in GMCS: {H[-1]:,.0f}")


# ==============================================================================
# 6. YOUR TEAM CHALLENGE
# ==============================================================================
# Run prevention_points = 0, 1, 2, 3, 4 and record all five survivor counts.
# You always have exactly 4 squads. Which split saves the most students?
# Use your graph to explain why, and name one way the model is unrealistic.
# When your table is full, tell the host your best plan, then STOP.


# ==============================================================================
# 7. NIGHT TWIST: NIGHT-OWL ZOMBIES
# ==============================================================================
# Run the boxes above first: this box reuses the model defined there.
# --- 7.1 Population, initial conditions, and time units ---
N = 42000
S0, I0 = 40000, 2000
# All times and rates below use HOURS, not days.



######################################################################################################
# --- 7.2 CHANGE THIS ONE NUMBER ---
# You have 4 Survival Squads. How many go to prevention?
prevention_points = 2         # Try 0, 1, 2, 3, and 4.
######################################################################################################
# Don't change anything below this line.


nighttime_bonus = True        # Night-owl zombies are ON in this box.
response_points = 4 - prevention_points   # The rest go on your mission.
beta_day = 0.12 + 0.23 * (0.30 ** prevention_points)
response_time = 1.0           # Hours; keep fixed for this activity.
H0 = 0
y0 = S0, I0, H0
capacity = 10000
entry_rate = 125 * response_points  # Students/hour; maximum 500.

# --- 7.3 Time grid: 7:30 p.m. to 7:30 p.m. tomorrow, with output every 0.1 hour ---
t = np.linspace(0, 24, 241)

# --- 7.4 Solve the differential equations (supplied code) ---
# odeint chooses internal steps; t controls the returned output times.
# A small maximum internal step resolves the nighttime switches reliably.
print("\n--- Running the simulation ---")
solution = odeint(zombie_model, y0, t,
                   args=(N, beta_day, nighttime_bonus,
                         entry_rate, capacity, response_time),
                   rtol=1e-8, atol=1e-7, hmax=0.05, mxstep=10000)
S, I, H = solution.T
print("--- Simulation complete ---")

plt.figure(figsize=(10, 6))
plt.plot(t, S, color="royalblue", linewidth=2, label="Susceptible humans")
plt.plot(t, I, color="firebrick", linewidth=2, label="Active zombies")
plt.plot(t, H, color="seagreen", linewidth=2, label="Humans sheltered in GMCS")
if nighttime_bonus:
    plt.axvspan(2.5, 8.5, color="gray", alpha=0.15, label="Night-owl zombies (10 p.m.-4 a.m.)")
plt.xticks([0, 2.5, 8.5, 16.5, 24], ["7:30 p.m.", "10 p.m.", "4 a.m.", "Noon", "Rescue\n7:30 p.m."])
plt.xlabel("Time since outbreak began (hours)")
plt.ylabel("Number of people")
plt.title("GROUP A: THE FORTRESS (GMCS SAFE ZONE): NIGHT-OWL ZOMBIES")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()

survivors = S[-1] + H[-1]
survivor_percent = 100 * survivors / 40000
peak_index = np.argmax(I)
peak_hour = t[peak_index]      # Use the TIME, not the array index.
print(f"\nHuman survivors at rescue: {survivors:,.0f}")
print(f"Survivor percentage: {survivor_percent:.1f}%")
print(f"Active zombies at rescue: {I[-1]:,.0f}")
print(f"Peak active zombies WITHIN these 24 hours: {I[peak_index]:,.0f}")
print(f"That peak occurs {peak_hour:.1f} hours after the 7:30 p.m. outbreak.")
# This is a grid-based peak within the rescue horizon, not an all-time peak.
print(f"Humans sheltered in GMCS: {H[-1]:,.0f}")
