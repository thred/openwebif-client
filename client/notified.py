import config
import codecs
import os.path

class Notified():

    def __init__(self, filename):
        self.keys = []
        self.filename = filename

    def load(self):
        if config.debug:
            print("Loading notified list from: " + self.filename)

        if os.path.isfile(self.filename):
            file = codecs.open(self.filename, "r", "UTF-8")

            for line in file:
                line = unicode(line).strip()

                if line.startswith("#"):
                    continue

                if len(line) == 0:
                    continue

                self.alreadyNotified(line)

            file.close()

    def store(self):
        if config.debug:
            print("Storing notified list to: " + self.filename)

        file = codecs.open(self.filename, "w", "UTF-8")

        file.write("# openwebif-client already notified\n")

        for key in self.keys:
            file.write(key + "\n")

        file.close()

    def alreadyNotified(self, key):
        if key in self.keys:
            return True

        self.keys.append(key)

        return False
