# Scaling Types
EMPTY = "empty"
NOMINAL = "nominal"
ORDINAL = "ordinal"
INTERORDINAL = "interordinal"

# Scaling Data Type
INT = "int"
GENERIC = "generic"

# System States
ORIGINAL = "original"
EXPANDED = "expanded"
SCALING = "scaling"
RESULT = "result"

# Levels of Measurement
LEVEL_NOM = "nominal"
LEVEL_NOM_COLOR = "#A0A0A0"

LEVEL_ORD = "ordinal"
LEVEL_ORD_COLOR = "#FFEC6E"

LEVEL_INT = "interval"
LEVEL_INT_COLOR = "#8177FF"

LEVEL_RAT = "ratio"
LEVEL_RAT_COLOR = "#FF5656"

# Lattice Draw Types

dim = "dim-draw-layout"
freese = "freese-layout"
standard = "standard-layout"
inf = "inf-additive-layout"

# API
api_version = "2.4.1-SNAPSHOT"


def color_conv(level):
    # returns the color valie corresponding to the input level of measurement
    if level == LEVEL_NOM:
        return LEVEL_NOM_COLOR
    if level == LEVEL_ORD:
        return LEVEL_ORD_COLOR
    if level == LEVEL_INT:
        return LEVEL_INT_COLOR
    if level == LEVEL_RAT:
        return LEVEL_RAT_COLOR


def allows_order(level):
    # returns true, if the level of measurement is of a type that allows ordering
    return level == LEVEL_ORD or level == LEVEL_INT or level == LEVEL_RAT


def allows_mean(level):
    # returns true, if the level of measurement allows computation of a mean
    return level == LEVEL_INT or level == LEVEL_RAT


def substring(a, b):
    # returns true, if a is a substring of b
    if a in b:
        return True

    return False


def prefix(a, b):
    # returns true, if b is prefixed with a
    return b.startswith(a)


def postfix(a, b):
    # returns true, if b is postfixed with a
    return b.endswith(a)


def topological_sort(values, comparator):
    # returns a topological order

    visited = dict.fromkeys(values, False)
    order = list()

    def visit(current_value):

        visited[current_value] = True
        for i in values:
            if not visited[i] and comparator(current_value, i):
                visit(i)
        order.append(current_value)

    for value in values:
        if not visited[value]:
            visit(value)

    order.reverse()

    return order
