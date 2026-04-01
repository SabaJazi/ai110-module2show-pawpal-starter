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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
