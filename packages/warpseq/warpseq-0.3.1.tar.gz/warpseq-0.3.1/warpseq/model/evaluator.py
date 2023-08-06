import random

VARIABLES = dict()

def set_variable(name, value):
    VARIABLES[name] = value

class Evaluator(object):

    __slots__ = ()

    def evaluate(self, context=None, subject=None):
        raise exceptions.NotImplementedError

class Probability(Evaluator):

    __slots__ = ('chance', 'a', 'b')

    def __init__(self, chance, a, b):
        self.chance = chance
        self.a = a
        self.b = b

    def evaluate(self, context=None, subject=None):
        if random.random() < self.chance:
            return self.a
        else:
            return self.b

class RandomChoice(Evaluator):

    __slots__ = ('values',)

    def __init__(self, *values):
        self.values = values
        super(RandomChoice, self).__init__()

    def evaluate(self, context=None, subject=None):
        res = random.choice(self.values)
        return res

class RandomRange(Evaluator):

    __slots__ = ('low','high')

    def __init__(self, low, high):
        self.low = low
        self.high = high
        super(RandomRange, self).__init__()

    def evaluate(self, context=None, subject=None):
        rng = random.randrange(self.low, self.high)
        return rng


class PatternGrab(Evaluator):

    __slots__ = ('pattern',)

    def __init__(self, pattern):
        self.pattern = pattern
        super(PatternGrab, self).__init__()

    def evaluate(self, context=None, subject=None):
        pattern = context.song.find_pattern(self.pattern)
        return pattern.next()

class LoadVariable(Evaluator):

    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name
        super(LoadVariable, self).__init__()

    def evaluate(self, context=None, subject=None):
        global VARIABLES
        return VARIABLES.get(self.name, 0)

