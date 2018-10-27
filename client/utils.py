import config
import datetime
import requests
import sys


def requestJson(command, params={}):
    url = config.url(command)

    if config.debug:
        print("Invoking: " + url)

    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        print("Request failed:")
        print(e)
        sys.exit(1)

    try:
        return response.json()
    except ValueError:
        print("Invalid response:")
        print(response.text)
        sys.exit(1)


def format(object, keys=None, delimiter=";"):
    if not keys:
        keys = object.keys()

    result = ""

    for key in keys:
        kind = "string"

        if ":" in key:
            kind = key[key.index(":")+1:]
            key = key[:key.index(":")]

        value = object.get(key)

        if kind == "timestamp":
            value = datetime.datetime.fromtimestamp(
                value).strftime("%Y-%m-%d %H:%M")
        else:
            value = unicode(object.get(key))

        value = value.replace("\"", "\"\"")

        if delimiter in value:
            value = "\"" + value + "\""

        if len(result) > 0:
            result += delimiter

        result += value

    return result
