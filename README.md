# is_flappy
This script will check a list of hosts to see if a service is listening in a given port

## usage
```
usage: is_flappy [-h] [-s SECONDS] port

positional arguments:
  port                  port to check

optional arguments:
  -h, --help            show this help message and exit
  -s SECONDS, --seconds SECONDS
                        number of seconds between checks (default is 5s)
```

For example:

```
./is_flappy $PORT < EOF
$HOST_1
$HOST_2
$HOST_3
EOF
```

## requirements
This script uses python3
