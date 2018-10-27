import commands
import utils


def getBRef(name):
    json = utils.requestJson("bouquets")

    for bouquet in json["bouquets"]:
        if bouquet[1] == name:
            return bouquet[0]
    else:
        raise ValueError("Bouquet not found: " + name)


def getDefaultBRef():
    json = utils.requestJson("bouquets")

    return json["bouquets"][0][0]


def consume():
    json = utils.requestJson("bouquets")

    for bouquet in json["bouquets"]:
        print(bouquet[1])


def help():
    print("""\
Usage: owifc bouquets

Lists all known bouquets.""")


commands.register("bouquets", "Lists all known bouquets.",
                  lambda: consume(), lambda: help())
