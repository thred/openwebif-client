import bouquets
import commands
import config
import datetime
import re
import json
import textwrap
import utils


def consume():
    bouquet = config.bouquet
    bRef = bouquets.getBRef(bouquet) if bouquet else bouquets.getDefaultBRef()

    if config.debug:
        print("Using bRef: " + bRef)

    intersections = map(compileIntersections, config.popArgs(1))

    if config.debug:
        for intersection in intersections:
            print("Filtering: " + formatIntersection(intersection))

    response = utils.requestJson("epgmulti", params={"bRef": bRef})

    for event in response["events"]:
        if intersections == None or len(intersections) == 0:
            report(event)

        else:
            matches = matching(intersections, event)

            if matches:
                report(event, matches)


def compileIntersections(tup):
    tuples = [(tup.strip(), True) for tup in re.split("\\bAND\\b", tup)]

    for index, tup in enumerate(tuples):
        if tup[0].startswith("NOT "):
            tuples[index] = (prepareRegex(tup[0][4:]), False)
        else:
            tuples[index] = (prepareRegex(tup[0]), True)

    return map(lambda tup: (re.compile(tup[0], re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL), tup[1]), tuples)


def prepareRegex(pattern):
    pattern = pattern.replace(" ", "\\s")
    pattern = "\\b" + pattern + "\\b"
    return pattern


def report(event, matches=None):
    if config.pretty:
        sname = fix(unicode(event.get("sname")))
        timestamp = datetime.datetime.fromtimestamp(
            event.get("begin_timestamp")).strftime("%Y-%m-%d %H:%M")
        title = fix(unicode(event.get("title")))
        shortdesc = fix(unicode(event.get("shortdesc")))
        longdesc = fix(unicode(event.get("longdesc")))

        print("")
        if len(title) > 40:
            print(textwrap.fill(title, 80))
            print(unicode("{:>80}").format(sname + ", " + timestamp))
        else:
            print(unicode("{:40}{:>40}").format(
                title, sname + ", " + timestamp))
        print("--------------------------------------------------------------------------------")
        printDescriptions([shortdesc, longdesc])
        print("")

        if matches:
            print("Matched by: " + ", ".join(matches))
            print("")
    else:
        print(utils.format(event, keys=[
            "sname", "title", "begin_timestamp:timestamp", "shortdesc", "longdesc"]))


def matching(intersections, event):
    if intersections == None or len(intersections) == 0:
        return None

    matches = []

    for intersection in intersections:
        intersects = True

        for tup in intersection:
            match = tup[0].search(unicode(event.get("sname"))) != None or tup[0].search(unicode(event.get("title"))) != None or tup[0].search(
                unicode(event.get("shortdesc"))) != None or tup[0].search(unicode(event.get("longdesc"))) != None

            if tup[1] == match:
                continue
            else:
                intersects = False
                break

        if intersects:
            matches.append(formatIntersection(intersection))

    return matches if len(matches) > 0 else None


def formatIntersection(intersections):
    texts = [intersection[0].pattern if intersection[1] else "NOT " + intersection[0].pattern for intersection in intersections]
    texts = [text.replace("\\b", "") for text in texts]
    texts = [text.replace("\\s", " ") for text in texts]
    return " AND ".join(texts)


def printDescriptions(texts):
    texts = filter(lambda text: len(text) > 0, map(
        lambda text: fix(text), filter(lambda text: text != None, texts)))

    if len(texts) == 0:
        texts = ["No description given."]

    text = "\n\n".join(texts)

    parts = re.split("\n", text)

    for part in parts:
        print(textwrap.fill(part, 80))


def fix(text):
    if text:
        text = text.replace("&quot;", "\"")
        text = text.replace("\\n", "\n")
        text = unicode(re.sub("\\s*//\\s*", "\n\n", text))
        text = text.strip()
    return text


def help():
    print("""\
Usage: owifc epg [OPTION ...] [PATTERN ...]

Calls the program guide and print's it in a parsable form.

The PATTERN is a regular expression. If at least one pattern is given,
it will print only lines, that contain the pattern.

Respects follwing options:

bouquet, debug, host, pretty.""")


commands.register("epg", "Displays the program guide.",
                  lambda: consume(), lambda: help())
