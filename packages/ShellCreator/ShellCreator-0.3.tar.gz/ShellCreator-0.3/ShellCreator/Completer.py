#!/usr/bin/python3

from prompt_toolkit.completion import Completer, Completion

class TabCompleter(Completer):
    index = 0
    def get_completions(self, document, complete_event):
        self.index += 4
        yield Completion(' '*self.index, start_position=4-self.index, display='')
