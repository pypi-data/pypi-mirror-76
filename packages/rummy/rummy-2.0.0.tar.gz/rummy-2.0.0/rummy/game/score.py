# -*- coding: utf-8 -*-

from ansi_colours import AnsiColours as Colour

from rummy.view.round_view import RoundView


class Score:
    def __init__(self, players):
        self.players = players

    def get_current_game_scores(self):
        return ''.join(["%s: %s\n" % (p, p.get_game_score()) for p in self.players])

    def get_end_of_round_scores(self):
        output = ''
        for p in self.players:
            output += RoundView.end_of_round_scores(p)
        return output

    def update_player_scores(self):
        for p in self.players:
            p.update_score()

    def is_end_of_game(self):
        for p in self.players:
            if p.get_game_score() >= 100:
                return True
        return False

    def show_winners(self):
        winners = self.find_lowest_scores()
        if len(winners) == 1:
            return Colour.green("%s is the Winner!!" % winners[0])
        else:
            return Colour.green(", ".join([str(w) for w in winners]) + " are joint winners!")

    def find_lowest_scores(self):
        lowest = []
        for p in self.players:
            if not lowest:
                lowest = [p]
                continue
            if p.get_game_score() < lowest[0].get_game_score():
                lowest = [p]
            elif p.get_game_score() == lowest[0].get_game_score():
                lowest.append(p)
        return lowest
