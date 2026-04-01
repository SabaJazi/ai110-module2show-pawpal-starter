from __future__ import annotations

from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


class DashboardSummary:
    """Initialize a dashboard summary with upcoming and overdue tasks."""
    def __init__(
        self,
        upcoming_walks: List[WalkSession],
        upcoming_medications: List[Medication],
        overdue_medications: List[Medication],
    ) -> None:
        self.upcoming_walks = upcoming_walks
        self.upcoming_medications = upcoming_medications
        self.overdue_medications = overdue_medications


class Reminder:
    """Initialize a reminder with a medication ID and time."""
    def __init__(self, medication_id: UUID, reminder_time: time) -> None:
        self.medication_id = medication_id
        self.reminder_time = reminder_time


class AdherenceEntry:
    def __init__(self, date_taken: date, was_taken: bool) -> None:
        """Initialize an adherence entry tracking when a dose was taken."""

        self.date_taken = date_taken
        self.was_taken = was_taken


class Frequency(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


class WalkSession:
    def __init__(
        self,
        walkId: UUID,
        pet: Pet,
        date: date,
        startTime: datetime,
        duration: int,
        distance: float,
        routePath: Optional[List[str]] = None,
    ) -> None:
        """Initialize a walk session with pet, date, time, and route details."""
        self.walkId = walkId
        self.pet = pet
        self.date = date
        self.startTime = startTime
        self.duration = duration
        self.distance = distance
        self.routePath = routePath if routePath is not None else []
        self.is_completed = False

    def startWalk(self) -> None:
        """Begins timing and GPS tracking."""
        self.startTime = datetime.now()
        print(f"Walk started at {self.startTime}")

    def endWalk(self) -> None:
        """Saves the duration and distance to the pet's history."""
        if self.startTime:
            self.duration = int((datetime.now() - self.startTime).total_seconds() // 60)
            self.is_completed = True
            print(f"Walk ended. Duration: {self.duration} minutes")

    def calculateCalories(self, species: str, distance: float) -> float:
        """Estimates energy burned based on pet species and distance."""
        species_factor = {
            "Dog": 5.0,
            "Cat": 3.0,
            "Rabbit": 2.5,
            "Hamster": 1.0,
        }
        factor = species_factor.get(species, 4.0)
        return distance * factor


class Medication:
    def __init__(
        self,
        medicationId: UUID,
        pet: Pet,
        drugName: str,
        dosage: str,
        frequency: Frequency,
        scheduledTimes: Optional[List[time]] = None,
        isCompleted: bool = False,
    ) -> None:
        """Initialize a medication with drug name, dosage, frequency, and scheduled times."""

        self.medicationId = medicationId
        self.pet = pet
        self.drugName = drugName
        self.dosage = dosage
        self.frequency = frequency
        self.scheduledTimes = scheduledTimes if scheduledTimes is not None else []
        self.isCompleted = isCompleted
        self.adherence_log: List[AdherenceEntry] = []

    def setReminder(self, reminder_time: time) -> None:
        """Configures the system push notification/alarm."""
        if reminder_time not in self.scheduledTimes:
            self.scheduledTimes.append(reminder_time)
            print(f"Reminder set for {self.drugName} at {reminder_time}")

    def markAsTaken(self) -> None:
        """Updates the status for the current time slot."""
        self.isCompleted = True
        today = date.today()
        self.adherence_log.append(AdherenceEntry(today, True))
        print(f"{self.drugName} marked as taken on {today}")

    def getAdherenceLog(self) -> List[AdherenceEntry]:
        """Returns a history of missed vs. taken doses."""
        return self.adherence_log


class Pet:
    def __init__(
        self,
        petId: UUID,
        name: str,
        species: str,
        breed: str,
        age: int,
        medicalRecords: Optional[List[Medication]] = None,
        walkHistory: Optional[List[WalkSession]] = None,
    ) -> None:
        """Initialize a pet with name, species, breed, age, and empty task lists."""
        self.petId = petId
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.medicalRecords = medicalRecords if medicalRecords is not None else []
        self.walkHistory = walkHistory if walkHistory is not None else []

    def updateProfile(self, data: Dict[str, Any]) -> None:
        """Modifies pet details."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
                print(f"Updated {key} to {value}")

    def getUpcomingReminders(self) -> List[Reminder]:
        """Filters medications and sessions by the current date."""
        today = date.today()
        upcoming_reminders = []
        
        for medication in self.medicalRecords:
            if medication.frequency == Frequency.DAILY:
                for scheduled_time in medication.scheduledTimes:
                    upcoming_reminders.append(
                        Reminder(medication.medicationId, scheduled_time)
                    )
        
        return upcoming_reminders


class User:
    def __init__(self, userId: UUID, name: str, email: str, pets: Optional[List[Pet]] = None) -> None:
        """Initialize a user with ID, name, email, and optional pet list."""
        self.userId = userId
        self.name = name
        self.email = email
        self.pets = pets if pets is not None else []

    def addPet(self, pet: Pet) -> None:
        """Links a new pet profile to the user."""
        if pet not in self.pets:
            self.pets.append(pet)
            print(f"Added pet {pet.name} to user {self.name}")

    def removePet(self, petId: str) -> None:
        """Deletes a pet profile."""
        self.pets = [p for p in self.pets if str(p.petId) != petId]
        print(f"Removed pet {petId}")

    def getDashboard(self) -> DashboardSummary:
        """Summarizes upcoming walks and medications for all pets."""
        today = date.today()
        upcoming_walks = []
        upcoming_medications = []
        overdue_medications = []
        
        for pet in self.pets:
            for walk in pet.walkHistory:
                if walk.date >= today and not walk.is_completed:
                    upcoming_walks.append(walk)
            
            for med in pet.medicalRecords:
                if not med.isCompleted and med.frequency == Frequency.DAILY:
                    upcoming_medications.append(med)
        
        return DashboardSummary(upcoming_walks, upcoming_medications, overdue_medications)


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    
    def __init__(self, user: User) -> None:
        """Initialize scheduler with a user."""
        self.user = user

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Retrieves all tasks (walks and medications) across all pets."""
        tasks = []
        
        for pet in self.user.pets:
            for walk in pet.walkHistory:
                tasks.append({
                    "type": "Walk",
                    "pet_name": pet.name,
                    "description": f"Walk for {pet.name}",
                    "date": walk.date,
                    "time": walk.startTime,
                    "completed": walk.is_completed,
                })
            
            for med in pet.medicalRecords:
                for scheduled_time in med.scheduledTimes:
                    # Normalize time to datetime for consistent sorting
                    med_datetime = datetime.combine(date.today(), scheduled_time)
                    tasks.append({
                        "type": "Medication",
                        "pet_name": pet.name,
                        "description": f"{med.drugName} ({med.dosage}) for {pet.name}",
                        "date": date.today(),
                        "time": med_datetime,  # Now a datetime, not time
                        "completed": med.isCompleted,
                    })
        
        return tasks

    def get_tasks_by_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Organizes tasks by a specific date."""
        all_tasks = self.get_all_tasks()
        return [task for task in all_tasks if task["date"] == target_date]

    def get_tasks_by_pet(self, pet_id: UUID) -> List[Dict[str, Any]]:
        """Retrieves all tasks for a specific pet."""
        pet = next((p for p in self.user.pets if p.petId == pet_id), None)
        if not pet:
            return []
        
        tasks = []
        
        for walk in pet.walkHistory:
            tasks.append({
                "type": "Walk",
                "description": f"Walk for {pet.name}",
                "date": walk.date,
                "time": walk.startTime,
                "completed": walk.is_completed,
            })
        
        for med in pet.medicalRecords:
            for scheduled_time in med.scheduledTimes:
                med_datetime = datetime.combine(date.today(), scheduled_time)
                tasks.append({
                    "type": "Medication",
                    "description": f"{med.drugName} ({med.dosage})",
                    "date": date.today(),
                    "time": med_datetime,  # Now a datetime, not time
                    "completed": med.isCompleted,
                })
        
        return tasks

    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Retrieves tasks that are overdue."""
        today = date.today()
        all_tasks = self.get_all_tasks()
        return [task for task in all_tasks if task["date"] < today and not task["completed"]]

    def schedule_task(self, pet_id: UUID, task_type: str, task_data: Dict[str, Any]) -> None:
        """Schedules a new task (walk or medication) for a pet."""
        pet = next((p for p in self.user.pets if p.petId == pet_id), None)
        if not pet:
            print(f"Pet {pet_id} not found")
            return
        
        if task_type == "Walk":
            walk = WalkSession(
                walkId=uuid4(),
                pet=pet,
                date=task_data.get("date"),
                startTime=task_data.get("startTime"),
                duration=task_data.get("duration", 0),
                distance=task_data.get("distance", 0.0),
                routePath=task_data.get("routePath"),
            )
            pet.walkHistory.append(walk)
            print(f"Scheduled walk for {pet.name} on {walk.date}")
        
        elif task_type == "Medication":
            med = Medication(
                medicationId=uuid4(),
                pet=pet,
                drugName=task_data.get("drugName"),
                dosage=task_data.get("dosage"),
                frequency=task_data.get("frequency", Frequency.DAILY),
                scheduledTimes=task_data.get("scheduledTimes"),
            )
            pet.medicalRecords.append(med)
            print(f"Scheduled medication {med.drugName} for {pet.name}")