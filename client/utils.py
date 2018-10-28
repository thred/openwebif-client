import config
import datetime
import requests
import re
import sys
import textwrap


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


def fix(text):
    """Some text comes with akward formatting, like // being a line break.
    This method tries to fix all the problems."""

    if text:
        text = unicode(text)
        text = text.replace("&quot;", "\"")
        text = text.replace("&amp;", "&")
        text = text.replace("\\n", "\n")
        text = re.sub("\\s*//\\s*", "\n\n", text)
        text = text.strip()

    return text


def wrap(text, length):
    """The word wrap does not handle line breaks in any form.
    This method tries to work around this limitation."""

    if text:
        lines = re.split("\n", text)
        text = u"\n".join([textwrap.fill(line, length) for line in lines])

    return text


def html(text):
    """Converts the text to HTML."""

    if text:
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace("\"", "&quot;")
        text = text.replace("\n", "<br/>")

    return text

