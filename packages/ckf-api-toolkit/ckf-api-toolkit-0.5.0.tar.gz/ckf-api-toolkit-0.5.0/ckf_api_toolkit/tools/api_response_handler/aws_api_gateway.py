from json import dumps

from ckf_api_toolkit.tools.api_response_handler import ApiResponseFactory
from ckf_api_toolkit.tools.logger import LogLevel, Logger


class AwsApiGatewayResponseFactory(ApiResponseFactory):
    headers: dict

    def __init__(self, *, return_trace=False):
        super(AwsApiGatewayResponseFactory, self).__init__(return_trace=return_trace)
        self.headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Credentials": True,
        }

    def get_response(self) -> dict:
        # noinspection PyProtectedMember
        Logger().log(
            LogLevel.debug,
            {
                'statusCode': self.status_code,
                'body': self.body._asdict(),
                'headers': self.headers,
            },
            title="API Response",
            pretty_json=True
        )
        # noinspection PyProtectedMember
        return {
            'statusCode': self.status_code,
            'body': dumps(self.body._asdict()),
            'headers': self.headers
        }
