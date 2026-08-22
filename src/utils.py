import json
import logging
from datetime import datetime

logger = logging.getLogger()


def load_system_prompt(s3_client, bucket, key):
    """Load the system prompt from S3."""
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to load prompt from S3: {e}")
        return "You are a helpful courier assistant."


def save_conversation(dynamodb, table_name, session_id, user_msg, ai_response):
    """Save conversation turn to DynamoDB."""
    try:
        table = dynamodb.Table(table_name)

        # Get existing history
        response = table.get_item(Key={'session_id': session_id})
        item = response.get('Item', {'session_id': session_id, 'history': []})

        # Append new turn
        item['history'].append({
            'user': user_msg,
            'assistant': ai_response,
            'timestamp': datetime.utcnow().isoformat()
        })

        # Keep only last 20 turns to save space
        item['history'] = item['history'][-20:]
        item['updated_at'] = datetime.utcnow().isoformat()

        table.put_item(Item=item)
    except Exception as e:
        logger.error(f"Failed to save conversation: {e}")


def log_to_s3(s3_client, bucket, session_id, user_msg, ai_response):
    """Log every interaction to S3 for monitoring and retraining."""
    log_entry = {
        'session_id': session_id,
        'timestamp': datetime.utcnow().isoformat(),
        'user_message': user_msg,
        'ai_response': ai_response
    }

    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    key = f"logs/{date_str}/{session_id}_{datetime.utcnow().timestamp()}.json"

    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(log_entry),
            ContentType='application/json'
        )
    except Exception as e:
        logger.error(f"Failed to log to S3: {e}")
