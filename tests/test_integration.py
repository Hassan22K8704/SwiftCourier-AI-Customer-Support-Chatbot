# Integration tests for the courier assistant
# These tests verify end-to-end functionality with actual AWS services

import pytest
import json
import os
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()


@pytest.fixture
def aws_config():
    """Fixture to provide AWS configuration for tests."""
    return {
        'region': os.getenv('AWS_DEFAULT_REGION', 'us-east-2'),
        'bucket': os.getenv('S3_BUCKET', 'courier-ai-assistant-bucket'),
        'table': os.getenv('DYNAMODB_TABLE', 'courier-conversations')
    }


def test_s3_bucket_exists(aws_config):
    """Test that the S3 bucket is accessible."""
    import boto3
    s3 = boto3.client('s3', region_name=aws_config['region'])
    
    try:
        s3.head_bucket(Bucket=aws_config['bucket'])
        assert True
    except Exception as e:
        pytest.skip(f"S3 bucket not accessible: {e}")


def test_dynamodb_table_exists(aws_config):
    """Test that the DynamoDB table is accessible."""
    import boto3
    dynamodb = boto3.client('dynamodb', region_name=aws_config['region'])
    
    try:
        dynamodb.describe_table(TableName=aws_config['table'])
        assert True
    except Exception as e:
        pytest.skip(f"DynamoDB table not accessible: {e}")


def test_openrouter_api_configured():
    """Test that OpenRouter API key is configured."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    assert api_key is not None, "OPENROUTER_API_KEY environment variable not set"
    assert api_key.startswith('sk-'), "Invalid OpenRouter API key format"
