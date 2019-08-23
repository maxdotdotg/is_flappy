# is_flappy
This script will check a list of hosts to see if a service is listening on a given port.

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
# read a file as stdin
./is_flappy $PORT < list_of_hosts
```

## requirements
This script is compatible with python 2 and python 3.


## questions and considerations
* How would you deploy this as a script/service/etc?

    As a script, this can be deployed to a target node via configuration management/wget/curl/scp/etc. I'd use the house tools to deliver the artifact. If it was to be a service, I'd recommend writing a systemd unit file in addition, which would handle logging and lifecycle management. Alternatively, the script could be run via crontab as well.

    The biggest complexity that comes to mind is how the list of hosts to check would be provided and managed over time. If this were to run on a VM, the list of hosts could be maintained via Chef/Ansible/Puppet/similar. If it were deployed to a functions-as-a-service platform or as a container, I can see the list of hosts being stored offsite in an object storage platform (s3/blob store/etc) and provided at runtime, or via a volume mounted specifically to provide this file. A future version could also take a list of hostsvia an HTTP endpoint, run the checks, and return the results.

* How would you work with developers to resolve any systems issues?

    I'd review application/system logs and telemetry with the dev team, to see if we could identify events before, during, and after the host went down (what was the app doing? was there a disk/network/file issue on this host? was there a high frequency of $ERROR_TYPE? did other hosts experience similar issues/behaviors?) that contributed to the issue, and work to reproduce the issue in the local dev environment, if possible. Any OS-related changes would be documented and added to the configuration management tooling used by the service.

    Going forward, I'd work with the dev team to implement a health check endpoint that could be scraped for greater service details, and use a test request/query to evaluate if the application could correctly perform it's functionality, giving us more context and a better picture of the application's behavior, since a TCP check could succeed even when an application is functionally unusable.

* What, if any, would the impact be of your script on the production service

    I expect minimal impact on the running service, since the TCP connection is short lived and each socket is explicitly closed before opening a new connection. If many instances of this check are running against the same host in parallel, however, the applicaiton could slow down, hang, or even crash because it can't open more files. 
