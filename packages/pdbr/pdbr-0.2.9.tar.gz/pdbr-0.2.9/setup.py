# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdbr']

package_data = \
{'': ['*']}

install_requires = \
['rich>=2.2.5,<3.0.0']

setup_kwargs = {
    'name': 'pdbr',
    'version': '0.2.9',
    'description': 'Pdb with Rich library.',
    'long_description': '# pdbr\n\n[![PyPI version](https://badge.fury.io/py/pdbr.svg)](https://pypi.org/project/pdbr/) [![Python Version](https://img.shields.io/pypi/pyversions/pdbr.svg)](https://pypi.org/project/pdbr/) [![](https://github.com/cansarigol/pdbr/workflows/Release/badge.svg)](https://github.com/cansarigol/pdbr/actions?query=workflow%3ARelease) [![](https://github.com/cansarigol/pdbr/workflows/Test/badge.svg)](https://github.com/cansarigol/pdbr/actions?query=workflow%3ATest)\n\n[Rich](https://github.com/willmcgugan/rich) is a great library for terminal output. In order to make the PDB results more colorful.\n\n\n## Installing\n\nInstall with `pip` or your favorite PyPi package manager.\n\n```\npip install pdbr\n```\n\n\n## Breakpoint\n\nIn order to use ```breakpoint()```, set **PYTHONBREAKPOINT** with "pdbr.set_trace"\n\n```python\nimport os\n\nos.environ["PYTHONBREAKPOINT"] = "pdbr.set_trace"\n```\n\nor just import pdbr\n\n```python\nimport pdbr\n```\n\n## New commands\n### vars(v)\nit is used to get the local variables list.\n\n![](/images/image5.png)\n\n## Config\n### Style\nIn order to use Rich\'s traceback, style, and theme, set **setup.cfg**.\n\n```\n[pdbr]\nstyle = yellow\nuse_traceback = True\ntheme = friendly\n```\n\n### History\n**store_history** setting is used to keep and reload history, even the prompt is closed and opened again.\n```\n[pdbr]\n...\nstore_history=.pdbr_history\n```\n\n## Vscode user snippet\n\nTo create or edit your own snippets, select **User Snippets** under **File > Preferences** (**Code > Preferences** on macOS), and then select **python.json**. Place the below snippet in json file.\n\n```\n{\n  ...\n  "pdbr": {\n        "prefix": "pdbr",\n        "body": "import pdbr; pdbr.set_trace()",\n        "description": "Code snippet for pdbr debug"\n    },\n}\n```\n\n## Samples\n![](/images/image1.png)\n\n![](/images/image3.png)\n\n![](/images/image4.png)\n\n### Traceback\n![](/images/image2.png)\n',
    'author': 'Can Sarigol',
    'author_email': 'ertugrulsarigol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cansarigol/pdbr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
