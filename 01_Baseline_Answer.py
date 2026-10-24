# ==============================================================================
# 1. SETUP AND INTRODUCTION
# ==============================================================================
# BASIC SIR MODEL: NO RESPONSE
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
# S: susceptible humans; I: active zombies; R: removed individuals.
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


# ==============================================================================
# 3. PART 2: SET PARAMETERS AND RUN THE SIMULATION
# ==============================================================================
# --- 3.1 Population, initial conditions, and time units ---
N = 42000
S0, I0 = 40000, 2000
# All times and rates below use HOURS, not days.
R0 = 0
y0 = S0, I0, R0

# --- 3.2 Baseline transmission and removal rates (1/hour) ---
beta = 0.35
gamma = 0.0                  # No cure, shelter, or fighting yet.

# --- 3.3 Time grid: 7:30 p.m. to 7:30 p.m. tomorrow, with output every 0.1 hour ---
t = np.linspace(0, 24, 241)

# --- 3.4 Solve the differential equations (supplied code) ---
# odeint chooses internal steps; t controls the returned output times.
# A small maximum internal step resolves the nighttime switches reliably.
print("\n--- Running the simulation ---")
solution = odeint(sir_model, y0, t, args=(N, beta, gamma),
                   rtol=1e-8, atol=1e-7, hmax=0.05, mxstep=10000)
S, I, R = solution.T
print("--- Simulation complete ---")


# ==============================================================================
# 4. PART 3: VISUALIZE THE OUTBREAK
# ==============================================================================
plt.figure(figsize=(10, 6))
plt.plot(t, S, color="royalblue", linewidth=2, label="Susceptible humans")
plt.plot(t, I, color="firebrick", linewidth=2, label="Active zombies")
plt.plot(t, R, color="seagreen", linewidth=2, label="Removed (zero in baseline)")
plt.xticks([0, 2.5, 8.5, 16.5, 24], ["7:30 p.m.", "10 p.m.", "4 a.m.", "Noon", "Rescue\n7:30 p.m."])
plt.xlabel("Time since outbreak began (hours)")
plt.ylabel("Number of people")
plt.title("BASIC SIR MODEL: NO RESPONSE")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()


# ==============================================================================
# 5. PART 4: REPORT YOUR RESULTS
# ==============================================================================
survivors = S[-1]
survivor_percent = 100 * survivors / 40000
peak_index = np.argmax(I)
peak_hour = t[peak_index]      # Use the TIME, not the array index.
print(f"\nHuman survivors at rescue: {survivors:,.0f}")
print(f"Survivor percentage: {survivor_percent:.1f}%")
print(f"Active zombies at rescue: {I[-1]:,.0f}")
print(f"Peak active zombies WITHIN these 24 hours: {I[peak_index]:,.0f}")
print(f"That peak occurs {peak_hour:.1f} hours after the 7:30 p.m. outbreak.")
# This is a grid-based peak within the rescue horizon, not an all-time peak.
one_hour = np.argmin(np.abs(t - 1))   # t = 1 is 8:30 p.m.
print(f"At 8:30 p.m.: S = {S[one_hour]:,.1f}, I = {I[one_hour]:,.1f}  (compare with your Euler estimate)")


# ==============================================================================
# 6. YOUR TEAM CHALLENGE
# ==============================================================================
# Explain why gamma=0 makes this the SI special case of SIR.
# Check S + I + R = N. Which curve never increases?
# Compare the first-hour Euler estimate with the continuous ODE solution.
# You will next receive your group's response scenario.
