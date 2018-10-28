from program import Program


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
        self.items = []

    def add(self, program):
        for item in self.items:
            if item.isSameAs(program):
                item.schedules += program.schedules
                return

        self.items.append(program)

    def __len__(self):
        return len(self.items)

    def toHumanReadable(self, lineLength=72):
        items = sorted(self.items, key=lambda item: item.title)

        return "\n".join(item.toHumanReadable(lineLength) for item in items)
