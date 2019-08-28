#!/usr/bin/env python

"""
check if a TCP connection to $PORT on $HOST can be established
if 5 checks fail, report that $HOST is down
"""

from flask import Flask, request, jsonify
import socket
import sys
from time import sleep


app = Flask(__name__)
host = "localhost"
port = 9000
seconds = 5


def tcp_check(host, port, seconds):
    # run tcp check on $HOST
    count = 0
    for i in range(5):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((host, port))
            s.close()
            if result == 0:
                count += 1
        except socket.gaierror:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((host.strip(), port))
            s.close()
            if result == 0:
                count += 1
        sleep(seconds)
    return count


@app.route("/check/<host>")
def check(host):
    # execute 5 tcp checks and report
    status = None
    successful_check = tcp_check(host, port, seconds)
    if successful_check == 5:
        status = "OK"
    elif successful_check == 0:
        status = "DOWN"
    else:
        status = "FLAPPY"

    return {
        "host": host.strip(),
        "port": port,
        "status": status,
        "message": "service using port {} on host {} is reporting {}".format(
            port, host.strip(), status
        ),
    }

@app.route("/json", methods=["POST"])
def print_list():
    return request