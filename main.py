from datetime import date, datetime, time, timedelta

from uuid import uuid4
from pawpal_system import User, Pet, WalkSession, Medication, Frequency, Scheduler

def print_tasks(title, tasks):
    # Helper function to print tasks in a readable format
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        task_time = task["time"]
        time_str = task_time.strftime("%Y-%m-%d %H:%M") if isinstance(task_time, datetime) else str(task_time)
        print(f"{i}. {task['type']} | {time_str} | {task['description']} | Completed: {task['completed']}")

def main():
    # Create sample data
    owner = User(userId=uuid4(), name="Alice Johnson", email="alice@example.com")
    dog = Pet(petId=uuid4(), name="Max", species="Dog", breed="Golden Retriever", age=5)
    cat = Pet(petId=uuid4(), name="Whiskers", species="Cat", breed="Persian", age=3)
    
    owner.addPet(dog)
    owner.addPet(cat)
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # Add tasks
    dog.walkHistory.append(WalkSession(walkId=uuid4(), pet=dog, date=today, startTime=datetime.combine(today, time(18, 0)), duration=30, distance=3.5))
    dog.walkHistory.append(WalkSession(walkId=uuid4(), pet=dog, date=today, startTime=datetime.combine(today, time(18, 0)), duration=20, distance=2.0))  # CONFLICT: same time as above
    dog.walkHistory.append(WalkSession(walkId=uuid4(), pet=dog, date=yesterday, startTime=datetime.combine(yesterday, time(20, 0)), duration=20, distance=2.0))
    
    cat.medicalRecords.append(Medication(medicationId=uuid4(), pet=cat, drugName="Amoxicillin", dosage="250mg", frequency=Frequency.DAILY, scheduledTimes=[time(14, 0)]))
    dog.medicalRecords.append(Medication(medicationId=uuid4(), pet=dog, drugName="Aspirin", dosage="100mg", frequency=Frequency.DAILY, scheduledTimes=[time(19, 0), time(9, 0)]))
    
    scheduler = Scheduler(owner)
    
    # Check conflicts
    print("\n" + "=" * 70)
    print("CONFLICT DETECTION")
    print("=" * 70)
    
    conflicts = scheduler.check_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")
    
    pet_conflicts = scheduler.check_conflicts(pet_id=dog.petId)
    if pet_conflicts:
        print(f"\nConflicts for Max:\n" + "\n".join(pet_conflicts))
        suggested = scheduler.suggest_reschedule(dog.petId, "Walk", datetime.now())
        if suggested:
            print(f"Try scheduling at {suggested.strftime('%H:%M')} instead")
    

# 1) Sorting check: all tasks sorted by time
    all_tasks = scheduler.get_all_tasks()
    print_tasks("ALL TASKS (SORTED BY TIME)", sorted(all_tasks, key=lambda task: task["time"]))
    
    todays_tasks = scheduler.get_tasks_by_date(today)
    print_tasks(f"TODAY'S TASKS ({today})", sorted(todays_tasks, key=lambda task: task["time"]))
    
    dog_tasks = scheduler.get_tasks_by_pet(dog.petId)
    print_tasks(f"TASKS FOR PET: {dog.name}", sorted(dog_tasks, key=lambda task: task["time"]))
    
    overdue_tasks = scheduler.get_overdue_tasks()
    print_tasks("OVERDUE TASKS", sorted(overdue_tasks, key=lambda task: task["time"]))

if __name__ == "__main__":
    main()