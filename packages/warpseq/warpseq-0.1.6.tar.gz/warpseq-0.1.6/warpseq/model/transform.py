# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a transform is a list of modifier expressions that can be used
# to build MIDI effects including Arps.

from ..notation.mod import ModExpression
from ..utils.utils import roller
from .base import NewReferenceObject
from .directions import *


CHORDS = 'chords'
NOTES = 'notes'
BOTH = 'both'
APPLIES_CHOICES = [ CHORDS, NOTES, BOTH ]

class Transform(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', 'current_slots', 'octave_slots', 'divide', 'applies_to', 'obj_id',
                  'direction', 'current_direction', '_iterator', '_mod', '_slot_mods', '_repeat_processor' ]

    def __init__(self, name=None, slots=None, octave_slots=None, divide=1, obj_id=None,
                 applies_to=None, _repeat_processor=False, direction=FORWARD):
        self.name = name
        self.slots = slots
        self.divide = divide
        self.octave_slots = octave_slots # FIXME: these could be removed
        self.applies_to = applies_to
        self.obj_id = obj_id
        self._repeat_processor = _repeat_processor
        self._mod = ModExpression(defer=False)
        self._slot_mods = roller(slots)
        self.direction = direction
        self.current_direction = direction

        if applies_to is None:
            applies_to = BOTH
        self.applies_to = applies_to

        assert applies_to in APPLIES_CHOICES
        self.reset()

        super(Transform, self).__init__()

    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots,
            octave_slots = self.octave_slots,
            applies_to = self.applies_to,
            divide = self.divide,
            direction = self.direction
        )

    @classmethod
    def from_dict(cls, song, data):
        return Transform(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots'],
            octave_slots = data['slots'],
            applies_to = data.get('applies_to', None),
            divide = data.get('divide', None),
            direction = data.get('direction',FORWARD)
        )

    def process(self, song, scale, track, note_list, t_start, slot_duration):


        """
        Given a list of notes or chords, apply the transform expressions in *slots* to produce
        a new list of notes or chords.
        """

        from .chord import Chord

        self._mod.scale = scale
        self._mod.track = track

        assert song is not None
        self._mod.song = song

        # notes is like: [n1, n2, n3], [n4], [], [n5, n6]
        # for each slot, we divide it by _divide_
        # record the first note start time and first note end time
        # get the delta between start and end, divide by _divide_
        # tick through the start to end times incrementing by delta/_divide_ (new_note_width)
        # at each step, adjust by the values in slots, as a mod expression
        # compute the new note list for this particular slot
        # move to the next slot

        new_note_list = []
        applies_to = self.applies_to

        # TODO: consider a roller option that does not reset at the pattern boundary, but survives between patterns?
        # could be musically interesting for odd lengths

        #slot_modifications = roller(self.slots)

        #slot_duration = clip.
        repeater = self._repeat_processor

        start_time = t_start

        self.reset()

        for (i, notes2) in enumerate(note_list):

            (actual_notes, is_chord) = _expand_notes(notes2)

            divide = self.divide



            if divide is None:
                # constructs an arp like transform that plays every note within the given slot time
                divide = len(actual_notes)

            skip = False
            chord_skip = False
            if is_chord:
                # leave chords unaffected if requested
                if applies_to not in [ BOTH, CHORDS ]:
                    skip = True
                    chord_skip = True
                    divide = 1
            else:
                # leave notes unaffected if requested
                if applies_to not in [ BOTH, NOTES ]:
                    skip = True
                    divide = 1

            if chord_skip:

                new_note_list.append(actual_notes)

            else:

                notes = actual_notes

                #new_notes = []


                if not notes: # None + len == 0:
                    # we don't attempt to transform rests
                    new_note_list.append([])

                    # start_time = start_time + slot_duration
                    continue


                if repeater:
                    divide = divide * notes[0].repeat

                # compute the new time information for the divided notes


                #new_delta = round(slot_duration / divide)

                new_delta = round(actual_notes[0].length / divide)

                # roll_notes picks values off the incoming note/chord list, it happens once each time a 'divide'
                # is looped through
                roll_notes = roller(notes)

                for j in range(0, divide):

                    # grab a note that is playing from all notes that are playing
                    if not repeater:
                        which_note = next(roll_notes) # .copy()
                    else:
                        which_note = notes

                    # get the next transform slot from the iterator

                    which_slot = self.get_next()
                    #print("WHICH SLOT=%s/%s/%s" % (i,j,which_slot))

                    # calculate the new note using the mod expression

                    if not skip:
                        if type(which_note) == list:
                            which_note = Chord(notes=which_note, from_scale=which_note[0].from_scale)
                        final_note = self._mod.do(which_note, which_slot)
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

                    for (k, final_note) in enumerate(final_notes):
                        new_start_time = start_time + (i * slot_duration) + (j * new_delta) + (k * inside_delta)
                        new_note_list.append(
                            final_note.with_timing(start_time=new_start_time, end_time=new_start_time + inside_delta, length=inside_delta).get_notes()
                        )

        return new_note_list

def _expand_notes(notes):

    # the list of notes coming out the system per step can look like:
    # [None] - a rest
    # [n1] - a single note
    # [n1,n2] - a bunch of arbitrary notes, usually from an extracted chord
    # [chord] - a chord object, usually from a transform that was not yet extracted
    # we need to convert this unilaterally to a list of notes

    from .note import Note
    from .chord import Chord

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
