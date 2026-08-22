import pytest
import json
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, 'src')


@patch('lambda_function.load_system_prompt')
@patch('lambda_function.call_openrouter')
@patch('lambda_function.save_conversation')
@patch('lambda_function.log_to_s3')
@patch('lambda_function.get_conversation_history')
def test_successful_response(mock_history, mock_log, mock_save, mock_openrouter, mock_prompt):
    """Test that a valid message returns a 200 response."""
    from lambda_function import lambda_handler

    mock_prompt.return_value = "You are a courier assistant."
    mock_openrouter.return_value = "Your shipment is in transit."
    mock_history.return_value = []

    event = {
        'body': json.dumps({
            'message': 'Where is my package?',
            'session_id': 'test-123'
        })
    }

    result = lambda_handler(event, {})
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert 'response' in body
    assert body['response'] == "Your shipment is in transit."


def test_missing_message_returns_400():
    """Test that a missing message returns 400."""
    from lambda_function import lambda_handler

    event = {'body': json.dumps({})}
    result = lambda_handler(event, {})
    assert result['statusCode'] == 400


def test_response_has_cors_headers():
    """Test that CORS headers are present in every response."""
    from lambda_function import build_response
    result = build_response(200, {'test': 'data'})
    assert 'Access-Control-Allow-Origin' in result['headers']
