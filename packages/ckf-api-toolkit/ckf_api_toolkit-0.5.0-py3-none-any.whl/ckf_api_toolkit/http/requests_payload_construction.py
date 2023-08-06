from typing import Any, Dict


# Very basic payload generation for requests
# TODO: Implement full requests feature set
class RequestsPayload:
    params: dict
    url: str
    headers: dict
    data: dict

    def __init__(self, url: str):
        self.url = url
        self.headers = {}
        self.data = {}
        self.params = {}

    def add_header(self, header_name: str, header_value: Any):
        self.headers[header_name] = header_value

    def add_data_key(self, data_key: str, data_value: Any):
        self.data[data_key] = data_value

    def set_data(self, data: Dict[str, Any]):
        self.data = {**data}

    def add_param(self, param_key: str, param_value: Any):
        self.params[param_key] = param_value

    def set_params(self, params: Dict[str, Any]):
        self.params = {**params}
