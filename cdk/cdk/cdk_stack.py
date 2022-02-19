from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigatewayv2_alpha as apigatewayv2,
    Duration,
)
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function_asset = lambda_.Code.from_asset(path="../api/src")

        get_data_function = lambda_.Function(
            self,
            "GetDataFunction",
            code=function_asset,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.get_data",
            timeout=Duration.seconds(5),
        )

        create_data_function = lambda_.Function(
            self,
            "CreateDataFunction",
            code=function_asset,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.create_data",
            timeout=Duration.seconds(5),
        )

        api = apigatewayv2.HttpApi(self, "Api")
        api.add_routes(
            path="/data",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=HttpLambdaIntegration("GetDataIntegration", get_data_function)
        )
        api.add_routes(
            path="/data",
            methods=[apigatewayv2.HttpMethod.POST],
            integration=HttpLambdaIntegration("CreateDataIntegration", create_data_function)
        )
