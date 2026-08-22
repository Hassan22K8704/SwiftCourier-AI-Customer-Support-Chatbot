#!/bin/bash
# AWS CLI setup script for Courier AI Assistant

echo "Setting up AWS CLI for Courier AI Assistant..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it from https://aws.amazon.com/cli/"
    exit 1
fi

# Configure AWS credentials
echo "Configuring AWS credentials..."
aws configure

# Create S3 bucket
BUCKET_NAME="courier-ai-assistant-bucket"
echo "Creating S3 bucket: $BUCKET_NAME"
aws s3 mb s3://$BUCKET_NAME --region us-east-1 || echo "Bucket already exists"

# Create S3 folder structure
echo "Creating S3 folder structure..."
aws s3api put-object --bucket $BUCKET_NAME --key prompts/
aws s3api put-object --bucket $BUCKET_NAME --key logs/
aws s3api put-object --bucket $BUCKET_NAME --key models/

# Upload the system prompt
echo "Uploading system prompt to S3..."
aws s3 cp ../src/prompt.txt s3://$BUCKET_NAME/prompts/prompt.txt

echo "AWS setup complete!"
