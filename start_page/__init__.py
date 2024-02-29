from otree.api import *
import random

c = cu

doc = 'Author: Zehao Zhang and Liu Xing'


# def randomize_app_sequence():
#     app_sequence = ['same_dice', 'diff_dice']
#     random.shuffle(app_sequence)
#     return app_sequence


class C(BaseConstants):
    NAME_IN_URL = 'start_page'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    first_app_enter = models.BooleanField(initial=False)


class Start(Page):
    form_model = 'player'

    def before_next_page(self, timeout_happened):
        self.participant.vars['first_app_enter'] = True
        self.participant.vars['same_dice_first'] = False
        self.participant.vars['diff_dice_first'] = False


page_sequence = [Start]
