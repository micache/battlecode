"""Offline operator-client tests; no Blaxel credentials or paid resources used."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("blaxel_operator", Path(__file__).parents[1] / "ops/blaxel.py")
operator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operator)


class BlaxelTests(unittest.TestCase):
    def test_administrator_key_never_sent_to_untrusted_endpoint(self):
        client = operator.Client("TEST-NOT-A-REAL-KEY", "test")
        for endpoint in ("http://api.blaxel.ai/v0", "https://evil.example", "https://api.blaxel.ai.evil.example"):
            with self.assertRaisesRegex(RuntimeError, "untrusted"):
                client.request("GET", "/health", base=endpoint)

    def test_redirects_never_forward_authorization(self):
        with self.assertRaisesRegex(RuntimeError, "refusing to forward"):
            operator.NoRedirect().redirect_request(None, None, 302, "Found", {}, "https://evil.example")

    def test_quota_failure_is_not_retried(self):
        client = operator.Client("TEST-NOT-A-REAL-KEY", "test")
        calls = []

        def request(method, path, body=None):
            calls.append((method, path))
            raise operator.APIError(404 if method == "GET" else 403, "fixture quota denial")

        with patch.object(client, "request", side_effect=request):
            with self.assertRaises(operator.APIError) as caught:
                client.ensure("volumes", operator.VOLUME, {"region": operator.REGION, "size": 102400})
        self.assertEqual(caught.exception.code, 403)
        self.assertEqual(calls, [("GET", "/volumes/battlecode-arena-data"), ("POST", "/volumes")])

    def test_existing_foreign_resource_is_not_adopted(self):
        client = operator.Client("TEST-NOT-A-REAL-KEY", "test")
        with patch.object(client, "get", return_value={"metadata": {"name": operator.VOLUME}, "spec": {}}):
            with self.assertRaisesRegex(RuntimeError, "unregistered"):
                client.ensure("volumes", operator.VOLUME, {})

    def test_status_omits_runtime_environment(self):
        report = operator.summary({"metadata": {"name": operator.NAME}, "spec": {
            "runtime": {"memory": 8192, "envs": [{"name": "EXAMPLE_SECRET", "value": "not-shared"}]}}})
        self.assertNotIn("not-shared", str(report))
        self.assertEqual(report["runtime"]["memory"], 8192)


if __name__ == "__main__":
    unittest.main()
