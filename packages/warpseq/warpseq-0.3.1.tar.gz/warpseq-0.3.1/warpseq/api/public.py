# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this implements the public Python API for WarpSeq.
# see examples/api/*.py for usage

import gc
import random

from warpseq.api.interfaces.devices import Devices
from warpseq.api.interfaces.instruments import Instruments
from warpseq.api.interfaces.patterns import Patterns
from warpseq.api.interfaces.transforms import Transforms
from warpseq.api.interfaces.player import Player
from warpseq.api.interfaces.scales import Scales
from warpseq.api.interfaces.scenes import Scenes
from warpseq.api.interfaces.song import SongApi
from warpseq.api.interfaces.tracks import Tracks
from warpseq.api.interfaces.clips import Clips
from warpseq.playback import midi
from warpseq.model.song import Song
from warpseq.api.callbacks import Callbacks, DefaultCallback

gc.disable()
MIDI_PORTS = midi.get_devices()

class Api(object):

    def __init__(self, default_callbacks=True):
        self._reset()
        self._callbacks = Callbacks()
        if default_callbacks:
            self._callbacks.clear()
            self._callbacks.register(DefaultCallback())

    def _reset(self):

        self._filename = None
        self._song = Song(name='')

        self.song = SongApi(self, self._song)
        self.devices = Devices(self, self._song)
        self.instruments = Instruments(self, self._song)
        self.scales  = Scales(self, self._song)
        self.patterns = Patterns(self, self._song)
        self.transforms = Transforms(self, self._song)
        self.scenes = Scenes(self, self._song)
        self.tracks = Tracks(self, self._song)
        self.clips = Clips(self, self._song)
        self.player = Player(self, self._song)

        random.seed()

    # ------------------------------------------------------------------------------------------------------------------
    # FIXME: song save/load work in progress

    def load(self, filename:str):

        fh = open(filename, "r")
        data = fh.read()
        fh.close()
        self._song = Song.from_json(data)
        self._filename = filename
        self._setup_api()

    def save(self):
        if not self._filename:
            raise InvalidUsage("no filename set, use save_as")
        data = self._song.to_json()
        fh = open(self._filename, "w+")
        fh.write(data)
        fh.close()

    def save_as(self, filename:str):
        self._filename = filename
        self.save()
