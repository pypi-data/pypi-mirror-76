# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['meteofrance', 'meteofrance.model']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2020.1,<2021.0', 'requests>=2.24.0,<3.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.9"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'meteofrance-api',
    'version': '0.1.1',
    'description': 'Python client for Météo-France API.',
    'long_description': "# meteofrance-api\n\nClient Python pour l'API Météo-France. | Python client for Météo-France API.\n\n[![Build Status][build-shield]][build]\n[![codecov][codecov-shield]][codecov]\n[![License][license-shield]](LICENSE)\n\n[![GitHub Release][releases-shield]][releases]\n[![PyPI version][pypi-shield]][pypi]\n[![GitHub Activity][commits-shield]][commits]\n\nYou will find English README content [here](#for-english-speaking-users).\n\nVous trouverez le contenu francophone du README [ici](#pour-les-francophones).\n\n## Pour les francophones\n\n### Description\n\nCe package Python permet de gérer la communication avec l'API non publique de\nMétéo-France utilisée par les applications moblies officielles.\n\nLe client permet:\n\n- Rechercher des lieux de prévisions.\n- Accéder aux prévisions météorologiques horraires ou quotidiennes.\n- Accéder aux prévisions de pluie dans l'heure quand disponibles.\n- Accéder aux alertes météo pour chaque département français et l'Andorre. Deux\n  bulletins sont disponibles : un synthétique et un second avec l'évolution des alertes\n  pour les prochaines 24 heures (exemple [ici](http://vigilance.meteofrance.com/Bulletin_sans.html?a=dept32&b=2&c=)).\n\nCe package a été développé avec l'intention d'être utilisé par [Home-Assistant](https://home-assistant.io/) mais il peut être utilsé dans d'autres contextes.\n\n### Installation\n\nPour utiliser le module Python `meteofrance` vous devez en premier installer\nle package:\n\n`pip install meteofrance-api`\n\nVous pouvez trouver un exemple d'usage dans un module Python en regardant [le test d'intégration](tests/test_integrations.py).\n\n### Contribuer\n\nLes contributions sont les bienvenues. Veuillez consulter les bonnes pratiques\ndétaillées dans [`CONTRIBUTING.md`](CONTRIBUTING.md).\n\n## For English speaking users\n\n### Descritption\n\nThis Python package manages the communication with the private Météo-France API\nused by the official moblie applications.\n\nThe client allows:\n\n- Search a forecast location.\n- Fetch daily or hourly weather forecast.\n- Fetch rain forecast within the next hour if available.\n- Fetch the weather alerts or phenomenoms for each French department or Andorre.\n  Two bulletin are availabe: one basic and an other advanced with the timelaps evolution for the next 24 hours (example [here](http://vigilance.meteofrance.com/Bulletin_sans.html?a=dept32&b=2&c=)).\n\nThis package have been developed to be used with [Home-Assistant](https://home-assistant.io/) but it can be used in other contexts.\n\n### Installation\n\nTo use the `meteofrance` Python module, you have to install this package first:\n\n`pip install meteofrance-api`\n\nYou will find an example ot usage in a Python program in the [integration test](tests/test_integrations.py).\n\n### Contributing\n\nContributions are welcomed. Please check the guidelines in [`CONTRIBUTING.md`](CONTRIBUTING.md).\n\n[commits-shield]: https://img.shields.io/github/commit-activity/y/hacf-fr/meteofrance-api.svg?style=for-the-badge\n[commits]: https://github.com/hacf-fr/meteofrance-api/commits/master\n[license-shield]: https://img.shields.io/github/license/hacf-fr/meteofrance-api.svg?style=for-the-badge\n[releases-shield]: https://img.shields.io/github/release/hacf-fr/meteofrance-api.svg?style=for-the-badge\n[releases]: https://github.com/hacf-fr/meteofrance-api/releases\n[build-shield]: https://img.shields.io/github/workflow/status/hacf-fr/meteofrance-api/Python%20package?style=for-the-badge\n[build]: https://github.com/hacf-fr/meteofrance-api/actions?query=workflow%3A%22Python+package%22\n[codecov-shield]: https://img.shields.io/codecov/c/github/hacf-fr/meteofrance-api?style=for-the-badge\n[codecov]: https://codecov.io/gh/hacf-fr/meteofrance-api\n[pypi-shield]: https://img.shields.io/pypi/v/meteofrance-api?style=for-the-badge\n[pypi]: https://pypi.org/project/meteofrance-api/\n",
    'author': 'oncleben31',
    'author_email': 'oncleben31@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hacf-fr/meteofrance-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
