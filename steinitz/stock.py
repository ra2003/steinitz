from untwisted.network import spawn
from untwisted.event import get_event
from untwisted.splits import Terminator
from re import compile, search, DOTALL

PATTERN_STR =  'bestmove (?P<move>[^\n ]+)'
PATTERN_RE  = compile(PATTERN_STR, DOTALL)
BESTMOVE    = get_event()

class Stockfish:
    def __init__(self, expect):
        self.expect = expect

        Terminator(expect, delim=b'\n')
        expect.add_map(Terminator.FOUND, self.tokenize)
        expect.send_cmd = self.send_cmd

    def send_cmd(self, data):
        cmd = data.encode('utf-8')
        self.expect.send(cmd)

    def tokenize(self, expect, data):
        data  = data.decode('utf-8')
        regex = search(PATTERN_RE, data) 

        if regex: 
            spawn(expect, BESTMOVE, regex.group('move'))
    



