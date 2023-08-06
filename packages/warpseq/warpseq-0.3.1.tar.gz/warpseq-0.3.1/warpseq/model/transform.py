# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a transform is a list of modifier expressions that can be used
# to build MIDI effects including Arps.

from ..utils.utils import roller
from .base import NewReferenceObject
from .directions import *
from warpseq.utils.serialization import Serializer
from warpseq.model.context import Context

CHORDS = 'chords'
NOTES = 'notes'
BOTH = 'both'
APPLIES_CHOICES = [ CHORDS, NOTES, BOTH ]

class Transform(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', 'current_slots', 'divide', 'applies_to', 'obj_id',
                  'direction', 'current_direction', '_iterator', '_mod', '_slot_mods', '_repeat_processor', 'auto_reset' ]

    SERIALIZER = Serializer(
        values = ( 'name', 'slots', 'divide', 'applies_to', 'direction', 'auto_reset' ),
        objects = ( ),
        object_lists = (),
        objects_2d = (),
        custom=(),
    )

    def __init__(self, song=None, name=None, slots=None, divide=1, obj_id=None,
                 applies_to=None, _repeat_processor=False, direction=FORWARD, auto_reset=False):

        self.name = name
        self.slots = slots
        self.divide = divide
        self.applies_to = applies_to
        self.obj_id = obj_id
        self._repeat_processor = _repeat_processor
        self._slot_mods = roller(slots)
        self.direction = direction
        self.current_direction = direction
        self.auto_reset = auto_reset

        if applies_to is None:
            applies_to = BOTH
        self.applies_to = applies_to

        assert applies_to in APPLIES_CHOICES
        self.reset()

        super(Transform, self).__init__()


    def process(self, song, pattern, scale, track, note_list, t_start, slot_duration):

        # FIXME: REFACTOR

        from .chord import Chord
        assert song is not None

        new_note_list = []
        applies_to = self.applies_to

        repeater = self._repeat_processor

        start_time = t_start

        if self.auto_reset:
            self.reset()

        for (i, notes2) in enumerate(note_list):
            # FIXME: internal function

            (actual_notes, is_chord) = _expand_notes(notes2)

            divide = self.divide

            if divide is None:
                # constructs an arp like transform that plays every note within the given slot time
                divide = len(actual_notes)

            process_exprs = True

            if is_chord:
                # leave chords unaffected if requested
                if applies_to not in [ BOTH, CHORDS ]:
                    process_exprs = False
            else:
                # leave notes unaffected if requested
                if applies_to not in [ BOTH, NOTES ]:
                    process_exprs = False
                    divide = 1

            if is_chord and not process_exprs:

                new_note_list.append(actual_notes)

            else:


                notes = actual_notes

                if not notes:
                    # we don't attempt to transform rests
                    new_note_list.append([])
                    continue

                if repeater:
                    divide = divide * notes[0].repeat

                # compute the new time information for the divided notes
                new_delta = round(actual_notes[0].length / divide)

                # roll_notes picks values off the incoming note/chord list, it happens once each time a 'divide' is looped through
                roll_notes = roller(notes)

                context = Context(
                    song = song,
                    pattern = pattern,
                    scale = scale,
                    track = track,
                    base_length = new_delta
                )

                for j in range(0, divide):
                    # FIXME: internal function?

                    # grab a note that is playing from all notes that are playing
                    if not repeater or (divide == 1):
                        which_note = next(roll_notes) # .copy()
                    else:
                        which_note = notes

                    # get the next transform slot from the iterator

                    which_slot = self.get_next()
                    #print("WHICH SLOT=%s/%s/%s" % (i,j,which_slot))

                    # calculate the new note using the mod expression

                    if process_exprs:

                        if type(which_note) == list:
                            which_note = Chord(notes=which_note, from_scale=which_note[0].from_scale)

                        final_note = which_slot.evaluate(context, which_note)


                        if final_note is None:
                            continue
                    else:
                        # this handles if the transform was set to skip chords or skip individual notes
                        final_note = which_note.copy()

                    # the transform can technically return a LIST of notes/chord here, which can occur (for example) if
                    # ratcheting. If this happens, we consider the items to be evenly spaced and REDO the "divide" math
                    # in an inner loop. In the simplest most common case, there is only one divide here

                    final_notes = final_note
                    if type(final_note) != list:
                        final_notes = [ final_note ]

                    divide2 = len(final_notes)
                    inside_delta = round(new_delta / divide2)

                    # FIXME: function
                    for (k, final_note) in enumerate(final_notes):
                        new_start_time = start_time + (i * slot_duration) + (j * new_delta) + (k * inside_delta)
                        new_note_list.append(
                            final_note.with_timing(start_time=new_start_time, end_time=new_start_time + inside_delta, length=inside_delta).get_notes()
                        )

        return new_note_list

def _expand_notes(notes):

    # FIXME: is this generic?  Do we have this pattern in the parser as well?

    # the list of notes coming out the system per step can look like:
    # [None] - a rest
    # [n1] - a single note
    # [n1,n2] - a bunch of arbitrary notes, usually from an extracted chord
    # [chord] - a chord object, usually from a transform that was not yet extracted
    # we need to convert this unilaterally to a list of notes

    from .note import Note

    # returns the notes and whether or not a chord was found

    ln = len(notes)

    if ln == 0:
        return (notes, False)

    n1 = notes[0]

    if type(n1) == Note:
        if ln == 1:
            return (notes, False)
        else:
            return (notes, True)
    else:

        # assume Chord
        return (notes[0].notes, True)
