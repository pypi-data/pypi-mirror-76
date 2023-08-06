# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# This is the class that evaluates mod expressions to return output.

from ..model.registers import get_first_playing_note
from .mod_parser import is_deferred_expr, process_expr
from warpseq.api.exceptions import *
from warpseq.utils import utils

class ModExpression(object):

    __slots__ = [ 'defer', 'execute_next', 'scale', 'track', 'song', 'pattern' ]

    def __init__(self, song=None, scale=None, track=None, defer=False, pattern=None):

        self.song = song
        self.defer = defer
        self.execute_next = True
        self.scale = scale
        self.track = track
        self.pattern = pattern

    def do(self, note, expressions):

        expressions = utils.ensure_string_list(expressions)

        input_note = note.copy()

        if not self.defer:

            # decide if we need to recompute the note again at play time because it includes intra-track events
            has_deferred = False
            for expr in expressions:
                if is_deferred_expr(expr):
                    has_deferred = True
                    break

            # if we do have intra-track events, we record them on the note for replay later
            if has_deferred:
                input_note.deferred = True
                input_note.deferred_expressions = expressions
                return input_note

        # execute next is a boolean toggled by probability events
        self.execute_next = True

        expr_index = 0

        for expr in expressions:

            expr_index = expr_index + 1

            # if false, execute next ignores the NEXT event and then toggles back on.
            if self.execute_next == False:
                self.execute_next = True
                continue

            # we might need to process deferred events depending on where this class is invoked
            if self.defer:
                input_note = process_expr(self, input_note, expr, deferred=True)
                if input_note is None:
                    return input_note

            # we ALWAYS need to process non-deferred events
            try:
                input_note = process_expr(self, input_note, expr, deferred=False)
            except InvalidNote:
                traceback.print_exc()
                # went way below -5 octaves in mod expression calculation current implementation doesn't allow you to add
                # that many octaves back
                input_note = None

            if input_note is None:
                return input_note

        from ..model.note import Note

        if type(input_note) == Note:
            input_note.from_scale = self.scale
        else:
            # Chord
            for x in input_note.notes:
                x.from_scale = x

        return input_note
