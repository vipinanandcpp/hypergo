import base64
import datetime
import hashlib
import hmac
import json
import os
from abc import abstractmethod
from typing import List

import requests

from hypergo.secrets import Secrets


class Monitor:
    def __init__(self, secrets: Secrets, metadata) -> None:
        self._secrets = secrets
        self.metadata = metadata

    @abstractmethod
    def send(self, metric_name, metric_value):
        pass


class AzureLogAnalyticsMonitorStorage(Monitor):
    def __init__(self, secrets: Secrets, metadata) -> None:
        super().__init__(secrets=secrets, metadata=metadata)
        # @TODO: move to secrets
        print(f"secrets: {self._secrets}")

        self.workspace_id = self._secrets.get("log-analytics-workspace-id")
        self.shared_key = self._secrets.get("log-analytics-primary-key")

    def send(self, metric_name, metric_value):
        self._push_metric(metric_name=metric_name, metric_value=metric_value)

    @staticmethod
    def _build_signature(workspace_id, shared_key, date, content_length, method, content_type):
        bytes_to_hash = bytes(
            f"{method}\n{content_length}\n{content_type}\nx-ms-date:{date}\n/api/logs", encoding="utf-8")

        decoded_key = base64.b64decode(f"/{shared_key}")
        encoded_hash = base64.b64encode(
            hmac.new(decoded_key, bytes_to_hash,
                     digestmod=hashlib.sha256).digest()
        ).decode()

        return f"SharedKey {workspace_id}:{encoded_hash}"

    def _post_data(self, body):
        content_type = 'application/json'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature = self._build_signature(workspace_id=self.workspace_id, shared_key=self.shared_key,
                                          date=rfc1123date, content_length=len(body), method='POST', content_type=content_type)
        url = 'https://' + self.workspace_id + \
            '.ods.opinsights.azure.com/api/logs?api-version=2016-04-01'

        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': 'TestCustomLogType',
            'x-ms-date': rfc1123date
        }

        response = requests.post(url=url, data=body, headers=headers)
        try:
            response.raise_for_status()
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

    def __init__(self, secrets: Secrets, metadata):
        super().__init__(secrets=secrets, metadata=metadata)
        self.monitors: List[Monitor] = [
            AzureLogAnalyticsMonitorStorage(secrets, metadata)]

    def send(self, metric_name, metric_value):
        for monitor in self.monitors:
            monitor.send(metric_name=metric_name, metric_value=metric_value)
