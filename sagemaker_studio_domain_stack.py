from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_sagemaker as sagemaker
from aws_cdk import CfnOutput
from aws_cdk import Tags
from constructs import Construct

class SageMakerStudioDomainStack(Stack):
    def __init__(self, scope: Construct, id: str, *, execution_role_arn: str, domain_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        Tags.of(self).add("created-by", "velga")

        # VPC
        vpc = ec2.Vpc(self, "StudioVPC", max_azs=2)

        # Security Group
        security_group = ec2.SecurityGroup(
            self,
            "StudioSecurityGroup",
            vpc=vpc,
            description="Allow traffic for SageMaker Studio Domain",
            allow_all_outbound=True
        )

        # SageMaker Studio Domain
        domain = sagemaker.CfnDomain(
            self,
            "SageMakerStudioDomain",
            auth_mode="IAM",
            default_user_settings=sagemaker.CfnDomain.UserSettingsProperty(
                execution_role=execution_role_arn
            ),
            domain_name=domain_name,
            vpc_id=vpc.vpc_id,
            subnet_ids=[subnet.subnet_id for subnet in vpc.private_subnets],
            app_network_access_type="VpcOnly"
        )


        # Save domain ID as property (can be used later for users)
        self.domain_id = domain.attr_domain_id

        CfnOutput(
            self,
            "SageMakerDomainId",
            value=domain.attr_domain_id,
            description="The ID of the SageMaker Studio Domain"
        )

        CfnOutput(
            self,
            "SageMakerDomainName",
            value=domain.domain_name,
            description="The name of the SageMaker Studio Domain"
        )

        CfnOutput(
            self,
            "VPCId",
            value=vpc.vpc_id,
            description="The ID of the VPC created for SageMaker Studio"
        )

        CfnOutput(
            self,
            "SecurityGroupId",
            value=security_group.security_group_id,
            description="Security Group for SageMaker Studio"
        )

        CfnOutput(
            self, "UnifiedStudioLandingURL",
            value=f"https://console.aws.amazon.com/sagemaker/home?region={self.region}#/studio-landing",
            description="Open the new Unified Studio AI home page"
        )
