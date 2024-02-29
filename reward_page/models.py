from otree.api import *
import random

c = cu

doc = 'Author: Zehao Zhang'


class Constants(BaseConstants):
    name_in_url = 'reward_page'
    players_per_group = None
    num_rounds = 1

    payoff_high = 10
    payoff_mid = 5
    payoff_low = 0


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    page_showed = models.BooleanField(initial=False)

    same_dice_first = models.BooleanField()
    diff_dice_first = models.BooleanField()

    same_selected_response = models.StringField()
    same_selected_rand_value = models.FloatField()
    same_final_payoff = models.FloatField()

    diff_selected_response = models.StringField()
    diff_selected_rand_value = models.FloatField()
    diff_red_payoff = models.IntegerField()
    diff_blue_payoff = models.IntegerField()
    diff_final_payoff = models.FloatField()

    total_final_payoff = models.FloatField()


