import sys
import commands
import ConfigParser
from notified import Notified
from os.path import expanduser

HOME = expanduser("~")
FILENAME = HOME + "/.owifc.conf"
CONFIG = ConfigParser.RawConfigParser()

CONFIG.read(FILENAME)

if not CONFIG.has_section("main"):
    CONFIG.add_section("main")

_args = map(lambda arg: unicode(arg, sys.getfilesystemencoding()), sys.argv[:])


def popArg(index, fallback=None):
    try:
        return _args.pop(index)
    except IndexError:
        return fallback


def popArgs(index):
    args = []
    arg = popArg(index)

    while arg != None:
        args.append(arg)
        arg = popArg(index)

    return args


def popFlag(key, fallback=False):
    try:
        index = _args.index(key)
        _args.pop(index)
        return True
    except ValueError:
        return fallback


def popValue(key, fallback=None):
    try:
        index = _args.index(key)
        _args.pop(index)
        return popArg(index, fallback)
    except ValueError:
        return fallback


def storeConfigFile():
    if debug:
        print("Writing config to: " + FILENAME)

    file = open(FILENAME, "w")

    try:
        CONFIG.write(file)
    finally:
        file.close()


def getConfiguredString(key, fallback=None):
    try:
        return CONFIG.get("main", key)
    except ConfigParser.NoOptionError:
        return fallback


def getConfiguredBoolean(key):
    try:
        return CONFIG.getboolean("main", key)
    except ConfigParser.NoOptionError:
        return False


def setConfiguredValue(key, value=None):
    if debug:
        print("Setting: " + key + " = " + value)

    CONFIG.set("main", key, value)
    storeConfigFile()


def removeConfiguredValue(key):
    if debug:
        print("Removing: " + key)

    CONFIG.remove_option("main", key)
    storeConfigFile()


def _get(key, abbreviation=None, fallback=None):
    if abbreviation:
        return popValue("-" + abbreviation, popValue("--" + key, getConfiguredString(key, fallback)))
    else:
        return popValue("--" + key, getConfiguredString(key, fallback))


def _getFlag(key, abbreviation=None, value=True):
    if abbreviation:
        return popFlag("-" + abbreviation, popFlag("--" + key, getConfiguredBoolean(key)))
    else:
        return popFlag("--" + key, getConfiguredBoolean(key))


file = _get("file", "f")

if file:
    with open(file) as f:
        content = f.readlines()
        content = [unicode(line, "UTF-8") for line in content]
        content = [line.strip() for line in content]
        content = filter(lambda line: len(line) > 0 and not line.startswith(
            "#"), content)
        _args += content


bouquet = _get("bouquet", "b")
command = popArg(1, "help").lower()
debug = _getFlag("debug", "X")
emailTo = _get("email-to")
host = _get("host", "h")
skipNotified = _getFlag("skip-notified")
smtp = _get("smtp")
smtps = _get("smtps")
pretty = _getFlag("pretty", "p")


def createNotified():
    filename = FILENAME

    if filename.endswith(".conf"):
        filename = filename[:-5]

    filename += ".notified"

    result = Notified(filename)
    result.load()

    return result


def url(command=None):
    if not host:
        raise ValueError("The --host is missing.")

    url = host

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    if not url.endswith("/"):
        url += "/"

    if not url.endswith("api/"):
        url += "api/"

    if command:
        url += command

    return url


def consume():
    key = popArg(1)

    if key == "list":
        for item in CONFIG.items("main"):
            print(item[0] + " = " + item[1])

    elif key == "set":
        key = popArg(1)
        if not key:
            raise ValueError("The KEY is missing.")

        value = popArg(1)
        if not value:
            raise ValueError("The VALUE is missing.")

        setConfiguredValue(key, value)

    elif key == "remove":
        key = popArg(1)
        if not key:
            raise ValueError("The KEY is missing.")

        removeConfiguredValue(key)

    else:
        raise ValueError("The ACTION ist missing.")


def help():
    print("""\
Usage: owifc config ACTION

Known ACTIONs are:

list ................ List all key/value pairs in the config file.
set KEY VALUE ....... Write a key/value pair to the config file.
remove KEY .......... Removes the value from the config file.
""")


commands.register("config", "Reads and writes the configuration.",
                  lambda: consume(), lambda: help())
