# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a device represents a physical or virtual MIDI interface

from .base import NewReferenceObject
from warpseq.playback.midi import open_port

class Device(NewReferenceObject):

    __slots__ = [ 'name', 'obj_id', '_midi_out' ]

    def __init__(self, name=None, obj_id=None):
        self.name = name
        self.obj_id = obj_id
        self._midi_out = None
        super(Device,self).__init__()

    def get_midi_out(self):
        if self._midi_out is None:
            self._midi_out = open_port(self.name)
        return self._midi_out

    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name
        )

    @classmethod
    def from_dict(cls, song, data):
        return Device(
            obj_id = data['obj_id'],
            name = data['name']
        )
