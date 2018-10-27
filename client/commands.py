_REGISTRY = {}


def register(key, description, consumeFn, helpFn):
    _REGISTRY[key] = {
        "description": description,
        "consume": consumeFn,
        "help": helpFn}


def knows(key):
    return key in _REGISTRY


def keys():
    return sorted(_REGISTRY.keys())


def describe(key):
    return _REGISTRY[key]["description"]


def consume(key):
    _REGISTRY[key]["consume"]()


def help(key):
    _REGISTRY[key]["help"]()
