from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import aws_sagemaker as sagemaker



class PreTrainedModelStack(Stack):
    def __init__(self, scope: Construct, id: str, *, execution_role_arn: str, model_container_image: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        model_name = "pretrained-text-classification-model"
        endpoint_config_name = "pretrained-endpoint-config"
        endpoint_name = "pretrained-endpoint"

        #  Deploy the Model
        model = sagemaker.CfnModel(
            self,
            "PretrainedJumpStartModel",
            execution_role_arn=execution_role_arn,
            primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                image=model_container_image,
                environment={
                    "SAGEMAKER_PROGRAM": "inference.py",
                    "SAGEMAKER_SUBMIT_DIRECTORY": "/opt/ml/model",
                    "SAGEMAKER_CONTAINER_LOG_LEVEL": "20",
                    "SAGEMAKER_REGION": self.region,
                }
            ),
            enable_network_isolation=False,
            model_name=model_name,
        )

        #  Create the Endpoint Config
        endpoint_config = sagemaker.CfnEndpointConfig(
            self,
            "PretrainedEndpointConfig",
            production_variants=[
                sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                    initial_variant_weight=1.0,
                    instance_type="ml.m5.large",  # cheaper instance for now
                    model_name=model.model_name,
                    variant_name="AllTraffic"
                )
            ],
            endpoint_config_name=endpoint_config_name
        )

        #  Create the Endpoint
        endpoint = sagemaker.CfnEndpoint(
            self,
            "PretrainedEndpoint",
            endpoint_name=endpoint_name,
            endpoint_config_name=endpoint_config.endpoint_config_name
        )

        #  Outputs
        CfnOutput(
            self,
            "PretrainedModelName",
            value=model.model_name,
            description="Name of the JumpStart model"
        )

        CfnOutput(
            self,
            "PretrainedEndpointName",
            value=endpoint.endpoint_name,
            description="Name of the deployed SageMaker endpoint"
        )

