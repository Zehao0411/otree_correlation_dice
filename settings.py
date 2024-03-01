import random
from os import environ


# def randomize_app_sequence():
#     app_sequence = ['same_dice', 'diff_dice']
#     random.shuffle(app_sequence)
#     return app_sequence

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

SESSION_CONFIG_DEFAULTS = (
    dict(real_world_currency_per_point=1, participation_fee=10))

SESSION_CONFIGS = [dict(
    name='my_session',
    num_demo_participants=8,
    # app_sequence=['start_page'] + randomize_app_sequence() + ['reward_page']
    app_sequence=['start_page', 'same_dice', 'diff_dice', 'questionnaire', 'reward_page']
    # app_sequence=['start_page', 'same_dice', 'diff_dice', 'reward_page']
)]

LANGUAGE_CODE = 'zh-hans'

REAL_WORLD_CURRENCY_CODE = 'CNY'

USE_POINTS = True

DEMO_PAGE_INTRO_HTML = ''

PARTICIPANT_FIELDS = []

SESSION_FIELDS = []

ROOMS = [
    {
        'name': 'CCBEF404A',
        'display_name': '颐德楼404A',
        'participant_label_file': '_rooms/CCBEF404A.txt',
    },
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
