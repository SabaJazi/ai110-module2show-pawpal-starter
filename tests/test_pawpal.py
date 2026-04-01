import unittest
from datetime import date, datetime, time
from uuid import uuid4
from pawpal_system import User, Pet, WalkSession, Medication, Frequency


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
            isCompleted=False,
        )
    
    def test_medication_completion(self):
        """Verify that calling markAsTaken() changes isCompleted to True."""
        self.assertFalse(self.medication.isCompleted)
        self.medication.markAsTaken()
        self.assertTrue(self.medication.isCompleted)
    
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


if __name__ == "__main__":
    unittest.main()