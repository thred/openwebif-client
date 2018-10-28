import datetime
from schedule import Schedule
import term
import utils


class Program:
    def __init__(self, event):
        self.title = utils.fix(event.get("title"))
        self.description = utils.fix(event.get("shortdesc"))
        self.content = utils.fix(event.get("longdesc"))
        self.schedules = [Schedule(event.get("sref"), utils.fix(event.get("sname")), datetime.datetime.fromtimestamp(
            event.get("begin_timestamp")).strftime("%Y-%m-%d %H:%M"), event.get("duration_sec"))]

    def isSameAs(self, other):
        return self.title == other.title and self.description == other.description and self.content == other.content

    def isMatching(self, term):
        return self.isMatchingAny([term])

    def isMatchingAny(self, terms):
        texts = [self.title, self.description, self.content]

        for schedule in self.schedules:
            texts.append(schedule.channel)

        for term in terms:
            if term.isMatching(texts):
                return True

        return False

    def toHumanReadable(self, lineLength=72):
        result = u""

        result += "="*lineLength + "\n"
        result += utils.wrap(self.title, lineLength) + "\n"
        result += "\n"

        if len(self.schedules) > 0:
            for schedule in self.schedules:
                result += unicode(schedule) + "\n"

            if self.description or self.content:
                result += "-"*lineLength + "\n"

        if self.description:
            result += utils.wrap(self.description, lineLength) + "\n"

            if self.content:
                result += "\n"

        if self.content:
            result += utils.wrap(self.content, lineLength) + "\n"

        result += "="*lineLength + "\n"

        return result

    def __unicode__(self):
        return self.toHumanReadable()
