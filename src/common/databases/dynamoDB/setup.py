from typing import Any
import boto3
from common.config import settings

from .models import STUDENT_TEACHER_RELATIONSHIP_TABLE_NAME

# Initialize DynamoDB resource with credentials from .env
dynamodb: Any = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def create_student_teacher_relationship_table():
    # Create StudentTeacherRelationships table
    TABLE_NAME = STUDENT_TEACHER_RELATIONSHIP_TABLE_NAME
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    "AttributeName": "StudentId",
                    "KeyType": "HASH",  # Partition key
                },
                {
                    "AttributeName": "CreatedAt",
                    "KeyType": "RANGE",  # Sort key
                },
            ],
            AttributeDefinitions=[
                {"AttributeName": "StudentId", "AttributeType": "S"},
                {"AttributeName": "CreatedAt", "AttributeType": "S"},
                {"AttributeName": "Subject", "AttributeType": "S"},
                {"AttributeName": "TeacherId", "AttributeType": "S"},
            ],
            LocalSecondaryIndexes=[
                {
                    "IndexName": "SubjectIndex",
                    "KeySchema": [
                        {"AttributeName": "StudentId", "KeyType": "HASH"},
                        {"AttributeName": "Subject", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "TeacherIdIndex",
                    "KeySchema": [
                        {"AttributeName": "TeacherId", "KeyType": "HASH"},
                        {"AttributeName": "CreatedAt", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 10,
                        "WriteCapacityUnits": 10,
                    },
                }
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        print("Table status:", table.table_status)

    except Exception as e:
        print(f"Error creating table: {e}")


def set_up():
    create_student_teacher_relationship_table()


if __name__ == "__main__":
    set_up()
