import unittest
from datetime import date, datetime, time, timedelta
from uuid import uuid4
from pawpal_system import User, Pet, WalkSession, Medication, Frequency, Scheduler


class TestTaskCompletion(unittest.TestCase):
    """Test that task completion status changes when marked as complete."""

    def setUp(self):
        """Create a test pet and medication."""
        self.pet = Pet(
            petId=uuid4(),
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
        )
        self.medication = Medication(
            medicationId=uuid4(),
            pet=self.pet,
            drugName="Aspirin",
            dosage="100mg",
            frequency=Frequency.DAILY,
            scheduledTimes=[time(9, 0)],
            isCompleted=False,  # fixed name
        )

    def test_medication_completion(self):
        """Verify that calling markAsTaken() changes is_completed to True."""
        self.assertFalse(self.medication.is_completed)
        self.medication.markAsTaken()
        self.assertTrue(self.medication.is_completed)

    def test_walk_completion(self):
        """Verify that calling endWalk() changes is_completed to True."""
        walk = WalkSession(
            walkId=uuid4(),
            pet=self.pet,
            date=date.today(),
            startTime=datetime.now(),
            duration=0,
            distance=0.0,
        )

        self.assertFalse(walk.is_completed)
        walk.endWalk()
        self.assertTrue(walk.is_completed)


class TestTaskAddition(unittest.TestCase):
    """Test that adding tasks to a pet increases the task count."""

    def setUp(self):
        """Create a test pet."""
        self.pet = Pet(
            petId=uuid4(),
            name="Whiskers",
            species="Cat",
            breed="Persian",
            age=3,
        )

    def test_add_walk_to_pet(self):
        """Verify that adding a walk increases the pet's walk count."""
        initial_count = len(self.pet.walkHistory)
        self.assertEqual(initial_count, 0)

        walk = WalkSession(
            walkId=uuid4(),
            pet=self.pet,
            date=date.today(),
            startTime=datetime.now(),
            duration=30,
            distance=2.5,
        )
        self.pet.walkHistory.append(walk)

        self.assertEqual(len(self.pet.walkHistory), initial_count + 1)

    def test_add_medication_to_pet(self):
        """Verify that adding a medication increases the pet's medication count."""
        initial_count = len(self.pet.medicalRecords)
        self.assertEqual(initial_count, 0)

        med = Medication(
            medicationId=uuid4(),
            pet=self.pet,
            drugName="Amoxicillin",
            dosage="250mg",
            frequency=Frequency.DAILY,
            scheduledTimes=[time(14, 0)],
        )
        self.pet.medicalRecords.append(med)

        self.assertEqual(len(self.pet.medicalRecords), initial_count + 1)

    def test_add_multiple_tasks(self):
        """Verify that adding multiple tasks increases counts appropriately."""
        for i in range(2):
            walk = WalkSession(
                walkId=uuid4(),
                pet=self.pet,
                date=date.today(),
                startTime=datetime.now(),
                duration=30,
                distance=2.5,
            )
            self.pet.walkHistory.append(walk)

        for i in range(3):
            med = Medication(
                medicationId=uuid4(),
                pet=self.pet,
                drugName=f"Drug{i}",
                dosage="100mg",
                frequency=Frequency.DAILY,
                scheduledTimes=[time(9 + i, 0)],
            )
            self.pet.medicalRecords.append(med)

        self.assertEqual(len(self.pet.walkHistory), 2)
        self.assertEqual(len(self.pet.medicalRecords), 3)


class TestSchedulerCoreBehaviors(unittest.TestCase):
    def setUp(self):
        self.pet = Pet(
            petId=uuid4(),
            name="Buddy",
            species="Dog",
            breed="Lab",
            age=4,
        )
        self.user = User(
            userId=uuid4(),
            name="Owner",
            email="owner@example.com",
            pets=[self.pet],
        )
        self.scheduler = Scheduler(self.user)

    def test_sorting_correctness_returns_chronological_order(self):
        base_day = date.today()

        walk_late = WalkSession(
            walkId=uuid4(),
            pet=self.pet,
            date=base_day,
            startTime=datetime.combine(base_day, time(18, 0)),
            duration=20,
            distance=1.2,
        )
        walk_early = WalkSession(
            walkId=uuid4(),
            pet=self.pet,
            date=base_day,
            startTime=datetime.combine(base_day, time(8, 0)),
            duration=15,
            distance=0.8,
        )
        self.pet.walkHistory.extend([walk_late, walk_early])

        med = Medication(
            medicationId=uuid4(),
            pet=self.pet,
            drugName="Omega",
            dosage="1 pill",
            frequency=Frequency.DAILY,
            scheduledTimes=[time(12, 0)],
            scheduledDate=base_day,
        )
        self.pet.medicalRecords.append(med)

        tasks = self.scheduler.get_all_tasks()
        sorted_tasks = self.scheduler.sort_by_time(tasks)
        sorted_times = [t["time"] for t in sorted_tasks]

        self.assertEqual(sorted_times, sorted(sorted_times))

    def test_recurrence_logic_daily_task_creates_next_day_task(self):
        today = date.today()
        med = Medication(
            medicationId=uuid4(),
            pet=self.pet,
            drugName="Antibiotic",
            dosage="100mg",
            frequency=Frequency.DAILY,
            scheduledTimes=[time(9, 0)],
            scheduledDate=today,
        )
        self.pet.medicalRecords.append(med)

        next_med = med.markAsTaken()

        self.assertIsNotNone(next_med)
        self.assertTrue(med.is_completed)
        self.assertEqual(next_med.scheduled_date, today + timedelta(days=1))
        self.assertIn(next_med, self.pet.medicalRecords)

    def test_conflict_detection_flags_duplicate_times(self):
        target_day = date.today()
        conflict_time = datetime.combine(target_day, time(10, 0))

        walk = WalkSession(
            walkId=uuid4(),
            pet=self.pet,
            date=target_day,
            startTime=conflict_time,
            duration=30,
            distance=2.0,
        )
        self.pet.walkHistory.append(walk)

        med = Medication(
            medicationId=uuid4(),
            pet=self.pet,
            drugName="Vitamin",
            dosage="50mg",
            frequency=Frequency.DAILY,
            scheduledTimes=[time(10, 0)],
            scheduledDate=target_day,
        )
        self.pet.medicalRecords.append(med)

        warnings = self.scheduler.check_conflicts()

        self.assertGreaterEqual(len(warnings), 1)
        self.assertTrue(any("CONFLICT" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()