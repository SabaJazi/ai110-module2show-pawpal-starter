# PawPal+ Project Reflection

## 1. System Design
- User should be able to add pets
- User should be able to add walking sessions in app.
- User should be able to schedule medications daily and with time alarms or notifications.
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Answer:
The initial UML design follows a hierarchical structure typical of management applications, where a central user entity coordinates multiple sub-entities. The architecture is designed to separate user-specific data from the physical and medical logs of the pets.

1. User Class
The User class acts as the System Administrator. Its primary responsibility is account and relationship management.

Responsibilities: It holds the credentials for the pet owner and maintains a collection of all registered pets. It acts as the entry point for the "Dashboard," aggregating data from all sub-classes to show a unified view of the day's tasks.

2. Pet Class
The Pet class is the Data Core and serves as the primary "Owner" of all activity logs.

Responsibilities: It stores static biological data (species, breed, age) and manages the relationship with health and exercise records. Instead of the User "owning" a walk, the Pet owns the walk, which allows for better data organization if multiple people (e.g., family members) share care for one animal.

3. WalkSession Class
This class is the Activity Tracker. It is responsible for the temporal and physical data related to exercise.

Responsibilities: It handles the logic for time-tracking (start/end) and calculates metrics like distance or duration. It provides a historical record of physical activity that can be referenced by the Pet class to monitor health trends.

4. Medication Class
The Medication class functions as the Scheduler and Notifier. It is the most logically complex class because it must handle recurring events.

Responsibilities: It manages "State" (whether a pill was taken) and "Triggers" (when the phone should alert the user). It keeps a strict log of adherence, ensuring that the pet's medical history is accurate and that doses are not missed or doubled.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Changes made:

✅ Added pet: Pet back-reference to both WalkSession and Medication eliminates the bottleneck of needing to pass species explicitly or traverse backwards.
✅ Fixed parameter shadowing: setReminder(self, reminder_time: time) instead of setReminder(self, time: time).
✅ Made constructors flexible: User, Pet now initialize empty lists by default; WalkSession and Medication have optional routePath and scheduledTimes.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Answer:
The Scheduler makes this key tradeoff:

Exact Time Matching vs. Duration Overlap Detection
The tradeoff:

✅ Fast & Simple: O(n) grouping, instant detection
❌ Misses Real Conflicts: Doesn't account for task duration
Why this tradeoff is reasonable:

1- Most users schedule tasks at discrete, non-overlapping times anyway
2- Keeps scheduler lightweight (important for Streamlit responsiveness)
3- Simple to understand and debug
4- Easy to improve later without breaking existing code
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
Answer: 
I used AI tools in four main ways during this project:

- Design brainstorming: I used AI early to turn project requirements into a class structure (User, Pet, Task, WalkSession, Medication, Scheduler) and to identify relationships and responsibilities for UML.
- Debugging: I used AI to diagnose runtime and test issues, especially constructor naming mismatches (isCompleted vs is_completed), circular import errors, and Streamlit duplicate widget key errors.
- Refactoring and alignment: I used AI to refactor code so implementation and tests matched, and to connect UI behavior directly to Scheduler methods (sorting, filtering, conflict checks) instead of ad-hoc UI logic.
- Documentation support: I used AI to draft README improvements (features, test command, confidence statement) and to update UML text so it matched the final implementation.
- What kinds of prompts or questions were most helpful?
Answer:
Very specific, outcome-focused prompts with constraints (for example: “include these three tests,” “use Scheduler methods,” “keep it aligned with current code”) produced the best and fastest results.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Answer:
One clear moment was when an AI-generated test edit accidentally overwrote my core system file and introduced a self-import in pawpal_system.py, which caused a circular import error during test collection. I did not accept that change as-is. Instead, I reviewed the traceback, compared file contents, restored pawpal_system.py to the actual class implementation, and then re-ran the test suite to verify the fix. This was a good reminder that AI output is useful, but it still needs code review and validation before being trusted.
- How did you evaluate or verify what the AI suggested?
I verified AI suggestions using a simple three-step process:

- Static code review: I checked whether the suggested change matched my class design, method names, and data flow (especially around Task, Medication, Scheduler, and Streamlit keys).
- Error-driven validation: I used stack traces and failing test output to confirm root causes before applying fixes (for example, circular import and constructor-argument mismatches).
- Behavioral testing: I re-ran my test suite and manually checked key app behavior (sorting, recurrence, conflict warnings, and UI rendering) to ensure the fix worked and did not break existing features.

I accepted AI output only when it passed all three checks.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested the following core behaviors:

-Medication completion flow: calling markAsTaken() correctly updates completion state.
-Walk completion flow: calling endWalk() marks the walk as completed.
-Task addition integrity: adding walk and medication tasks increases the correct pet record counts (single and multiple additions).
-Sorting correctness: scheduler returns tasks in chronological order when sorted by time.
-Recurrence logic: completing a daily medication creates the next occurrence for the following day.
-Conflict detection: scheduler flags duplicate scheduled times as conflicts.
- Why were these tests important?
These tests cover the most failure-prone parts of the app and reduce the risk of missed care tasks, duplicate scheduling, or misleading schedule output.
**b. Confidence**

- How confident are you that your scheduler works correctly?
Confidence Level: 4/5 stars

Reasoning: Current results show 8 passing unit tests, including key scheduling logic. Reliability looks good for core behaviors, but confidence is not 5/5 yet because edge cases such as timezone handling, DST transitions, and invalid-input validation are not fully covered.
- What edge cases would you test next if you had more time?
Answer:
If I had more time, I would test: end-of-month and leap-day recurrence, duplicate completion calls (to prevent double next-task creation), timezone and DST transitions, invalid inputs (missing date/time or bad frequency), and tie-breaking when tasks share the same timestamp.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Answer:
I am most satisfied with how the backend scheduler and the Streamlit UI now align. The app does not just display placeholder data anymore; it uses the Scheduler methods for sorting, filtering, recurrence outcomes, and conflict warnings, which makes the demo reflect real system behavior.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Answer:
In another iteration, I would redesign conflict detection to consider duration overlap instead of exact-time matches only, normalize all naming conventions (for example isCompleted vs is_completed), and add stronger input validation and persistence (database storage instead of in-memory session state).

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Answer:
A key takeaway is that AI is most effective as a collaborator, not an autopilot. The best results came from giving precise prompts, reviewing each suggestion against the system design, and verifying behavior with tests before accepting changes.
