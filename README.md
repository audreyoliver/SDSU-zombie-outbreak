# SDSU: Can you survive?!?!

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
