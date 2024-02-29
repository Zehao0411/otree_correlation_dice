from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import json

doc = 'Author: Zehao Zhang and Liu Xing'


class Constants(BaseConstants):
    name_in_url = 'same_dice'
    players_per_group = None
    num_rounds = 1

    payoff_high = 10
    payoff_mid = 5
    payoff_low = 0

    value_list = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    Q3_counter_init = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Q2_rand_num = models.FloatField()
    Q3_rand_num = models.FloatField()
    same_subj_responses = models.StringField(initial='')
    same_subj_rand_values = models.StringField(initial='')

    Q0_SameProb = models.StringField(
        choices=['正确', '错误'],
        label='''
            每支彩票都有相同的几率为您赢得10元、5元和0元。''',
        widget=widgets.RadioSelectHorizontal()
    )

    Q1 = models.StringField(
        choices=['彩票A', '彩票B'],
        label='''
            请问对于上述两支彩票，您希望拥有哪支？''',
        widget=widgets.RadioSelect()
    )

    Q2 = models.StringField(
        choices=['彩票A', '彩票B'],
        label='''
            请问对于上述两支彩票, 您希望拥有哪支? ''',
        widget=widgets.RadioSelect()
    )

    Q3 = models.StringField(
        choices=['彩票A', '彩票B'],
        label='''
            请问对于上述两支彩票, 您希望拥有哪支? ''',
        widget=widgets.RadioSelect()
    )

