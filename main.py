from datetime import date, datetime, time
from uuid import uuid4
from pawpal_system import User, Pet, WalkSession, Medication, Frequency, Scheduler


def main():
    # Create an Owner (User)
    owner_id = uuid4()
    owner = User(
        userId=owner_id,
        name="Alice Johnson",
        email="alice@example.com",
    )
    
    # Create two Pets
    dog_id = uuid4()
    dog = Pet(
        petId=dog_id,
        name="Max",
        species="Dog",
        breed="Golden Retriever",
        age=5,
    )
    
    cat_id = uuid4()
    cat = Pet(
        petId=cat_id,
        name="Whiskers",
        species="Cat",
        breed="Persian",
        age=3,
    )
    
    # Add pets to owner
    owner.addPet(dog)
    owner.addPet(cat)
    
    # Create at least three tasks with different times
    today = date.today()
    
    # Task 1: Morning walk for Max
    walk_1 = WalkSession(
        walkId=uuid4(),
        pet=dog,
        date=today,
        startTime=datetime.combine(today, time(7, 0)),
        duration=30,
        distance=3.5,
    )
    dog.walkHistory.append(walk_1)
    
    # Task 2: Afternoon medication for Whiskers
    med_1 = Medication(
        medicationId=uuid4(),
        pet=cat,
        drugName="Amoxicillin",
        dosage="250mg",
        frequency=Frequency.DAILY,
        scheduledTimes=[time(14, 0)],
    )
    cat.medicalRecords.append(med_1)
    
    # Task 3: Evening walk for Max
    walk_2 = WalkSession(
        walkId=uuid4(),
        pet=dog,
        date=today,
        startTime=datetime.combine(today, time(18, 30)),
        duration=45,
        distance=5.0,
    )
    dog.walkHistory.append(walk_2)
    
    # Additional task: Evening medication for Max
    med_2 = Medication(
        medicationId=uuid4(),
        pet=dog,
        drugName="Aspirin",
        dosage="100mg",
        frequency=Frequency.DAILY,
        scheduledTimes=[time(19, 0), time(9, 0)],
    )
    dog.medicalRecords.append(med_2)
    
    # Create a Scheduler and get today's tasks
    scheduler = Scheduler(owner)
    todays_tasks = scheduler.get_tasks_by_date(today)
    
    # Print Today's Schedule
    print("=" * 60)
    print(f"TODAY'S SCHEDULE - {owner.name}")
    print(f"Date: {today}")
    print("=" * 60)
    print()
    
    if todays_tasks:
        # Sort tasks by time
        todays_tasks.sort(key=lambda x: x["time"])
        
        for i, task in enumerate(todays_tasks, 1):
            task_time = task["time"]
            if isinstance(task_time, datetime):
                time_str = task_time.strftime("%H:%M")
            else:
                time_str = str(task_time)
            
            print(f"{i}. [{time_str}] {task['type']} - {task['description']}")
            print(f"   Pet: {task['pet_name']}")
            print(f"   Status: {'✓ Completed' if task['completed'] else '○ Pending'}")
            print()
    else:
        print("No tasks scheduled for today.")
    
    print("=" * 60)
    print(f"Total tasks today: {len(todays_tasks)}")
    print("=" * 60)


if __name__ == "__main__":
    main()