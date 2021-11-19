import base64
import os
from datetime import timedelta


def parse_timeleft(delta_str):
    """Parse an Eiger timeLeft response.

    Assuming the format consists of whitespace-separated fields, each of which
    is terminated by a 1-character time identifier (e.g "13h 12m").

    Time identifers may be the following:
        s: Second
        m: Minute
        h: Hour
        d: Day
        w: Week

    Not all identifiers will be present.

    @param delta_str String representation of timedelta

    @returns timedelta python timedelta object
    """
    TIME_MAP = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
    }
    fields = delta_str.split()

    seconds = sum([int(field[0:-1]) * TIME_MAP[field[-1]] for field in fields])

    return timedelta(seconds=seconds)


def get_auth(filepath):
    """Return Base64-encoded API key from a file

    Expects `ACCESS_KEY` and `SECRET_KEY` to be first & second line of file.
    Used with HTTP bindings and 'basic' authentication.

    @returns Base64-encoded API key
    """
    with open(filepath, "r") as keyfile:
        ACCESS_KEY = keyfile.readline().strip()
        SECRET_KEY = keyfile.readline().strip()

    key = base64.encodestring("{}:{}".format(ACCESS_KEY, SECRET_KEY).encode())
    key = "".join(key.split())

    return key.decode()


def get_auth_raw(filepath):
    """Return tuple containing API username/password.

    Expects `ACCESS_KEY` and `SECRET_KEY` to be first & second line of file.
    Used with system.net.httpGet

    @returns tuple of ACCESS_KEY, SECRET_KEY
    """
    with open(filepath, "r") as keyfile:
        ACCESS_KEY = keyfile.readline().strip()
        SECRET_KEY = keyfile.readline().strip()

    return (ACCESS_KEY, SECRET_KEY)
