import random
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Start(Page):
    form_model = 'player'
    form_fields = ['Q0_WhichDice']

    def vars_for_template(self):
        if self.participant.vars['first_app_enter']:
            self.participant.vars['diff_dice_first'] = True

        if self.participant.vars['diff_dice_first']:
            which_part = '一'
        else:
            which_part = '二'

        return dict(
            which_part=which_part
        )

    def before_next_page(self):
        self.player.diff_subj_responses += self.player.Q0_WhichDice + ', '
        self.player.diff_subj_rand_values += ', '

class StartA(Page):
    def is_displayed(self):
        treat_A_cond = self.player.treatment == 'A'
        return treat_A_cond
        
    def vars_for_template(self):
        if self.player.Q0_WhichDice == '彩票C':
            lottery_chosen = '彩票C'
            lottery_not_chosen = '彩票D'
        elif self.player.Q0_WhichDice == '彩票D':
            lottery_chosen = '彩票D'
            lottery_not_chosen = '彩票C'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        if self.participant.vars['diff_dice_first']:
            which_part = '一'
        else:
            which_part = '二'

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            which_part=which_part,
        )


class Q1A(Page):
    form_model = 'player'
    form_fields = ['Q1A']

    def is_displayed(self):
        treat_A_cond = self.player.treatment == 'A'
        return treat_A_cond

    def vars_for_template(self):
        treat_A_cond = self.player.treatment == 'A'

        if self.player.Q0_WhichDice == '彩票C':
            lottery_chosen = '彩票C'
            lottery_not_chosen = '彩票D'
        elif self.player.Q0_WhichDice == '彩票D':
            lottery_chosen = '彩票D'
            lottery_not_chosen = '彩票C'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        rand_num = random.choice(Constants.value_list)

        if treat_A_cond:
            self.player.Q1A_rand_num = rand_num

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
        )

    def before_next_page(self):
        treat_A_cond = self.player.treatment == 'A'
        if treat_A_cond:
            self.participant.vars['prev_list'] = Constants.value_list.copy()
            self.participant.vars['prev_choice'] = self.player.Q1A
            self.participant.vars['prev_rand_num'] = self.player.Q1A_rand_num
            self.participant.vars['Q2A_counter'] = Constants.Q2A_counter_init

            self.player.diff_subj_responses += self.player.Q1A + ', '
            self.player.diff_subj_rand_values += str(self.player.Q1A_rand_num) + ', '


class Q2A(Page):
    form_model = 'player'
    form_fields = ['Q2A']

    def is_displayed(self):
        treat_A_cond = self.player.treatment == 'A'
        exclusion_1 = False
        exclusion_2 = False
        end_cond = False

        if treat_A_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']
            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            exclusion_1 = self.player.Q1A == '愿意' and self.player.Q1A_rand_num == 2
            exclusion_2 = self.player.Q1A == '不愿意' and self.player.Q1A_rand_num == 0.2
            end_cond = len(value_list) == 0

        return (not (exclusion_1 or exclusion_2 or end_cond)) and treat_A_cond

    def vars_for_template(self):
        treat_A_cond = self.player.treatment == 'A'

        if treat_A_cond:
            if self.player.Q0_WhichDice == '彩票C':
                lottery_chosen = '彩票C'
                lottery_not_chosen = '彩票D'
            elif self.player.Q0_WhichDice == '彩票D':
                lottery_chosen = '彩票D'
                lottery_not_chosen = '彩票C'
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            rand_num = random.choice(value_list)
            self.player.Q2A_rand_num = rand_num
            Q2A_counter = self.participant.vars['Q2A_counter']

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
            Q2A_counter=Q2A_counter,
        )

    def before_next_page(self):
        treat_A_cond = self.player.treatment == 'A'

        if treat_A_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            self.participant.vars['prev_list'] = value_list
            self.participant.vars['prev_choice'] = self.player.Q2A
            self.participant.vars['prev_rand_num'] = self.player.Q2A_rand_num
            self.participant.vars['Q2A_counter'] += 1

            self.player.diff_subj_responses += self.player.Q2A + ', '
            self.player.diff_subj_rand_values += str(self.player.Q2A_rand_num) + ', '


class StartB(Page):
    def is_displayed(self):
        treat_B_cond = self.player.treatment == 'B'
        return treat_B_cond
    
    def vars_for_template(self):
        if self.player.Q0_WhichDice == '彩票C':
            lottery_chosen = '彩票C'
            lottery_not_chosen = '彩票D'
        elif self.player.Q0_WhichDice == '彩票D':
            lottery_chosen = '彩票D'
            lottery_not_chosen = '彩票C'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        if self.participant.vars['diff_dice_first']:
            which_part = '一'
        else:
            which_part = '二'

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            which_part=which_part,
        )


class Q1B(Page):
    form_model = 'player'
    form_fields = ['Q1B']

    def is_displayed(self):
        treat_B_cond = self.player.treatment == 'B'
        return treat_B_cond

    def vars_for_template(self):
        treat_B_cond = self.player.treatment == 'B'

        if treat_B_cond:
            if self.player.Q0_WhichDice == '彩票C':
                lottery_chosen = '彩票C'
                lottery_not_chosen = '彩票D'
            elif self.player.Q0_WhichDice == '彩票D':
                lottery_chosen = '彩票D'
                lottery_not_chosen = '彩票C'
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

            rand_num = random.choice(Constants.value_list)
            self.player.Q1B_rand_num = rand_num

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
        )

    def before_next_page(self):
        treat_B_cond = self.player.treatment == 'B'

        if treat_B_cond:
            self.participant.vars['prev_list'] = Constants.value_list.copy()
            self.participant.vars['prev_choice'] = self.player.Q1B
            self.participant.vars['prev_rand_num'] = self.player.Q1B_rand_num
            self.participant.vars['Q2B_counter'] = Constants.Q2B_counter_init

            self.player.diff_subj_responses += self.player.Q1B + ', '
            self.player.diff_subj_rand_values += str(self.player.Q1B_rand_num) + ', '


class Q2B(Page):
    form_model = 'player'
    form_fields = ['Q2B']

    def is_displayed(self):
        treat_B_cond = self.player.treatment == 'B'
        exclusion_1 = False
        exclusion_2 = False
        end_cond = False

        if treat_B_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']
            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            exclusion_1 = self.player.Q1B == '愿意' and self.player.Q1B_rand_num == 2
            exclusion_2 = self.player.Q1B == '不愿意' and self.player.Q1B_rand_num == 0.2
            end_cond = len(value_list) == 0

        return (not (exclusion_1 or exclusion_2 or end_cond)) and treat_B_cond

    def vars_for_template(self):
        treat_B_cond = self.player.treatment == 'B'

        if treat_B_cond:
            if self.player.Q0_WhichDice == '彩票C':
                lottery_chosen = '彩票C'
                lottery_not_chosen = '彩票D'
            elif self.player.Q0_WhichDice == '彩票D':
                lottery_chosen = '彩票D'
                lottery_not_chosen = '彩票C'
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            rand_num = random.choice(value_list)
            self.player.Q2B_rand_num = rand_num
            Q2B_counter = self.participant.vars['Q2B_counter']

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
            Q2B_counter=Q2B_counter,
        )

    def before_next_page(self):
        treat_B_cond = self.player.treatment == 'B'

        if treat_B_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            self.participant.vars['prev_list'] = value_list
            self.participant.vars['prev_choice'] = self.player.Q2B
            self.participant.vars['prev_rand_num'] = self.player.Q2B_rand_num
            self.participant.vars['Q2B_counter'] += 1

            self.player.diff_subj_responses += self.player.Q2B + ', '
            self.player.diff_subj_rand_values += str(self.player.Q2B_rand_num) + ', '

class StartC(Page):
    def is_displayed(self):
        treat_C_cond = self.player.treatment == 'C'
        return treat_C_cond

    def vars_for_template(self):
        if self.player.Q0_WhichDice == '彩票C':
            lottery_chosen = '彩票C'
            lottery_not_chosen = '彩票D'
        elif self.player.Q0_WhichDice == '彩票D':
            lottery_chosen = '彩票D'
            lottery_not_chosen = '彩票C'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        if self.participant.vars['diff_dice_first']:
            which_part = '一'
        else:
            which_part = '二'

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            which_part=which_part,
        )


class Q1C(Page):
    form_model = 'player'
    form_fields = ['Q1C']

    def is_displayed(self):
        treat_C_cond = self.player.treatment == 'C'
        return treat_C_cond

    def vars_for_template(self):
        treat_C_cond = self.player.treatment == 'C'

        if treat_C_cond:
            if self.player.Q0_WhichDice == '彩票C':
                lottery_chosen = '彩票C'
                lottery_not_chosen = '彩票D'
            elif self.player.Q0_WhichDice == '彩票D':
                lottery_chosen = '彩票D'
                lottery_not_chosen = '彩票C'
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

            rand_num = random.choice(Constants.value_list)

            self.player.Q1C_rand_num = rand_num

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
        )

    def before_next_page(self):
        treat_C_cond = self.player.treatment == 'C'
        if treat_C_cond:
            self.participant.vars['prev_list'] = Constants.value_list.copy()
            self.participant.vars['prev_choice'] = self.player.Q1C
            self.participant.vars['prev_rand_num'] = self.player.Q1C_rand_num
            self.participant.vars['Q2C_counter'] = Constants.Q2C_counter_init

            self.player.diff_subj_responses += self.player.Q1C + ', '
            self.player.diff_subj_rand_values += str(self.player.Q1C_rand_num) + ', '


class Q2C(Page):
    form_model = 'player'
    form_fields = ['Q2C']

    def is_displayed(self):
        treat_C_cond = self.player.treatment == 'C'
        exclusion_1 = False
        exclusion_2 = False
        end_cond = False

        if treat_C_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']
            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            exclusion_1 = self.player.Q1C == '愿意' and self.player.Q1C_rand_num == 2
            exclusion_2 = self.player.Q1C == '不愿意' and self.player.Q1C_rand_num == 0.2
            end_cond = len(value_list) == 0

        return (not (exclusion_1 or exclusion_2 or end_cond)) and treat_C_cond

    def vars_for_template(self):
        treat_C_cond = self.player.treatment == 'C'

        if treat_C_cond:
            if self.player.Q0_WhichDice == '彩票C':
                lottery_chosen = '彩票C'
                lottery_not_chosen = '彩票D'
            elif self.player.Q0_WhichDice == '彩票D':
                lottery_chosen = '彩票D'
                lottery_not_chosen = '彩票C'
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            rand_num = random.choice(value_list)
            self.player.Q2C_rand_num = rand_num
            Q2C_counter = self.participant.vars['Q2C_counter']

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
            Q2C_counter=Q2C_counter,
        )

    def before_next_page(self):
        treat_C_cond = self.player.treatment == 'C'

        if treat_C_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            self.participant.vars['prev_list'] = value_list
            self.participant.vars['prev_choice'] = self.player.Q2C
            self.participant.vars['prev_rand_num'] = self.player.Q2C_rand_num
            self.participant.vars['Q2C_counter'] += 1

            self.player.diff_subj_responses += self.player.Q2C + ', '
            self.player.diff_subj_rand_values += str(self.player.Q2C_rand_num) + ', '
        

class StartD(Page):
    def is_displayed(self):
        treat_D_cond = self.player.treatment == 'D'
        return treat_D_cond

    def vars_for_template(self):
        if self.player.Q0_WhichDice == '彩票C':
            lottery_chosen = '彩票C'
            lottery_not_chosen = '彩票D'
        elif self.player.Q0_WhichDice == '彩票D':
            lottery_chosen = '彩票D'
            lottery_not_chosen = '彩票C'
        else:
            raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

        if self.participant.vars['diff_dice_first']:
            which_part = '一'
        else:
            which_part = '二'

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            which_part=which_part,
        )


class Q1D(Page):
    form_model = 'player'
    form_fields = ['Q1D']

    def is_displayed(self):
        treat_D_cond = self.player.treatment == 'D'
        return treat_D_cond

    def vars_for_template(self):
        treat_D_cond = self.player.treatment == 'D'

        if treat_D_cond:
            if self.player.Q0_WhichDice == '彩票C':
                lottery_chosen = '彩票C'
                lottery_not_chosen = '彩票D'
            elif self.player.Q0_WhichDice == '彩票D':
                lottery_chosen = '彩票D'
                lottery_not_chosen = '彩票C'
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

            rand_num = random.choice(Constants.value_list)
            self.player.Q1D_rand_num = rand_num

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
        )

    def before_next_page(self):
        treat_D_cond = self.player.treatment == 'D'

        if treat_D_cond:
            self.participant.vars['prev_list'] = Constants.value_list.copy()
            self.participant.vars['prev_choice'] = self.player.Q1D
            self.participant.vars['prev_rand_num'] = self.player.Q1D_rand_num
            self.participant.vars['Q2D_counter'] = Constants.Q2D_counter_init

            self.player.diff_subj_responses += self.player.Q1D + ', '
            self.player.diff_subj_rand_values += str(self.player.Q1D_rand_num) + ', '


class Q2D(Page):
    form_model = 'player'
    form_fields = ['Q2D']

    def is_displayed(self):
        treat_D_cond = self.player.treatment == 'D'
        exclusion_1 = False
        exclusion_2 = False
        end_cond = False

        if treat_D_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']
            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            exclusion_1 = self.player.Q1D == '愿意' and self.player.Q1D_rand_num == 2
            exclusion_2 = self.player.Q1D == '不愿意' and self.player.Q1D_rand_num == 0.2
            end_cond = len(value_list) == 0

        return (not (exclusion_1 or exclusion_2 or end_cond)) and treat_D_cond

    def vars_for_template(self):
        treat_D_cond = self.player.treatment == 'D'

        if treat_D_cond:
            if self.player.Q0_WhichDice == '彩票C':
                lottery_chosen = '彩票C'
                lottery_not_chosen = '彩票D'
            elif self.player.Q0_WhichDice == '彩票D':
                lottery_chosen = '彩票D'
                lottery_not_chosen = '彩票C'
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating lottery chosen.")

            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            rand_num = random.choice(value_list)
            self.player.Q2D_rand_num = rand_num
            Q2D_counter = self.participant.vars['Q2D_counter']

        return dict(
            lottery_chosen=lottery_chosen,
            lottery_not_chosen=lottery_not_chosen,
            rand_num=rand_num,
            Q2D_counter=Q2D_counter,
        )

    def before_next_page(self):
        treat_D_cond = self.player.treatment == 'D'

        if treat_D_cond:
            prev_value_list = self.participant.vars['prev_list']
            prev_choice = self.participant.vars['prev_choice']
            prev_rand_num = self.participant.vars['prev_rand_num']

            if prev_choice == '愿意':
                value_list = [x for x in prev_value_list if x > prev_rand_num]
            elif prev_choice == '不愿意':
                value_list = [x for x in prev_value_list if x < prev_rand_num]
            else:
                raise ValueError("Wrong input in previous choice. Error in calculating value list.")

            self.participant.vars['prev_list'] = value_list
            self.participant.vars['prev_choice'] = self.player.Q2D
            self.participant.vars['prev_rand_num'] = self.player.Q2D_rand_num
            self.participant.vars['Q2D_counter'] += 1

            self.player.diff_subj_responses += self.player.Q2D + ', '
            self.player.diff_subj_rand_values += str(self.player.Q2D_rand_num) + ', '


class Finish(Page):
    form_model = 'player'
    form_fields = ['Finish']

    def vars_for_template(self):
        self.participant.vars['first_app_enter'] = False

        if self.participant.vars['diff_dice_first']:
            which_part = '一'
        else:
            which_part = '二'

        return dict(
            which_part=which_part,
        )

    def before_next_page(self):
        self.participant.vars['diff_subj_treatment'] = self.player.treatment
        self.participant.vars['diff_init_choice'] = self.player.Q0_WhichDice
        self.participant.vars['diff_subj_responses'] = self.player.diff_subj_responses
        self.participant.vars['diff_subj_rand_values'] = self.player.diff_subj_rand_values


page_sequence = [Start,
                 StartA, Q1A, Q2A, Q2A, Q2A, Q2A, Q2A, Q2A, Q2A, Q2A, Q2A, Q2A,
                 StartB, Q1B, Q2B, Q2B, Q2B, Q2B, Q2B, Q2B, Q2B, Q2B, Q2B, Q2B,
                 StartC, Q1C, Q2C, Q2C, Q2C, Q2C, Q2C, Q2C, Q2C, Q2C, Q2C, Q2C,
                 StartD, Q1D, Q2D, Q2D, Q2D, Q2D, Q2D, Q2D, Q2D, Q2D, Q2D, Q2D,
                 Finish
                 ]
