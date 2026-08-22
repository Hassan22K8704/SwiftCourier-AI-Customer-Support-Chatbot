import json
import os
import boto3
import logging
from datetime import datetime
from openai import OpenAI
from utils import save_conversation, load_system_prompt, log_to_s3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

BUCKET_NAME = 'courier-ai-assistant-bucket'
TABLE_NAME = 'courier-conversations'
PROMPT_KEY = 'prompts/prompt.txt'


def lambda_handler(event, context):
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        user_message = body.get('message', '')
        session_id = body.get('session_id', 'default')

        if not user_message:
            return build_response(400, {'error': 'Message is required'})

        logger.info(f"Received message from session {session_id}: {user_message}")

        system_prompt = load_system_prompt(s3_client, BUCKET_NAME, PROMPT_KEY)
        conversation_history = get_conversation_history(session_id)
        ai_response = call_openrouter(user_message, system_prompt, conversation_history)
        save_conversation(dynamodb, TABLE_NAME, session_id, user_message, ai_response)
        log_to_s3(s3_client, BUCKET_NAME, session_id, user_message, ai_response)

        logger.info(f"Response generated for session {session_id}")
        return build_response(200, {'response': ai_response, 'session_id': session_id})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return build_response(500, {'error': 'Internal server error'})


def call_openrouter(user_message, system_prompt, history):
    client = OpenAI(
        api_key=os.environ['OPENROUTER_API_KEY'],  # ← from environment variable
        base_url="https://openrouter.ai/api/v1"    # ← correct URL
    )

    messages = [{"role": "system", "content": system_prompt}]
    for turn in history[-5:]:
        messages.append({"role": "user", "content": turn['user']})
        messages.append({"role": "assistant", "content": turn['assistant']})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content


def get_conversation_history(session_id):
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={'session_id': session_id})
        item = response.get('Item', {})
        return item.get('history', [])
    except Exception as e:
        logger.warning(f"Could not fetch history: {e}")
        return []


def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body)
    }

    
