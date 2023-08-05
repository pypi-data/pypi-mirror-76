# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpanel_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cpanel-api',
    'version': '0.2.1',
    'description': 'CPanel API Client. Supports cPanel API 2 and UAPI.',
    'long_description': "# CPanel API Client for Python\n\nSupports cPanel API 2 and UAPI.\n\n## Install\n\n```zsh\n$ pip install cpanel-api\n```\n\n## Examples\n\nCreate client:\n\n```python\n#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport logging\nimport sys\n\nfrom cpanel_api import *\n\nlogging.basicConfig(level=logging.WARNING, stream=sys.stderr)\n\nhostname = 'HOSTNAME_OR_IPADRESS'\nusername = 'USERNAME'\npassword = 'PASSWORD'\n\nclient = CPanelApi(hostname, username, password)\n```\n\nFunction call syntax:\n\n```python\nclient.api_version.ModuleName.function_name({'param': 'value'})\nclient.api_version.ModuleName.function_name(param='value')\nclient.api_version.ModuleName.function_name({'param': 'value'}, param='value')\nclient.api_cal('api_version', 'ModuleName', 'function_name', {'param': 'value'}, param='value')\n```\n\nWhere `api_version` is `cpanel2` or `uapi`.\n\nDomain list:\n\n```python\nIn [10]: client.uapi.DomainInfo.list_domains()\nOut [10]:\n{'messages': None,\n 'status': 1,\n 'data': {'main_domain': 'site.info',\n  'sub_domains': ['cabinet.site.info',\n   'news.site.info',\n   'shop.site.info'],\n  'parked_domains': [],\n  'addon_domains': []},\n 'errors': None,\n 'metadata': {},\n 'warnings': None}\n```\n\nSSH kyes:\n\n```python\nIn [20]: client.cpanel2.SSH.listkeys()\nOut [20]:\n{'cpanelresult': {'postevent': {'result': 1},\n  'apiversion': 2,\n  'preevent': {'result': 1},\n  'module': 'SSH',\n  'func': 'listkeys',\n  'data': [],\n  'event': {'result': 1}}}\n```\n\n## Links:\n\n- [Official documentation](https://documentation.cpanel.net/display/DD/Developer+Documentation+Home).\n",
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/cpanel-api',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
