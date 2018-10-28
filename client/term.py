import re


def parse(source):
    source = source.strip()
    andParts = re.split("\\bAND\\b", source)

    if len(andParts) > 1:
        return AndTerm(map(parse, andParts))

    orParts = re.split("\\bOR\\b", source)

    if len(orParts) > 1:
        return OrTerm(map(parse, orParts))

    if source.find("NOT ") == 0:
        return NotTerm(parse(source[4:]))

    inParts = re.split("\\bIN\\b", source)

    if len(inParts) == 2:
        return InTerm(parse(inParts[0]), inParts[1])

    elif len(inParts) > 2:
        raise "Invalid term: " + source

    return PatternTerm(source)


class PatternTerm:

    def __init__(self, pattern):
        self.pattern = pattern.strip()
        self.expression = re.compile(
            "\\b" + self.pattern + "\\b", re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL)

    def isMatching(self, obj):
        if not obj:
            return False

        for key in obj.keys():
            if obj[key] and self.expression.search(obj[key]):
                return True

        return False

    def __unicode__(self):
        return self.pattern


class AndTerm:

    def __init__(self, terms):
        self.terms = terms

    def isMatching(self, obj):
        for term in self.terms:
            if not term.isMatching(obj):
                return False

        return True

    def __unicode__(self):
        return u" AND ".join(map(lambda term: unicode(term), self.terms))


class OrTerm:
    def __init__(self, terms):
        self.terms = terms

    def isMatching(self, obj):
        for term in self.terms:
            if term.isMatching(obj):
                return True

        return False

    def __unicode__(self):
        return u" OR ".join(map(lambda term: unicode(term), self.terms))


class NotTerm:
    def __init__(self, term):
        print(unicode(term))
        self.term = term

    def isMatching(self, obj):
        return not self.term.isMatching(obj)

    def __unicode__(self):
        return u"NOT " + unicode(self.term)


class InTerm:
    def __init__(self, term, key):
        self.term = term
        self.key = key.strip()

    def isMatching(self, obj):
        subObj = {self.key: obj[self.key]}

        return self.term.isMatching(subObj)

    def __unicode__(self):
        return u"{} IN {}".format(unicode(self.term), self.key)
