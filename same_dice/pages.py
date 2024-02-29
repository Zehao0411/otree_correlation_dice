import random
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json


class Start(Page):
    form_model = 'player'
    form_fields = ['Q0_SameProb']

    def vars_for_template(self):
        if self.participant.vars['first_app_enter']:
            self.participant.vars['same_dice_first'] = True

        if self.participant.vars['same_dice_first']:
            which_part = '一'
        else:
            which_part = '二'
        return dict(
            which_part=which_part
        )

    def before_next_page(self):
        if self.participant.vars['first_app_enter']:
            self.participant.vars['same_dice_first'] = True

class Q1(Page):
    form_model = 'player'
    form_fields = ['Q1']

    def before_next_page(self):
        self.player.same_subj_responses += self.player.Q1 + ', '
        self.player.same_subj_rand_values += ', '

class Q2(Page):
    form_model = 'player'
    form_fields = ['Q2']

    def vars_for_template(self):
        if self.player.Q1 == '彩票A':
            lottery_chosen = '彩票A'
            lottery_not_chosen = '彩票B'
        elif self.player.Q1 == '彩票B':
            lottery_chosen = '彩票B'
            lottery_not_chosen = '彩票A'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        rand_num = random.choice(Constants.value_list)
        self.player.Q2_rand_num = rand_num
        payoff_high = Constants.payoff_high + rand_num
        payoff_mid = Constants.payoff_mid + rand_num
        payoff_low = Constants.payoff_low + rand_num

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
            payoff_high=payoff_high,
            payoff_mid=payoff_mid,
            payoff_low=payoff_low
        )

    def before_next_page(self):
        self.participant.vars['prev_list'] = Constants.value_list.copy()
        self.participant.vars['prev_choice'] = self.player.Q2
        self.participant.vars['prev_rand_num'] = self.player.Q2_rand_num
        self.participant.vars['Q3_counter'] = Constants.Q3_counter_init

        self.player.same_subj_responses += self.player.Q2 + ', '
        self.player.same_subj_rand_values += str(self.player.Q2_rand_num) + ', '

class Q3(Page):
    form_model = 'player'
    form_fields = ['Q3']

    def is_displayed(self):
        if self.player.Q1 == '彩票A':
            lottery_chosen = '彩票A'
            lottery_not_chosen = '彩票B'
        elif self.player.Q1 == '彩票B':
            lottery_chosen = '彩票B'
            lottery_not_chosen = '彩票A'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        prev_value_list = self.participant.vars['prev_list']
        prev_choice = self.participant.vars['prev_choice']
        prev_rand_num = self.participant.vars['prev_rand_num']
        
        if prev_choice == lottery_chosen:
            value_list = [x for x in prev_value_list if x > prev_rand_num]
        elif prev_choice == lottery_not_chosen:
            value_list = [x for x in prev_value_list if x < prev_rand_num]
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating value list.")

        exclusion_1 = self.player.Q2 == lottery_chosen and self.player.Q2_rand_num == 2
        exclusion_2 = self.player.Q2 == lottery_not_chosen and self.player.Q2_rand_num == 0.2
        end_cond = len(value_list) == 0

        return not (exclusion_1 or exclusion_2 or end_cond)

    def vars_for_template(self):
        if self.player.Q1 == '彩票A':
            lottery_chosen = '彩票A'
            lottery_not_chosen = '彩票B'
        elif self.player.Q1 == '彩票B':
            lottery_chosen = '彩票B'
            lottery_not_chosen = '彩票A'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        prev_value_list = self.participant.vars['prev_list']
        prev_choice = self.participant.vars['prev_choice']
        prev_rand_num = self.participant.vars['prev_rand_num']

        if prev_choice == lottery_chosen:
            value_list = [x for x in prev_value_list if x > prev_rand_num]
        elif prev_choice == lottery_not_chosen:
            value_list = [x for x in prev_value_list if x < prev_rand_num]
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating value list.")

        rand_num = random.choice(value_list)

        self.player.Q3_rand_num = rand_num
        payoff_high = Constants.payoff_high + rand_num
        payoff_mid = Constants.payoff_mid + rand_num
        payoff_low = Constants.payoff_low + rand_num

        Q3_counter = self.participant.vars['Q3_counter']

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
            payoff_high=payoff_high,
            payoff_mid=payoff_mid,
            payoff_low=payoff_low,
            Q3_counter=Q3_counter,
        )

    def before_next_page(self):
        if self.player.Q1 == '彩票A':
            lottery_chosen = '彩票A'
            lottery_not_chosen = '彩票B'
        elif self.player.Q1 == '彩票B':
            lottery_chosen = '彩票B'
            lottery_not_chosen = '彩票A'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        prev_value_list = self.participant.vars['prev_list']
        prev_choice = self.participant.vars['prev_choice']
        prev_rand_num = self.participant.vars['prev_rand_num']

        if prev_choice == lottery_chosen:
            value_list = [x for x in prev_value_list if x > prev_rand_num]
        elif prev_choice == lottery_not_chosen:
            value_list = [x for x in prev_value_list if x < prev_rand_num]
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating value list.")

        self.participant.vars['prev_list'] = value_list
        self.participant.vars['prev_choice'] = self.player.Q3
        self.participant.vars['prev_rand_num'] = self.player.Q3_rand_num
        self.participant.vars['Q3_counter'] += 1

        self.player.same_subj_responses += self.player.Q3 + ', '
        self.player.same_subj_rand_values += str(self.player.Q3_rand_num) + ', '


class Finish(Page):
    def vars_for_template(self):
        if self.participant.vars['same_dice_first']:
            which_part = '一'
        else:
            which_part = '二'
        return dict(
            which_part=which_part
        )

    def before_next_page(self):
        self.participant.vars['same_init_choice'] = self.player.Q1
        self.participant.vars['same_subj_responses'] = self.player.same_subj_responses
        self.participant.vars['same_subj_rand_values'] = self.player.same_subj_rand_values

        self.participant.vars['first_app_enter'] = False


page_sequence = [Start, Q1, Q2, Q3, Q3, Q3, Q3, Q3, Q3, Q3, Q3, Q3, Q3, Finish]
