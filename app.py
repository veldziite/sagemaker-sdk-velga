#!/usr/bin/env python3

from aws_cdk import App, Environment
from sagemaker_studio_domain_stack import SageMakerStudioDomainStack
from studio_user_profile_stack import StudioUserProfileStack
from pretrained_model_stack import PreTrainedModelStack
import os
import boto3

# Fetch account and region dynamically
sts_client = boto3.client('sts')
account_id = os.environ.get(
    'CDK_DEFAULT_ACCOUNT',
    sts_client.get_caller_identity()["Account"]
)
region = os.environ.get('CDK_DEFAULT_REGION', 'eu-central-1')

# Fetch execution role dynamically
iam_client = boto3.client('iam')
role_name = "service-role/AmazonSageMaker-ExecutionRole-20250219T114668"
role = iam_client.get_role(RoleName=role_name.split('/')[-1])
execution_role_arn = role["Role"]["Arn"]

# Dynamic domain name
domain_name = os.environ.get('SAGEMAKER_DOMAIN_NAME', 'sagemaker-studio-domain')

app = App()

# 1) Create the Studio Domain stack and keep a reference
domain_stack = SageMakerStudioDomainStack(
    app,
    "SageMakerStudioDomainStack",
    env=Environment(account=account_id, region=region),
    execution_role_arn=execution_role_arn,
    domain_name=domain_name
)

# 2) Create the User Profile stack, passing in the domain_id
StudioUserProfileStack(
    app,
    "StudioUserProfileStack",
    env=Environment(account=account_id, region=region),
    domain_id=domain_stack.domain_id,
    execution_role_arn=execution_role_arn,
    usernames=["admin", "developer", "analyst"]
)

#Pre-trained Model stack
PreTrainedModelStack(
    app, "PreTrainedModelStack",
    env=Environment(account=account_id, region=region),
    execution_role_arn=execution_role_arn,
    model_container_image=os.environ["PRETRAINED_CONTAINER_URI"],

)

app.synth()

