import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def create_table():
    dynamodb = boto3.client('dynamodb', region_name='us-east-2')

    try:
        dynamodb.create_table(
            TableName='courier-conversations',
            KeySchema=[
                {'AttributeName': 'session_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'session_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'  # Free tier — no provisioned capacity needed
        )
        print("Table created successfully!")
    except dynamodb.exceptions.ResourceInUseException:
        print("Table already exists.")

if __name__ == '__main__':
    create_table()
 
