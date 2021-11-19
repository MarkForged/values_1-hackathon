import base64
import os


def get_auth(filepath="/var/lib/ignition/eiger_api_v3.key"):
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


def get_auth_raw(filepath="/var/lib/ignition/eiger_api_v3.key"):
    """Return tuple containing API username/password.

    Expects `ACCESS_KEY` and `SECRET_KEY` to be first & second line of file.
    Used with system.net.httpGet

    @returns tuple of ACCESS_KEY, SECRET_KEY
    """
    with open(filepath, "r") as keyfile:
        ACCESS_KEY = keyfile.readline().strip()
        SECRET_KEY = keyfile.readline().strip()

    return (ACCESS_KEY, SECRET_KEY)
