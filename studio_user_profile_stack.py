from aws_cdk import Stack
from aws_cdk import aws_sagemaker as sagemaker
from constructs import Construct
from typing import List

class StudioUserProfileStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        domain_id: str,
        execution_role_arn: str,
        usernames: List[str],
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        for username in usernames:
            sagemaker.CfnUserProfile(
                self,
                f"StudioUserProfile-{username}",
                domain_id=domain_id,
                user_profile_name=username,
                user_settings=sagemaker.CfnUserProfile.UserSettingsProperty(
                    execution_role=execution_role_arn
                )
            )
