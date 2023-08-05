# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpanel_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cpanel-api',
    'version': '0.1.2',
    'description': 'CPanel API Client. Supports latest UAPI.',
    'long_description': "# CPanel API Client for Python\n\nSupports only UAPI.\n\n```zsh\n$ pip install cpanel-api\n```\n\nBasic usage:\n\n```python\n#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport logging\nimport sys\n\nfrom cpanel_api import *\n\nlogging.basicConfig(level=logging.DEBUG, stream=sys.stderr)\n\nhostname = 'HOSTNAME_OR_IPADRESS'\nusername = 'USERNAME'\npassword = 'PASSWORD'\n\nclient = CPanelClient(hostname, username, password)\n\nr = client.SSH.get_port()\nprint('SSH port:', r.data.port)\n\nfrom pprint import pprint\nr = client.DomainInfo.list_domains()\npprint(r.data)\n```\n\nFunction call syntax:\n\n```python\nclient.ModuleName.function_name({'param': 'value'})\nclient.ModuleName.function_name(param='value')\nclient.ModuleName.function_name({'param': 'value'}, param='value')\nclient.api('ModuleName', 'function_name', {'param': 'value'}, param='value')\n```\n\nPagination:\n\n```python\nclient.ModuleName.function_name({'api.paginate': 1, 'api.paginate_size': 10, 'api.paginate_page': 2})\n```\n\nLinks:\n\n- [Official documentation](https://documentation.cpanel.net/display/DD/Guide+to+UAPI).\n",
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
