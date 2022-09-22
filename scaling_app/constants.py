# Scaling Types
EMPTY = "empty"
DIAGONAL = "diagonal"
ORDINAL = "ordinal"
INTERORDINAL = "interordinal"
DICHOTOM = "dichotom"

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
LEVEL_NOM_COLOR = "#C4CDE7"

LEVEL_ORD = "ordinal"
LEVEL_ORD_COLOR = "#A1BBE7"

LEVEL_INT = "interval"
LEVEL_INT_COLOR = "#6FADE7"

LEVEL_RAT = "ratio"
LEVEL_RAT_COLOR = "#4B9AE7"


def color_conv(level):

    if level == LEVEL_NOM:
        return LEVEL_NOM_COLOR
    if level == LEVEL_ORD:
        return LEVEL_ORD_COLOR
    if level == LEVEL_INT:
        return LEVEL_INT_COLOR
    if level == LEVEL_RAT:
        return LEVEL_RAT_COLOR


def allows_order(level):

    return level == LEVEL_ORD or level == LEVEL_INT or level == LEVEL_RAT


def allows_mean(level):

    return level == LEVEL_INT or level == LEVEL_RAT
