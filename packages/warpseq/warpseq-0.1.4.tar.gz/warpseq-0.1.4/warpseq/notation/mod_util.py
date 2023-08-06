# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# various functions around mod expressions to mostly support parsing out
# their argument values

import random
from warpseq.api.exceptions import *

VARIABLES = dict()

def is_choice(how):
    return "," in how

def is_range(how):
    return ":" in how

def pick_choice(how):
    tokens = how.split(",")
    choices = []
    for t in tokens:
        if is_variable(t):
            choices.append(_get_variable(t))
        else:
            choices.append(t)
    return random.choice(choices)

def pick_range(how):
    bounds = how.split(":",1)
    left = bounds[0]
    right = bounds[1]
    if is_variable(left):
        left = get_variable(left)
    if is_variable(right):
        right = get_variable(right)
    left = int(left)
    right = int(right)
    rc = random.randrange(left, right)
    return rc

def evaluate_params(parser, how, want_int=False, want_string=False, want_float=False):

    if is_choice(how):
        result = pick_choice(how)
    elif is_range(how):
        result = pick_range(how)
    else:
        result = how
        if is_variable(result):
            result = get_variable(result)
        elif is_pattern_grab(result):
            result = get_pattern_item(parser.song, result)
    if want_int:
        result = int(result)
    if want_string:
        result = str(result)
    if want_float:
        result = float(result)
    return result

def get_pattern_item(song, result):
    result = result[1:]
    pattern = song.find_pattern_by_name(result)
    if pattern is None:
        raise InvalidExpression("referenced pattern %s does not exist" % result)
    return pattern.get_next()

def is_variable(what):
    return what.startswith("$")

def is_pattern_grab(what):
    return what.startswith("@")

def get_variable(what):
    what = what.lower()
    name = what.replace("$","")
    return VARIABLES.get(name, 0)

def set_variable(what, value):
    what = what.lower()
    global VARIABLES
    VARIABLES[what] = value
