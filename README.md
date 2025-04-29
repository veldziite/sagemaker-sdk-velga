# SageMaker Studio CDK Deployment

This project uses the **AWS Cloud Development Kit (CDK)** in Python to deploy and manage a SageMaker Studio environment with user profiles and a pre-trained model.

## 🚀 Features

- **SageMaker Studio Domain**: Creates a secure VPC, subnets, and a SageMaker Studio domain with required configurations.
- **User Profiles**: Adds multiple SageMaker Studio user profiles (e.g., `admin`, `developer`, `analyst`).
- **Pre-trained Model (Optional)**: Script support for identifying and deploying a JumpStart pre-trained text classification model.
- **Tagging & Outputs**: Adds metadata tags and CloudFormation outputs for visibility and tracking.
  
## 📁 Structure

- `app.py` – Entry point that wires all CDK stacks together.
- `sagemaker_studio_domain_stack.py` – Defines the SageMaker Studio Domain and its networking setup.
- `studio_user_profile_stack.py` – Defines user profiles tied to the domain.
- `pretrained_model_stack.py` – (Optional) Attempts to deploy a pre-trained model endpoint using JumpStart (experimental).
- `test.py` – Utility script to extract container image and model data URI for a selected JumpStart model.
  
## ⚙️ Prerequisites

- Python 3.8+
- AWS credentials with permissions for SageMaker, IAM, EC2, and CloudFormation
- CDK CLI (`npm install -g aws-cdk`)
- Bootstrap your environment:  
  ```bash
  cdk bootstrap

# Install dependencies
python -m venv .cdk-venv
source .cdk-venv/bin/activate
pip install -r requirements.txt

# Synthesize and deploy
cdk deploy

## 📌 Notes
- SageMaker domain and user profiles are required before deploying model stacks.

- Some JumpStart models may not expose full S3 model artifacts publicly; adapt as needed.

- Uses environment variables for pre-trained model configuration:

`export PRETRAINED_CONTAINER_URI=...`
`export PRETRAINED_MODEL_S3_URL=...`
