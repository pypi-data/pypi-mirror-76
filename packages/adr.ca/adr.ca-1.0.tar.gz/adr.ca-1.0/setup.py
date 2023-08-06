# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['ADR',
 'ADR.Analysis',
 'ADR.Analysis.Aerodynamics',
 'ADR.Analysis.Performance',
 'ADR.Analysis.Performance.tests',
 'ADR.Analysis.Stability',
 'ADR.Analysis.Stability.FlightStability',
 'ADR.Analysis.Stability.FlightStability.tests',
 'ADR.Checkers',
 'ADR.Checkers.tests',
 'ADR.Components',
 'ADR.Components.Aerodynamic_components',
 'ADR.Components.Aerodynamic_components.tests',
 'ADR.Components.Points',
 'ADR.Components.Points.tests',
 'ADR.Components.Propulsion',
 'ADR.Components.Propulsion.test',
 'ADR.Components.References',
 'ADR.Components.References.test',
 'ADR.Components.tests',
 'ADR.Core',
 'ADR.Methods',
 'ADR.Methods.VLM.AVL',
 'ADR.Methods.tests',
 'ADR.World.Air',
 'ADR.World.Constants',
 'ADR.World.Profiles',
 'ADR.World.Profiles.AerodynamicData',
 'ADR.World.Profiles.Coordinates',
 'ADR.World.References',
 'ADR.World.tests',
 'ADR.tests']

package_data = \
{'': ['*'],
 'ADR': ['saved_planes/*'],
 'ADR.World.References': ['X5_Stability/*']}

install_requires = \
['avlwrapper>=0.2.1,<0.3.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'adr.ca',
    'version': '1.0',
    'description': 'ADR is a python library to analyse aircraft conceptual designs. ADR has several tools that allows one to create different aircraft designs and analyse those from different points os view.',
    'long_description': '# ADR\n[![Build Status](https://travis-ci.com/CeuAzul/ADR.svg?branch=master)](https://travis-ci.com/CeuAzul/ADR)\n[![Coverage Status](https://coveralls.io/repos/github/CeuAzul/ADR/badge.svg)](https://coveralls.io/github/CeuAzul/ADR)\n\n\nAircraft Design Resources aims to help engineers on conceptual design analysis, giving them the tools necessary to easily simulate different aircraft designs.\n\n## Installation\n### Regular usage\n```\ngit clone https://github.com/CeuAzul/ADR.git\ncd ADR\npip install setuptools\npip install ./\n```\n\n### Development\n```\ngit clone https://github.com/CeuAzul/ADR.git\ncd ADR\npip install setuptools\npip install -e ./\n```\n\n## Usage\n\nTo run an analysis modify the inputs on *parameters.py* as needed and run *main.py*.\n\n### Contributors\n\nThis project exists thanks to all the people who contribute.\n\n[![Contributors](https://contributors-img.web.app/image?repo=CeuAzul/ADR)](https://github.com/CeuAzul/ADR/graphs/contributors)\n',
    'author': 'Rafael Araujo Lehmkuhl',
    'author_email': 'rafael.lehmkuhl93@gmail.com',
    'maintainer': 'Rafael Araujo Lehmkuhl',
    'maintainer_email': 'rafael.lehmkuhl93@gmail.com',
    'url': 'https://CeuAzul.github.io/ADR',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
