from typing import Union

from aws_cdk.aws_apigateway import IRestApi, CfnApiV2, CfnRestApi
from aws_cdk.aws_apigatewayv2 import CfnIntegration, CfnApi
from aws_cdk.aws_lambda import IFunction, CfnFunction
from aws_cdk.core import Stack


class LambdaIntegration(CfnIntegration):
    def __init__(
            self,
            scope: Stack,
            integration_name: str,
            api: Union[IRestApi, CfnApi, CfnApiV2, CfnRestApi],
            integration_method: str,
            lambda_function: [IFunction, CfnFunction],
            integration_type: str = 'AWS_PROXY',
            connection_type='INTERNET',
            **kwargs
    ) -> None:
        if isinstance(api, IRestApi):
            api_id = api.rest_api_id
        elif isinstance(api, CfnApi):
            api_id = api.ref
        elif isinstance(api, CfnApiV2):
            api_id = api.ref
        elif isinstance(api, CfnRestApi):
            api_id = api.ref
        else:
            raise TypeError('Unsupported api type.')

        if isinstance(lambda_function, IFunction):
            fun_arn = lambda_function.function_arn
        elif isinstance(lambda_function, CfnFunction):
            fun_arn = lambda_function.attr_arn
        else:
            raise TypeError('Unsupported lambda function type.')

        super().__init__(
            scope=scope,
            id=integration_name,
            api_id=api_id,
            connection_type=connection_type,
            integration_type=integration_type,
            integration_method=integration_method,
            integration_uri=f'arn:aws:apigateway:{scope.region}:lambda:path/2015-03-31/functions/{fun_arn}/invocations',
            **kwargs
        )
