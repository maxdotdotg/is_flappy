# is_flappy
This script will check a list of hosts to see if a service is listening on a given port

## usage
```
usage: is_flappy [-h] [-s SECONDS] port [hosts]

check if a TCP connection to $PORT on $HOST can be established

positional arguments:
  port                  port to check
  hosts                 new-line delimited list of hosts read from stdin

optional arguments:
  -h, --help            show this help message and exit
  -s SECONDS, --seconds SECONDS
                        number of seconds between checks (default is 5s)

```

For example:

```
# read list from heredoc
./is_flappy $PORT <<EOF
$HOST_1
$HOST_2
$HOST_3
EOF
```

```
# read file as stdin
./is_flappy $PORT < list_of_hosts
```

## requirements
This script uses python3
