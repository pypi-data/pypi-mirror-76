from random import choice

from rummy.controller.player_controller import PlayerController
from rummy.player.player import Player
from rummy.ui.view import View
from rummy.view.ai_view import AiView


class AiController(PlayerController):

    @staticmethod
    def show_start_turn(player: Player):
        output = ''
        if player.ai_only:
            output += AiView.turn_start(player)
        else:
            output += AiView.turn_start(player)
        output += AiView.thinking(player, 'Choosing pick up')
        View.render(output)

    @staticmethod
    def show_end_turn(player: Player):
        output = ''
        if player.ai_only:
            output += AiView.turn_end(player)
        output += AiView.thinking(player, 'Choosing card to discard')
        View.render(output)

    @staticmethod
    def show_knocked(player):
        if player.has_someone_knocked():
            View.render(AiView.knocked())

    @staticmethod
    def show_discard(player: Player):
        output = ''
        if player.ai_only:
            output += AiView.hand_data(player.hand.get_score())
        output += AiView.discarded(player.round.deck.inspect_discard())
        View.render(output)

    @classmethod
    def draw_card(cls, player):
        output = ''
        if player.round.deck.has_discard():
            current_score = player.hand.get_score()
            scores = player.melds.find_discard_scores(player.hand.get_hand(), player.round.deck.inspect_discard())
            if player.ai_only:
                output += AiView.discard_data(current_score, scores)
            output += cls._choose_pickup(player, current_score, scores)
        else:
            player.take_from_deck()
            output += AiView.thinking(player, 'Drawing from deck')
        View.render(output)

    @staticmethod
    def _choose_pickup(player, current_score, scores):
        output = ''
        if min(scores) < current_score - 4 or min(scores) <= 10:
            player.take_from_discard()
            output += AiView.thinking(player, 'Drawing from discard')
        else:
            player.take_from_deck()
            output += AiView.thinking(player, 'Drawing from deck')
        return output

    @classmethod
    def discard_or_knock(cls, player):
        scores = player.melds.find_discard_scores(player.hand.get_hand())
        score = min(scores)
        if score <= 10 and not player.round.knocked:
            player.round.knocked = True
        discard = cls._choose_discard(player, score, scores)
        player.round.deck.discard_card(discard)

    @staticmethod
    def _choose_discard(player, score, scores):
        if scores.count(score) > 1:
            choices = [(i, x) for (i, x) in enumerate(scores) if (x == score)]
            discard = choice(choices)[0]
        else:
            discard = scores.index(score)
        return player.hand.discard_card(discard)
