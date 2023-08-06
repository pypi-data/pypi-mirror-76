# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_timezoner']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.8,<4.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'slackclient>=2.7.2,<3.0.0']

entry_points = \
{'console_scripts': ['slack_timezoner = minimal:run_as_server']}

setup_kwargs = {
    'name': 'slack-timezoner',
    'version': '0.1.2',
    'description': 'A toy app to give a breakdown of timezone distribution in a slack workgroup',
    'long_description': '# Slack Timezoner\n\nIf you use slack, it\'s sometimes useful to get an idea of the geographic distribution of members.\n\nAnd because we\'re online, while geographic distance is important to know it\'s often the timezone that\'s more relevant for working out when might be sensible to contact someone, or see how a commmunity is distributed.\n\nThis is what slack timezoner does. Right now all it does is print out a count of members in your community, by timezone.\n\n\n##\xa0Usage\n\n\n1. Create an app for a single slack group\n2. Get a Web API token - https://api.slack.com/web#authentication\n3. Checkout this code\n4. Install dependencies\n5. Either use the code programatically, or run it this as a server, to see the JSON output\n\n\n### Create an app\n\nYou need to create an app for a single team. See below for more\n\nhttps://slack.dev/python-slackclient/auth.html#\n\nYou can create an app at the link below:\n\nhttps://api.slack.com/apps\n\n### Get a web api token\n\nThis is detailed in slack\'s extensive documentation. You need a Web API token\n\nhttps://api.slack.com/web#authentication\n\nIf it helps it should be visible at a link that looks like the pattern below, and it will be called `OAuth Access Token` in the web UI:\n\nhttps://api.slack.com/apps/YOUR_APP_ID/oauth\n\n\n### Check out this code\n\n### Use the code programatically, or run the server\n\nThis project includes a minimal, single-file Django app, to serve the summary as JSON, to display using some charting or tabular renderer.\n\n```\npython ./minimal.py runserver\n```\n\nAlternatively, you can also import the library and use it programatically in python code:\n\n\n```\nimport slack_timezoner.group_by_timezones\n\ntzc = group_by_timezones.TimeZoneCounter()\n\n# returns a Counter datastructure\nres = tzc.summary()\n\n```\n\n\n### Next steps\n\nThis was thrown together in a hurry, and I\'d like to adapt this to allow running the same kind of summaries for any public channel in slack workspace.\n\nYou can list all the channels in workspace with this API call:\nhttps://api.slack.com/methods/conversations.list\n\n\nOnce you have that, you can get a list of the members like so:\nhttps://api.slack.com/methods/conversations.members\n\nThis returns a list of member ids like so:\n\n```\n{\n    "ok": true,\n    "members": [\n        "U023BECGF",\n        "U061F7AUR",\n        "W012A3CDE"\n    ],\n    "response_metadata": {\n        "next_cursor": "e3VzZXJfaWQ6IFcxMjM0NTY3fQ=="\n    }\n}\n```\n\nYou can then look up the timezones, with this call to recontruct a datastructure similar to the one used in the TimeZoneCounter already.\n\nhttps://slack.dev/python-slackclient/basic_usage.html#listing-team-members\n\n\n\n### Contributing\n\nThis is currently used in the ClimateAction.tech slack. If you\'re interested in helping out, please file an issue, or join the slack there.\n\n\nYou can join the link below:\n\nhttps://climateaction.tech/#join\n\n\n\n\n',
    'author': 'Chris Adams',
    'author_email': 'chris@productscience.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrchrisadams/slack-timezoner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
