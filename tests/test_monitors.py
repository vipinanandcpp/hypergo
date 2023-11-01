import json
import os
import unittest
import datetime

import mock
from freezegun import freeze_time

from hypergo.monitors import AzureLogAnalyticsMonitorStorage




class TestAzureLogAnalyticsMonitorStorage(unittest.TestCase):
    @freeze_time("2023-11-01")
    @mock.patch("hypergo.monitors.requests.post")
    @mock.patch.dict(os.environ, {"LOG_ANALYTICS_WORKSPACE_ID": "shmorkspace_id"})
    @mock.patch.dict(os.environ, {"LOG_ANALYTICS_PRIMARY_KEY": "shmimary_key"})
    def test_send(
        self, mock_post
    ) -> None:
        test_metadata = {"some": "metadata"}
        test_metric = "test_metric"
        test_value = 10

        monitor = AzureLogAnalyticsMonitorStorage({"some": "metadata"})

        expected_body = json.dumps(
            [
                {
                    "metadata": test_metadata,
                    "datetime": datetime.datetime.now().isoformat(),
                    "metric_name": test_metric,
                    "metric_value": test_value
                }
            ]
        ).encode('utf-8')
        expected_headers = {
            'content-type': 'application/json',
            'Authorization': 'SharedKey shmorkspace_id:abBpQaHOfXXH1Dr/A6EJhEj7284c0VXHU+7WCWI2op4=',
            'Log-Type': 'TestCustomLogType',
            'x-ms-date': 'Wed, 01 Nov 2023 00:00:00 GMT'
        }

        monitor.send(test_metric, test_value)

        mock_post.assert_called_with(
            url="https://shmorkspace_id.ods.opinsights.azure.com/api/logs?api-version=2016-04-01",
            data=expected_body,
            headers=expected_headers
        )        
        self.assertEquals(datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'), "Wed, 01 Nov 2023 00:00:00 GMT")

if __name__ == "__main__":
    unittest.main()
