# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dazl',
 'dazl._gen',
 'dazl._gen.com',
 'dazl._gen.com.daml',
 'dazl._gen.com.daml.daml_lf_dev',
 'dazl._gen.com.daml.ledger',
 'dazl._gen.com.daml.ledger.api',
 'dazl._gen.com.daml.ledger.api.v1',
 'dazl._gen.com.daml.ledger.api.v1.admin',
 'dazl._gen.com.daml.ledger.api.v1.testing',
 'dazl._gen.google',
 'dazl._gen.google.rpc',
 'dazl.cli',
 'dazl.client',
 'dazl.damlast',
 'dazl.damleval',
 'dazl.metrics',
 'dazl.model',
 'dazl.pretty',
 'dazl.pretty.table',
 'dazl.protocols',
 'dazl.protocols.v0',
 'dazl.protocols.v1',
 'dazl.protocols.v1.model',
 'dazl.scheduler',
 'dazl.server',
 'dazl.util']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.29.1', 'protobuf>=3.12.0', 'requests', 'semver', 'toposort']

extras_require = \
{':python_version < "3.8.0"': ['typing_extensions'],
 ':python_version >= "3.6.0" and python_version < "3.7.0"': ['dataclasses'],
 'oauth': ['google-auth', 'oauthlib'],
 'prometheus': ['prometheus_client'],
 'pygments': ['pygments'],
 'server': ['aiohttp']}

entry_points = \
{'console_scripts': ['dazl = dazl.cli:main']}

setup_kwargs = {
    'name': 'dazl',
    'version': '7.0.0',
    'description': 'high-level Ledger API client for DAML ledgers',
    'long_description': 'dazl\n====\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/digital-asset/dazl-client/blob/master/LICENSE)\n<a href="https://circleci.com/gh/digital-asset/dazl-client">\n<img src="https://circleci.com/gh/digital-asset/dazl-client.svg?style=svg">\n</a>\n\nCopyright 2020 Digital Asset (Switzerland) GmbH and/or its affiliates. All Rights Reserved.\nSPDX-License-Identifier: Apache-2.0\n\n\nRich Python bindings for accessing Ledger API-based applications.\n\nRequirements\n------------\n* Python 3.6+\n* [Poetry](https://python-poetry.org/)\n* [DAML SDK](https://www.daml.com)\n\nExamples\n--------\n\nAll of the examples below assume you imported `dazl`.\n\nConnect to the ledger and submit a single command:\n\n```py\nwith dazl.simple_client(\'http://localhost:7600\', \'Alice\') as client:\n    client.submit_create(\'Alice\', \'My.Template\', { someField: \'someText\' })\n```\n\nConnect to the ledger as a single party, print all contracts, and close:\n\n```py\nwith dazl.simple_client(\'http://localhost:7600\', \'Alice\') as client:\n    # wait for the ACS to be fully read\n    client.ready()\n    contract_dict = client.find_active(\'*\')\nprint(contract_dict)\n```\n\nConnect to the ledger as multiple parties:\n\n```py\nnetwork = dazl.Network()\nnetwork.set_config(url=\'http://localhost:7600\')\n\nalice = network.simple_party(\'Alice\')\nbob = network.simple_party(\'Bob\')\n\n@alice.ledger_ready()\ndef set_up(event):\n    currency_cid, _ = await event.acs_find_one(\'My.Currency\', {"currency": "USD"})\n    return dazl.create(\'SomethingOf.Value\', {\n        \'amount\': 100,\n        \'currency\': currency_cid,\n        \'from\': \'Accept\',\n        \'to\': \'Bob\' })\n\n@bob.ledger_created(\'SomethingOf.Value\')\ndef on_something_of_value(event):\n    return dazl.exercise(event.cid, \'Accept\', { \'message\': \'Thanks!\' })\n\nnetwork.start()\n```\n\n\nBuilding locally\n----------------\n```sh\nmake package\n```\n\nTests\n-----\n\nTests in dazl are written using [pytest](https://docs.pytest.org/en/latest/). You can run them by doing:\n\n```sh\nmake test\n```\n',
    'author': 'Davin K. Tanabe',
    'author_email': 'davin.tanabe@digitalasset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digital-asset/dazl-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
