# is_flappy
Check a list of hosts to see if a service is listening on a given port.

## Installation
Install dependencies using pip: `pip install -r requirements.txt`

## Usage
This app exposes two endponts, `/check` and `/json`.

Start the app: `gunicorn -b 127.0.0.1:9001 is_flappy:app -w 4`

### `/check`
Accept one host via GET, and checks on port 80: `/check/$HOST`
```
curl localhost:9001/check/www.google.com
```

### `/json`
Accept a list of hosts to check in json format via POST
```
$ cat port443-test.json
{ "port": 443,
  "hosts":
  [
    "www.amazon.com",
    "www.google.com",
    "localhost"
  ]
}

$ curl -s -X POST localhost:9001/json -H "Content-Type: application/json" -d @port443-test.json | jq
{
  "results": [
    {
      "host": "www.amazon.com",
      "message": "service using port 443 on host www.amazon.com is reporting OK",
      "port": 443,
      "status": "OK"
    },
    {
      "host": "www.google.com",
      "message": "service using port 443 on host www.google.com is reporting OK",
      "port": 443,
      "status": "OK"
    },
    {
      "host": "localhost",
      "message": "service using port 443 on host localhost is reporting DOWN",
      "port": 443,
      "status": "DOWN"
    }
  ]
}

```

Alternately, build and run as a docker container using the included `Dockerfile`. When running the image, the log level defaults to DEBUG unless the environment variable `LOG_LEVEL` is set.
```
sudo docker build . -t is_flappy
sudo docker run --name is_flappy -e LOG_LEVEL=INFO -p 9001:9001 -d is_flappy
```

## Testing
This service can be manually tested using the built-in unittest module: `python -m unittest tests.py`.
