# MLOps Courier Assistant

A courier chatbot powered by OpenRouter Groq API with AWS Lambda, DynamoDB, and GitHub Actions CI/CD pipeline.

## Architecture

- **Lambda**: Serverless compute for the chatbot
- **OpenRouter Groq API**: GPT models via OpenRouter for conversational AI
- **DynamoDB**: Stores conversation history
- **S3**: Stores prompts and logs
- **API Gateway**: REST endpoint
- **GitHub Actions**: Automated testing and deployment

## Quick Start

1. **Clone and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

3. **Configure AWS credentials:**
   ```bash
   aws configure
   ```

4. **Set up DynamoDB:**
   ```bash
   python infrastructure/create_table.py
   ```

5. **Run tests:**
   ```bash
   pytest tests/
   ```

## Prerequisites

- Python 3.11+
- AWS Account (free tier eligible)
- OpenRouter API Key ([Get one here](https://openrouter.io/))

## Environment Variables

Create a `.env` file based on `.env.example`:
```
OPENROUTER_API_KEY=sk-or-your-openrouter-key-here
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET=courier-ai-assistant-bucket
DYNAMODB_TABLE=courier-conversations
```

## GitHub Secrets

For automated deployment, add these secrets to your GitHub repository:
- `OPENROUTER_API_KEY`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
