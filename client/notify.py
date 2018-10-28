import bouquets
import commands
import config
import datetime
import re
import json
import smtp
import term
import textwrap
import timetable
import utils


def consume():
    bouquet = config.bouquet
    bRef = bouquets.getBRef(bouquet) if bouquet else bouquets.getDefaultBRef()

    if config.debug:
        print("Using bRef: " + bRef)

    terms = [term.parse(arg) for arg in config.popArgs(1)]

    if config.debug:
        for item in terms:
            print("Filtering: " + unicode(item))

    response = utils.requestJson("epgmulti", params={"bRef": bRef})

    timeTable = timetable.of(response["events"], terms)

    if config.emailTo:
        if config.debug:
            print("Sending result to: " + config.emailTo)

        smtp.send(config.emailTo, "OpenWebIF Client", timeTable.toHumanReadable(), timeTable.toHtml())
    else:
        print(timeTable.toHumanReadable())


def help():
    print("""\
Usage: owifc notify [OPTION ...] [TERM ...]

Calls the program guide and print's matching programs.

The TERM is a regular expression. It may contain the keywords AND, NOT and IN.
If at least one TERM is given, it will print only lines, that contain the pattern.
Don't forget to put your search term in quotes!

Examples:

"foo AND bar" - Must contain "foo" and "bar" in any field.
"foo IN title" - Must contain "foo" in the field "title". Other fields are 
               "description" and "channel".
"foo AND NOT bar IN channel" - The channel must not contain "bar".

Currently it matches whole words only. The case is ignored.

Respects follwing options: bouquet, debug, email, host, html.""")


commands.register("notify", "Searches the program guide and prints notifications.",
                  lambda: consume(), lambda: help())
