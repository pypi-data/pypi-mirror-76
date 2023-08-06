# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a clip is a set of patterns and other details at the intersection
# of a scene and track

from ..notation.note_parser import NoteParser
from ..notation.time_stream import (standardize_notes, notes_to_events)
from ..playback.player import Player
from ..utils import utils
from .base import NewReferenceObject
from .scale import Scale
from .transform import Transform, BOTH
from warpseq.utils.serialization import Serializer

# FAIR WARNING: this code has some larger functions because it is trying to be more efficient

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
        '_scale_roller','_notation'
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
        self.scales = scales
        self.patterns = patterns
        self.transforms = transforms
        self.rate = rate
        self.repeat = repeat
        self.auto_scene_advance = auto_scene_advance
        self.next_clip = next_clip
        self.tempo_shifts = tempo_shifts
        self.obj_id = obj_id
        self.track = track
        self.scene = scene
        self.slot_length = slot_length
        self._current_tempo_shift = 0
        self._notation = NoteParser(clip=self)

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

        notation = self._notation
        notation.scale = scale
        notation.song = song
        notation.track = self.track
        notation.pattern = pattern
        notation.setup()

        notes = []
        for expression in pattern.get_iterator():
            notes.append(notation.do(expression, octave_shift))

        notes = standardize_notes(notes, scale, slot_duration, t_start)

        repeater = Transform(name=INTERNAL_REPEATER, slots=[1], divide=1, applies_to=BOTH, _repeat_processor=True)
        notes = repeater.process(song, pattern, scale, self.track, notes, t_start, slot_duration)

        if transform:
            if type(transform) != list:
                transform = [transform]
            for tform in transform:
                notes  = tform.process(song, pattern, scale, self.track, notes, t_start, slot_duration)

        return notes

    def get_events(self, song):
        t_start = 0
        results = []
        for pattern in self.patterns:
            results.extend(self._process_pattern(song, t_start, pattern))
            t_start = t_start + (self.slot_duration(song, pattern) * pattern.get_length())
        return notes_to_events(self, results)

    def get_player(self, song, engine_class):
        player = Player(
            clip=self,
            song=song,
            engine=engine_class(song=song, track=self.track, clip=self),
        )
        player.engine.player = player
        return player
