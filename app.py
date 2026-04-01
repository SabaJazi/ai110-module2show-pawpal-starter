import streamlit as st
import pandas as pd
from uuid import uuid4  
from datetime import date, datetime

from pawpal_system import User, Pet, WalkSession, Medication, Frequency, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

st.divider()
st.subheader("Owner & Pet Setup")

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )
owner_name = st.text_input("Owner name", value="Jordan", key="setup_owner_name")
owner_email = st.text_input("Owner email", value="demo@example.com", key="setup_owner_email")


if "owner" not in st.session_state:
    st.session_state["owner"] = User(
        userId=uuid4(),
        name=owner_name,
        email=owner_email,
        pets=[],
    )

owner = st.session_state["owner"]
owner.name = owner_name
owner.email = owner_email

pet_name = st.text_input("Pet name", value="Mochi", key="setup_pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="setup_species")
breed = st.text_input("Breed", value="Mixed", key="setup_breed")
age = st.number_input("Age", min_value=0, max_value=40, value=2, key="setup_age")
if st.button("Add pet"):
    exists = any(p.name.lower() == pet_name.strip().lower() for p in owner.pets)
    if exists:
        st.info("That pet already exists for this owner.")
    else:
        new_pet = Pet(
            petId=uuid4(),
            name=pet_name.strip(),
            species=species,
            breed=breed.strip(),
            age=int(age),
        )
        owner.addPet(new_pet)
        st.success(f"Added pet: {new_pet.name}")
if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": p.name, "species": p.species, "breed": p.breed, "age": p.age} for p in owner.pets]
    )
else:
    st.info("No pets added yet.")
st.divider()
st.subheader("Schedule a Task")

scheduler = Scheduler(owner)

if not owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    pet_options = {f"{p.name} ({p.species})": p for p in owner.pets}
    selected_pet_label = st.selectbox("Select pet", list(pet_options.keys()), key="selected_pet")
    selected_pet = pet_options[selected_pet_label]

    task_type = st.selectbox("Task type", ["Walk", "Medication"], key="schedule_task_type")

    if task_type == "Walk":
        walk_date = st.date_input("Walk date", value=date.today(), key="walk_date")
        walk_time = st.time_input("Walk start time", key="walk_time")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="walk_duration")
        distance = st.number_input("Distance", min_value=0.0, value=1.0, step=0.1, key="walk_distance")

        if st.button("Schedule walk"):
            scheduler.schedule_task(
                pet_id=selected_pet.petId,
                task_type="Walk",
                task_data={
                    "date": walk_date,
                    "startTime": datetime.combine(walk_date, walk_time),
                    "duration": int(duration),
                    "distance": float(distance),
                    "routePath": [],
                },
            )
            st.success(f"Walk scheduled for {selected_pet.name}")

    else:
        drug_name = st.text_input("Medication name", value="Amoxicillin", key="med_name")
        dosage = st.text_input("Dosage", value="250mg", key="med_dosage")
        freq_label = st.selectbox("Frequency", ["DAILY", "WEEKLY"], key="med_frequency")
        med_time = st.time_input("Medication time", key="med_time")

        if st.button("Schedule medication"):
            scheduler.schedule_task(
                pet_id=selected_pet.petId,
                task_type="Medication",
                task_data={
                    "drugName": drug_name.strip(),
                    "dosage": dosage.strip(),
                    "frequency": Frequency[freq_label],
                    "scheduledTimes": [med_time],
                },
            )
            st.success(f"Medication scheduled for {selected_pet.name}")

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan", key="quick_owner_name")
pet_name = st.text_input("Pet name", value="Mochi", key="quick_pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="quick_species")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="quick_task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="quick_duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="quick_priority")

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    today_tasks = scheduler.get_tasks_by_date(date.today())

    if not today_tasks:
        st.info("No tasks scheduled for today.")
    else:
        sorted_tasks = scheduler.sort_by_time(today_tasks)
        pending_tasks = scheduler.filter_by_status(sorted_tasks, completed=False)
        completed_tasks = scheduler.filter_by_status(sorted_tasks, completed=True)

        st.success(f"Schedule generated with {len(sorted_tasks)} task(s) for today.")

        summary_col1, summary_col2, summary_col3 = st.columns(3)
        summary_col1.metric("Total", len(sorted_tasks))
        summary_col2.metric("Pending", len(pending_tasks))
        summary_col3.metric("Completed", len(completed_tasks))

        display_rows = [
            {
                "time": task["time"].strftime("%H:%M"),
                "type": task["type"],
                "pet": task.get("pet_name", ""),
                "description": task["description"],
                "completed": task["completed"],
            }
            for task in sorted_tasks
        ]

        schedule_df = pd.DataFrame(display_rows)

        def highlight_status(row):
            row_color = "#eaf7ee" if row["completed"] else "#fff4e5"
            return [f"background-color: {row_color}"] * len(row)

        st.markdown("### Full Schedule (Sorted)")
        st.dataframe(
            schedule_df.style.apply(highlight_status, axis=1),
            use_container_width=True,
            hide_index=True,
        )

        pending_rows = [row for row in display_rows if not row["completed"]]
        completed_rows = [row for row in display_rows if row["completed"]]

        pending_col, completed_col = st.columns(2)
        with pending_col:
            st.markdown("#### Pending Tasks")
            if pending_rows:
                st.dataframe(pd.DataFrame(pending_rows), use_container_width=True, hide_index=True)
            else:
                st.success("All tasks are completed for today.")

        with completed_col:
            st.markdown("#### Completed Tasks")
            if completed_rows:
                st.dataframe(pd.DataFrame(completed_rows), use_container_width=True, hide_index=True)
            else:
                st.info("No completed tasks yet.")

    conflicts = scheduler.check_conflicts()
    if conflicts:
        st.warning("Scheduling conflicts detected:")
        for warning in conflicts:
            st.write(f"- {warning}")
    else:
        st.success("No scheduling conflicts detected.")

    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
