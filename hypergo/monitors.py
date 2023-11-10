import base64
import datetime
import hashlib
import hmac
import json
from abc import abstractmethod
from typing import Any, List, Union

import requests

from hypergo.logger import logger
from hypergo.secrets import Secrets


class Monitor:
    def __init__(self, secrets: Secrets, metadata: Any) -> None:
        self._secrets = secrets
        self.metadata = metadata

    @abstractmethod
    def send(self, metric_name: str, metric_value: Any) -> None:
        pass


class AzureLogAnalyticsMonitorStorage(Monitor):
    def __init__(self, secrets: Secrets, metadata: Any) -> None:
        super().__init__(secrets=secrets, metadata=metadata)
        self.workspace_id = self._secrets.get(key="LOG_ANALYTICS_WORKSPACE_ID")
        self.shared_key = self._secrets.get(key="LOG_ANALYTICS_PRIMARY_KEY")

    def send(self, metric_name: str, metric_value: Any) -> None:
        if hasattr(self, "workspace_id"):
            self._push_metric(metric_name=metric_name, metric_value=metric_value)

    @staticmethod
    def _build_signature(**kwargs: Any) -> str:
        workspace_id = kwargs["workspace_id"]
        shared_key = kwargs["shared_key"]
        date = kwargs["date"]
        content_length = kwargs["content_length"]
        method = kwargs["method"]
        content_type = kwargs["content_type"]
        bytes_to_hash = bytes(
            f"{method}\n{content_length}\n{content_type}\nx-ms-date:{date}\n/api/logs",
            encoding="utf-8",
        )

        decoded_key = base64.b64decode(f"/{shared_key}")
        encoded_hash = base64.b64encode(
            hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
        ).decode()

        return f"SharedKey {workspace_id}:{encoded_hash}"

    def _post_data(self, body: Union[bytes, str]) -> None:
        content_type = "application/json"
        rfc1123date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        kwargs = {
            "workspace_id": self.workspace_id,
            "shared_key": self.shared_key,
            "date": rfc1123date,
            "content_length": len(body),
            "method": "POST",
            "content_type": content_type,
        }
        signature = self._build_signature(**kwargs)
        url = f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"

        headers = {
            "content-type": content_type,
            "Authorization": signature,
            "Log-Type": "TestCustomLogType",
            "x-ms-date": rfc1123date,
        }

        response = requests.post(url=url, data=body, headers=headers, timeout=300)
        response.raise_for_status()
        try:
            logger.info(response.json())
        except json.decoder.JSONDecodeError:
            logger.error(response.text)

    def _push_metric(self, metric_name: str, metric_value: Any) -> None:
        body = json.dumps(
            [
                {
                    "metadata": self.metadata,
                    "datetime": datetime.datetime.now().isoformat(),
                    "metric_name": metric_name,
                    "metric_value": metric_value,
                }
            ]
        )

        self._post_data(body.encode("utf-8"))


class DatalinkMonitor(Monitor):
    def __init__(self, secrets: Secrets, metadata: Any):
        super().__init__(secrets=secrets, metadata=metadata)
        self.monitors: List[Monitor] = [AzureLogAnalyticsMonitorStorage(secrets, metadata)]

    def send(self, metric_name: str, metric_value: Any) -> None:
        for monitor in self.monitors:
            monitor.send(metric_name=metric_name, metric_value=metric_value)
