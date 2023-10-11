from typing import List
import requests
import json
import datetime
import hashlib
import hmac
import base64

class Monitor:

    def __init__(self, metadata) -> None:
        self.metadata = metadata

    def send(self, metric_name, metric_value):
        raise NotImplementedError()


class AzureLogAnalyticsMonitorStorage(Monitor):
    def __init__(self, metadata) -> None:
        super().__init__(metadata=metadata)
        # @TODO: move to env 
        self.workspace_id = 'b304b831-4fad-458b-b710-87428f724e54'
        self.shared_key = '/NVu1M3N0TYjwKhDs1Z4LR4sBcszCuyonxjtzUI37KsgCn03LRRa1WcsSK0pXY8RPnOH8Tmew5f6TszGIPnl9A=='

        self.custom_log_type = 'CustomLogType' # @TODO: add comments


    def send(self, metric_name, metric_value):
        self._push_metric(metric_name=metric_name, metric_value=metric_value)


    # Build the API signature
    @staticmethod
    def _build_signature(workspace_id, shared_key, date, content_length, method, content_type, resource):
        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
        decoded_key = base64.b64decode(shared_key)
        encoded_hash = base64.b64encode(
            hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
        ).decode()
        authorization = "SharedKey {}:{}".format(workspace_id, encoded_hash)
        return authorization


    # Build and send a request to the POST API
    def _post_data(self, body):
        # Define a custom log type for Azure Log Analytics workspace
        log_type = 'TestCustomLogType'

        method = 'POST'
        content_type = 'application/json'
        resource = '/api/logs'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(body)
        signature = self._build_signature(workspace_id=self.workspace_id, shared_key=self.shared_key, date=rfc1123date, content_length=content_length, method=method, content_type=content_type, resource=resource)
        uri = 'https://' + self.workspace_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'
        
        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': log_type,
            'x-ms-date': rfc1123date
        }
        
        response = requests.post(uri, data=body, headers=headers)
        if response.status_code >= 200 and response.status_code <= 299:
            print('Accepted')
        # add further Azure Log Analytics API response codes here
        else:
            print("Response code: {}".format(response.status_code))



    def _push_metric(self, metric_name, metric_value):

        body = json.dumps(
            [
                {
                    "metadata": self.metadata,
                    "datetime": datetime.datetime.now().isoformat(),
                    "metric_name": metric_name,
                    "metric_value": metric_value
                }
            ]
        )

        body = body.encode('utf-8')

        self._post_data(body)


class DatalinkMonitor(Monitor):
    
    def __init__(self, metadata):
        super().__init__(metadata=metadata)
        self.monitors: List[Monitor] = [AzureLogAnalyticsMonitorStorage(metadata)]


    def send(self, metric_name, metric_value):
        for monitor in self.monitors:
            monitor.send(metric_name=metric_name, metric_value=metric_value)