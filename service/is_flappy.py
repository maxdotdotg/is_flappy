#!/usr/bin/env python

"""
check if a TCP connection to $PORT on $HOST can be established
if 5 checks fail, report that $HOST is down
"""

from flask import Flask, request, jsonify
import socket
from time import sleep


app = Flask(__name__)


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


@app.route("/check/<host>", methods=["GET"])
def check(host, port=80, seconds=2):
    # execute tcp checks on $HOST and report
    # returns json
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
def check_list():
    # check list of hosts provided via posts
    # returns json
    if not request.json:
        abort(404)

    results = [check(hosts, request.json["port"]) for hosts in request.json["hosts"]]
    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)
