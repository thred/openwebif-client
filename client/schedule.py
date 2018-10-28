import datetime

class Schedule:
    def __init__(self, channel, timestamp, duration):
        self.channel = channel
        self.timestamp = timestamp

        try:
            self.duration = int(duration) / 60
        except ValueError:
            self.duration = None

    def toHumanReadable(self, lineLength=72):
        timestamp = datetime.datetime.fromtimestamp(self.timestamp).strftime("%A, %Y-%m-%d %H:%M")

        if self.duration:
            timestamp += " (" + unicode(self.duration) + " min)"

        space = lineLength - len(timestamp) - len(self.channel)

        if space > 0:
            return timestamp + " " * space + self.channel
        else:
            return timestamp + "\n" + self.channel

    def __unicode__(self):
        return self.toHumanReadable()
