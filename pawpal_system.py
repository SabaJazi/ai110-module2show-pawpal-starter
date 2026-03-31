from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import Any, Dict, List
from uuid import UUID


class DashboardSummary:
    pass


class Reminder:
    pass


class AdherenceEntry:
    pass


class Frequency(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


class User:
    def __init__(self, userId: UUID, name: str, email: str, pets: List["Pet"]) -> None:
        self.userId = userId
        self.name = name
        self.email = email
        self.pets = pets

    def addPet(self, pet: "Pet") -> None:
        pass

    def removePet(self, petId: str) -> None:
        pass

    def getDashboard(self) -> DashboardSummary:
        pass


class Pet:
    def __init__(
        self,
        petId: UUID,
        name: str,
        species: str,
        breed: str,
        age: int,
        medicalRecords: List["Medication"],
        walkHistory: List["WalkSession"],
    ) -> None:
        self.petId = petId
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.medicalRecords = medicalRecords
        self.walkHistory = walkHistory

    def updateProfile(self, data: Dict[str, Any]) -> None:
        pass

    def getUpcomingReminders(self) -> List[Reminder]:
        pass


class WalkSession:
    def __init__(
        self,
        walkId: UUID,
        date: date,
        startTime: datetime,
        duration: int,
        distance: float,
        routePath: List[str],
    ) -> None:
        self.walkId = walkId
        self.date = date
        self.startTime = startTime
        self.duration = duration
        self.distance = distance
        self.routePath = routePath

    def startWalk(self) -> None:
        pass

    def endWalk(self) -> None:
        pass

    def calculateCalories(self, species: str, distance: float) -> float:
        pass


class Medication:
    def __init__(
        self,
        medicationId: UUID,
        drugName: str,
        dosage: str,
        frequency: Frequency,
        scheduledTimes: List[time],
        isCompleted: bool,
    ) -> None:
        self.medicationId = medicationId
        self.drugName = drugName
        self.dosage = dosage
        self.frequency = frequency
        self.scheduledTimes = scheduledTimes
        self.isCompleted = isCompleted

    def setReminder(self, time: time) -> None:
        pass

    def markAsTaken(self) -> None:
        pass

    def getAdherenceLog(self) -> List[AdherenceEntry]:
        pass