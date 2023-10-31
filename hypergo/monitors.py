from abc import abstractmethod
import os
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

    @abstractmethod
    def send(self, metric_name, metric_value):
        pass


class AzureLogAnalyticsMonitorStorage(Monitor):
    def __init__(self, metadata) -> None:
        super().__init__(metadata=metadata)
        # @TODO: move to secrets
        self.workspace_id = os.environ.get("LOG_ANALYTICS_WORKSPACE_ID", 'b304b831-4fad-458b-b710-87428f724e54') # Default to dev workspace
        
        self.shared_key = '/NVu1M3N0TYjwKhDs1Z4LR4sBcszCuyonxjtzUI37KsgCn03LRRa1WcsSK0pXY8RPnOH8Tmew5f6TszGIPnl9A=='

    def send(self, metric_name, metric_value):
        self._push_metric(metric_name=metric_name, metric_value=metric_value)


    # Build the API signature
    @staticmethod
    def _build_signature(workspace_id, shared_key, date, content_length, method, content_type):
        bytes_to_hash = bytes(f"{method}\n{content_length}\n{content_type}\nx-ms-date:{date}\n/api/logs", encoding="utf-8")

        decoded_key = base64.b64decode(shared_key)
        encoded_hash = base64.b64encode(
            hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
        ).decode()

        return f"SharedKey {workspace_id}:{encoded_hash}"

    # Build and send a request to the POST API
    def _post_data(self, body):
        # Define a custom log type for Azure Log Analytics workspace
        content_type = 'application/json'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature = self._build_signature(workspace_id=self.workspace_id, shared_key=self.shared_key, date=rfc1123date, content_length=len(body), method='POST', content_type=content_type)
        uri = 'https://' + self.workspace_id + '.ods.opinsights.azure.com/api/logs?api-version=2016-04-01'
        
        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': 'TestCustomLogType',
            'x-ms-date': rfc1123date
        }
        
        response = requests.post(uri, data=body, headers=headers)
        try:
            response.raise_for_status()
            print('log accepted')
        except:
            print(response.text)



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

        self._post_data(body.encode('utf-8'))


class DatalinkMonitor(Monitor):
    
    def __init__(self, metadata):
        super().__init__(metadata=metadata)
        self.monitors: List[Monitor] = [AzureLogAnalyticsMonitorStorage(metadata)]


    def send(self, metric_name, metric_value):
        for monitor in self.monitors:
            monitor.send(metric_name=metric_name, metric_value=metric_value)