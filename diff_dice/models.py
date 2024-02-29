import random
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

doc = 'Author: Zehao Zhang and Liu Xing'


def gen_which_treatment():
    return random.random()


class Constants(BaseConstants):
    name_in_url = 'diff_dice'
    players_per_group = None
    num_rounds = 1
    num_groups = 4

    treatments = ['A', 'B', 'C', 'D']

    payoff_high = 10
    payoff_mid = 5
    payoff_low = 0

    value_list = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]

    Q2A_counter_init = 2
    Q2B_counter_init = 2
    Q2C_counter_init = 2
    Q2D_counter_init = 2


class Subsession(BaseSubsession):
    def creating_session(self):
        randomized_treatments = Constants.treatments.copy()
        random.shuffle(randomized_treatments)

        for player in self.get_players():
            if player.id_in_group % 4 == 0:
                player.treatment = randomized_treatments[0]
            elif player.id_in_group % 4 == 1:
                player.treatment = randomized_treatments[1]
            elif player.id_in_group % 4 == 2:
                player.treatment = randomized_treatments[2]
            elif player.id_in_group % 4 == 3:
                player.treatment = randomized_treatments[3]
            else:
                raise ValueError("Error in assigning treatment")


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()

    diff_subj_responses = models.StringField(initial='')
    diff_subj_rand_values = models.StringField(initial='')

    Q1A_rand_num = models.FloatField()
    Q2A_rand_num = models.FloatField()
    Q1B_rand_num = models.FloatField()
    Q2B_rand_num = models.FloatField()
    Q1C_rand_num = models.FloatField()
    Q2C_rand_num = models.FloatField()
    Q1D_rand_num = models.FloatField()
    Q2D_rand_num = models.FloatField()

    Q0_WhichDice = models.StringField(
        choices=['彩票C', '彩票D'],
        label='''
            请问对于上述两支彩票, 您希望拥有哪支?''',
        widget=widgets.RadioSelect()
    )

    Q1A = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Q2A = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Q1B = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Q2B = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Q1C = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Q2C = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Q1D = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Q2D = models.StringField(
        choices=['愿意', '不愿意'],
        label='''
            您的选择是？''',
        widget=widgets.RadioSelect()
    )

    Finish = models.StringField(
        label='''
            请问您在做出上述选择时都有哪些考虑 (选填)？''',
        blank=True
    )
