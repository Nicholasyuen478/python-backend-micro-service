from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, timezone
import uuid


STUDENT_TEACHER_RELATIONSHIP_TABLE_NAME = "poc-StudentTeacherRelationships"


class StudentTeacherRelationship(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "StudentId": "S001",
                "CreatedAt": "2024-10-08T10:30:00Z",
                "TeacherId": "T001",
                "Subject": "Mathematics",
            }
        }
    )

    # Primary Keys
    StudentId: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Student ID (Partition Key)",
        min_length=1,
        max_length=50,
    )
    CreatedAt: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Creation timestamp (Sort Key) in ISO format",
    )

    # Required Fields
    TeacherId: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Teacher ID",
        min_length=1,
        max_length=50,
    )
    Subject: str = Field(..., description="Subject name", min_length=1, max_length=100)

    # Optional Fields with Defaults
    StudentName: Optional[str] = Field(
        default=None, description="Full name of student", max_length=200
    )
    TeacherName: Optional[str] = Field(
        default=None, description="Full name of teacher", max_length=200
    )

    @field_validator("CreatedAt")
    @classmethod
    def validate_created_at(cls, v: str) -> str:
        """Validate CreatedAt is a valid ISO datetime string"""
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
            return v
        except ValueError:
            raise ValueError("CreatedAt must be a valid ISO datetime string")
