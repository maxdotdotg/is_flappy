import unittest
from json import dumps

import is_flappy


class Test_service(unittest.TestCase):

    def test_service_is_running(self):
        # service running on localhost should return 200
        test_client = is_flappy.app.test_client()

        r = test_client.get("/check/localhost")
        self.assertEqual(r.status_code, 200)

    def test_service_returns_json(self):
        # return type should always be json
        test_client = is_flappy.app.test_client()
        
        r = test_client.get("/check/localhost")
        self.assertEqual(r.is_json, True)

    def test_check_not_running_service(self):
        # check a service that is not running
        test_client = is_flappy.app.test_client()
        payload = {"port": 9001, "hosts": ["localhost"]}

        r = test_client.post(
            "/json", 
            data=dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(r.json["results"][0]["status"], "DOWN")

    def test_check_running_service(self):
        # test a service that IS running
        test_client = is_flappy.app.test_client()
        payload = {"port": 80, "hosts": ["www.google.com"]}

        r = test_client.post(
            "/json", 
            data=dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(r.json["results"][0]["status"], "OK")

