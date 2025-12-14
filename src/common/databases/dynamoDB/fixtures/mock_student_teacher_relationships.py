from typing import Any, List, Dict
import boto3
from faker import Faker

from ....config import settings
from ..models import STUDENT_TEACHER_RELATIONSHIP_TABLE_NAME

# Constants
TABLE_NAME = STUDENT_TEACHER_RELATIONSHIP_TABLE_NAME
NUM_STUDENTS = 20
NUM_TEACHERS = 8
NUM_ENROLLMENTS = 50

# Initialize Faker and DynamoDB resource
fake = Faker()
dynamodb: Any = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)
table = dynamodb.Table(TABLE_NAME)


def generate_students(num_students: int) -> List[Dict[str, str]]:
    """Generate a list of students."""
    return [{"id": fake.uuid4(), "name": fake.name()} for i in range(num_students)]


def generate_teachers(num_teachers: int) -> List[Dict[str, str]]:
    """Generate a list of teachers."""
    return [
        {"id": fake.uuid4(), "name": f"{fake.prefix()} {fake.name()}"}
        for i in range(num_teachers)
    ]


def generate_subjects(num_subjects: int) -> List[str]:
    """Generate a list of subjects."""
    return [
        f"{fake.word().capitalize()} {fake.random_element(['Science', 'Studies', 'Arts', 'Engineering', 'Mathematics'])}"
        for _ in range(num_subjects)
    ]


def generate_enrollment(
    student: Dict[str, str], teacher: Dict[str, str], subject: str
) -> Dict[str, Any]:
    """Generate a single enrollment record."""
    created_at = fake.date_time_between(start_date="-1y", end_date="now").isoformat()
    return {
        "StudentId": student["id"],
        "CreatedAt": created_at,
        "TeacherId": teacher["id"],
        "Subject": subject,
        "StudentName": student["name"],
        "TeacherName": teacher["name"],
    }


def seed_data():
    """Seed mock data into the DynamoDB table."""
    print("🎲 Generating mock data with Faker...")

    students = generate_students(NUM_STUDENTS)
    teachers = generate_teachers(NUM_TEACHERS)
    subjects = generate_subjects(10)

    print(f"📝 Creating {NUM_ENROLLMENTS} enrollments...")

    with table.batch_writer() as batch:
        enrollments = [
            generate_enrollment(
                fake.random_element(students),
                fake.random_element(teachers),
                fake.random_element(subjects),
            )
            for _ in range(NUM_ENROLLMENTS)
        ]

        for i, enrollment in enumerate(enrollments):
            batch.put_item(Item=enrollment)
            if (i + 1) % 25 == 0:
                print(f"   ✓ Written {i + 1}/{NUM_ENROLLMENTS} items...")

    print(f"✅ Successfully seeded {NUM_ENROLLMENTS} items to '{TABLE_NAME}'!")


if __name__ == "__main__":
    seed_data()
