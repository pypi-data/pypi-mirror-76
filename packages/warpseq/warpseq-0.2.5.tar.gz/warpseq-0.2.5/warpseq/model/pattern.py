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
from warpseq.model.directions import *

class Pattern(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', 'current_slots', 'octave_shift', 'rate', 'scale', 'direction', 'current_direction', 'mod_expressions_callback', 'length', '_iterator', 'obj_id' ]

    def __init__(self, name=None, slots=None, octave_shift=0, rate=1, scale=None, direction=FORWARD, length=None, mod_expressions_callback=None, obj_id=None):

        self.name = name
        self.slots = slots
        self.octave_shift = octave_shift
        self.rate = rate
        self.scale = scale

        if mod_expressions_callback:
            # activate the generator
            mod_expressions_callback = mod_expressions_callback()

        self.mod_expressions_callback = mod_expressions_callback


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

    def get_octave_shift(self, track):
        return self.octave_shift

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
