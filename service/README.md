# is_flappy
Check a list of hosts to see if a service is listening on a given port.

[![Build Status](https://travis-ci.com/maxdotdotg/is_flappy.svg?branch=master)](https://travis-ci.com/maxdotdotg/is_flappy)

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

Alternately, build and run as a docker container using the included `Dockerfile`. Please note that the `Dockerfile` runs the app in DEBUG mode.
```
sudo docker build . -t is_flappy
sudo docker run --name is_flappy -p 9001:9001 -d is_flappy
```

## testing
This service can be tested using the built-in unittest module: `python -m unittest tests.py`
Currently, also working on `.travis.yml`
