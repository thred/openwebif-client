import datetime
from schedule import Schedule
import term
import utils


class Program:
    def __init__(self, event):
        self.title = utils.fix(event.get("title"))
        self.description = utils.fix(event.get("shortdesc"))
        self.content = utils.fix(event.get("longdesc"))
        self.hint = None
        self.schedules = [Schedule(utils.fix(event.get("sname")), event.get(
            "begin_timestamp"), event.get("duration_sec"))]

    def isSameAs(self, other):
        return self.title == other.title and self.description == other.description and self.content == other.content

    def isScheduled(self):
        return len(self.schedules) > 0

    def isMatching(self, term):
        return self.isMatchingAny([term])

    def isMatchingAny(self, terms):
        texts = [self.title, self.description, self.content]

        for schedule in self.schedules:
            texts.append(schedule.channel)

        matchingTerms = []

        for term in terms:
            if term.isMatching(texts):
                matchingTerms.append(term)

        if matchingTerms:
            self.hint = u"\n".join(["Matching: " + unicode(term)
                                    for term in matchingTerms])
            return True

        return False

    def toHumanReadable(self, lineLength=72):
        result = u""

        result += "="*lineLength + "\n"
        result += utils.wrap(self.title, lineLength) + "\n"
        result += "\n"

        notes = [note for note in [self.description,
                                   self.content, self.hint] if note]

        if len(self.schedules) > 0:
            for schedule in self.schedules:
                result += unicode(schedule) + "\n"

            if notes:
                result += "-"*lineLength + "\n"

        result += u"\n".join([utils.wrap(note, lineLength) +
                              "\n" for note in notes])

        if notes:
            result += "="*lineLength + "\n"

        return result

    def toHtml(self):
        result = u"""
<h1>{title}</h1>
<p>{schedules}</p>
""".format(title=utils.html(self.title), schedules=u"\n".join([schedule.toHtml() for schedule in self.schedules]))

        notes = [note for note in [self.description,
                                   self.content, self.hint] if note]

        for note in notes:
            result += u"<p>{}</p>\n".format(utils.html(note))

        return result

    def __unicode__(self):
        return self.toHumanReadable()
