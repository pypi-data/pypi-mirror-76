# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpanel_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cpanel-api',
    'version': '0.1.1',
    'description': 'CPanel API Client. Supports latest UAPI.',
    'long_description': "# CPanel API Client for Python\n\nSupports only UAPI.\n\n```zsh\n$ pip install cpanel_api\n```\n\nExamples:\n\n```python\n#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport logging\nimport sys\n\nfrom cpanel_api import *\n\nlogging.basicConfig(level=logging.DEBUG, stream=sys.stderr)\n\nhostname = 'HOSTNAME_OR_IP_ADRESS'\nusername = 'USERNAME'\npassword = 'PASSWORD'\n\nclient = CPanelClient(hostname, username, password)\n\nclient.Module.function({'param': 'value'}, param='value')\nclient.api('Module', 'function', {'param': 'value'}, param='value')\n\nres = client.SSH.get_port()\n# {\n#     'data': {'port': '1243'},\n#     'errors': None,\n#     'metadata': {},\n#     'warnings': None,\n#     'messages': None,\n#     'status': 1,\n# }\nprint(res.data.port)\n```\n\nLinks:\n\n- [Official documentation](https://documentation.cpanel.net/display/DD/Guide+to+UAPI).\n",
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
