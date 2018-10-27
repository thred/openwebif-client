import commands
import json
import utils


def consume():
    response = utils.requestJson("about")

    print(json.dumps(response, indent=4))

def help():
    print("""\
Usage: owifc about

Calls the about service and prints the result.""")


commands.register("about", "Calls the about service.",
                  lambda: consume(), lambda: help())
