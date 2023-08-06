# assorted smallish functions

means_true = set("yes y sure ja j jou si on t true  aye 1 affirmative".split())
means_false = set("no n nope nein nee   off f false nay 0 negative".split())

def boolish(value, default=None):
    """Return a truth value for the argument.

    If that cannot be determined, fall back to default (if not None) or raise a
    ValueError exception. This can be used for parsing config files (that aren't
    Python) or interactive answers or the like.

    """

    val = value.lower()
    if val in means_true:
        return True
    if val in means_false:
        return False
    if default is None:
        raise ValueError("value '{}' cannot be understood as false or true".
                         format(value))
    else:
        return default
