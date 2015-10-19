import re

EXPAND_GROUP = re.compile(r"\{([^}]*)\}")

def expand(expr):
    match = EXPAND_GROUP.search(expr)

    if match:
        before = expr[:match.start()]
        after = expr[match.end():]
        variants = match.group(1).split(",")

        for v in variants:
            for rest in expand(after):
                yield before + v + rest
    else:
        yield expr
