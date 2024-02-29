import random
# from numpy import *
from otree.api import *
import numpy as np

doc = """Author is LiuXing
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None  # 每个组1个人
    num_rounds = 1  #



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    Q1 = models.StringField(
        label='Q1. 一个球拍和一个球总共卖1.10元, 球拍比球多卖1.00元, 请问球的价格是多少元?'
        ,)

    Q2 = models.StringField(
        label='Q2. 如果5个机器耗时5分钟制作了5个装饰品, 请问100个机器制作100个装饰品要耗时多久?'
        ,)

    Q3 = models.StringField(
        label='Q3. 湖面上有一片睡莲, 它们每天以两倍的数量增加着。如果睡莲铺满整个湖面需要48天, 那么它覆盖湖面的一半区域需要几天?'
        ,)

    Q4 = models.StringField(
        label='Q4. 每当我做出一个选择, 我都会好奇如果我选择了不同的方式会发生什么 (Q4-Q8中：1 代表‘‘完全不同意’’，5 代表‘‘完全同意’’，其他选项介于两者之间。)',
        choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'],['5', '5']],
        widget=widgets.RadioSelectHorizontal)

    Q5 = models.StringField(
        label='Q5. 每当我做出一个选择, 我都会试图获取关于其他选择结果的信息',
        choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5']],
        widget=widgets.RadioSelectHorizontal)

    Q6 = models.StringField(
        label='Q6. 如果我做出了一个选择, 结果是好的, 但如果我发现另一个选择可能会更好, 我仍然会感觉有些失败',
        choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5']],
        widget=widgets.RadioSelectHorizontal)

    Q7 = models.StringField(
        label='Q7. 当我思考自己在生活中的表现时, 我经常评估我放弃的机会',
        choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5']],
        widget=widgets.RadioSelectHorizontal)

    Q8 = models.StringField(
        label='Q8. 一旦我做出决定, 我就不再回头',
        choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5']],
        widget=widgets.RadioSelectHorizontal)

    Q9 = models.StringField(
        label='Q9. 您认为通常来说您是一个非常喜欢冒险的人还是尽量规避风险的人? (0 代表‘‘完全不愿意冒险’’，10 代表‘‘非常喜欢冒险’’，其他选项介于两者之间)',
        choices=[['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10']],
        widget=widgets.RadioSelectHorizontal)

    Q10 = models.IntegerField(
        label='Q10. 请问您的年龄是?',
        min=15, max=70)

    Q11 = models.StringField(
        choices=[['男', '男'], ['女', '女']],
        label='Q11. 请问您的性别是?',
        widget=widgets.RadioSelectHorizontal)

    Q12 = models.StringField(
        label='Q12. 请问您的最高学历是?',
        choices=[['低于高中', '低于高中'], ['高中', '高中'], ['本科', '本科'], ['硕士', '硕士'], ['博士', '博士'], ['以上均不适用', '以上均不适用']],
        widget=widgets.RadioSelectHorizontal)

    Q13 = models.StringField(
        label='Q13. 请问您的总家庭年收入是?',
        choices=[['15万以下', '15万以下'], ['15万至25万', '15万至25万'], ['25万-35万', '25万-35万'],
                 ['35万-45万', '35万-45万'], ['45万以上', '45万以上'], ['我不想回答', '我不想回答']],
        widget=widgets.RadioSelectHorizontal)

    Q14 = models.StringField(
        label='Q14. 请问您目前的工作状态是?',
        choices=[['学生', '学生'], ['退休', '退休'], ['失业或者无业', '失业或者无业'],
                 ['非全日制就业', '非全日制就业'], ['全职工作', '全职工作'], ['其他', '其他']],
        widget=widgets.RadioSelectHorizontal)

    Q15 = models.StringField(
        label='Q15. 请问您目前的婚姻状态是?',
        choices=[['已婚', '已婚'], ['离异', '离异'], ['丧偶', '丧偶'],
                 ['未婚', '未婚'], ['我不想回答', '我不想回答']],
        widget=widgets.RadioSelectHorizontal)


# PAGES
class q1(Page):
    form_model = 'player'

class q2(Page):
    form_model = 'player'

    form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15',
                    ]

page_sequence = [q1, q2]