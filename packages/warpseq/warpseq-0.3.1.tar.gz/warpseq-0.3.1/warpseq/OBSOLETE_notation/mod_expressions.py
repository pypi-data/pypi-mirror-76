# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this file contains the implementation of all Mod Expression symbols.

from ..model.registers import get_first_playing_note
from .mod_util import *
from warpseq.api.exceptions import *

# ----------------------------------------------------------------------------------------------------------------------
# SPECIAL (these do not take parameters)

def silence(parser, input):
    return None

def sharp(parser, input):
    return input.transpose(semitones=1)

def flat(parser, input):
    return input.transpose(semitones=-1)

def same(parser, input):
    return input.copy()

# ----------------------------------------------------------------------------------------------------------------------
# IGNORE EXPRESSIONS (used for defer events in non-deferral mode)

def expr_ignore(parser, input, how, extra_info):
    return input.copy()

# ----------------------------------------------------------------------------------------------------------------------

def reset(parser, input):
    parser.pattern.reset()
    return input.copy()

def reverse(parser, input):
    parser.pattern.reverse()
    return input.copy()

def shuffle(parser, input):
    parser.pattern.shuffle()
    return input.copy()

# ----------------------------------------------------------------------------------------------------------------------
# OCTAVES

def expr_octave_up(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    res = input.transpose(octaves=how)
    return res

def expr_octave_down(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    res = input.transpose(octaves=-how)
    return res

def expr_octave_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    res = input.with_octave(how)
    return res

# ----------------------------------------------------------------------------------------------------------------------

def expr_invert_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    res = input.invert(how)
    return res

# ----------------------------------------------------------------------------------------------------------------------
# REPEATS

def expr_repeat_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    res = input.with_repeat(how)
    return res

# ----------------------------------------------------------------------------------------------------------------------
# SKIPS

def expr_skip_set(parser, input, how, extra_info):

    from warpseq.model.chord import Chord
    from warpseq.model.note import Note

    how = evaluate_params(parser, how, want_int=True)
    pattern = parser.pattern
    note_parser = input.get_parser()

    res = input

    for _ in range(0, how):
        sym = pattern.get_next()
        octave_shift = pattern.get_octave_shift(parser.track)
        res = note_parser.do(sym, octave_shift)
        #print("RES=%s" % res)

    if type(res) == Note:
        res = [ res ]

    return Chord(notes=res, from_scale=input.from_scale)


# ----------------------------------------------------------------------------------------------------------------------
# SCALE NOTES

def expr_scale_note_up(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    return input.scale_transpose(parser.scale, how)


def expr_scale_note_down(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    return input.scale_transpose(parser.scale, -how)

# ----------------------------------------------------------------------------------------------------------------------
# SCALE DEGREES

def expr_degree_up(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    return input.transpose(degrees=how)

def expr_degree_down(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    return input.transpose(degrees=-how)

# ----------------------------------------------------------------------------------------------------------------------
# VELOCITY

def expr_velocity_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    return input.with_velocity(how)

# ----------------------------------------------------------------------------------------------------------------------
# LENGTH AND DELAY

def expr_length_mod_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_float=True)
    return input.with_length_mod(how)

def expr_delay_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_float=True)
    return input.with_delay(how)

def expr_rush_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_float=True)
    return input.with_delay(-how)

# ----------------------------------------------------------------------------------------------------------------------
# CCs

def expr_cc_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_int=True)
    return input.with_cc(extra_info, how)

# ----------------------------------------------------------------------------------------------------------------------
# VARIABLES

def expr_variable_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_string=True)
    set_variable(extra_info, how)
    return input

# ----------------------------------------------------------------------------------------------------------------------
# CHORDS

def expr_chord_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_string=True)
    return input.chordify(how)

# ----------------------------------------------------------------------------------------------------------------------
# TRACK MOVE & COPY

def expr_track_copy(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_string=True)
    pattern = parser.song.find_track_by_name(how)
    if pattern is None:
        raise InvalidExpression("no such track to move note to: %s" % how)
    res = input.with_track_copy(pattern)
    return res

# ----------------------------------------------------------------------------------------------------------------------
# INTRA-TRACK EVENTS

def expr_track_grab(parser, input, how, extra_info):

    how = evaluate_params(parser, how, want_string=True)

    track = parser.song.find_track_by_name(how)
    my_track = parser.track
    playing = get_first_playing_note(track.name)

    if playing is None:
        print("NO PLAYING")
        return None

    copy_tracks = playing.track_copy
    if copy_tracks:
        if my_track not in copy_tracks:
            print("NO COPY")
            return None

    res = input.replace_with_note(playing.name, playing.octave)
    return res

# ----------------------------------------------------------------------------------------------------------------------
# NOTE REPLACEMENT

def expr_note_set(parser, input, how, extra_info):


    from warpseq.model.chord import Chord
    from warpseq.model.note import Note

    #song = parser.song
    note_parser = input.get_parser()
    how = evaluate_params(parser, how, want_string=True)


    pattern = parser.pattern
    octave_shift = pattern.get_octave_shift(parser.track)
    result = note_parser.do(how, octave_shift)
    # the result will be a list of notes, so we must return a Chord

    # FIXME: repeating code with skip_set above

    if type(result) == Note:
        result = [ res ]

    return Chord(notes=result, from_scale=input.from_scale)


# ----------------------------------------------------------------------------------------------------------------------    
# PROBABILITY    

def expr_probability_set(parser, input, how, extra_info):
    how = evaluate_params(parser, how, want_string=True)
    how = float(how)
    rn = random.random()

    # example: p=0.1
    #
    # event should only happen in 1 in 10 times
    # random number chosen is 0.9
    # rn is higher than the threshold
    # the event should NOT happen
    #
    # random number chosen is 0.02
    # rn is LOWER than the threshold
    # the event should happen

    if rn > how:
        parser.execute_next = False
    return input
