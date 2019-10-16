#!/usr/bin/env python

"""
check if a TCP connection to $PORT on $HOST can be established
if 5 checks fail, report that $HOST is down
"""

from flask import Flask, request, jsonify
import gunicorn
import logging
import socket
from time import sleep

# flask app
app = Flask(__name__)

# logging for gunicorn
# https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers


def tcp_check(host, port, seconds):
    # run tcp check on $HOST
    # return success count as int
    count = 0
    for i in range(5):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            app.logger.debug("starting socket connection to {}".format(host))
            result = s.connect_ex((host, port))
            app.logger.debug("closing socket connection to {}".format(host))
            s.close()
            if result == 0:
                app.logger.debug(
                    "result of socket connection to {} is 0, incrementing success count".format(
                        host
                    )
                )
                app.logger.info("connection to {} succeeded".format(host))
                count += 1
        except socket.gaierror:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            app.logger.debug("starting socket_ex connection to {}".format(host))
            result = s.connect_ex((host.strip(), port))
            app.logger.debug("closing socket_ex connection to {}".format(host))
            s.close()
            if result == 0:
                app.logger.debug(
                    "result of socket_ex connection to {} is 0, incrementing success count".format(
                        host
                    )
                )
                app.logger.info("connection to {} succeeded".format(host))
                count += 1
        sleep(seconds)
    app.logger.debug("success count for connecting to {} is {}".format(host, count))
    return count


@app.route("/check/<host>", methods=["GET"])
def check(host, port=80, seconds=2):
    # execute tcp checks on $HOST and report
    # returns json
    status = None
    successful_check = tcp_check(host, port, seconds)
    if successful_check == 5:
        status = "OK"
        app.logger.debug(
            "success count for {} equals {}, status is {}".format(
                host, successful_check, status
            )
        )
        app.logger.info("host {} is {}".format(host, status))
    elif successful_check == 0:
        status = "DOWN"
        app.logger.debug(
            "success count for {} equals {}, status is {}".format(
                host, successful_check, status
            )
        )
        app.logger.info("host {} is {}".format(host, status))
    else:
        status = "FLAPPY"
        app.logger.debug(
            "success count for {} equals {}, status is {}".format(
                host, successful_check, status
            )
        )
        app.logger.info("host {} is {}".format(host, status))

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
        app.logger.debug("received body that wasn't JSON: {}".format(request))
        abort(404)

    results = [check(hosts, request.json["port"]) for hosts in request.json["hosts"]]
    app.logger.debug("results: {}".format(results))
    return jsonify({"results": results})


# bind to 9001
if __name__ == "__main__":
    app.run(host="localhost", port=9001)

# use gunicorn logger when app is not run directly
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
