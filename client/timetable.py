from program import Program
import hashlib

def of(events, terms=None):
    timetable = TimeTable()

    for event in events:
        program = Program(event)

        if terms and not program.isMatchingAny(terms):
            continue

        timetable.add(program)

    return timetable


class TimeTable():

    def __init__(self):
        self.programs = []

    def add(self, program):
        for existing in self.programs:
            if existing.isSameAs(program):
                existing.schedules += program.schedules
                return

        self.programs.append(program)

    def notified(self, notified, target):
        for program in self.programs:
            for schedule in program.schedules[:]:
                key = u"{},{},{},{}".format(program.title, schedule.channel, schedule.timestamp, target)
                checksum = hashlib.md5()
                checksum.update(key.encode("UTF-8"))
                key = checksum.hexdigest()

                if notified.alreadyNotified(key):
                    program.schedules.remove(schedule)

        self.removeUnscheduled()


    def removeUnscheduled(self):
        self.programs = [
            program for program in self.programs if program.isScheduled()]

    def __len__(self):
        return len(self.programs)

    def toHumanReadable(self, lineLength=72):
        programs = sorted(self.programs, key=lambda item: item.title)

        return "\n".join(program.toHumanReadable(lineLength) for program in programs)

    def toHtml(self):
        programs = sorted(self.programs, key=lambda item: item.title)
        result = "<hr/>".join(program.toHtml() for program in programs)

        return u"<html><body>{}</body></html>".format(result)
