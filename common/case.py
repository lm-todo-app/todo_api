import inflection

def camelcase(s):
    """
    Convert snake case to camel case.
    """
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def snakecase(s):
    """
    Convert camel case to snake case.
    """
    return inflection.underscore(s)
