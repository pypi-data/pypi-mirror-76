# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a Pattern is a list of symbols/expressions that will eventually
# evaluate into Chords/Notes.

from .base import NewReferenceObject
from .scale import Scale
from .transform import Transform
import warpseq.utils.utils as utils
from warpseq.api.exceptions import *

FORWARD='forward'
REVERSE='reverse'
OSCILLATE='oscillate'
PENDULUM='pendulum'
RANDOM='random'
SERIALIZED='serialized'
BROWNIAN1='brownian1'
BROWNIAN2='brownian2'
BROWNIAN3='brownian3'
BROWNIAN4='brownian4'
BROWNIAN5='brownian5'
BROWNIAN6='brownian6'
BUILD='build'

DIRECTIONS = [
    FORWARD,
    REVERSE,
    OSCILLATE,
    PENDULUM,
    RANDOM,
    SERIALIZED,
    BROWNIAN1,
    BROWNIAN2,
    BROWNIAN3,
    BROWNIAN4,
    BROWNIAN5,
    BROWNIAN6,
    BUILD
]

DIRECTION_MAP = {
    FORWARD:    utils.roller,
    REVERSE:    utils.reverse_roller,
    OSCILLATE:  utils.oscillate_roller,
    PENDULUM:   utils.pendulum_roller,
    SERIALIZED: utils.serialized_roller,
    RANDOM:     utils.random_roller,
    BROWNIAN1:  utils.brownian1_roller,
    BROWNIAN2:  utils.brownian2_roller,
    BROWNIAN3:  utils.brownian3_roller,
    BROWNIAN4:  utils.brownian4_roller,
    BROWNIAN5:  utils.brownian5_roller,
    BROWNIAN6:  utils.brownian6_roller,
    BUILD:      utils.build_roller
}

class Pattern(NewReferenceObject):

    __slots__ = [ 'name', 'slots', 'current_slots', 'octave_shift', 'rate', 'scale', 'direction', 'current_direction', 'length', '_iterator', 'obj_id' ]

    def __init__(self, name=None, slots=None, octave_shift=0, rate=1, scale=None, direction=FORWARD, length=None, obj_id=None):

        self.name = name
        self.slots = slots
        self.octave_shift = octave_shift
        self.rate = rate
        self.scale = scale

        if length is None:
            length = len(slots)

        self.length = length

        if not direction in DIRECTIONS:
            raise InvalidInput("direction must be one of: %s" % DIRECTIONS)

        self.direction = direction
        self.current_direction = direction
        self.obj_id = obj_id

        super(Pattern, self).__init__()
        self.reset()

    def reset(self):
        self.current_slots = self.slots[:]
        self.apply_direction()

    def get_octave_shift(self, track):
        return track.instrument.base_octave + self.octave_shift

    def apply_direction(self):
        fn = DIRECTION_MAP.get(self.direction, None)
        if fn is not None:
            self._iterator = fn(self.current_slots)
        else:
            raise Exception("internal error: direction (%s) not implemented" % self.direction)

    def get_next(self):
        return next(self._iterator)

    def get_length(self):
        return self.length

    def get_iterator(self):
        for x in range(0, self.get_length()):
            yield next(self._iterator)

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots,
            octave_shift = self.octave_shift,
            rate = self.rate,
            direction = self.direction,
            length = self.length,
        )
        if self.scale:
            result['scale'] = self.obj_id
        else:
            result['scale'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Pattern(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots'],
            octave_shift = data['octave_shift'],
            rate = data['rate'],
            scale = song.find_scale(data['scale']),
            direction = data.get('direction', FORWARD),
            length = data.get('length', None)
        )
