# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# modelling of notes, including step math necessary for creating
# chords and understanding scales.

from ..api.exceptions import *
from . note_table import NOTE_TABLE

DEFAULT_VELOCITY = 120

NOTES          = [ 'C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A', 'Bb', 'B' ]
EQUIVALENCE    = [ 'C',  'C#', 'D', 'D#', 'E',  'F',  'F#', 'G',  'G#', 'A', 'A#', 'B' ]
EQUIVALENCE_SET = set(EQUIVALENCE)

SCALE_DEGREES_TO_STEPS = {
   '0'  : 0, # people may enter this meaning "do nothing", but really it is 1.
   '1'  : 0, # C (if C major)
   'b2' : 0.5,
   '2'  : 1, # D
   'b3' : 1.5,
   '3'  : 2, # E
   '4'  : 2.5, # F
   'b5' : 3,
   '5'  : 3.5, # G
   'b6' : 4,
   '6'  : 4.5, # A
   'b7' : 5,
   '7'  : 5.5, # B
   '8'  : 6
}

class Note(object):

    __slots__ = ( 'name', 'octave', 'tie', 'length', 'start_time', 'end_time', 'flags', 'velocity', 'from_scale', 'from_parser', 'repeat', 'length_mod', 'tied', 'delay', 'no_shift')

    def __init__(self, name=None, octave=0, tie=False, length=None, start_time=None, end_time=None, flags=None, velocity=DEFAULT_VELOCITY, from_scale=None,
                 from_parser=None, repeat=1, length_mod=1, tied=0, delay=0, no_shift=False):

         self.octave = octave
         self.tie = tie
         self.length = length
         self.start_time = start_time
         self.end_time = end_time
         self.flags = flags
         self.velocity = velocity
         self.from_scale = from_scale
         self.from_parser = from_parser
         self.repeat = repeat
         self.length_mod = length_mod
         self.no_shift = no_shift
         self.tied = tied
         self.delay = delay

         if name in EQUIVALENCE_SET:
             name = NOTES[EQUIVALENCE.index(name)]
         self.name = name

         if self.flags is None:
             self.flags = {
                'deferred' : False,
                'deferred_expressions' : [],
                'cc' : {}
             }

    def shiftable(self):
        if self.no_shift == True:
            return False
        return True

    def copy(self):
        """
        Returns a new Note with the same data as the current Note
        """
        return Note(name=self.name,
                    octave=self.octave,
                    tie=self.tie,
                    length=self.length,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    velocity=self.velocity,
                    from_scale=self.from_scale,
                    from_parser=self.from_parser,
                    repeat = self.repeat,
                    length_mod = self.length_mod,
                    tied = self.tied,
                    delay = self.delay,
                    no_shift = self.no_shift,
                    flags={
                        'deferred' : self.flags['deferred'],
                        'deferred_expressions' : self.flags['deferred_expressions'].copy(),
                        'cc' : self.flags['cc'].copy()
                    }
        )

    def get_parser(self):
        return self.from_parser

    def chordify(self, chord_type):
        """
        Returns a chord of a given type using this note as the root note.
        """
        from . chord import Chord
        return Chord(root=self, chord_type=chord_type, from_scale=self.from_scale)

    def scale_transpose(self, scale_obj, steps):
        """
        Return the note N steps up (or down) within the current scale.
        """

        snn = self.note_number()
        scale_notes = scale_obj.get_notes()
        note_numbers = scale_obj.get_note_numbers()

        print("SELF: %s" % self)
        print("SNN: %s" % snn)

        index = None
        for (i,x) in enumerate(note_numbers):
            if x >= snn:
                index = i
                break

        # index of None will crash the program but shouldn't happen

        print("INDEX: %s" % index)

        if index + steps < 0:
            # out of bounds!
            raise Exception("STOP!")

        scale_note = scale_notes[index + steps]

        n1 = self.copy()
        n1.name = scale_note.name
        n1.octave = scale_note.octave
        n1.from_scale = scale_obj
        print("RES: %s" % n1)
        return n1

    def with_velocity(self, velocity):
        """
        Return a copy of this note with the set velocity
        """
        n1 = self.copy()
        n1.velocity = velocity
        return n1

    def with_repeat(self, repeat):
        n1 = self.copy()
        n1.repeat = repeat
        return n1

    def with_no_shift(self):
        n1 = self.copy()
        n1.no_shift = True
        return n1

    def with_delay(self, delay):
        n1 = self.copy()
        n1.delay = delay
        return n1

    def with_octave(self, octave):
        """
        Return a copy of this note with the set octave.
        """
        n1 = self.copy()
        n1.octave = octave
        return n1

    def with_length_mod(self, mod):
        """
        Return a copy of this note with the set octave.
        """
        n1 = self.copy()
        n1.length_mod = mod
        return n1

    def replace_with_note(self, name, octave):
        n1 = self.copy()
        n1.name = name
        n1.octave = octave
        return n1

    def with_cc(self, channel, value):
        """
        Return a copy of the note with the set MIDI CC value.
        """
        n1 = self.copy()
        n1.flags["cc"][str(channel)] = value
        return n1

    def with_timing(self, start_time=None, end_time=None, length=None):
        n1 = self.copy()
        n1.start_time = start_time
        n1.end_time = end_time
        n1.length = length
        return n1

    def transpose(self, steps=0, semitones=0, degrees=0, octaves=0):
        """
        Returns a note a given number of steps or octaves or (other things) higher.
        steps -- half step as 0.5, whole step as 1, or any combination.  The most basic way to do things.
        semitones - 1 semitone is simply a half step.  Provided to keep some implementations more music-literate.
        octaves - 6 whole steps, or 12 half steps.  Easy enough.
        degrees - scale degrees, to keep scale definition somewhat music literate.  "3" is a third, "b3" is a flat third, "3#" is an augmented third, etc.
        You can combine all of them at the same time if you really want (why?), in which case they are additive.
        """

        degree_steps = SCALE_DEGREES_TO_STEPS[str(degrees)]
        steps = steps + (semitones * 0.5) + degree_steps

        result = self.copy()
        if steps:
            # this is in an in-place edit because the note was already copied
            (result.name, result.octave) = NOTE_TABLE[result.note_number() + int(2 * steps)]
        if octaves:
            result.octave = result.octave + octaves
        return result

    def get_notes(self):
        """
        To provide polymorphic behavior with Chord
        """
        return [ self ]

    def note_number(self):
        """
        What order is this note on the keyboard?
        """
        return NOTES.index(self.name) + (12 * self.octave)

    def __repr__(self):
        return "Note<%s|%s,len=%s,time=%s/%s,cc=%s,tie=%s>" % (self.name, self.octave, self.length, self.start_time, self.end_time, self.flags['cc'], self.tie)


