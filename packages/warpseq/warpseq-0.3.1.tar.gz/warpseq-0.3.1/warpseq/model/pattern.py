# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a Pattern is a list of symbols/expressions that will eventually
# evaluate into Chords/Notes.

from .base import NewReferenceObject
from warpseq.api.exceptions import *
from warpseq.model.directions import *
from warpseq.utils.serialization import Serializer

class Pattern(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', 'current_slots', 'octave_shift', 'rate', 'scale', 'direction', 'current_direction', 'mod_expressions_callback', 'length', '_iterator', 'obj_id' ]

    SERIALIZER = Serializer(
        values = ( 'name', 'octave_shift', 'rate', 'scale', 'direction', 'length' ),
        objects = ( 'scale' ),
        object_lists = (),
        objects_2d = (),
        custom=( 'slots' ),
    )

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
        for _ in range(0, self.get_length()):
            yield next(self._iterator)
