# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.api.exceptions import InvalidInput
from warpseq.model.evaluator import Evaluator
from warpseq.model.note import Note

def evaluate(context=None, subject=None, how=None):
    if isinstance(how, Evaluator):
        res = how.evaluate(context=context, subject=input)
        return evaluate(context=context,  subject=input, how=res)
    return how


class Slot(object):

    __slots__ = ( "note", "octave", "degree", "repeats", "length", "sharp", "flat", "chord_type", "inversion",
        "variable_set", "copy_to_track", "track_grab", "rest", "ccs", "delay", "velocity", "skip", "shuffle",
        "reverse", "reset", "tie", "degree_shift", "octave_shift" )

    def __init__(self, note=None, octave=None, octave_shift=None, degree_shift=None, degree=None, repeats=None, length=None, sharp=None, flat=None,
                 chord_type=None, inversion=None, variable_set=None, copy_to_track=None, track_grab=None, rest=False, ccs=None,
                 delay=None, velocity=None, skip=None, shuffle=None, reverse=None, reset=None, tie=None):

        self.note = note
        self.octave = octave
        self.degree = degree
        self.repeats = repeats
        self.length = length
        self.sharp = sharp
        self.flat = flat
        self.chord_type = chord_type
        self.inversion = inversion

        self.variable_set = variable_set
        self.copy_to_track = copy_to_track
        self.ccs = ccs
        self.delay = delay
        self.velocity = velocity
        self.skip = skip
        self.track_grab = track_grab
        self.rest = rest
        self.shuffle = shuffle
        self.reverse = reverse
        self.reset = reset
        self.tie = tie
        self.degree_shift = degree_shift
        self.octave_shift = octave_shift

    def evaluate(self, context, note):

        note = note.copy()

        if note.length is None:
            note.length = context.base_length

        # ----
        # NON-NOTE RELATED OPS

        if evaluate(context=context, subject=note, how=self.tie):
            return Note(tie=True)

        if self.skip:
            grabs = evaluate(context=context, subject=note, how=self.skip)
            for _ in range(0, grabs):
                context.pattern.next()

        if self.shuffle and evaluate(context=context, subject=note, how=self.shuffle):
            context.pattern.shuffle()

        if self.reverse and evaluate(context=context, subject=note, how=self.reverse):
            context.pattern.reverse()

        if self.reset and evaluate(context=context, subject=note, how=self.reset):
            context.pattern.reset()

        if self.rest and evaluate(context=context, subject=note, how=self.rest):
            return None

        # ---
        # NOTE BASICS HERE

        if self.note:
            note = note.with_name(evaluate(context=context, subject=note, how=self.note))
            assert note.length is not None

        if self.degree:
            note = note.scale_transpose(context.scale, self.degree)

        if self.octave is not None:
            res = evaluate(context=context, subject=note, how=self.octave)
            note = note.with_octave(res)

        # -----
        # NOTE MODIFICATIONS HERE

        if self.octave_shift is not None:
            res = evaluate(context=context, subject=note, how=self.octave_shift)
            note = note.transpose(octaves=res)

        if self.degree_shift is not None:
            note = note.scale_transpose(context.scale, evaluate(context=context, subject=note, how=self.degree_shift))

        if self.repeats:
            note = note.with_repeats(evaluate(context=context, subject=note, how=self.repeats))

        if self.length and self.length != 1:
            note = note.with_length(evaluate(context=context, subject=note, how=self.length))

        if self.sharp and evaluate(context=context, subject=note, how=self.sharp):
            note = note.transpose(semitones=1)

        if self.flat and evaluate(context=context, subject=note, how=self.flat):
            note = note.transpose(semitones=-1)

        if self.chord_type:
            note = note.chordify(evaluate(context=context, subject=note, how=self.chord_type))

        if self.variable_set:
            for (k,v) in self.variable_set.items():
                set_global(k, evaluate(context=context, subject=note, how=v))

        if self.copy_to_track:
            note.with_track_copy(evaluate(context=context, subject=note, how=self.copy_to_track))

        if self.track_grab:
            note.deferred = True
            note.deferred_expressions.append(lambda x: Slot(
                evaluate(context=context, subject=note, how=self.track_grab)
            ))

        if self.ccs:
            items = {}
            for (k,v) in self.ccs.items():
                items = {}
                items[k] = evaluate(context=context, subject=note, how=v)
            for (k,v) in items.items():
                note = note.with_cc(k,v)

        if self.delay:
            note = note.with_delay(evaluate(context=context, subject=note, how=v))

        if self.velocity is not None:
            note = note.with_velocity(evaluate(context=context, subject=note, how=self.velocity))

        if self.inversion:
            note = note.invert(evaluate(context=context, subject=note, how=self.inversion))

        return note


S = Slot