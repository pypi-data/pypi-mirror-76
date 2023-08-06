# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a clip is a set of patterns and other details at the intersection
# of a scene and track

from warpseq.model.time_stream import (standardize_notes, notes_to_events)
from ..playback.player import Player
from ..utils import utils
from .base import NewReferenceObject
from .scale import Scale
from warpseq.utils.serialization import Serializer
from warpseq.model.context import Context
from warpseq.model.transform import Transform, BOTH
from warpseq.model.slot import Slot
import time

# FAIR WARNING: this code has some larger functions because it is trying to be more efficient
# refactoring pending

DEFAULT_SCALE = None
INTERNAL_REPEATER = '__INTERNAL_REPEATER__'

def get_default_scale():
    from .note import Note
    global DEFAULT_SCALE
    if DEFAULT_SCALE is None:
        DEFAULT_SCALE = Scale(root=Note(name="C", octave=0), scale_type='chromatic')
    return DEFAULT_SCALE

class Clip(NewReferenceObject):

    __slots__ = [
        'name', 'scales', 'patterns', 'transforms', 'rate', 'repeat', 'auto_scene_advance', 'next_clip', 'tempo_shifts',
        'obj_id', 'slot_length', 'track','scene','_current_tempo_shift','_tempo_roller','_transform_roller',
        '_scale_roller'
    ]

    SERIALIZER = Serializer(
        values = ( 'name', 'repeat', 'slot_length', 'next_clip', 'auto_scene_advance', 'tempo_shifts', 'rate' ),
        objects = ( 'track', 'scene' ),
        object_lists = ( 'patterns', 'scales' ),
        objects_2d = ( 'transforms', ),
        custom = ()
    )

    def __init__(self, name=None, scales=None, patterns=None, transforms=None,  rate=1, repeat=-1,
                 auto_scene_advance=False, next_clip=None, tempo_shifts=None, track=None,
                 scene=None, slot_length=0.0625, obj_id=None):

        self.name = name
        self.obj_id = obj_id
        self.scales = scales
        self.patterns = patterns
        self.transforms = transforms
        self.rate = rate
        self.repeat = repeat
        self.auto_scene_advance = auto_scene_advance
        self.next_clip = next_clip
        self.tempo_shifts = tempo_shifts
        self.track = track
        self.scene = scene
        self.slot_length = slot_length
        self._current_tempo_shift = 0

        super(Clip, self).__init__()
        self.reset()

    def reset(self):
        """
        Resetting a clip (restarting it) moves all rolling positions in
        scales and so on to the first position in those lists.
        """

        # FIXME: refactor

        if self.tempo_shifts:
            self._tempo_roller = utils.roller(self.tempo_shifts)
        else:
            self._tempo_roller = utils.roller([0])

        if self.scales:
            self._scale_roller = utils.roller(self.scales)
        else:
            self._scale_roller = None

        if self.transforms is not None:
            self._transform_roller = utils.roller(self.transforms)
        else:
            self._transform_roller = utils.roller([ None ])

    def scenes(self, song):
        return [ song.find_scene(x) for x in self.scene_ids ]

    def tracks(self, song):
        return [ song.find_track(x) for x in self.track_ids ]

    def get_actual_scale(self, song, pattern, roller):
        if roller:
            return next(roller)
        elif pattern and pattern.scale:
            return pattern.scale
        elif self.scene.scale:
            return self.scene.scale
        elif song.scale:
            return song.scale
        return get_default_scale()

    def slot_duration(self, song, pattern):
        # in milliseconds
        return (120 / (song.tempo * self.rate * pattern.rate * self.scene.rate + self._current_tempo_shift)) * 125

    def get_clip_duration(self, song):
        # in milliseconds
        total = 0
        for pattern in self.patterns:
            ns = self.slot_duration(song, pattern) * pattern.get_length()
            total = total+ns
        return total

    def _process_pattern(self, song, t_start, pattern):

        # FIXME: refactor

        self._current_tempo_shift = next(self._tempo_roller)
        octave_shift = pattern.get_octave_shift(self.track)
        slot_duration = self.slot_duration(song, pattern)
        scale = self.get_actual_scale(song, pattern, self._scale_roller)

        if self._transform_roller:
            transform = next(self._transform_roller)
        else:
            transform = None

        context = Context(
            song = song,
            clip = self,
            pattern = pattern,
            scale = scale,
            base_length = slot_duration
        )


        notes = []

        for expression in pattern.get_iterator():

            note = scale.get_first().copy()
            note.length = slot_duration
            note.from_context = context
            note = expression.evaluate(context, note)
            if note:
                note = note.transpose(octaves=octave_shift)

            # these should always be notes or chord objects!
            notes.append(note)

        notes = standardize_notes(notes, scale, slot_duration, t_start)

        repeater = Transform(name=INTERNAL_REPEATER, slots=[Slot()], divide=1, applies_to=BOTH, _repeat_processor=True)
        notes = repeater.process(song, pattern, scale, self.track, notes, t_start, slot_duration)

        if transform:
            if type(transform) != list:
                transform = [transform]
            for tform in transform:
                notes  = tform.process(song, pattern, scale, self.track, notes, t_start, slot_duration)

        return notes

    def get_events(self, song):
        t_start = 0
        t1 = time.perf_counter()
        results = []
        for pattern in self.patterns:
            results.extend(self._process_pattern(song, t_start, pattern))
            t_start = t_start + (self.slot_duration(song, pattern) * pattern.get_length())

        res = notes_to_events(self, results)
        t2 = time.perf_counter()
        print(t2-t1)
        return res

    def get_player(self, song, engine_class):
        player = Player(
            clip=self,
            song=song,
            engine=engine_class(song=song, track=self.track, clip=self),
        )
        player.engine.player = player
        return player
