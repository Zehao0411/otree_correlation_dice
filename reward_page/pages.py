import random
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class SameFirstReward(Page):
    form_model = 'player'

    def is_displayed(self):
        page_showed = self.player.page_showed
        return (not page_showed) and self.participant.vars['same_dice_first']

    def vars_for_template(self):
        if self.participant.vars['same_dice_first']:
            same_dice_first = True
            diff_dice_first = False
        elif self.participant.vars['diff_dice_first']:
            same_dice_first = False
            diff_dice_first = True
        else:
            raise ValueError('Error in determining whether same_dice app goes first.')

        ###################################################################
        # same dice app
        same_init_choice = self.participant.vars.get('same_init_choice', '')
        if same_init_choice == '彩票A':
            same_lottery_chosen = '彩票A'
            same_lottery_not_chosen = '彩票B'
        elif same_init_choice == '彩票B':
            same_lottery_chosen = '彩票B'
            same_lottery_not_chosen = '彩票A'
        else:
            raise ValueError("Wrong input in initial choice. (Reward Page)")

        same_subj_responses = self.participant.vars.get('same_subj_responses', '')
        same_subj_rand_values = self.participant.vars.get('same_subj_rand_values', '')
        # step1: split the strings
        same_subj_responses_list = same_subj_responses.split(", ")
        same_subj_rand_values_list = same_subj_rand_values.split(", ")
        # delete the last element, which is an empty string by construction
        same_subj_responses_list.pop()
        same_subj_rand_values_list.pop()
        # delete the first element, which is payoff-irrelevant by construction
        same_subj_responses_list.pop(0)
        same_subj_rand_values_list.pop(0)
        # step2: randomly draw a response
        same_selected_index = random.randint(0, len(same_subj_responses_list) - 1)
        same_selected_response = same_subj_responses_list[same_selected_index]
        same_selected_rand_value = float(same_subj_rand_values_list[same_selected_index])

        same_base_payoff = random.choice([0, 5, 10])

        same_dice_low_cond = same_base_payoff == 0
        same_dice_mid_cond = same_base_payoff == 5
        same_dice_high_cond = same_base_payoff == 10

        if same_selected_response == "彩票A":
            if same_dice_high_cond:
                same_dice_num = random.choice([1, 2])
            elif same_dice_mid_cond:
                same_dice_num = random.choice([3, 4])
            elif same_dice_low_cond:
                same_dice_num = random.choice([5, 6])
            else:
                raise ValueError("Error in determining same dice number. (inside if-sentence)")
        elif same_selected_response == "彩票B":
            if same_dice_high_cond:
                same_dice_num = random.choice([3, 4])
            elif same_dice_mid_cond:
                same_dice_num = random.choice([5, 6])
            elif same_dice_low_cond:
                same_dice_num = random.choice([1, 2])
            else:
                raise ValueError("Error in determining same dice number. (inside if-sentence)")
        else:
            raise ValueError("Error in determining same dice number. (outside if-sentence)")

        if same_selected_response == same_init_choice:
            same_final_payoff = same_base_payoff
        else:
            same_final_payoff = same_base_payoff + same_selected_rand_value

        same_payoff_high = Constants.payoff_high + same_selected_rand_value
        same_payoff_mid = Constants.payoff_mid + same_selected_rand_value
        same_payoff_low = Constants.payoff_low + same_selected_rand_value

        ###################################################################
        # diff dice app
        diff_subj_treatment = self.participant.vars.get('diff_subj_treatment', '')

        diff_init_choice = self.participant.vars.get('diff_init_choice', '')
        if diff_init_choice == '彩票C':
            diff_lottery_chosen = '彩票C'
            diff_lottery_not_chosen = '彩票D'
        elif diff_init_choice == '彩票D':
            diff_lottery_chosen = '彩票D'
            diff_lottery_not_chosen = '彩票C'
        else:
            raise ValueError("Wrong input in initial choice. (Reward Page)")

        diff_subj_responses = self.participant.vars.get('diff_subj_responses', '')
        diff_subj_rand_values = self.participant.vars.get('diff_subj_rand_values', '')
        # step1: split the strings
        diff_subj_responses_list = diff_subj_responses.split(", ")
        diff_subj_rand_values_list = diff_subj_rand_values.split(", ")
        # delete the last element, which is an empty string by construction
        diff_subj_responses_list.pop()
        diff_subj_rand_values_list.pop()
        # delete the first element, which is payoff-irrelevant by construction
        diff_subj_responses_list.pop(0)
        diff_subj_rand_values_list.pop(0)
        # step2: randomly draw a response
        diff_selected_index = random.randint(0, len(diff_subj_responses_list) - 1)
        diff_selected_response = diff_subj_responses_list[diff_selected_index]
        diff_selected_rand_value = float(diff_subj_rand_values_list[diff_selected_index])

        diff_red_payoff = random.choice([2, 8])
        diff_blue_payoff = random.choice([0, 10])

        if diff_red_payoff == 2:
            diff_red_dice_num = random.choice([1, 2, 3])
        elif diff_red_payoff == 8:
            diff_red_dice_num = random.choice([4, 5, 6])
        else:
            raise ValueError("Error in determining the red dice number.")

        if diff_blue_payoff == 0:
            diff_blue_dice_num = random.choice([1, 2, 3])
        elif diff_blue_payoff == 10:
            diff_blue_dice_num = random.choice([4, 5, 6])
        else:
            raise ValueError("Error in determining the blue dice number.")

        if diff_init_choice == '彩票C':
            diff_dice_payoff = diff_red_payoff
        elif diff_init_choice == '彩票D':
            diff_dice_payoff = diff_blue_payoff
        else:
            raise ValueError("Wrong input in calculating dice payoff for the diff dice app.")

        if diff_selected_response == '愿意':
            diff_final_payoff = diff_dice_payoff - diff_selected_rand_value
        elif diff_selected_response == '不愿意':
            diff_final_payoff = diff_dice_payoff
        else:
            raise ValueError("Wrong input in calculating dice payoff for the diff dice app.")

        ###################################################################
        # total final payoff
        total_final_payoff = round(10 + same_final_payoff + diff_final_payoff, 1)

        ###################################################################
        # record values
        self.player.same_dice_first = same_dice_first
        self.player.diff_dice_first = diff_dice_first

        self.player.same_selected_response = same_selected_response
        self.player.same_selected_rand_value = same_selected_rand_value
        self.player.same_final_payoff = same_final_payoff

        self.player.diff_selected_response = diff_selected_response
        self.player.diff_selected_rand_value = diff_selected_rand_value
        self.player.diff_red_payoff = diff_red_payoff
        self.player.diff_blue_payoff = diff_blue_payoff
        self.player.diff_final_payoff = diff_final_payoff

        self.player.total_final_payoff = total_final_payoff

        self.player.page_showed = True

        return dict(
            same_dice_first=same_dice_first,
            diff_dice_first=diff_dice_first,

            same_lottery_chosen=same_lottery_chosen,
            same_lottery_not_chosen=same_lottery_not_chosen,
            same_selected_response=same_selected_response,
            same_selected_rand_value=same_selected_rand_value,
            same_final_payoff=same_final_payoff,
            same_payoff_high=same_payoff_high,
            same_payoff_mid=same_payoff_mid,
            same_payoff_low=same_payoff_low,
            same_dice_num=same_dice_num,

            diff_subj_treatment=diff_subj_treatment,
            diff_lottery_chosen=diff_lottery_chosen,
            diff_lottery_not_chosen=diff_lottery_not_chosen,
            diff_selected_response=diff_selected_response,
            diff_selected_rand_value=diff_selected_rand_value,
            diff_red_payoff=diff_red_payoff,
            diff_blue_payoff=diff_blue_payoff,
            diff_red_dice_num=diff_red_dice_num,
            diff_blue_dice_num=diff_blue_dice_num,
            diff_final_payoff=diff_final_payoff,

            total_final_payoff=total_final_payoff,
        )


class DiffFirstReward(Page):
    form_model = 'player'

    def is_displayed(self):
        page_showed = self.player.page_showed
        return (not page_showed) and self.participant.vars['diff_dice_first']

    def vars_for_template(self):
        if self.participant.vars['same_dice_first']:
            same_dice_first = True
            diff_dice_first = False
        elif self.participant.vars['diff_dice_first']:
            same_dice_first = False
            diff_dice_first = True
        else:
            raise ValueError('Error in determining whether same_dice app goes first.')

        ###################################################################
        # same dice app
        same_init_choice = self.participant.vars.get('same_init_choice', '')
        if same_init_choice == '彩票A':
            same_lottery_chosen = '彩票A'
            same_lottery_not_chosen = '彩票B'
        elif same_init_choice == '彩票B':
            same_lottery_chosen = '彩票B'
            same_lottery_not_chosen = '彩票A'
        else:
            raise ValueError("Wrong input in initial choice. (Reward Page)")

        same_subj_responses = self.participant.vars.get('same_subj_responses', '')
        same_subj_rand_values = self.participant.vars.get('same_subj_rand_values', '')
        # step1: split the strings
        same_subj_responses_list = same_subj_responses.split(", ")
        same_subj_rand_values_list = same_subj_rand_values.split(", ")
        # delete the last element, which is an empty string by construction
        same_subj_responses_list.pop()
        same_subj_rand_values_list.pop()
        # delete the first element, which is payoff-irrelevant by construction
        same_subj_responses_list.pop(0)
        same_subj_rand_values_list.pop(0)
        # step2: randomly draw a response
        same_selected_index = random.randint(0, len(same_subj_responses_list) - 1)
        same_selected_response = same_subj_responses_list[same_selected_index]
        same_selected_rand_value = float(same_subj_rand_values_list[same_selected_index])

        same_base_payoff = random.choice([0, 5, 10])

        same_dice_low_cond = same_base_payoff == 0
        same_dice_mid_cond = same_base_payoff == 5
        same_dice_high_cond = same_base_payoff == 10

        if same_selected_response == "彩票A":
            if same_dice_high_cond:
                same_dice_num = random.choice([1, 2])
            elif same_dice_mid_cond:
                same_dice_num = random.choice([3, 4])
            elif same_dice_low_cond:
                same_dice_num = random.choice([5, 6])
            else:
                raise ValueError("Error in determining same dice number. (inside if-sentence)")
        elif same_selected_response == "彩票B":
            if same_dice_high_cond:
                same_dice_num = random.choice([3, 4])
            elif same_dice_mid_cond:
                same_dice_num = random.choice([5, 6])
            elif same_dice_low_cond:
                same_dice_num = random.choice([1, 2])
            else:
                raise ValueError("Error in determining same dice number. (inside if-sentence)")
        else:
            raise ValueError("Error in determining same dice number. (outside if-sentence)")

        if same_selected_response == same_init_choice:
            same_final_payoff = same_base_payoff
        else:
            same_final_payoff = same_base_payoff + same_selected_rand_value

        same_payoff_high = Constants.payoff_high + same_selected_rand_value
        same_payoff_mid = Constants.payoff_mid + same_selected_rand_value
        same_payoff_low = Constants.payoff_low + same_selected_rand_value

        ###################################################################
        # diff dice app
        diff_subj_treatment = self.participant.vars.get('diff_subj_treatment', '')

        diff_init_choice = self.participant.vars.get('diff_init_choice', '')
        if diff_init_choice == '彩票C':
            diff_lottery_chosen = '彩票C'
            diff_lottery_not_chosen = '彩票D'
        elif diff_init_choice == '彩票D':
            diff_lottery_chosen = '彩票D'
            diff_lottery_not_chosen = '彩票C'
        else:
            raise ValueError("Wrong input in initial choice. (Reward Page)")

        diff_subj_responses = self.participant.vars.get('diff_subj_responses', '')
        diff_subj_rand_values = self.participant.vars.get('diff_subj_rand_values', '')
        # step1: split the strings
        diff_subj_responses_list = diff_subj_responses.split(", ")
        diff_subj_rand_values_list = diff_subj_rand_values.split(", ")
        # delete the last element, which is an empty string by construction
        diff_subj_responses_list.pop()
        diff_subj_rand_values_list.pop()
        # delete the first element, which is payoff-irrelevant by construction
        diff_subj_responses_list.pop(0)
        diff_subj_rand_values_list.pop(0)
        # step2: randomly draw a response
        diff_selected_index = random.randint(0, len(diff_subj_responses_list) - 1)
        diff_selected_response = diff_subj_responses_list[diff_selected_index]
        diff_selected_rand_value = float(diff_subj_rand_values_list[diff_selected_index])

        diff_red_payoff = random.choice([2, 8])
        diff_blue_payoff = random.choice([0, 10])

        if diff_red_payoff == 2:
            diff_red_dice_num = random.choice([1, 2, 3])
        elif diff_red_payoff == 8:
            diff_red_dice_num = random.choice([4, 5, 6])
        else:
            raise ValueError("Error in determining the red dice number.")

        if diff_blue_payoff == 0:
            diff_blue_dice_num = random.choice([1, 2, 3])
        elif diff_blue_payoff == 10:
            diff_blue_dice_num = random.choice([4, 5, 6])
        else:
            raise ValueError("Error in determining the blue dice number.")

        if diff_init_choice == '彩票C':
            diff_dice_payoff = diff_red_payoff
        elif diff_init_choice == '彩票D':
            diff_dice_payoff = diff_blue_payoff
        else:
            raise ValueError("Wrong input in calculating dice payoff for the diff dice app.")

        if diff_selected_response == '愿意':
            diff_final_payoff = diff_dice_payoff - diff_selected_rand_value
        elif diff_selected_response == '不愿意':
            diff_final_payoff = diff_dice_payoff
        else:
            raise ValueError("Wrong input in calculating dice payoff for the diff dice app.")

        ###################################################################
        # total final payoff
        total_final_payoff = round(10 + same_final_payoff + diff_final_payoff, 1)

        ###################################################################
        # record values
        self.player.same_dice_first = same_dice_first
        self.player.diff_dice_first = diff_dice_first

        self.player.same_selected_response = same_selected_response
        self.player.same_selected_rand_value = same_selected_rand_value
        self.player.same_final_payoff = same_final_payoff

        self.player.diff_selected_response = diff_selected_response
        self.player.diff_selected_rand_value = diff_selected_rand_value
        self.player.diff_red_payoff = diff_red_payoff
        self.player.diff_blue_payoff = diff_blue_payoff
        self.player.diff_final_payoff = diff_final_payoff

        self.player.total_final_payoff = total_final_payoff

        self.player.page_showed = True

        return dict(
            same_dice_first=same_dice_first,
            diff_dice_first=diff_dice_first,

            same_lottery_chosen=same_lottery_chosen,
            same_lottery_not_chosen=same_lottery_not_chosen,
            same_selected_response=same_selected_response,
            same_selected_rand_value=same_selected_rand_value,
            same_final_payoff=same_final_payoff,
            same_payoff_high=same_payoff_high,
            same_payoff_mid=same_payoff_mid,
            same_payoff_low=same_payoff_low,
            same_dice_num=same_dice_num,

            diff_subj_treatment=diff_subj_treatment,
            diff_lottery_chosen=diff_lottery_chosen,
            diff_lottery_not_chosen=diff_lottery_not_chosen,
            diff_selected_response=diff_selected_response,
            diff_selected_rand_value=diff_selected_rand_value,
            diff_red_payoff=diff_red_payoff,
            diff_blue_payoff=diff_blue_payoff,
            diff_red_dice_num=diff_red_dice_num,
            diff_blue_dice_num=diff_blue_dice_num,
            diff_final_payoff=diff_final_payoff,

            total_final_payoff=total_final_payoff,
        )


class PageIfSubjectRefresh(Page):
    form_model = 'player'

page_sequence = [SameFirstReward, DiffFirstReward, PageIfSubjectRefresh]
