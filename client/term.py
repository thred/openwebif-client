import re


def parse(source):
    andParts = re.split("\\bAND\\b", source)

    if len(andParts) > 1:
        return AndTerm(map(parse, andParts))

    orParts = re.split("\\bOR\\b", source)

    if len(orParts) > 1:
        return OrTerm(map(parse, orParts))

    if source.find("NOT ") == 0:
        return NotTerm(parse(source[4:]))

    return PatternTerm(source)



class PatternTerm:

    def __init__(self, pattern):
        self.pattern = pattern.strip()
        self.expression = re.compile(
            "\\b" + self.pattern + "\\b", re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL)

    def isMatching(self, texts):
        for text in texts:
            if text and self.expression.search(text):
                return True

        return False

    def __unicode__(self):
        return self.pattern


class AndTerm:

    def __init__(self, terms):
        self.terms = terms

    def isMatching(self, texts):
        for term in self.terms:
            if not term.isMatching(texts):
                return False

        return True

    def __unicode__(self):
        return u" AND ".join(map(lambda term: unicode(term), self.terms))


class OrTerm:
    def __init__(self, terms):
        self.terms = terms

    def isMatching(self, texts):
        for term in self.terms:
            if term.isMatching(texts):
                return True

        return False

    def __unicode__(self):
        return u" OR ".join(map(lambda term: unicode(term), self.terms))


class NotTerm:
    def __init__(self, term):
        self.term = term

    def isMatching(self, texts):
        return not self.term.isMatching(texts)

    def __unicode__(self):
        return u"NOT " + unicode(self.term)
