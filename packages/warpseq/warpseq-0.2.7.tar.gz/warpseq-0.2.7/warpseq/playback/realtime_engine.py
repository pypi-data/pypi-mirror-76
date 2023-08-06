# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class is used by the player code to send MIDI events to hardware
# it contains some logic to convert chords to note events and must also
# process deferred mod-expressions caused by late-binding intra-track
# events.

#import rtmidi as rtmidi

from warpseq.api.callbacks import Callbacks
from warpseq.api.exceptions import *
from warpseq.model.registers import register_playing_note, unregister_playing_note
from warpseq.notation.mod import ModExpression

from warpseq.playback.midi import midi_note_on, midi_note_off, midi_cc

from warpseq.model.chord import Chord
from warpseq.model.event import Event, NOTE_OFF, NOTE_ON

def _get_note_number(note, instrument):

    max_o = instrument.max_octave
    min_o = instrument.min_octave

    note2 = note.transpose(octaves=instrument.base_octave)

    if note2.octave > max_o:
        note2.octave = max_o
    if note2.octave < min_o:
        note2.octave = min_o

    nn = note2.note_number()

    if nn < 0 or nn > 127:
        raise InvalidNote()

    return nn


class RealtimeEngine(object):

    __slots__ = ['song','track','clip','midi_out','midi_port','mod_expressions','callbacks','on_count','player','on_ct']

    def __init__(self, song=None, track=None, clip=None, player=None):

        self.song = song
        self.track = track
        self.clip = clip
        self.on_ct = 0


        self.mod_expressions = ModExpression(defer=True, track=self.track, song=song)

        self.player = player
        self.callbacks = Callbacks()


    def play(self, event):

        # deferred events happen when there are intra-track events such as replacing the note
        # with the currently playing note from a guide track (see docs). In this case we must
        # re-evaluate all mod expressions... we do not need to re-evaluate the track expressions
        # because the mod expression does throw away the note value and capture the value from
        # the guide track...

        pattern = event.note.from_parser.pattern
        cb = pattern.mod_expressions_callback # this must be a generator

        if event.type == NOTE_ON and (cb or event.note.flags['deferred'] == True):

            # we have to process deferred expressions twice because of the mod events
            # UNLESS we pair the off event.

            self.mod_expressions.scale = event.scale
            self.mod_expressions.pattern = event.note.from_parser.pattern
            self.mod_expressions.scale = event.note.from_scale

            exprs = event.note.flags['deferred_expressions']
            for expr in exprs:
                value = self.mod_expressions.do(event.note, expr)
                if value is None:
                    return
                event.note = value

            #event.note.flags['deferred'] = False

            # run mod expressions callback if attached
            if cb is not None:
                value = event.note

                new_mod_expressions = next(cb)
                for expr in new_mod_expressions:
                    value = self.mod_expressions.do(event.note, expr)
                    #if type(value) == Chord:
                    #    print("NOTES=%s" % value.notes)
                    if value is None:
                        return
                    event.note = value

                    # not entirely sure how this happens but we need to guard against it for now
                    # this really should be part of "mod_expressions.do"
                    if type(value) == Chord and len(value.notes) == 1:
                        event.note = value.notes[0]

        # it is possible for mod expressions to take notes and return Chords. We have to do
        # cleanup here to turn this back into a list of notes.

        if type(event.note) == Chord:
            for x in event.note.notes:
                evt = event.copy()
                evt.note = x
                evt.note.flags['deferred'] = False
                self.play(evt)

            return

        if not event.note:
            return

        if event.type == NOTE_ON:

            # FIXME: assign note vs always redeferencing event.note



            velocity = event.note.velocity
            if velocity is None:
                velocity = self.instrument.default_velocity

            register_playing_note(self.track, event.note)

            for (control, value) in event.note.flags['cc'].items():
                control = int(control)


                for instrument in self.track.get_instruments_to_play():

                    #print("SEND MIDI CC: %s/%s" % (control, value))

                    # command = (MIDI_CONTROLLER_CHANGE & 0xf0) | (self.channel - 1 & 0xf)
                    # self.midi_out.send_message([command, channel & 0x7f, value & 0x7f])

                    #msg = mido.Message(MIDO_CONTROLLER_CHANGE, channel=instrument.channel-1, control=control, value=int(value))
                    #print(msg)
                    #instrument.get_midi_out().send(msg)

                    midi_cc(instrument.get_midi_out(), instrument.channel, control, int(value))


            if not (self.track.muted or event.note.muted):

                #print("%s ON: %s" % (self.track.name, event.note))
                self.on_ct = self.on_ct + 1
                self.player.inject_off_event(event)

                for instrument in self.track.get_instruments_to_play():
                    if not instrument.muted:

                        midi_note_on(instrument.get_midi_out(), instrument.channel, _get_note_number(event.note, instrument), velocity)

                        #msg = mido.Message(MIDO_NOTE_ON, note=_get_note_number(event.note, instrument), velocity=velocity, channel=instrument.channel-1)
                        #instrument.get_midi_out().send(msg)

        elif event.type == NOTE_OFF:

            # similar logic to the above: there is a chance we have an event tied to a chord, and we then need to silence
            # all notes in that chord separately.

            if type(event.on_event.note) == Chord:
                for x in event.on_event.note.notes:
                    evt = event.copy()
                    evt.on_event = Event(time = event.on_event.time, scale=event.scale, note = x, type=event.on_event.type, on_event=None)
                    self.play(evt)
                return

            velocity = event.note.velocity
            if velocity is None:
                velocity = self.instrument.default_velocity
            note_number = event.on_event.note.note_number()

            unregister_playing_note(self.track, event.on_event.note)

            if self.track.muted:
                return

            #print("OFF (%s): %s" % (self.on_ct, event.on_event.note))
            self.on_ct = self.on_ct - 1

            for instrument in self.track.get_instruments_to_play():
                if not instrument.muted:

                    midi_note_off(instrument.get_midi_out(), instrument.channel,  _get_note_number(event.note, instrument), velocity)

