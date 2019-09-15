import requests
import unittest
import is_flappy


class Test_service(unittest.TestCase):
    def setUp(self):
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(("", 9001))

    def tearDown(self):
        client_socket.close()

    def test1():
        # service running on localhost should return 200
        r = requests.get("localhost:9001/check/localhost")
        self.assertEqual(r.status, 200)

    def test2():
        # return type should always be json
        r = requests.get("localhost:9001/check/localhost")
        self.assertEqual(type(r.json), "dict")

    def test3():
        # service should be running
        headers = {"Content-Type": "application/json"}
        payload = {"port": 9001, "hosts": ["localhost"]}
        r = requests.post(
            "localhost:9001/check/localhost", data=payload, headers=headers
        )
        response = r.json()
        self.assertEqual(response["results"][0]["status"], "OK")
