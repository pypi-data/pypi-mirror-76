# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpanel_api']

package_data = \
{'': ['*']}

install_requires = \
['pysocks>=1.7.1,<2.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'cpanel-api',
    'version': '0.2.2',
    'description': 'CPanel API Client. Supports cPanel API 2 and UAPI.',
    'long_description': '# CPanel API Client for Python\n\nSupports cPanel API 2 and UAPI.\n\n## Install\n\n```zsh\n$ pip install cpanel-api\n```\n\n## Examples\n\nBasic usage:\n\n```python\n#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport logging\nimport sys\n\nfrom pprint import pprint\n\nfrom cpanel_api import CPanelApi\n\nlogging.basicConfig(level=logging.WARNING, stream=sys.stderr)\n\nhostname = \'HOSTNAME_OR_IPADRESS\'\nusername = \'USERNAME\'\npassword = \'PASSWORD\'\n\nclient = CPanelApi(hostname, username, password)\n# {\'warnings\': None, \'errors\': None, \'data\': {\'port\': \'1243\'}, \'metadata\': {}, \'status\': 1, \'messages\': None}\nr = client.uapi.SSH.get_port()\nprint(\'SSH port:\', r.data.port)\n# get all public ssh keys\n# {\'cpanelresult\': {\'postevent\': {\'result\': 1}, \'apiversion\': 2, \'data\': [...], \'func\': \'listkeys\', \'event\': {\'result\': 1}, \'module\': \'SSH\', \'preevent\': {\'result\': 1}}}\nr = client.cpanel2.SSH.listkeys()\npprint(r.cpanelresult.data)\n# retrieve key\nr = client.cpanel2.SSH.fetchkey(name=\'id_rsa\')\n# {"name": "id_rsa", "key": "ssh-rsa XXX"}\nprint(r.cpanelresult.data[0].key)\nr = client.cpanel2.SSH.importkey(name=\'new_rsa.pub\', key=\'*data*\')\npprint(r)\n# ...\nr = client.cpanel2.DomainLookup.getdocroot(domain=\'site.info\')\nprint(r.cpanelresult.data[0].reldocroot)  # public_html\n```\n\nFunction call syntax:\n\n```python\nclient.api_version.ModuleName.function_name({\'param\': \'value\'})\nclient.api_version.ModuleName.function_name(param=\'value\')\nclient.api_version.ModuleName.function_name({\'param\': \'value\'}, param=\'value\')\nclient.api_cal(\'api_version\', \'ModuleName\', \'function_name\', {\'param\': \'value\'}, param=\'value\')\n```\n\nWhere `api_version` is `cpanel2` or `uapi`.\n\n## Links:\n\n- [Official documentation](https://documentation.cpanel.net/display/DD/Developer+Documentation+Home).\n',
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/cpanel-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
